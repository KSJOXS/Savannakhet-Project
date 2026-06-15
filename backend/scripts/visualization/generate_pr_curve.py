from app.services.recommendation import SavannakhetRecommender
from app.services.gnn_service import build_gnn_graph
from app.database import SessionLocal
from torch_geometric.utils import negative_sampling
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_recall_curve, average_precision_score
import matplotlib as mpl
import matplotlib.pyplot as plt
import os
import sys
import torch
import torch.nn.functional as F
import numpy as np
import matplotlib
matplotlib.use('Agg')

# Set font
mpl.rcParams['font.family'] = 'Tahoma'

# Add backend root to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(backend_dir)


# ============================================================
# Step 1: Load real data from database
# ============================================================
print("Loading real data from database...")
db = SessionLocal()
data, user_mapping, place_mapping = build_gnn_graph(db)
db.close()

edge_index = data['user', 'interacts_with', 'place'].edge_index
num_edges = edge_index.size(1)

if num_edges < 10:
    print(
        f"Error: Not enough interaction data (found only {num_edges} edges). Please add more user interactions first.")
    sys.exit(1)

print(f"Found {num_edges} real interactions (edges) in the database.")
print(f"  - Users: {data['user'].x.size(0)}")
print(f"  - Places: {data['place'].x.size(0)}")

# ============================================================
# Step 2: Prepare user+place feature matrix for sklearn models
# ============================================================
# Combine user and place embeddings as flat features for sklearn
user_feats = data['user'].x.numpy()   # shape: (num_users, user_feat_dim)
place_feats = data['place'].x.numpy()  # shape: (num_places, place_feat_dim)

# Build positive samples (real interactions from DB)
pos_u = edge_index[0].numpy()
pos_p = edge_index[1].numpy()
pos_X = np.hstack([user_feats[pos_u], place_feats[pos_p]])
pos_y = np.ones(len(pos_u))

# Build negative samples (random non-interacted pairs, same count)
all_user_ids = np.arange(data['user'].x.size(0))
all_place_ids = np.arange(data['place'].x.size(0))

# Create set of existing edges to avoid false negatives
existing_edges = set(zip(pos_u.tolist(), pos_p.tolist()))

neg_u, neg_p = [], []
rng = np.random.default_rng(42)
max_tries = num_edges * 20
tries = 0
while len(neg_u) < num_edges and tries < max_tries:
    ru = rng.integers(0, data['user'].x.size(0))
    rp = rng.integers(0, data['place'].x.size(0))
    if (ru, rp) not in existing_edges:
        neg_u.append(ru)
        neg_p.append(rp)
    tries += 1

neg_u = np.array(neg_u)
neg_p = np.array(neg_p)
neg_X = np.hstack([user_feats[neg_u], place_feats[neg_p]])
neg_y = np.zeros(len(neg_u))

# Combine positive + negative
X_all = np.vstack([pos_X, neg_X])
y_all = np.concatenate([pos_y, neg_y])

X_train, X_test, y_train, y_test = train_test_split(
    X_all, y_all, test_size=0.3, random_state=42, stratify=y_all)
print(f"\nData split: Train={len(y_train)}, Test={len(y_test)}")
print(f"  Positive rate in test set: {y_test.mean():.1%}")

# ============================================================
# Step 3: Train GNN and get predictions
# ============================================================
print("\nTraining GNN model on real data...")

# Split edges for GNN train/test
perm = torch.randperm(num_edges)
train_size = int(0.7 * num_edges)
train_edges = edge_index[:, perm[:train_size]]
test_edges = edge_index[:, perm[train_size:]]

gnn_model = SavannakhetRecommender(
    hidden_channels=64, data_metadata=data.metadata())
optimizer = torch.optim.Adam(gnn_model.parameters(), lr=0.01)

best_val_auc = -1
best_y_true = None
best_y_score = None

for epoch in range(150):
    gnn_model.train()
    optimizer.zero_grad()

    out_dict = gnn_model(data.x_dict, data.edge_index_dict)
    pos_out = (out_dict['user'][train_edges[0]] *
               out_dict['place'][train_edges[1]]).sum(dim=-1)

    neg_train_edges = negative_sampling(
        edge_index=train_edges,
        num_nodes=(data['user'].num_nodes, data['place'].num_nodes),
        num_neg_samples=train_edges.size(1)
    )
    neg_out = (out_dict['user'][neg_train_edges[0]] *
               out_dict['place'][neg_train_edges[1]]).sum(dim=-1)

    loss = F.binary_cross_entropy_with_logits(
        torch.cat([pos_out, neg_out]),
        torch.cat([torch.ones(pos_out.size(0)), torch.zeros(neg_out.size(0))])
    )
    loss.backward()
    optimizer.step()

    if (epoch + 1) % 30 == 0:
        print(f"  Epoch {epoch+1}/150 | Loss: {loss.item():.4f}")

# Final GNN test evaluation
gnn_model.eval()
with torch.no_grad():
    out_dict = gnn_model(data.x_dict, data.edge_index_dict)
    pos_test_out = (out_dict['user'][test_edges[0]] *
                    out_dict['place'][test_edges[1]]).sum(dim=-1)

    neg_test_edges = negative_sampling(
        edge_index=test_edges,
        num_nodes=(data['user'].num_nodes, data['place'].num_nodes),
        num_neg_samples=test_edges.size(1)
    )
    neg_test_out = (out_dict['user'][neg_test_edges[0]]
                    * out_dict['place'][neg_test_edges[1]]).sum(dim=-1)

    gnn_y_true = torch.cat([torch.ones(pos_test_out.size(
        0)), torch.zeros(neg_test_out.size(0))]).cpu().numpy()
    gnn_y_score = torch.sigmoid(
        torch.cat([pos_test_out, neg_test_out])).cpu().numpy()

gnn_precision, gnn_recall, _ = precision_recall_curve(gnn_y_true, gnn_y_score)
gnn_ap = average_precision_score(gnn_y_true, gnn_y_score)
print(f"\nGNN Average Precision (AP): {gnn_ap:.4f}")

# ============================================================
# Step 4: Train Logistic Regression
# ============================================================
print("Training Logistic Regression baseline...")
lr_model = LogisticRegression(max_iter=1000)
lr_model.fit(X_train, y_train)
lr_y_score = lr_model.predict_proba(X_test)[:, 1]
lr_precision, lr_recall, _ = precision_recall_curve(y_test, lr_y_score)
lr_ap = average_precision_score(y_test, lr_y_score)
print(f"Logistic Regression AP: {lr_ap:.4f}")

# ============================================================
# Step 5: Train Random Forest
# ============================================================
print("Training Random Forest baseline...")
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
rf_y_score = rf_model.predict_proba(X_test)[:, 1]
rf_precision, rf_recall, _ = precision_recall_curve(y_test, rf_y_score)
rf_ap = average_precision_score(y_test, rf_y_score)
print(f"Random Forest AP:         {rf_ap:.4f}")

# ============================================================
# Step 6: Plot — Academic document style (single GNN curve)
# ============================================================
print("\nPlotting Precision-Recall Curve (academic style)...")

fig, ax = plt.subplots(figsize=(7, 6))

# White background, clean style
ax.set_facecolor('white')
fig.patch.set_facecolor('white')

# ---- GNN Precision-Recall Curve (blue, with light fill) ----
ax.plot(gnn_recall, gnn_precision,
        color='steelblue', lw=1.5,
        label=f'Precision-Recall curve (AP = {gnn_ap:.2f})')
ax.fill_between(gnn_recall, gnn_precision,
                alpha=0.15, color='steelblue')

# ---- Axes labels ----
ax.set_xlabel('Recall', fontsize=12)
ax.set_ylabel('Precision', fontsize=12)

# ---- Title (same style as in the document) ----
ax.set_title('Precision-Recall Curve', fontsize=13,
             fontweight='normal', pad=10)

# ---- Axis range ----
ax.set_xlim([0.0, 1.0])
ax.set_ylim([0.0, 1.05])
ax.set_xticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])

# ---- Grid (light, matching document style) ----
ax.grid(True, color='#e0e0e0', linewidth=0.8, linestyle='-')
ax.set_axisbelow(True)

# ---- Border (all 4 sides, thin) ----
for spine in ax.spines.values():
    spine.set_edgecolor('#aaaaaa')
    spine.set_linewidth(0.8)

# ---- Legend (bottom left, inside plot) ----
ax.legend(loc='lower left', fontsize=10, framealpha=0.9,
          edgecolor='#cccccc', facecolor='white')

plt.tight_layout()
plots_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'plots')
os.makedirs(plots_dir, exist_ok=True)
output_path = os.path.join(plots_dir, 'pr_curve_real.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"\nSuccessfully saved: {output_path}")

# ============================================================
# Step 7: Print summary for report/advisor
# ============================================================
baseline = y_test.mean()
print("\n" + "="*55)
print("  PRECISION-RECALL SUMMARY (Real Data)")
print("="*55)
print(f"  Total interactions (edges) : {num_edges}")
print(f"  Users                      : {data['user'].x.size(0)}")
print(f"  Places                     : {data['place'].x.size(0)}")
print(f"  Test set size              : {len(y_test)}")
print(f"  Positive rate (test)       : {baseline:.1%}")
print("-"*55)
print(f"  Logistic Regression AP     : {lr_ap:.4f}")
print(f"  Random Forest AP           : {rf_ap:.4f}")
print(f"  GNN (our model) AP         : {gnn_ap:.4f}")
best_model = max([("Logistic Regression", lr_ap),
                 ("Random Forest", rf_ap), ("GNN", gnn_ap)], key=lambda x: x[1])
print(f"\n  Best model: {best_model[0]} (AP = {best_model[1]:.4f})")
print("="*55)
