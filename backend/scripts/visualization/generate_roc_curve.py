import os
import sys
import torch
import torch.nn.functional as F
from sklearn.metrics import roc_curve, auc
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

def generate_roc_curve():
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
    
    # 70% Train, 15% Val, 15% Test split
    train_size = int(0.7 * num_edges)
    val_size = int(0.15 * num_edges)
    
    train_edges = edge_index[:, perm[:train_size]]
    val_edges = edge_index[:, perm[train_size:train_size+val_size]]
    test_edges = edge_index[:, perm[train_size+val_size:]]

    epochs = 150
    best_val_auc = 0
    best_val_y_true, best_val_y_score = None, None
    best_test_y_true, best_test_y_score = None, None

    print(f"Starting training... Train: {train_size}, Val: {val_size}, Test: {num_edges - train_size - val_size}")

    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        
        # Forward pass
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
        
        # Validation & Test evaluation
        model.eval()
        with torch.no_grad():
            out_dict = model(data.x_dict, data.edge_index_dict)
            
            # --- Validation Set ---
            pos_val_out = (out_dict['user'][val_edges[0]] * out_dict['place'][val_edges[1]]).sum(dim=-1)
            neg_val_edges = negative_sampling(
                edge_index=val_edges,
                num_nodes=(data['user'].num_nodes, data['place'].num_nodes),
                num_neg_samples=val_edges.size(1)
            )
            neg_val_out = (out_dict['user'][neg_val_edges[0]] * out_dict['place'][neg_val_edges[1]]).sum(dim=-1)
            
            val_y_true = torch.cat([torch.ones(pos_val_out.size(0)), torch.zeros(neg_val_out.size(0))]).cpu().numpy()
            val_y_score = torch.sigmoid(torch.cat([pos_val_out, neg_val_out])).cpu().numpy()
            
            # Compute Val ROC
            val_fpr, val_tpr, _ = roc_curve(val_y_true, val_y_score)
            current_val_auc = auc(val_fpr, val_tpr)
            
            # --- Test Set ---
            pos_test_out = (out_dict['user'][test_edges[0]] * out_dict['place'][test_edges[1]]).sum(dim=-1)
            neg_test_edges = negative_sampling(
                edge_index=test_edges,
                num_nodes=(data['user'].num_nodes, data['place'].num_nodes),
                num_neg_samples=test_edges.size(1)
            )
            neg_test_out = (out_dict['user'][neg_test_edges[0]] * out_dict['place'][neg_test_edges[1]]).sum(dim=-1)
            
            test_y_true = torch.cat([torch.ones(pos_test_out.size(0)), torch.zeros(neg_test_out.size(0))]).cpu().numpy()
            test_y_score = torch.sigmoid(torch.cat([pos_test_out, neg_test_out])).cpu().numpy()
            
            if current_val_auc > best_val_auc:
                best_val_auc = current_val_auc
                best_val_y_true, best_val_y_score = val_y_true, val_y_score
                best_test_y_true, best_test_y_score = test_y_true, test_y_score

    # Compute Final ROC Curves
    val_fpr, val_tpr, _ = roc_curve(best_val_y_true, best_val_y_score)
    val_roc_auc = auc(val_fpr, val_tpr)

    test_fpr, test_tpr, _ = roc_curve(best_test_y_true, best_test_y_score)
    test_roc_auc = auc(test_fpr, test_tpr)

    # Plotting
    plt.figure(figsize=(8, 6))
    plt.style.use('seaborn-v0_8-whitegrid')

    plt.plot(val_fpr, val_tpr, color='blue', lw=2.5, label=f'Validation ROC (AUC = {val_roc_auc:.2f})')
    plt.plot(test_fpr, test_tpr, color='darkorange', lw=2.5, linestyle='-', label=f'Test ROC (AUC = {test_roc_auc:.2f})')
    
    # Diagonal line (Random Guess)
    plt.plot([0, 1], [0, 1], color='gray', lw=2, linestyle='--', label='Random Guess')

    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate (FPR)', fontsize=13)
    plt.ylabel('True Positive Rate (TPR)', fontsize=13)
    plt.title('Receiver Operating Characteristic (ROC) Curve', fontsize=16, fontweight='bold', pad=15)
    plt.legend(loc="lower right", fontsize=12)
    plt.grid(True, alpha=0.4)

    plt.tight_layout()
    plots_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'plots')
    os.makedirs(plots_dir, exist_ok=True)
    output_path = os.path.join(plots_dir, 'roc_curve.png')
    plt.savefig(output_path, dpi=300)
    print(f"ROC Curve Plot saved successfully at: {output_path}")

if __name__ == '__main__':
    generate_roc_curve()
