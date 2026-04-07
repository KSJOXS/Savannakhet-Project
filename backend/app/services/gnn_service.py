import torch
from sqlalchemy.orm import Session
from torch_geometric.data import HeteroData
from app.models import User, Place, Interaction, Favorite

def build_gnn_graph(db: Session):
    users = db.query(User).all()
    places = db.query(Place).all()
    interactions = db.query(Interaction).all()
    favorites = db.query(Favorite).all()

    user_mapping = {user.id: i for i, user in enumerate(users)}
    place_mapping = {place.id: i for i, place in enumerate(places)}

    data = HeteroData()
    data['user'].num_nodes = len(users)
    data['place'].num_nodes = len(places)

    edge_index_interact = []
    for interact in interactions:
        if interact.user_id in user_mapping and interact.place_id in place_mapping:
            edge_index_interact.append([user_mapping[interact.user_id], place_mapping[interact.place_id]])
    
    if edge_index_interact:
        data['user', 'interacts_with', 'place'].edge_index = torch.tensor(edge_index_interact, dtype=torch.long).t().contiguous()

    edge_index_fav = []
    for fav in favorites:
        if fav.user_id in user_mapping and fav.place_id in place_mapping:
            edge_index_fav.append([user_mapping[fav.user_id], place_mapping[fav.place_id]])

    if edge_index_fav:
        data['user', 'likes', 'place'].edge_index = torch.tensor(edge_index_fav, dtype=torch.long).t().contiguous()

    return data, user_mapping, place_mapping