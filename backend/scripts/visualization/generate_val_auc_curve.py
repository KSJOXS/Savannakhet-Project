import os
import sys
import torch
import torch.nn.functional as F
from sklearn.metrics import roc_auc_score
import matplotlib.pyplot as plt
import matplotlib as mpl

# Set font
mpl.rcParams['font.family'] = 'Tahoma'

# Add backend root to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(backend_dir)

from app.database import SessionLocal
from app.services.gnn_service import build_gnn_graph
from app.services.recommendation import SavannakhetRecommender
from torch_geometric.utils import negative_sampling

def generate_auc_plot():
    db = SessionLocal()
    data, _, _ = build_gnn_graph(db)
    db.close()

    edge_index = data['user', 'interacts_with', 'place'].edge_index
    if not edge_index.numel():
        print("Error: No interaction data found in database.")
        return

    model = SavannakhetRecommender(hidden_channels=64, data_metadata=data.metadata())
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

    num_edges = edge_index.size(1)
    perm = torch.randperm(num_edges)
    train_size = int(0.8 * num_edges)
    
    train_edges = edge_index[:, perm[:train_size]]
    val_edges = edge_index[:, perm[train_size:]]

    epochs = 150
    val_aucs = []

    print(f"Starting training... {train_size} train edges, {num_edges - train_size} val edges.")

    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        
        out_dict = model(data.x_dict, data.edge_index_dict)
        pos_out = (out_dict['user'][train_edges[0]] * out_dict['place'][train_edges[1]]).sum(dim=-1)
        neg_train_edges = negative_sampling(
            edge_index=train_edges,
            num_nodes=(data['user'].num_nodes, data['place'].num_nodes),
            num_neg_samples=train_edges.size(1)
        )
        neg_out = (out_dict['user'][neg_train_edges[0]] * out_dict['place'][neg_train_edges[1]]).sum(dim=-1)
        loss = F.binary_cross_entropy_with_logits(
            torch.cat([pos_out, neg_out]),
            torch.cat([torch.ones(pos_out.size(0)), torch.zeros(neg_out.size(0))])
        )
        loss.backward()
        optimizer.step()
        
        # Validation
        model.eval()
        with torch.no_grad():
            out_dict = model(data.x_dict, data.edge_index_dict)
            pos_val_out = (out_dict['user'][val_edges[0]] * out_dict['place'][val_edges[1]]).sum(dim=-1)
            neg_val_edges = negative_sampling(
                edge_index=val_edges,
                num_nodes=(data['user'].num_nodes, data['place'].num_nodes),
                num_neg_samples=val_edges.size(1)
            )
            neg_val_out = (out_dict['user'][neg_val_edges[0]] * out_dict['place'][neg_val_edges[1]]).sum(dim=-1)
            
            y_true = torch.cat([torch.ones(pos_val_out.size(0)), torch.zeros(neg_val_out.size(0))]).cpu().numpy()
            y_scores = torch.sigmoid(torch.cat([pos_val_out, neg_val_out])).cpu().numpy()
            try:
                auc = roc_auc_score(y_true, y_scores)
            except ValueError:
                auc = 0.5
            val_aucs.append(auc)

    # Plotting AUC separately
    plt.figure(figsize=(8, 5))
    plt.style.use('seaborn-v0_8-whitegrid')

    plt.plot(val_aucs, label='Validation AUC', color='green', linewidth=2.5)
    plt.xlabel('Epoch', fontsize=12)
    plt.ylabel('ROC-AUC Score', fontsize=12)
    plt.title('Validation AUC over Epochs', fontsize=16, fontweight='bold', pad=15)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.4)

    plt.tight_layout()
    plots_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'plots')
    os.makedirs(plots_dir, exist_ok=True)
    output_path = os.path.join(plots_dir, 'val_auc_curve.png')
    plt.savefig(output_path, dpi=300)
    print(f"Validation AUC Plot saved successfully at: {output_path}")

if __name__ == '__main__':
    generate_auc_plot()
