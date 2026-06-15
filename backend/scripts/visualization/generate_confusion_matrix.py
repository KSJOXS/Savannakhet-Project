from torch_geometric.utils import negative_sampling
from app.services.recommendation import SavannakhetRecommender
from app.services.gnn_service import build_gnn_graph
from app.database import SessionLocal
import seaborn as sns
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import os
import sys
import torch
import torch.nn.functional as F
from sklearn.metrics import confusion_matrix
import matplotlib
matplotlib.use('Agg')

# Set font
mpl.rcParams['font.family'] = 'Arial'

# Add backend root to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(backend_dir)


def generate_cm():
    # ============================================================
    # Step 1: Load real data
    # ============================================================
    print("Loading real data from database...")
    db = SessionLocal()
    data, _, _ = build_gnn_graph(db)
    db.close()

    edge_index = data['user', 'interacts_with', 'place'].edge_index
    num_edges = edge_index.size(1)

    if not edge_index.numel():
        print("Error: No interaction data found in database.")
        return

    print(
        f"Found {num_edges} interactions | Users: {data['user'].x.size(0)} | Places: {data['place'].x.size(0)}")

    # ============================================================
    # Step 2: Train/Test split and GNN training
    # ============================================================
    perm = torch.randperm(num_edges)
    train_size = int(0.8 * num_edges)
    train_edges = edge_index[:, perm[:train_size]]
    test_edges = edge_index[:, perm[train_size:]]

    model = SavannakhetRecommender(
        hidden_channels=64, data_metadata=data.metadata())
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

    print("Training GNN model (150 epochs)...")
    for epoch in range(150):
        model.train()
        optimizer.zero_grad()
        out_dict = model(data.x_dict, data.edge_index_dict)
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
            torch.cat([torch.ones(pos_out.size(0)),
                      torch.zeros(neg_out.size(0))])
        )
        loss.backward()
        optimizer.step()
        if (epoch + 1) % 30 == 0:
            print(f"  Epoch {epoch+1}/150 | Loss: {loss.item():.4f}")

    # ============================================================
    # Step 3: Evaluate on test set
    # ============================================================
    print("\nEvaluating on test set...")
    model.eval()
    with torch.no_grad():
        out_dict = model(data.x_dict, data.edge_index_dict)
        pos_test_out = (out_dict['user'][test_edges[0]]
                        * out_dict['place'][test_edges[1]]).sum(dim=-1)
        neg_test_edges = negative_sampling(
            edge_index=test_edges,
            num_nodes=(data['user'].num_nodes, data['place'].num_nodes),
            num_neg_samples=test_edges.size(1)
        )
        neg_test_out = (out_dict['user'][neg_test_edges[0]]
                        * out_dict['place'][neg_test_edges[1]]).sum(dim=-1)

        y_true = torch.cat([torch.ones(pos_test_out.size(0)),
                           torch.zeros(neg_test_out.size(0))]).cpu().numpy()
        y_score = torch.sigmoid(torch.cat([pos_test_out, neg_test_out]))
        y_pred = (y_score >= 0.5).int().cpu().numpy()

    # ============================================================
    # Step 4: Compute and print confusion matrix values
    # ============================================================
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()

    print(f"\nConfusion Matrix:")
    print(f"  TN (True Negative)  = {tn}")
    print(f"  FP (False Positive) = {fp}")
    print(f"  FN (False Negative) = {fn}")
    print(f"  TP (True Positive)  = {tp}")
    total = tn + fp + fn + tp
    accuracy = (tp + tn) / total
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / \
        (precision + recall) if (precision + recall) > 0 else 0
    print(f"\n  Accuracy  = {accuracy:.4f}")
    print(f"  Precision = {precision:.4f}")
    print(f"  Recall    = {recall:.4f}")
    print(f"  F1-Score  = {f1:.4f}")

    # ============================================================
    # Step 5: Plot — academic document style
    # ============================================================
    fig, ax = plt.subplots(figsize=(6, 5))
    fig.patch.set_facecolor('white')

    # Blues colormap (matching document style)
    sns.heatmap(
        cm,
        annot=False,          # we draw numbers manually for full control
        fmt='d',
        cmap='Blues',
        cbar=True,
        linewidths=0.5,
        linecolor='#cccccc',
        ax=ax,
        xticklabels=['Negative', 'Positive'],
        yticklabels=['Negative', 'Positive']
    )

    # Draw numbers inside cells
    thresh = cm.max() / 2.0
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j + 0.5, i + 0.5,
                    str(cm[i, j]),
                    ha='center', va='center',
                    fontsize=18, fontweight='bold',
                    color='white' if cm[i, j] > thresh else 'black')

    # Labels
    ax.set_xlabel('Predicted Label', fontsize=12, labelpad=8)
    ax.set_ylabel('True Label', fontsize=12, labelpad=8)
    ax.set_title('Confusion Matrix', fontsize=13, fontweight='normal', pad=10)

    # Tick label style
    ax.tick_params(axis='both', labelsize=11)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, va='center')

    plt.tight_layout()
    plots_dir = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'plots')
    os.makedirs(plots_dir, exist_ok=True)
    output_path = os.path.join(plots_dir, 'gnn_confusion_matrix.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"\nSuccessfully saved: {output_path}")


if __name__ == '__main__':
    generate_cm()
