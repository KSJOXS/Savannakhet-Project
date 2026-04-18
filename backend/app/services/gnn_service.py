import torch
from sqlalchemy.orm import Session
from torch_geometric.data import HeteroData
from app.models import User, Place, InteractionLog

def build_gnn_graph(db: Session):
    users = db.query(User).all()
    places = db.query(Place).all()
    logs = db.query(InteractionLog).all()

    user_mapping = {user.id: i for i, user in enumerate(users)}
    place_mapping = {place.id: i for i, place in enumerate(places)}

    data = HeteroData()
    data['user'].num_nodes = len(users)
    data['place'].num_nodes = len(places)

    edges = []
    edge_weights = []

    # Map interactions
    for log in logs:
        if log.user_id in user_mapping and log.place_id in place_mapping:
            u_idx = user_mapping[log.user_id]
            p_idx = place_mapping[log.place_id]
            w = float(log.interaction_weight)
            edges.append([u_idx, p_idx])
            edge_weights.append(w)

    if edges:
        data['user', 'interacts_with', 'place'].edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous()
        data['user', 'interacts_with', 'place'].edge_weight = torch.tensor(edge_weights, dtype=torch.float)
    else:
        # fallback empty
        data['user', 'interacts_with', 'place'].edge_index = torch.empty((2, 0), dtype=torch.long)
        data['user', 'interacts_with', 'place'].edge_weight = torch.empty((0,), dtype=torch.float)

    # For undirected reasoning, we might want reverse edges
    if edges:
        edges_rev = [[e[1], e[0]] for e in edges]
        data['place', 'interacted_by', 'user'].edge_index = torch.tensor(edges_rev, dtype=torch.long).t().contiguous()
        data['place', 'interacted_by', 'user'].edge_weight = torch.tensor(edge_weights, dtype=torch.float)

    return data, user_mapping, place_mapping