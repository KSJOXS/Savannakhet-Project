# ╔══════════════════════════════════════════════════════════════════╗
# ║   COPY โค้ดทั้งหมดนี้ไปวางใน Google Colab แล้วรันได้เลย!        ║
# ║   Hybrid Recommendation: HeteroGraphSAGE + Content-Based        ║
# ║   โปรเจกต์: ระบบแนะนำสถานที่ท่องเที่ยว จ.สะหวันนะเขต          ║
# ╚══════════════════════════════════════════════════════════════════╝

# ═══════════════════════════════════════════════════════════════
# CELL 1: ติดตั้ง Library ที่จำเป็น
# ═══════════════════════════════════════════════════════════════
# !pip install torch-geometric torch-scatter torch-sparse -q

# ─────────────────────────────────────────────────────────────
# หมายเหตุ: ถ้า pip ข้างบน error ให้ใช้คำสั่งนี้แทน:
#
# !pip install torch_geometric -q
# !pip install pyg_lib torch_scatter torch_sparse torch_cluster torch_spline_conv \
#     -f https://data.pyg.org/whl/torch-$(python -c "import torch; print(torch.__version__)")+cu121.html -q
# ─────────────────────────────────────────────────────────────

import torch
import torch.nn.functional as F
from torch_geometric.nn import SAGEConv, to_hetero
from torch_geometric.data import HeteroData
from torch_geometric.utils import negative_sampling
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import random
import json
import time

torch.manual_seed(42)
random.seed(42)
np.random.seed(42)

print("✅ Import สำเร็จ!")
print(f"   PyTorch version : {torch.__version__}")
print(f"   CUDA available  : {torch.cuda.is_available()}")
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"   Device          : {device}")


# ═══════════════════════════════════════════════════════════════
# CELL 2: สร้างข้อมูล Synthetic จำลองสถานที่สะหวันนะเขต
# ═══════════════════════════════════════════════════════════════

# ── หมวดหมู่สถานที่ ──
CATEGORIES = ['nature', 'culture', 'restaurant', 'hotel',
              'shopping', 'nightlife', 'cafe', 'local_food', 'chill', 'landmark']

# ── ข้อมูลสถานที่จำลอง (สะหวันนะเขต) ──
PLACES_DATA = [
    {"name": "วัดสะหวัน",              "category": "culture",     "rating": 4.8},
    {"name": "ตลาดเช้า",               "category": "local_food",  "rating": 4.3},
    {"name": "หาดทรายฟอง",             "category": "nature",      "rating": 4.6},
    {"name": "พิพิธภัณฑ์จังหวัด",       "category": "culture",     "rating": 4.1},
    {"name": "ร้านอาหารริมโขง",         "category": "restaurant",  "rating": 4.5},
    {"name": "สวนสาธารณะ",             "category": "chill",       "rating": 4.0},
    {"name": "คาเฟ่วิวแม่น้ำ",          "category": "cafe",        "rating": 4.7},
    {"name": "ตลาดดินแดง",             "category": "shopping",    "rating": 4.2},
    {"name": "บาร์ริมน้ำ",             "category": "nightlife",   "rating": 3.9},
    {"name": "โรงแรมสะหวันนะเขต",       "category": "hotel",       "rating": 4.4},
    {"name": "น้ำตกบัวระบัด",           "category": "nature",      "rating": 4.9},
    {"name": "หมู่บ้านวัฒนธรรม",        "category": "culture",     "rating": 4.3},
    {"name": "ร้านข้าวเหนียวสังขยา",    "category": "local_food",  "rating": 4.6},
    {"name": "สะพานมิตรภาพ 2",         "category": "landmark",    "rating": 4.5},
    {"name": "ตลาดกลางคืน",            "category": "nightlife",   "rating": 4.1},
    {"name": "ร้านกาแฟลาว",            "category": "cafe",        "rating": 4.4},
    {"name": "อุทยานแห่งชาติ",          "category": "nature",      "rating": 4.7},
    {"name": "ตลาดสด",                 "category": "shopping",    "rating": 3.8},
    {"name": "เกสต์เฮ้าส์ริมโขง",       "category": "hotel",       "rating": 4.2},
    {"name": "ลานวัฒนธรรม",            "category": "chill",       "rating": 4.0},
]

# ── ข้อมูลผู้ใช้จำลอง ──
USERS_DATA = [
    {"name": "dee",  "preferences": ["nature", "culture", "landmark"]},
    {"name": "big",  "preferences": ["restaurant", "cafe", "local_food"]},
    {"name": "noi",  "preferences": ["nightlife", "shopping", "cafe"]},
    {"name": "kai",  "preferences": ["culture", "chill", "local_food"]},
    {"name": "pam",  "preferences": ["nature", "chill", "hotel"]},
    {"name": "tong", "preferences": ["restaurant", "nightlife", "shopping"]},
    {"name": "may",  "preferences": ["culture", "landmark", "local_food"]},
    {"name": "oat",  "preferences": ["nature", "cafe", "chill"]},
    {"name": "bee",  "preferences": ["hotel", "restaurant", "cafe"]},
    {"name": "nam",  "preferences": ["shopping", "nightlife", "landmark"]},
]

NUM_USERS  = len(USERS_DATA)
NUM_PLACES = len(PLACES_DATA)

print(f"✅ ข้อมูลพร้อม!")
print(f"   จำนวนผู้ใช้   : {NUM_USERS}  คน")
print(f"   จำนวนสถานที่  : {NUM_PLACES} แห่ง")
print(f"   หมวดหมู่      : {len(CATEGORIES)} ประเภท")


# ═══════════════════════════════════════════════════════════════
# CELL 3: สร้าง Feature Vectors และ Graph
# ═══════════════════════════════════════════════════════════════

def build_graph():
    """สร้าง HeteroData Graph จากข้อมูลจำลอง"""
    data = HeteroData()

    # ── User Features: Multi-hot Encoding (10 หมวดหมู่) ──
    user_features = []
    for u in USERS_DATA:
        vec = [1.0 if cat in u["preferences"] else 0.0 for cat in CATEGORIES]
        user_features.append(vec)
    data['user'].x = torch.tensor(user_features, dtype=torch.float)

    # ── Place Features: One-hot Category (10 dim) + Rating (1 dim) = 11 dim ──
    place_features = []
    for p in PLACES_DATA:
        vec = [1.0 if cat == p["category"] else 0.0 for cat in CATEGORIES]
        vec.append(p["rating"] / 5.0)   # normalize rating
        place_features.append(vec)
    data['place'].x = torch.tensor(place_features, dtype=torch.float)

    # ── สร้าง Edges: ผู้ใช้ที่ชอบหมวดหมู่เดียวกับสถานที่ → มี interaction ──
    edge_src, edge_dst = [], []
    for u_idx, u in enumerate(USERS_DATA):
        for p_idx, p in enumerate(PLACES_DATA):
            if p["category"] in u["preferences"]:
                edge_src.append(u_idx)
                edge_dst.append(p_idx)
            # เพิ่ม random interaction บ้างเพื่อความหลากหลาย
            elif random.random() < 0.1:
                edge_src.append(u_idx)
                edge_dst.append(p_idx)

    data['user', 'interacts_with', 'place'].edge_index = torch.tensor(
        [edge_src, edge_dst], dtype=torch.long
    )

    print(f"✅ สร้าง Graph สำเร็จ!")
    print(f"   User nodes   : {data['user'].x.shape}   (10 คน × 10 features)")
    print(f"   Place nodes  : {data['place'].x.shape}  (20 แห่ง × 11 features)")
    print(f"   Edges        : {data['user', 'interacts_with', 'place'].edge_index.shape[1]} connections")
    return data

data = build_graph()


# ═══════════════════════════════════════════════════════════════
# CELL 4: นิยาม GNN Model (HeteroGraphSAGE)
# ═══════════════════════════════════════════════════════════════

class BaseGNN(torch.nn.Module):
    """
    2-Layer GraphSAGE
    Tang 1: MEAN Aggregation จาก Neighbors
    Tang 2: Update Embedding ด้วย CONCAT + Linear + ReLU
    """
    def __init__(self, hidden_channels=64):
        super().__init__()
        self.conv1 = SAGEConv((-1, -1), hidden_channels)
        self.conv2 = SAGEConv((-1, -1), hidden_channels)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index).relu()
        x = self.conv2(x, edge_index)
        return x

# แปลง BaseGNN → HeteroGNN (รองรับ node หลายประเภท)
model = to_hetero(BaseGNN(hidden_channels=64), metadata=data.metadata())
model = model.to(device)
data  = data.to(device)

optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

total_params = sum(p.numel() for p in model.parameters())
print(f"✅ สร้างโมเดลสำเร็จ!")
print(f"   Architecture : HeteroGraphSAGE (2 Layers)")
print(f"   Hidden dim   : 64")
print(f"   Parameters   : {total_params:,}")
print(f"   Optimizer    : Adam (lr=0.01)")
print(f"   Loss         : Binary Cross-Entropy with Logits")


# ═══════════════════════════════════════════════════════════════
# CELL 5: เทรนโมเดล (100 Epochs)
# ═══════════════════════════════════════════════════════════════

EPOCHS = 100
losses, accuracies = [], []

pos_edge_index = data['user', 'interacts_with', 'place'].edge_index
n_steps = max(1, pos_edge_index.size(1) // 5)

print("=" * 65)
print("       เริ่มเทรน HeteroGraphSAGE  (100 Epochs)")
print("=" * 65)

for epoch in range(1, EPOCHS + 1):
    model.train()
    t_start = time.time()
    optimizer.zero_grad()

    # Forward pass
    out_dict = model(data.x_dict, data.edge_index_dict)

    # Positive pairs score
    pos_src, pos_dst = pos_edge_index[0], pos_edge_index[1]
    pos_out = (out_dict['user'][pos_src] * out_dict['place'][pos_dst]).sum(dim=-1)

    # Negative sampling
    neg_edge_index = negative_sampling(
        edge_index=pos_edge_index,
        num_nodes=(data['user'].num_nodes, data['place'].num_nodes),
        num_neg_samples=pos_edge_index.size(1)
    )
    neg_src, neg_dst = neg_edge_index[0], neg_edge_index[1]
    neg_out = (out_dict['user'][neg_src] * out_dict['place'][neg_dst]).sum(dim=-1)

    # Compute Loss (BCE)
    labels = torch.cat([torch.ones(pos_out.size(0)), torch.zeros(neg_out.size(0))]).to(device)
    preds  = torch.cat([pos_out, neg_out])
    loss   = F.binary_cross_entropy_with_logits(preds, labels)

    loss.backward()
    optimizer.step()
    losses.append(loss.item())

    # Accuracy
    with torch.no_grad():
        pos_pred = (pos_out >= 0).float()
        neg_pred = (neg_out  < 0).float()
        correct  = pos_pred.sum().item() + neg_pred.sum().item()
        total    = pos_out.size(0) + neg_out.size(0)
        acc      = correct / total
        accuracies.append(acc)

    # แสดงผลทุก 5 epoch
    if epoch % 5 == 0 or epoch == 1:
        t_elapsed  = (time.time() - t_start) * 1000
        step_time  = max(1, int(t_elapsed / n_steps))
        total_time = int(t_elapsed / 1000)
        print(f"Epoch {epoch:>3}/{EPOCHS}  |  "
              f"{n_steps}/{n_steps} ━━━━━━━━━━━━━━━━━━━━  "
              f"{total_time}s {step_time}ms/step  "
              f"accuracy: {acc:.4f}  loss: {loss.item():.4f}")

print("\n✅ เทรนเสร็จแล้ว!")
print(f"   Final Accuracy : {accuracies[-1]*100:.2f}%")
print(f"   Final Loss     : {losses[-1]:.4f}")


# ═══════════════════════════════════════════════════════════════
# CELL 6: วาดกราฟ Accuracy & Loss
# ═══════════════════════════════════════════════════════════════

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle("Savannakhet GNN - Training Results", fontsize=14, fontweight='bold', y=1.02)

epoch_range = range(1, EPOCHS + 1)

# ── Left: Accuracy ──
ax1 = axes[0]
ax1.plot(epoch_range, accuracies, color='#2563EB', linewidth=2, label='Train Accuracy')
ax1.fill_between(epoch_range, accuracies, alpha=0.15, color='#2563EB')
ax1.axhline(y=0.85, color='#059669', linestyle='--', linewidth=1.2, label='Target 85%')
ax1.set_title('Model Accuracy', fontsize=11, fontweight='bold')
ax1.set_xlabel('Epochs')
ax1.set_ylabel('Accuracy')
ax1.set_ylim(0.4, 1.05)
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y*100:.0f}%'))

# ── Right: Loss ──
ax2 = axes[1]
ax2.plot(epoch_range, losses, color='#DC2626', linewidth=2, label='Train Loss')
ax2.fill_between(epoch_range, losses, alpha=0.12, color='#DC2626')
ax2.set_title('Model Loss', fontsize=11, fontweight='bold')
ax2.set_xlabel('Epochs')
ax2.set_ylabel('Loss')
ax2.set_ylim(bottom=0)
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/content/training_results.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ บันทึกกราฟ: /content/training_results.png")


# ═══════════════════════════════════════════════════════════════
# CELL 7: ทดสอบ Recommendation (Inference)
# ═══════════════════════════════════════════════════════════════

def recommend(user_name: str, top_k: int = 5):
    """แนะนำสถานที่สำหรับผู้ใช้ที่ระบุ"""
    model.eval()

    # หา user index
    user_idx = next((i for i, u in enumerate(USERS_DATA) if u["name"] == user_name), 0)
    user_info = USERS_DATA[user_idx]
    prefs     = user_info["preferences"]

    with torch.no_grad():
        embeddings = model(data.x_dict, data.edge_index_dict)

        user_emb   = embeddings['user'][user_idx]
        place_embs = embeddings['place']

        # ── GNN Collaborative Score (60%) ──
        gnn_scores = F.cosine_similarity(place_embs, user_emb.unsqueeze(0))

        # ── Content-Based Score (40%) ──
        user_pref_vec  = data['user'].x[user_idx, :len(CATEGORIES)]
        place_cat_vecs = data['place'].x[:, :len(CATEGORIES)]
        if user_pref_vec.sum() > 0:
            cb_scores = F.cosine_similarity(place_cat_vecs, user_pref_vec.unsqueeze(0))
        else:
            cb_scores = torch.zeros(NUM_PLACES).to(device)

        # ── Hybrid Score ──
        alpha  = 0.6
        scores = alpha * gnn_scores + (1 - alpha) * cb_scores

        top_vals, top_idxs = torch.topk(scores, k=top_k)

    print("=" * 65)
    print(f"  🌟  Top {top_k} คำแนะนำสำหรับ: {user_name}")
    print(f"  🎯  ความชอบ: {', '.join(prefs)}")
    print("=" * 65)
    for rank, (val, idx) in enumerate(zip(top_vals, top_idxs), 1):
        p    = PLACES_DATA[idx.item()]
        pct  = (val.item() + 1) / 2 * 100
        gnn  = (gnn_scores[idx].item() + 1) / 2 * 100
        cb   = (cb_scores[idx].item() + 1) / 2 * 100
        match = "✓" if p["category"] in prefs else " "
        print(f"  {rank}. {match} {p['name']:<22} [{p['category']:<12}]  ⭐{p['rating']}")
        print(f"       💯 Overall: {pct:.1f}%  "
              f"│  👥 GNN(60%): {gnn:.1f}%  "
              f"│  🎯 Content(40%): {cb:.1f}%")
    print()

# ── ทดสอบกับผู้ใช้หลายคน ──
for test_user in ["dee", "big", "noi"]:
    recommend(test_user, top_k=5)


# ═══════════════════════════════════════════════════════════════
# CELL 8: บันทึกโมเดล (Save Model)
# ═══════════════════════════════════════════════════════════════

SAVE_PATH = '/content/gnn_savannakhet.pt'
torch.save({
    'epoch'       : EPOCHS,
    'model_state' : model.state_dict(),
    'optimizer'   : optimizer.state_dict(),
    'final_acc'   : accuracies[-1],
    'final_loss'  : losses[-1],
    'metadata'    : {
        'hidden_dim' : 64,
        'categories' : CATEGORIES,
        'num_users'  : NUM_USERS,
        'num_places' : NUM_PLACES,
    }
}, SAVE_PATH)
print(f"✅ บันทึกโมเดลแล้ว: {SAVE_PATH}")

# ── สรุปผลลัพธ์ ──
print("\n" + "═" * 65)
print("       📊  สรุปผลการเทรน")
print("═" * 65)
print(f"  Architecture : HeteroGraphSAGE (K=2 layers, hidden=64)")
print(f"  Dataset      : {NUM_USERS} users × {NUM_PLACES} places (Savannakhet)")
print(f"  Epochs       : {EPOCHS}")
print(f"  Best Acc     : {max(accuracies)*100:.2f}%")
print(f"  Final Acc    : {accuracies[-1]*100:.2f}%")
print(f"  Final Loss   : {losses[-1]:.4f}")
print(f"  Model saved  : {SAVE_PATH}")
print("═" * 65)

# ── Download ไฟล์กลับมาที่เครื่อง ──
try:
    from google.colab import files
    files.download(SAVE_PATH)
    files.download('/content/training_results.png')
    print("\n✅ กำลัง Download ไฟล์ไปยังเครื่องของคุณ...")
except ImportError:
    print("\n[INFO] ไม่ได้รันบน Colab - ไฟล์ถูกบันทึกใน /content/")
