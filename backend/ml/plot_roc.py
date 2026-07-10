"""
plot_roc.py
──────────────────────────────────────────────
Generate ROC Curve (Validation + Test) from the
trained HeteroGraphSAGE model (gnn_model.pt).

Run:
    python plot_roc.py
──────────────────────────────────────────────
"""

import os, sys, json, random, math
import numpy as np
import torch
import torch.nn.functional as F
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc

# ── Try importing PyG ──────────────────────────────────────────
try:
    from torch_geometric.nn import SAGEConv, to_hetero
    from torch_geometric.data import HeteroData
    from torch_geometric.utils import negative_sampling
except ImportError:
    print("[!] Installing torch_geometric ...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "torch_geometric", "-q"], check=True)
    from torch_geometric.nn import SAGEConv, to_hetero
    from torch_geometric.data import HeteroData
    from torch_geometric.utils import negative_sampling

try:
    from sklearn.metrics import roc_curve, auc
except ImportError:
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "scikit-learn", "-q"], check=True)
    from sklearn.metrics import roc_curve, auc

# ════════════════════════════════════════════════════════════════
# CONFIG
# ════════════════════════════════════════════════════════════════
SAVE_DIR   = os.path.dirname(os.path.abspath(__file__))
DATA_FILE  = os.path.join(SAVE_DIR, "savannakhet_real_data.json")
MODEL_FILE = os.path.join(SAVE_DIR, "gnn_model.pt")
OUT_FILE   = os.path.join(SAVE_DIR, "roc_curve.png")

HIDDEN_DIM = 64
SEED       = 42

torch.manual_seed(SEED)
random.seed(SEED)
np.random.seed(SEED)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ════════════════════════════════════════════════════════════════
# 1. Load data
# ════════════════════════════════════════════════════════════════
print("[*] Loading data ...")
with open(DATA_FILE, "r", encoding="utf-8") as f:
    DB = json.load(f)

CATEGORIES   = DB["categories"]
USERS_DATA   = DB["users"]
PLACES_DATA  = DB["places"]
INTERACTIONS = DB["interactions"]

for u in USERS_DATA:
    if "name" in u and "username" not in u:
        u["username"] = u["name"]

user_id2idx  = {u["id"]: i for i, u in enumerate(USERS_DATA)}
place_id2idx = {p["id"]: i for i, p in enumerate(PLACES_DATA)}

# ════════════════════════════════════════════════════════════════
# 2. Build HeteroGraph (same logic as train_gnn.py)
# ════════════════════════════════════════════════════════════════
print("[*] Building HeteroGraph ...")
data = HeteroData()

data["user"].x = torch.tensor(
    [[1.0 if cat in (u.get("preferences") or []) else 0.0 for cat in CATEGORIES]
     for u in USERS_DATA], dtype=torch.float
)

data["place"].x = torch.tensor(
    [[1.0 if cat == p.get("category", "") else 0.0 for cat in CATEGORIES]
     + [min(float(p.get("rating", 0)) / 5.0, 1.0)]
     for p in PLACES_DATA], dtype=torch.float
)

edge_src, edge_dst, added = [], [], set()
for intr in INTERACTIONS:
    uid, pid = intr["user_id"], intr["place_id"]
    if uid not in user_id2idx or pid not in place_id2idx:
        continue
    key = (user_id2idx[uid], place_id2idx[pid])
    if key not in added:
        added.add(key)
        edge_src.append(key[0])
        edge_dst.append(key[1])

NUM_USERS  = len(USERS_DATA)
if len(edge_src) < NUM_USERS * 2:
    print(f"  [!] Few interactions — adding preference edges")
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
data["place", "rev_interacts", "user"].edge_index = torch.tensor(
    [edge_dst, edge_src], dtype=torch.long
)
data = data.to(device)

print(f"  User nodes  : {data['user'].x.shape}")
print(f"  Place nodes : {data['place'].x.shape}")
print(f"  Edges       : {data['user','interacts_with','place'].edge_index.shape[1]}")

# ════════════════════════════════════════════════════════════════
# 3. Reproduce same train/val/test split (same SEED)
# ════════════════════════════════════════════════════════════════
pos_edge_index = data["user", "interacts_with", "place"].edge_index
num_edges = pos_edge_index.size(1)
perm      = torch.randperm(num_edges, generator=torch.Generator().manual_seed(SEED))

val_size  = max(1, int(num_edges * 0.15))
test_size = max(1, int(num_edges * 0.15))

test_edge_index = pos_edge_index[:, perm[:test_size]]
val_edge_index  = pos_edge_index[:, perm[test_size : test_size + val_size]]

# ════════════════════════════════════════════════════════════════
# 4. Define model (identical architecture)
# ════════════════════════════════════════════════════════════════
class BaseGNN(torch.nn.Module):
    def __init__(self, hidden_channels):
        super().__init__()
        self.conv1 = SAGEConv((-1, -1), hidden_channels)
        self.conv2 = SAGEConv((-1, -1), hidden_channels)
        self.dropout = torch.nn.Dropout(p=0.3)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index).relu()
        x = self.dropout(x)
        x = self.conv2(x, edge_index)
        return x

model = to_hetero(BaseGNN(HIDDEN_DIM), metadata=data.metadata()).to(device)

# Lazy init
with torch.no_grad():
    model(data.x_dict, data.edge_index_dict)

# ════════════════════════════════════════════════════════════════
# 5. Load trained weights
# ════════════════════════════════════════════════════════════════
if not os.path.exists(MODEL_FILE):
    print(f"\n[ERROR] gnn_model.pt not found at: {MODEL_FILE}")
    print("  Please run train_gnn.py first.")
    sys.exit(1)

ckpt = torch.load(MODEL_FILE, map_location=device)
model.load_state_dict(ckpt["model_state"])
model.eval()
print(f"[OK] Loaded model from: {MODEL_FILE}")

# ════════════════════════════════════════════════════════════════
# 6. Compute scores for ROC
# ════════════════════════════════════════════════════════════════
def get_scores_labels(edge_pos, num_u, num_p):
    """Return (scores, labels) for positive + equal-size negative edges."""
    with torch.no_grad():
        out = model(data.x_dict, data.edge_index_dict)

        # Positive pairs
        ps, pd = edge_pos[0], edge_pos[1]
        pos_scores = torch.sigmoid(
            (out["user"][ps] * out["place"][pd]).sum(dim=-1)
        ).cpu().numpy()

        # Negative pairs (same count)
        neg_ei = negative_sampling(
            edge_index=edge_pos,
            num_nodes=(num_u, num_p),
            num_neg_samples=edge_pos.size(1),
        )
        ns, nd = neg_ei[0], neg_ei[1]
        neg_scores = torch.sigmoid(
            (out["user"][ns] * out["place"][nd]).sum(dim=-1)
        ).cpu().numpy()

    scores = np.concatenate([pos_scores, neg_scores])
    labels = np.concatenate([np.ones(len(pos_scores)), np.zeros(len(neg_scores))])
    return scores, labels


nu = data["user"].num_nodes
np_ = data["place"].num_nodes

print("[*] Computing validation scores ...")
val_scores, val_labels = get_scores_labels(val_edge_index, nu, np_)

print("[*] Computing test scores ...")
test_scores, test_labels = get_scores_labels(test_edge_index, nu, np_)

# ════════════════════════════════════════════════════════════════
# 7. Plot ROC Curve
# ════════════════════════════════════════════════════════════════
val_fpr,  val_tpr,  _ = roc_curve(val_labels,  val_scores)
test_fpr, test_tpr, _ = roc_curve(test_labels, test_scores)
val_auc  = auc(val_fpr,  val_tpr)
test_auc = auc(test_fpr, test_tpr)

fig, ax = plt.subplots(figsize=(7, 6))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

# Random guess baseline
ax.plot([0, 1], [0, 1], linestyle="--", color="#aaaaaa", linewidth=1.5,
        label="Random Guess")

# Val ROC
ax.plot(val_fpr, val_tpr,
        color="#1a56db", linewidth=2.5,
        label=f"Validation ROC (AUC = {val_auc:.2f})")

# Test ROC
ax.plot(test_fpr, test_tpr,
        color="#e67e22", linewidth=2.5,
        label=f"Test ROC (AUC = {test_auc:.2f})")

ax.set_xlim([0.0, 1.0])
ax.set_ylim([0.0, 1.05])
ax.set_xlabel("False Positive Rate (FPR)", fontsize=12)
ax.set_ylabel("True Positive Rate (TPR)", fontsize=12)
ax.set_title("Receiver Operating Characteristic (ROC) Curve",
             fontsize=13, fontweight="bold")
ax.legend(loc="lower right", fontsize=10)
ax.grid(alpha=0.3)

for spine in ax.spines.values():
    spine.set_edgecolor("#cccccc")

plt.tight_layout()
plt.savefig(OUT_FILE, dpi=150, bbox_inches="tight")
plt.close()

print(f"\n[OK] ROC curve saved: {OUT_FILE}")
print(f"     Validation AUC : {val_auc:.4f}")
print(f"     Test AUC       : {test_auc:.4f}")
