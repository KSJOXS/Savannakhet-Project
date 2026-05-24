import os
import sys
import json
import time

# Force system standard output to use UTF-8 encoding to prevent Windows cp1252 crash
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

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
        accuracies = []
        print("\n--- Training AI ---")
        pos_edge_index = data['user', 'interacts_with', 'place'].edge_index
        n_steps = max(1, pos_edge_index.size(1) // 5)
        
        for epoch in range(1, 21):
            print(f"Epoch {epoch}/20")
            t_start = time.time()
            optimizer.zero_grad()
            out_dict = model(data.x_dict, data.edge_index_dict)
            
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
            
            # Calculate Link Prediction Accuracy (BCE Threshold Accuracy)
            with torch.no_grad():
                pos_pred = (pos_out >= 0).float()
                neg_pred = (neg_out < 0).float()
                correct = pos_pred.sum().item() + neg_pred.sum().item()
                total = pos_out.size(0) + neg_out.size(0)
                accuracy_decimal = correct / total
                accuracies.append(accuracy_decimal)
                
            t_elapsed = (time.time() - t_start) * 1000  # ms
            step_time = max(1, int(t_elapsed / n_steps))
            total_time_s = int(t_elapsed / 1000)
            
            # Output Keras-style logs
            print(f"{n_steps}/{n_steps} ━━━━━━━━━━━━━━━━━━━━ {total_time_s}s {step_time}ms/step - accuracy: {accuracy_decimal:.4f} - loss: {loss.item():.4f}")

        # 2. Save Dual-Panel Accuracy & Loss Chart
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))
        
        # Left Panel: Model Accuracy
        ax1.plot(accuracies, label='accuracy', color='#1f77b4')
        ax1.set_title('Model Accuracy', fontsize=10)
        ax1.set_xlabel('Epochs', fontsize=9)
        ax1.set_ylabel('Accuracy', fontsize=9)
        ax1.set_ylim(0.0, 1.05)
        ax1.legend(loc='upper left')
        
        # Right Panel: Model Loss
        ax2.plot(losses, label='loss', color='#1f77b4')
        ax2.set_title('Model Loss', fontsize=10)
        ax2.set_xlabel('Epochs', fontsize=9)
        ax2.set_ylabel('Loss', fontsize=9)
        ax2.set_ylim(bottom=0.0)
        ax2.legend(loc='upper right')
        
        plt.tight_layout()
        plt.savefig(os.path.join(current_dir, "loss_chart.png"))
        print(f"Saved: {os.path.join(current_dir, 'loss_chart.png')}")

        print("\n--- Recommendation Test ---")
        model.eval()
        with torch.no_grad():
            target_user = db.query(User).filter(User.username == "dee").first()
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
            
            print("\n" + "="*60)
            print("       AI (GNN) Evaluation and Recommendation Results")
            print("="*60)
            print(f"👤 User: {user_name}")
            print(f"🎯 Preferences: {prefs}")
            print(f"------------------------------------------------------------")
            print(f"📊 System Data Summary:")
            print(f"  • Places matching your preferences: {total_matching}")
            print(f"  • Places already reviewed/visited (filtered): {already_visited_matching}")
            print(f"  • New places matching preferences: {total_matching - already_visited_matching}")
            
            if total_matching > 0 and already_visited_matching == total_matching:
                print(f"\n  [!] You have already visited all places in the category {prefs}!")
                print(f"      The system is scanning for alternative options from your Taste Profile.")
            
            print("\n" + "="*60)
            print(f"🌟 Top 3 Recommendations for You")
            print("="*60)
            
            for idx, (v, i) in enumerate(zip(top_v, top_i), 1):
                p_id = reverse_place_map[i.item()]
                place_obj = db.query(Place).filter(Place.id == p_id).first()
                cat_name = place_obj.category.parent_type if place_obj and place_obj.category else "?"
                
                # Retrieve raw scores
                overall_score = v.item()
                gnn_score = gnn_scores[i.item()].item()
                content_score = content_scores[i.item()].item()
                
                # Convert cosine similarity [-1, 1] to percentage [0%, 100%]
                overall_pct = (overall_score + 1) / 2 * 100
                gnn_pct = (gnn_score + 1) / 2 * 100
                content_pct = (content_score + 1) / 2 * 100
                
                # Bound percentage to [0%, 100%]
                overall_pct = max(0.0, min(100.0, overall_pct))
                gnn_pct = max(0.0, min(100.0, gnn_pct))
                content_pct = max(0.0, min(100.0, content_pct))
                
                # Place details
                place_name = place_obj.name if place_obj else f"Place ID {p_id}"
                avg_rating = float(place_obj.rating_avg) if place_obj and place_obj.rating_avg else 0.0
                location = place_obj.location_name if place_obj and place_obj.location_name else "Savannakhet"
                desc_text = place_obj.description.strip() if place_obj and place_obj.description else "No description available"
                if len(desc_text) > 100:
                    desc_text = desc_text[:100] + "..."
                
                # Print detailed analysis
                print(f"\n {idx}. 📍 {place_name}")
                print(f"    ⭐ Average Rating: {avg_rating:.2f}/5.0 | 📌 Location: {location} | 📂 Category: {cat_name}")
                print(f"    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                print(f"    💖 Overall Match: {overall_pct:.2f}%")
                print(f"      ├─ 👥 GNN Social Match: {gnn_pct:.2f}%  (Weight 60%)")
                print(f"      └─ 🎯 Preference Match: {content_pct:.2f}%  (Weight 40%)")
                
                # Reasoning explanation
                reasons = []
                if cat_name in prefs:
                    reasons.append(f"it matches the category you selected ('{cat_name}')")
                if gnn_pct > 70:
                    reasons.append(f"you are highly likely to like it based on travel behavior of similar users")
                elif gnn_pct > 50:
                    reasons.append(f"it aligns with general system taste profiles")
                
                if reasons:
                    reason_str = " and ".join(reasons)
                    print(f"    ℹ️  Reasoning: The system recommends this because {reason_str}")
                else:
                    print(f"    ℹ️  Reasoning: Recommended based on your AI-evaluated Taste Profile")
                
                print(f"    📝 Description: {desc_text}")
                print(f"    ------------------------------------------------------------")

    finally:
        db.close()

if __name__ == "__main__":
    run_real_demo()
