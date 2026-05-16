import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch
import torch.nn.functional as F
from torch_geometric.nn import SAGEConv, to_hetero
from app.database import SessionLocal
from app.services.gnn_service import build_gnn_graph
from app.models import User, Place, Category

db = SessionLocal()
data, user_map, place_map = build_gnn_graph(db)

dee = db.query(User).filter(User.username == 'dee').first()
dee_idx = user_map[dee.id]

# Check dee's feature vector
print("=== DEE's FEATURE VECTOR ===")
print(f"Index: {dee_idx}")
print(f"Features: {data['user'].x[dee_idx]}")

# Check edges for dee
edge_index = data['user', 'interacts_with', 'place'].edge_index
edge_weight = data['user', 'interacts_with', 'place'].edge_weight
dee_mask = edge_index[0] == dee_idx
dee_edges = edge_index[:, dee_mask]
dee_weights = edge_weight[dee_mask]

print(f"\n=== DEE's EDGES (total: {dee_edges.size(1)}) ===")
reverse_place_map = {v: k for k, v in place_map.items()}
for i in range(dee_edges.size(1)):
    p_idx = dee_edges[1, i].item()
    p_id = reverse_place_map[p_idx]
    p = db.query(Place).filter(Place.id == p_id).first()
    c = p.category
    print(f"  -> {p.name} (idx={p_idx}) weight={dee_weights[i].item():.2f} cat={c.parent_type if c else '?'}")

# Check cafe place feature vectors
print("\n=== CAFE PLACE FEATURES ===")
cafe_places = db.query(Place).join(Category).filter(Category.parent_type == 'cafe').all()
for cp in cafe_places:
    if cp.id in place_map:
        idx = place_map[cp.id]
        print(f"  {cp.name} (idx={idx}): {data['place'].x[idx]}")

# Now train and check what happens
class BaseGNN(torch.nn.Module):
    def __init__(self, hidden_channels):
        super().__init__()
        self.conv1 = SAGEConv((-1, -1), hidden_channels)
        self.conv2 = SAGEConv((-1, -1), hidden_channels)
    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index).relu()
        x = self.conv2(x, edge_index)
        return x

torch.manual_seed(42)
model = to_hetero(BaseGNN(hidden_channels=32), metadata=data.metadata())
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

for epoch in range(100):
    optimizer.zero_grad()
    out_dict = model(data.x_dict, data.edge_index_dict)
    
    pos_edge_index = data['user', 'interacts_with', 'place'].edge_index
    pos_src, pos_dst = pos_edge_index[0], pos_edge_index[1]
    pos_out = (out_dict['user'][pos_src] * out_dict['place'][pos_dst]).sum(dim=-1)
    
    from torch_geometric.utils import negative_sampling
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

print(f"\nFinal loss: {loss.item():.6f}")

# Get recommendations
model.eval()
with torch.no_grad():
    final = model(data.x_dict, data.edge_index_dict)
    user_emb = final['user'][dee_idx]
    place_embs = final['place']
    
    scores = F.cosine_similarity(place_embs, user_emb.unsqueeze(0))
    
    print("\n=== ALL PLACE SCORES FOR DEE ===")
    sorted_indices = torch.argsort(scores, descending=True)
    for rank, idx in enumerate(sorted_indices):
        p_id = reverse_place_map[idx.item()]
        p = db.query(Place).filter(Place.id == p_id).first()
        c = p.category
        already = "* ALREADY LIKED *" if p_id in [24, 28, 30] else ""
        is_cafe = "CAFE" if (c and c.parent_type == 'cafe') else c.parent_type if c else '?'
        print(f"  #{rank+1} {p.name.ljust(30)} Score: {scores[idx]:.4f} | {is_cafe} {already}")

db.close()
