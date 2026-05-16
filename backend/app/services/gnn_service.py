import torch
import json
from sqlalchemy import func
from sqlalchemy.orm import Session
from torch_geometric.data import HeteroData
from app.models import User, Place, InteractionLog, Category

def build_gnn_graph(db: Session):
    users = db.query(User).all()
    places = db.query(Place).all()
    logs = db.query(InteractionLog).all()

    user_mapping = {user.id: i for i, user in enumerate(users)}
    place_mapping = {place.id: i for i, place in enumerate(places)}

    data = HeteroData()
    
    # 1. User Features (Multi-hot encoding based on preferences)
    # Categories: nature, culture, restaurant, hotel, shopping, nightlife, cafe, local_food, chill, landmark
    pref_cats = ['nature', 'culture', 'restaurant', 'hotel', 'shopping', 'nightlife', 'cafe', 'local_food', 'chill', 'landmark']
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

    # 2. Place Features (One-Hot Category + Rating)
    pref_cats = ['nature', 'culture', 'restaurant', 'hotel', 'shopping', 'nightlife', 'cafe', 'local_food', 'chill', 'landmark']
    place_features = []
    
    for place in places:
        # Determine which index to set based on category parent_type
        cat_feat = [0.0] * len(pref_cats)
        if place.category and place.category.parent_type in pref_cats:
            idx = pref_cats.index(place.category.parent_type)
            cat_feat[idx] = 1.0
            
        rat_feat = float(place.rating_avg) / 5.0
        place_features.append(cat_feat + [rat_feat])
        
    data['place'].x = torch.tensor(place_features, dtype=torch.float)

    # 3. Edges - Aggregate duplicate (user, place) pairs into single edges
    # This prevents users with many 'view' logs from dominating the graph
    edge_agg = {}  # (u_idx, p_idx) -> total_weight

    for log in logs:
        if log.user_id in user_mapping and log.place_id in place_mapping:
            u_idx = user_mapping[log.user_id]
            p_idx = place_mapping[log.place_id]
            w = float(log.interaction_weight)
            key = (u_idx, p_idx)
            edge_agg[key] = edge_agg.get(key, 0.0) + w

    # Normalize weights to reduce popularity bias from heavy users
    if edge_agg:
        max_w = max(edge_agg.values())
        edges = []
        edge_weights = []
        for (u_idx, p_idx), w in edge_agg.items():
            edges.append([u_idx, p_idx])
            edge_weights.append(w / max_w)  # Normalize to [0, 1]

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