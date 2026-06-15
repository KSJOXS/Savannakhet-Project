# ================================================================
# train_gnn.py
# ================================================================
# This is the HeteroGraphSAGE model training script written in VS Code.
# It is designed to be executed on Google Colab via Google Drive.
#
# Usage (Workflow 3: Local Dev + Cloud Training):
#   1. Write this code locally using VS Code.
#   2. Upload this file + savannakhet_real_data.json to Google Drive.
#   3. Open Colab → Mount Drive → Run: !python train_gnn.py
# ================================================================

import matplotlib.pyplot as plt
import sys
import os
import json
import time
import random
import numpy as np
import torch
import torch.nn.functional as F
import matplotlib
matplotlib.use('Agg')  # Disable display for Colab server mode

# ── Check PyTorch Geometric ──
try:
    from torch_geometric.nn import SAGEConv, to_hetero
    from torch_geometric.data import HeteroData
    from torch_geometric.utils import negative_sampling
except ImportError:
    print("[!] torch_geometric not found — installing...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install",
                   "torch_geometric", "-q"], check=True)
    from torch_geometric.nn import SAGEConv, to_hetero
    from torch_geometric.data import HeteroData
    from torch_geometric.utils import negative_sampling

# ════════════════════════════════════════════════════════════════
# CONFIGURATION
# ════════════════════════════════════════════════════════════════
EPOCHS = 100
HIDDEN_DIM = 64
LR = 0.01
SEED = 42
# Save in the same folder as the script
SAVE_DIR = os.path.dirname(os.path.abspath(__file__))
# ════════════════════════════════════════════════════════════════

torch.manual_seed(SEED)
random.seed(SEED)
np.random.seed(SEED)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print("=" * 65)
print("  Savannakhet GNN — HeteroGraphSAGE Training")
print("  (Local Dev + Cloud Training Workflow)")
print("=" * 65)
print(f"  Device   : {device}")
if torch.cuda.is_available():
    print(f"  GPU      : {torch.cuda.get_device_name(0)}")
print(f"  Epochs   : {EPOCHS}")
print(f"  Hidden   : {HIDDEN_DIM}")
print(f"  LR       : {LR}")
print("=" * 65)

# ────────────────────────────────────────────────────────────────
# 1. Load data from JSON (Exported from DB via export_data_for_colab.py)
# ────────────────────────────────────────────────────────────────
DATA_FILE = os.path.join(SAVE_DIR, "savannakhet_real_data.json")

if not os.path.exists(DATA_FILE):
    print(f"\n[ERROR] File not found: {DATA_FILE}")
    print("  Please upload savannakhet_real_data.json")
    print("  to the same folder as train_gnn.py")
    sys.exit(1)

with open(DATA_FILE, "r", encoding="utf-8") as f:
    DB = json.load(f)

CATEGORIES = DB["categories"]
USERS_DATA = DB["users"]
PLACES_DATA = DB["places"]
INTERACTIONS = DB["interactions"]
NUM_USERS = len(USERS_DATA)
NUM_PLACES = len(PLACES_DATA)

# compatibility: real data uses 'username'
for u in USERS_DATA:
    if "name" in u and "username" not in u:
        u["username"] = u["name"]

print(f"\n[OK] Data loaded successfully!")
print(f"  Users        : {NUM_USERS}")
print(f"  Places       : {NUM_PLACES}")
print(f"  Interactions : {len(INTERACTIONS)}")

# Index Mapping: DB id → tensor index
user_id2idx = {u["id"]: i for i, u in enumerate(USERS_DATA)}
place_id2idx = {p["id"]: i for i, p in enumerate(PLACES_DATA)}
place_idx2id = {i: p["id"] for i, p in enumerate(PLACES_DATA)}

# ────────────────────────────────────────────────────────────────
# 2. Build HeteroGraph
# ────────────────────────────────────────────────────────────────
print("\n[*] Building HeteroGraph...")

data = HeteroData()

# User Features: Multi-hot Encoding (10 dim)
data["user"].x = torch.tensor(
    [[1.0 if cat in (u.get("preferences") or []) else 0.0 for cat in CATEGORIES]
     for u in USERS_DATA], dtype=torch.float
)

# Place Features: One-hot Category (10 dim) + Rating (1 dim) = 11 dim
data["place"].x = torch.tensor(
    [[1.0 if cat == p.get("category", "") else 0.0 for cat in CATEGORIES]
     + [min(float(p.get("rating", 0)) / 5.0, 1.0)]
     for p in PLACES_DATA], dtype=torch.float
)

# Edges from real interactions
edge_src, edge_dst, added = [], [], set()
for intr in INTERACTIONS:
    uid = intr["user_id"]
    pid = intr["place_id"]
    if uid not in user_id2idx or pid not in place_id2idx:
        continue
    key = (user_id2idx[uid], place_id2idx[pid])
    if key not in added:
        added.add(key)
        edge_src.append(key[0])
        edge_dst.append(key[1])

# Fallback: add preference-based edges if interactions are too few
if len(edge_src) < NUM_USERS * 2:
    print(
        f"  [!] Too few interactions ({len(edge_src)}) — adding preference edges")
    for u_idx, u in enumerate(USERS_DATA):
        prefs = u.get("preferences", [])
        for p_idx, p in enumerate(PLACES_DATA):
            if p.get("category") in prefs and (u_idx, p_idx) not in added:
                added.add((u_idx, p_idx))
                edge_src.append(u_idx)
                edge_dst.append(p_idx)

data["user", "interacts_with", "place"].edge_index = torch.tensor(
    [edge_src, edge_dst], dtype=torch.long
)

# ── Add Reverse Edges (place → user) ──
# Necessary for user nodes to receive messages during propagation.
# Without this, to_hetero() will error: "cannot generate node for type 'user'"
data["place", "rev_interacts", "user"].edge_index = torch.tensor(
    [edge_dst, edge_src], dtype=torch.long
)

data = data.to(device)

print(f"  User nodes  : {data['user'].x.shape}")
print(f"  Place nodes : {data['place'].x.shape}")
print(
    f"  Forward edges (user->place) : {data['user', 'interacts_with', 'place'].edge_index.shape[1]}")
print(
    f"  Reverse edges (place->user) : {data['place', 'rev_interacts', 'user'].edge_index.shape[1]}")

# ────────────────────────────────────────────────────────────────
# 3. Define HeteroGraphSAGE Model
# ────────────────────────────────────────────────────────────────


class BaseGNN(torch.nn.Module):
    """
    2-Layer GraphSAGE
    Layer 1: MEAN Aggregation → ReLU
    Layer 2: CONCAT + Linear → Embedding
    """

    def __init__(self, hidden_channels):
        super().__init__()
        self.conv1 = SAGEConv((-1, -1), hidden_channels)
        self.conv2 = SAGEConv((-1, -1), hidden_channels)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index).relu()
        x = self.conv2(x, edge_index)
        return x


model = to_hetero(BaseGNN(HIDDEN_DIM), metadata=data.metadata()).to(device)

# ── Lazy Initialization (Fix Error: uninitialized parameter) ──
with torch.no_grad():
    model(data.x_dict, data.edge_index_dict)

optimizer = torch.optim.Adam(model.parameters(), lr=LR)
total_params = sum(p.numel() for p in model.parameters())
print(f"\n[OK] Model: HeteroGraphSAGE | Params: {total_params:,}")

# ────────────────────────────────────────────────────────────────
# 4. Training Loop
# ────────────────────────────────────────────────────────────────
losses, accuracies = [], []
pos_edge_index = data["user", "interacts_with", "place"].edge_index
n_steps = max(1, pos_edge_index.size(1) // 5)

print(f"\n{'='*65}")
print(f"  Starting training... ({EPOCHS} Epochs)")
print(f"{'='*65}")

for epoch in range(1, EPOCHS + 1):
    model.train()
    t0 = time.time()
    optimizer.zero_grad()

    out = model(data.x_dict, data.edge_index_dict)
    ps, pd = pos_edge_index[0], pos_edge_index[1]
    pos_out = (out["user"][ps] * out["place"][pd]).sum(dim=-1)

    neg_ei = negative_sampling(
        edge_index=pos_edge_index,
        num_nodes=(data["user"].num_nodes, data["place"].num_nodes),
        num_neg_samples=pos_edge_index.size(1),
    )
    neg_out = (out["user"][neg_ei[0]] * out["place"][neg_ei[1]]).sum(dim=-1)

    labels = torch.cat([torch.ones(pos_out.size(0)),
                        torch.zeros(neg_out.size(0))]).to(device)
    loss = F.binary_cross_entropy_with_logits(
        torch.cat([pos_out, neg_out]), labels)
    loss.backward()
    optimizer.step()
    losses.append(loss.item())

    with torch.no_grad():
        correct = (pos_out >= 0).float().sum() + (neg_out < 0).float().sum()
        acc = correct.item() / (pos_out.size(0) + neg_out.size(0))
        accuracies.append(acc)

    # Display progress every 5 epochs
    if epoch % 5 == 0 or epoch == 1:
        ms = int((time.time() - t0) * 1000 / max(1, n_steps))
        print(f"Epoch {epoch:>3}/{EPOCHS}  "
              f"{n_steps}/{n_steps} "
              f"━━━━━━━━━━━━━━━━━━━━  "
              f"0s {ms}ms/step  "
              f"accuracy: {acc:.4f}  loss: {loss.item():.4f}")

print(f"\n[OK] Training completed!")
print(f"  Final Accuracy : {accuracies[-1]*100:.2f}%")
print(f"  Final Loss     : {losses[-1]:.4f}")

# ────────────────────────────────────────────────────────────────
# 5. Save Accuracy & Loss Chart
# ────────────────────────────────────────────────────────────────
print("\n[*] Generating chart...")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle(
    f"Savannakhet GNN — Training Results ({NUM_USERS} users x {NUM_PLACES} places)",
    fontsize=12, fontweight="bold"
)
ep = range(1, EPOCHS + 1)

ax1.plot(ep, accuracies, color="#2563EB", lw=2, label="accuracy")
ax1.fill_between(ep, accuracies, alpha=0.15, color="#2563EB")
ax1.axhline(0.85, color="#059669", ls="--", lw=1.5, label="target 85%")
ax1.set(title="Model Accuracy", xlabel="Epochs",
        ylabel="Accuracy", ylim=(0.4, 1.05))
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{y*100:.0f}%"))
ax1.legend()
ax1.grid(alpha=0.3)

ax2.plot(ep, losses, color="#DC2626", lw=2, label="loss")
ax2.fill_between(ep, losses, alpha=0.12, color="#DC2626")
ax2.set(title="Model Loss", xlabel="Epochs", ylabel="Loss", ylim=(0, None))
ax2.legend()
ax2.grid(alpha=0.3)

plt.tight_layout()
chart_path = os.path.join(SAVE_DIR, "training_results.png")
plt.savefig(chart_path, dpi=150, bbox_inches="tight")
plt.close()
print(f"  [OK] Chart saved: {chart_path}")

# ────────────────────────────────────────────────────────────────
# 6. Save Model
# ────────────────────────────────────────────────────────────────
model_path = os.path.join(SAVE_DIR, "gnn_model.pt")
torch.save({
    "epoch": EPOCHS,
    "model_state": model.state_dict(),
    "final_acc": accuracies[-1],
    "final_loss": losses[-1],
    "user_id2idx": user_id2idx,
    "place_id2idx": place_id2idx,
    "place_idx2id": place_idx2id,
    "metadata": {
        "hidden_dim": HIDDEN_DIM,
        "categories": CATEGORIES,
        "num_users": NUM_USERS,
        "num_places": NUM_PLACES,
        "source": "real_database",
    },
}, model_path)
print(f"  [OK] Model saved: {model_path}")

# ────────────────────────────────────────────────────────────────
# 7. Summary
# ────────────────────────────────────────────────────────────────
print(f"\n{'='*65}")
print("  Training Summary")
print(f"{'='*65}")
print(f"  Architecture : HeteroGraphSAGE (K=2, hidden={HIDDEN_DIM})")
print(f"  Dataset      : {NUM_USERS} users x {NUM_PLACES} places (Real Data)")
print(
    f"  Edges        : {data['user', 'interacts_with', 'place'].edge_index.shape[1]}")
print(f"  Epochs       : {EPOCHS}")
print(f"  Best Acc     : {max(accuracies)*100:.2f}%")
print(f"  Final Acc    : {accuracies[-1]*100:.2f}%")
print(f"  Final Loss   : {losses[-1]:.4f}")
print(f"  Optimizer    : Adam (lr={LR})")
print(f"  Loss Fn      : BCEWithLogitsLoss")
print(f"{'='*65}")
print(f"  Files saved:")
print(f"    gnn_model.pt         <- Trained model weights")
print(f"    training_results.png <- Training accuracy/loss chart")
print(f"{'='*65}")
