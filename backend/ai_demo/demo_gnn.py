import os
import sys
import json
import torch
import torch.nn.functional as F
from torch_geometric.nn import SAGEConv, to_hetero
from torch_geometric.utils import negative_sampling
import matplotlib.pyplot as plt
import networkx as nx

# Add parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

try:
    from app.database import SessionLocal
    from app.services.gnn_service import build_gnn_graph
    from app.models import User, Place, InteractionLog
    DATABASE_AVAILABLE = True
except ImportError as e:
    DATABASE_AVAILABLE = False

class BaseGNN(torch.nn.Module):
    def __init__(self, hidden_channels):
        super().__init__()
        self.conv1 = SAGEConv((-1, -1), hidden_channels)
        self.conv2 = SAGEConv((-1, -1), hidden_channels)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index).relu()
        x = self.conv2(x, edge_index)
        return x

def visualize_graph(data, user_map, place_map, db):
    print("Generating Graph Structure Visualization (Highlighting dee)...")
    G = nx.Graph()
    
    edge_index = data['user', 'interacts_with', 'place'].edge_index
    reverse_user_map = {v: k for k, v in user_map.items()}
    reverse_place_map = {v: k for k, v in place_map.items()}
    
    # 1. Find 'dee' ID and mapped index
    target_user = db.query(User).filter(User.username == "big").first()
    dee_idx = user_map[target_user.id] if target_user and target_user.id in user_map else None
    
    # 2. Collect edges for 'dee' and a few others
    dee_edges = []
    other_edges = []
    
    for i in range(edge_index.size(1)):
        u_idx = edge_index[0, i].item()
        p_idx = edge_index[1, i].item()
        
        if u_idx == dee_idx:
            dee_edges.append((u_idx, p_idx))
        elif len(other_edges) < 15: # Sample 15 other edges for context
            other_edges.append((u_idx, p_idx))
            
    # Combine edges
    sampled_edges = dee_edges + other_edges
    
    for u_idx, p_idx in sampled_edges:
        user_id = reverse_user_map[u_idx]
        place_id = reverse_place_map[p_idx]
        
        user_obj = db.query(User).filter(User.id == user_id).first()
        place_obj = db.query(Place).filter(Place.id == place_id).first()
        
        u_name = user_obj.username if user_obj else f"U{user_id}"
        p_name = place_obj.name if place_obj else f"P{place_id}"
        
        # Color dee differently
        u_color = 'orange' if u_name == 'dee' else 'skyblue'
        
        G.add_node(u_name, color=u_color, label='User')
        G.add_node(p_name, color='lightgreen', label='Place')
        G.add_edge(u_name, p_name)

    plt.figure(figsize=(12, 10))
    pos = nx.spring_layout(G, k=0.5, seed=42)
    
    colors = [G.nodes[n]['color'] for n in G.nodes]
    nx.draw(G, pos, with_labels=True, node_color=colors, node_size=2500, font_size=9, edge_color='gray', width=1.5)
    
    plt.title("Savannakhet Project - Graph Visualization (dee highlighted in orange)")
    plt.savefig(os.path.join(current_dir, "graph_structure.png"))
    print(f"Saved: {os.path.join(current_dir, 'graph_structure.png')}")

def run_real_demo():
    print("\n" + "="*60)
    print("      SAVANNAKHET GNN - REAL DATA AI DEMO      ")
    print("="*60)
    
    if not DATABASE_AVAILABLE:
        print("Error: Database connection failed.")
        return

    # Set deterministic seed for reproducible results
    torch.manual_seed(42)

    db = SessionLocal()
    try:
        data, user_map, place_map = build_gnn_graph(db)
        
        # 1. Visualize Graph Structure
        visualize_graph(data, user_map, place_map, db)
        
        model = to_hetero(BaseGNN(hidden_channels=32), metadata=data.metadata())
        optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
        
        losses = []
        print("\n--- Training AI ---")
        for epoch in range(1, 101):
            optimizer.zero_grad()
            out_dict = model(data.x_dict, data.edge_index_dict)
            
            pos_edge_index = data['user', 'interacts_with', 'place'].edge_index
            pos_src, pos_dst = pos_edge_index[0], pos_edge_index[1]
            pos_out = (out_dict['user'][pos_src] * out_dict['place'][pos_dst]).sum(dim=-1)
            
            neg_edge_index = negative_sampling(
                edge_index=pos_edge_index,
                num_nodes=(data['user'].num_nodes, data['place'].num_nodes),
                num_neg_samples=pos_edge_index.size(1)
            )
            neg_src, neg_dst = neg_edge_index[0], neg_edge_index[1]
            neg_out = (out_dict['user'][neg_src] * out_dict['place'][neg_dst]).sum(dim=-1)
            
            loss = F.binary_cross_entropy_with_logits(
                torch.cat([pos_out, neg_out]),
                torch.cat([torch.ones(pos_out.size(0)), torch.zeros(neg_out.size(0))])
            )
            loss.backward()
            optimizer.step()
            losses.append(loss.item())
            
            if epoch % 20 == 0:
                print(f"Epoch {epoch:03d}: Loss = {loss.item():.6f}")

        # 2. Save Loss Chart
        plt.figure(figsize=(8, 5))
        plt.plot(losses, label='Training Loss', color='red')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.title('AI Learning Progress (Loss Curve)')
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(current_dir, "loss_chart.png"))
        print(f"Saved: {os.path.join(current_dir, 'loss_chart.png')}")

        print("\n--- Recommendation Test ---")
        model.eval()
        with torch.no_grad():
            target_user = db.query(User).filter(User.username == "nam").first()
            test_user_id = target_user.id if (target_user and target_user.id in user_map) else list(user_map.keys())[0]
            
            mapped_user = user_map[test_user_id]
            user_name = db.query(User).filter(User.id == test_user_id).first().username
            
            final_embeddings = model(data.x_dict, data.edge_index_dict)
            
            # === FIX: Hybrid Score (GNN + Content-Based) ===
            user_emb = final_embeddings['user'][mapped_user]
            place_embs = final_embeddings['place']
            
            # 1) GNN Collaborative Score
            gnn_scores = F.cosine_similarity(place_embs, user_emb.unsqueeze(0))
            
            # 2) Content-Based Score (user preferences x place category)
            pref_cats = ['nature', 'culture', 'restaurant', 'hotel', 'shopping', 'nightlife', 'cafe', 'local_food', 'chill', 'landmark']
            user_obj = db.query(User).filter(User.id == test_user_id).first()
            try:
                prefs = user_obj.preferences
                if isinstance(prefs, str):
                    prefs = json.loads(prefs)
                if not isinstance(prefs, list):
                    prefs = []
            except:
                prefs = []
            
            user_pref_vec = torch.tensor([1.0 if cat in prefs else 0.0 for cat in pref_cats], dtype=torch.float)
            place_cat_vecs = data['place'].x[:, :len(pref_cats)]
            
            if user_pref_vec.sum() > 0:
                content_scores = F.cosine_similarity(place_cat_vecs, user_pref_vec.unsqueeze(0))
            else:
                content_scores = torch.zeros(place_embs.size(0))
            
            # 3) Hybrid: 60% GNN + 40% Content-Based
            alpha = 0.6
            final_scores = alpha * gnn_scores + (1 - alpha) * content_scores
            
            # === Exclude only places user already reviewed (liked places still show) ===
            interacted_logs = db.query(InteractionLog).filter(
                InteractionLog.user_id == test_user_id,
                InteractionLog.action_type == 'review'
            ).all()
            interacted_place_ids = set(log.place_id for log in interacted_logs)
            reverse_place_map = {v: k for k, v in place_map.items()}
            
            # Count how many places match user preferences
            total_matching = 0
            already_visited_matching = 0
            for p_idx in range(final_scores.size(0)):
                p_id = reverse_place_map[p_idx]
                place_obj = db.query(Place).filter(Place.id == p_id).first()
                cat_type = place_obj.category.parent_type if place_obj and place_obj.category else None
                if cat_type in prefs:
                    total_matching += 1
                    if p_id in interacted_place_ids:
                        already_visited_matching += 1
            
            for p_idx in range(final_scores.size(0)):
                p_id = reverse_place_map[p_idx]
                if p_id in interacted_place_ids:
                    final_scores[p_idx] = -float('inf')
            
            top_v, top_i = torch.topk(final_scores, k=3)
            
            print(f"User: {user_name} | Preferences: {prefs}")
            print(f"  Preferred places in DB: {total_matching}")
            print(f"  Already visited/liked:  {already_visited_matching}")
            print(f"  New places to discover: {total_matching - already_visited_matching}")
            
            if total_matching > 0 and already_visited_matching == total_matching:
                print(f"\n  [!] All {prefs} places have been visited!")
                print(f"      Showing best alternatives based on your taste profile.")
            
            print(f"\nTop Recommendations for {user_name}:")
            for v, i in zip(top_v, top_i):
                p_id = reverse_place_map[i.item()]
                place_obj = db.query(Place).filter(Place.id == p_id).first()
                cat_name = place_obj.category.parent_type if place_obj.category else "?"
                print(f" - {place_obj.name.ljust(25)} | Score: {v:.4f} | Category: {cat_name}")

    finally:
        db.close()

if __name__ == "__main__":
    run_real_demo()
