import torch
import json
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
    
    # 1. User Features (Multi-hot encoding based on preferences)
    # Categories: nature, culture, restaurant, hotel, shopping, nightlife
    pref_cats = ['nature', 'culture', 'restaurant', 'hotel', 'shopping', 'nightlife']
    user_features = []
    
    for user in users:
        # Load preferences (handle JSON string or list)
        try:
            prefs = user.preferences
            if isinstance(prefs, str):
                prefs = json.loads(prefs)
            if not isinstance(prefs, list):
                prefs = []
        except:
            prefs = []
            
        # Create multi-hot vector
        feat = [1.0 if cat in prefs else 0.0 for cat in pref_cats]
        # If no preferences, set all to 0.1 as a small baseline
        if sum(feat) == 0:
            feat = [0.1] * len(pref_cats)
        user_features.append(feat)
        
    data['user'].x = torch.tensor(user_features, dtype=torch.float)

    # 2. Place Features (Category ID normalized + Rating)
    place_features = []
    # Get max category ID for normalization
    max_cat_id = db.query(func.max(Category.id)).scalar() or 1
    
    for place in places:
        cat_feat = float(place.category_id) / max_cat_id
        rat_feat = float(place.rating_avg) / 5.0
        place_features.append([cat_feat, rat_feat])
    data['place'].x = torch.tensor(place_features, dtype=torch.float)

    # 3. Edges
    edges = []
    edge_weights = []

    for log in logs:
        if log.user_id in user_mapping and log.place_id in place_mapping:
            u_idx = user_mapping[log.user_id]
            p_idx = place_mapping[log.place_id]
            w = float(log.interaction_weight)
            edges.append([u_idx, p_idx])
            edge_weights.append(w)

    if edges:
        edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous()
        data['user', 'interacts_with', 'place'].edge_index = edge_index
        data['user', 'interacts_with', 'place'].edge_weight = torch.tensor(edge_weights, dtype=torch.float)
        
        # Add reverse edges for undirected message passing
        edges_rev = [[e[1], e[0]] for e in edges]
        data['place', 'rev_interacts_with', 'user'].edge_index = torch.tensor(edges_rev, dtype=torch.long).t().contiguous()
        data['place', 'rev_interacts_with', 'user'].edge_weight = torch.tensor(edge_weights, dtype=torch.float)
    else:
        data['user', 'interacts_with', 'place'].edge_index = torch.empty((2, 0), dtype=torch.long)
        data['user', 'interacts_with', 'place'].edge_weight = torch.empty((0,), dtype=torch.float)
        data['place', 'rev_interacts_with', 'user'].edge_index = torch.empty((2, 0), dtype=torch.long)
        data['place', 'rev_interacts_with', 'user'].edge_weight = torch.empty((0,), dtype=torch.float)

    return data, user_mapping, place_mapping