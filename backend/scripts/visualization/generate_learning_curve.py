from torch_geometric.utils import negative_sampling
from app.services.recommendation import SavannakhetRecommender
from app.services.gnn_service import build_gnn_graph
from app.database import SessionLocal
import matplotlib as mpl
import matplotlib.pyplot as plt
import os
import sys
import torch
import torch.nn.functional as F
from sklearn.metrics import roc_auc_score
import matplotlib
matplotlib.use('Agg')

mpl.rcParams['font.family'] = 'Arial'


# Add backend root to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(backend_dir)


def generate_plot():
    db = SessionLocal()
    data, _, _ = build_gnn_graph(db)
    db.close()

    edge_index = data['user', 'interacts_with', 'place'].edge_index
    if not edge_index.numel():
        print("Error: No interaction data found in database.")
        return

    # Prepare model
    model = SavannakhetRecommender(
        hidden_channels=64, data_metadata=data.metadata())
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

    # 80-20 Train-Val split
    num_edges = edge_index.size(1)
    perm = torch.randperm(num_edges)
    train_size = int(0.8 * num_edges)

    train_edges = edge_index[:, perm[:train_size]]
    val_edges = edge_index[:, perm[train_size:]]

    epochs = 150
    train_losses = []
    val_losses = []
    val_aucs = []

    print(
        f"Starting training... {train_size} train edges, {num_edges - train_size} val edges.")

    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()

        # Forward
        out_dict = model(data.x_dict, data.edge_index_dict)

        # Positive train edges
        pos_out = (out_dict['user'][train_edges[0]] *
                   out_dict['place'][train_edges[1]]).sum(dim=-1)

        # Negative train edges
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

        train_losses.append(loss.item())

        # Validation
        model.eval()
        with torch.no_grad():
            out_dict = model(data.x_dict, data.edge_index_dict)

            # Pos val edges
            pos_val_out = (out_dict['user'][val_edges[0]]
                           * out_dict['place'][val_edges[1]]).sum(dim=-1)

            # Neg val edges
            neg_val_edges = negative_sampling(
                edge_index=val_edges,
                num_nodes=(data['user'].num_nodes, data['place'].num_nodes),
                num_neg_samples=val_edges.size(1)
            )
            neg_val_out = (out_dict['user'][neg_val_edges[0]]
                           * out_dict['place'][neg_val_edges[1]]).sum(dim=-1)

            val_loss = F.binary_cross_entropy_with_logits(
                torch.cat([pos_val_out, neg_val_out]),
                torch.cat([torch.ones(pos_val_out.size(0)),
                          torch.zeros(neg_val_out.size(0))])
            )
            val_losses.append(val_loss.item())

            # Calculate AUC
            y_true = torch.cat([torch.ones(pos_val_out.size(0)), torch.zeros(
                neg_val_out.size(0))]).cpu().numpy()
            y_scores = torch.sigmoid(
                torch.cat([pos_val_out, neg_val_out])).cpu().numpy()
            try:
                auc = roc_auc_score(y_true, y_scores)
            except ValueError:
                auc = 0.5
            val_aucs.append(auc)

        if (epoch + 1) % 10 == 0:
            print(
                f"Epoch {epoch+1:03d}: Train Loss: {loss.item():.4f}, Val Loss: {val_loss.item():.4f}, Val AUC: {auc:.4f}")

    # ============================================================
    # Plotting — academic document style
    # ============================================================
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    fig.patch.set_facecolor('white')

    # ---- Loss Curve ----
    ax1.set_facecolor('white')
    ax1.plot(train_losses, label='Train Loss',
             color='steelblue', linewidth=1.5)
    ax1.plot(val_losses,   label='Validation Loss',
             color='tomato', linestyle='--', linewidth=1.5)
    ax1.set_xlabel('Epoch', fontsize=12)
    ax1.set_ylabel('Binary Cross-Entropy Loss', fontsize=12)
    ax1.set_title('Learning Curve (Loss)', fontsize=13,
                  fontweight='normal', pad=10)
    ax1.legend(fontsize=10, framealpha=0.9, edgecolor='#cccccc')
    ax1.grid(True, color='#e0e0e0', linewidth=0.8)
    ax1.set_axisbelow(True)
    for spine in ax1.spines.values():
        spine.set_edgecolor('#aaaaaa')
        spine.set_linewidth(0.8)

    # ---- AUC Curve ----
    ax2.set_facecolor('white')
    ax2.plot(val_aucs, label='Validation AUC', color='seagreen', linewidth=1.5)
    ax2.set_xlabel('Epoch', fontsize=12)
    ax2.set_ylabel('ROC-AUC Score', fontsize=12)
    ax2.set_title('Validation AUC over Epochs',
                  fontsize=13, fontweight='normal', pad=10)
    ax2.legend(fontsize=10, framealpha=0.9, edgecolor='#cccccc')
    ax2.grid(True, color='#e0e0e0', linewidth=0.8)
    ax2.set_axisbelow(True)
    ax2.set_ylim([0.0, 1.05])
    for spine in ax2.spines.values():
        spine.set_edgecolor('#aaaaaa')
        spine.set_linewidth(0.8)

    plt.tight_layout()
    plots_dir = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'plots')
    os.makedirs(plots_dir, exist_ok=True)
    output_path = os.path.join(plots_dir, 'gnn_learning_curve.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Successfully saved: {output_path}")


if __name__ == '__main__':
    generate_plot()
