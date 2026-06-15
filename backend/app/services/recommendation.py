import os
import json
import torch
import torch.nn.functional as F
from torch_geometric.nn import SAGEConv, to_hetero
from torch_geometric.utils import negative_sampling
from sqlalchemy.sql import func
from app.services.gnn_service import build_gnn_graph
from app.models import InteractionLog, Place, Category, User
from sqlalchemy.orm import Session

MODEL_PATH = "gnn_model.pt"

# --- AI Structure ---


class BaseGNN(torch.nn.Module):
    def __init__(self, hidden_channels):
        super().__init__()
        # SAGEConv is better for heterogeneous and inductive learning
        self.conv1 = SAGEConv((-1, -1), hidden_channels)
        self.conv2 = SAGEConv((-1, -1), hidden_channels)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index).relu()
        x = self.conv2(x, edge_index)
        return x


class SavannakhetRecommender(torch.nn.Module):
    def __init__(self, hidden_channels, data_metadata):
        super().__init__()
        self.gnn = to_hetero(BaseGNN(hidden_channels), metadata=data_metadata)

    def forward(self, x_dict, edge_index_dict):
        return self.gnn(x_dict, edge_index_dict)

    def recommend_places(self, user_id, updated_x_dict, top_k=5, interacted_indices=None):
        user_features = updated_x_dict['user'][user_id]
        all_place_features = updated_x_dict['place']

        # Use Cosine Similarity for better score normalization
        scores = F.cosine_similarity(
            all_place_features, user_features.unsqueeze(0))

        # Exclude already-interacted places by setting score to -infinity
        if interacted_indices is not None:
            for idx in interacted_indices:
                scores[idx] = -float('inf')

        actual_k = min(top_k, all_place_features.size(0))
        top_scores, top_place_indices = torch.topk(scores, k=actual_k)

        return top_place_indices.tolist(), top_scores.tolist()

# --- Model Persistence ---


def save_model(model: torch.nn.Module):
    torch.save(model.state_dict(), MODEL_PATH)


def load_model(model: torch.nn.Module):
    if os.path.exists(MODEL_PATH):
        try:
            model.load_state_dict(torch.load(MODEL_PATH))
            model.eval()
            return True
        except:
            return False
    return False

# --- Helper functions ---


def get_user_favorite_category(db: Session, user_id: int):
    result = db.query(Category.parent_type, func.count(InteractionLog.id).label('total'))\
        .join(Place, InteractionLog.place_id == Place.id)\
        .join(Category, Place.category_id == Category.id)\
        .filter(InteractionLog.user_id == user_id)\
        .group_by(Category.parent_type)\
        .order_by(func.count(InteractionLog.id).desc())\
        .first()
    return result.parent_type if result else "nature"


def get_explainability(db: Session, user_id: int, recommended_place_id: int):
    liked = db.query(Place.name)\
        .join(InteractionLog, InteractionLog.place_id == Place.id)\
        .filter(InteractionLog.user_id == user_id, InteractionLog.interaction_weight >= 3.0)\
        .order_by(InteractionLog.interaction_weight.desc())\
        .first()

    if liked:
        return f"เพราะคุณเคยชอบ {liked[0]}"
    return "ยอดนิยมในสะหวันนะเขต"

# --- Main logic ---


def train_gnn_link_prediction(db: Session, epochs=100):
    """
    Train the GNN model using Link Prediction with Negative Sampling.
    """
    data, _, _ = build_gnn_graph(db)

    if not data['user', 'interacts_with', 'place'].edge_index.numel():
        return {"status": "error", "message": "No interaction data to train."}

    model = SavannakhetRecommender(
        hidden_channels=64, data_metadata=data.metadata())
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

    model.train()
    for epoch in range(epochs):
        optimizer.zero_grad()

        # Forward pass to get embeddings
        out_dict = model(data.x_dict, data.edge_index_dict)

        # Positive edges
        pos_edge_index = data['user', 'interacts_with', 'place'].edge_index
        pos_src, pos_dst = pos_edge_index[0], pos_edge_index[1]
        pos_out = (out_dict['user'][pos_src] *
                   out_dict['place'][pos_dst]).sum(dim=-1)

        # Negative sampling
        neg_edge_index = negative_sampling(
            edge_index=pos_edge_index,
            num_nodes=(data['user'].num_nodes, data['place'].num_nodes),
            num_neg_samples=pos_edge_index.size(1)
        )
        neg_src, neg_dst = neg_edge_index[0], neg_edge_index[1]
        neg_out = (out_dict['user'][neg_src] *
                   out_dict['place'][neg_dst]).sum(dim=-1)

        # Loss: Binary Cross Entropy
        loss = F.binary_cross_entropy_with_logits(
            torch.cat([pos_out, neg_out]),
            torch.cat([torch.ones(pos_out.size(0)),
                      torch.zeros(neg_out.size(0))])
        )

        loss.backward()
        optimizer.step()

    save_model(model)
    return {"status": "success", "loss": float(loss)}


def get_recommendations_for_user(db: Session, user_id_from_db: int, top_k=5):
    data, user_map, place_map = build_gnn_graph(db)

    if user_id_from_db not in user_map:
        return {"status": "error", "message": "ไม่พบผู้ใช้งานนี้ หรือยังไม่มีข้อมูลเพียงพอ (Cold Start)"}

    mapped_user_id = user_map[user_id_from_db]

    model = SavannakhetRecommender(
        hidden_channels=64, data_metadata=data.metadata())

    # Load trained model, if not exists, it will use random (untrained)
    is_trained = load_model(model)

    # Find places the user already reviewed to exclude (liked places still show)
    interacted_logs = db.query(InteractionLog).filter(
        InteractionLog.user_id == user_id_from_db,
        InteractionLog.action_type == 'review'
    ).all()
    interacted_place_ids = set(log.place_id for log in interacted_logs)
    interacted_indices = [place_map[pid]
                          for pid in interacted_place_ids if pid in place_map]

    model.eval()
    with torch.no_grad():
        updated_features = model(data.x_dict, data.edge_index_dict)

        # --- Hybrid Score: GNN Collaborative + Content-Based ---
        user_emb = updated_features['user'][mapped_user_id]
        place_embs = updated_features['place']

        # 1) GNN Collaborative Score (cosine similarity)
        gnn_scores = F.cosine_similarity(place_embs, user_emb.unsqueeze(0))

        # 2) Content-Based Score (user preferences × place category)
        pref_cats = ['nature', 'culture', 'restaurant', 'hotel', 'shopping',
                     'nightlife', 'cafe', 'local_food', 'chill', 'landmark']
        user_obj = db.query(User).filter(User.id == user_id_from_db).first()
        try:
            prefs = user_obj.preferences
            if isinstance(prefs, str):
                prefs = json.loads(prefs)
            if not isinstance(prefs, list):
                prefs = []
        except:
            prefs = []

        user_pref_vec = torch.tensor(
            [1.0 if cat in prefs else 0.0 for cat in pref_cats], dtype=torch.float)

        # Place category vectors (first 10 dims of place features = category one-hot)
        place_cat_vecs = data['place'].x[:, :len(pref_cats)]

        if user_pref_vec.sum() > 0:
            content_scores = F.cosine_similarity(
                place_cat_vecs, user_pref_vec.unsqueeze(0))
        else:
            content_scores = torch.zeros(place_embs.size(0))

        # 3) Hybrid: 60% GNN + 40% Content-Based (preferences matter!)
        alpha = 0.6
        final_scores = alpha * gnn_scores + (1 - alpha) * content_scores

        # Exclude already-interacted places
        for idx in interacted_indices:
            final_scores[idx] = -float('inf')

        actual_k = min(top_k, place_embs.size(0))
        top_scores, top_indices = torch.topk(final_scores, k=actual_k)

        recommended_indices = top_indices.tolist()
        scores = top_scores.tolist()

    reverse_place_map = {v: k for k, v in place_map.items()}
    recommended_place_ids = [reverse_place_map[idx]
                             for idx in recommended_indices]

    dynamic_cat = get_user_favorite_category(db, user_id_from_db)

    recommended_details = []
    for idx, place_id in enumerate(recommended_place_ids):
        place_obj = db.query(Place).filter(Place.id == place_id).first()
        if place_obj:
            reason = get_explainability(db, user_id_from_db, place_id)
            recommended_details.append({
                "place": {
                    "id": place_obj.id,
                    "name": place_obj.name,
                    "description": place_obj.description,
                    "image_url": place_obj.image_url,
                    "rating_avg": float(place_obj.rating_avg) if place_obj.rating_avg else 0.0,
                    "category_id": place_obj.category_id,
                    "location_lat": float(place_obj.location_lat) if place_obj.location_lat else None,
                    "location_lng": float(place_obj.location_lng) if place_obj.location_lng else None,
                    "is_published": place_obj.is_published,
                },
                "reason": reason,
                "score": round(scores[idx], 4)
            })

    return {
        "status": "success",
        "user_id": user_id_from_db,
        "is_trained": is_trained,
        "dynamic_hero_category": dynamic_cat,
        "recommended_places": recommended_details
    }


def get_similar_places(db: Session, target_place_id: int, top_k=3):
    data, user_map, place_map = build_gnn_graph(db)

    if target_place_id not in place_map:
        return {"status": "error", "message": "ยังไม่มีข้อมูล Interaction ของสถานที่นี้มากพอ"}

    mapped_target_id = place_map[target_place_id]

    model = SavannakhetRecommender(
        hidden_channels=64, data_metadata=data.metadata())
    load_model(model)

    model.eval()
    with torch.no_grad():
        updated_features = model(data.x_dict, data.edge_index_dict)
        all_place_features = updated_features['place']

        target_feature = all_place_features[mapped_target_id].unsqueeze(0)
        similarities = F.cosine_similarity(target_feature, all_place_features)

        actual_k = min(top_k + 1, all_place_features.size(0))
        top_scores, top_indices = torch.topk(similarities, k=actual_k)

    reverse_place_map = {v: k for k, v in place_map.items()}
    recommended_place_ids = []

    for i in range(actual_k):
        idx = top_indices[i].item()
        if idx == mapped_target_id:
            continue
        recommended_place_ids.append(
            (reverse_place_map[idx], top_scores[i].item()))
        if len(recommended_place_ids) == top_k:
            break

    recommended_details = []
    for place_id, score in recommended_place_ids:
        place_obj = db.query(Place).filter(Place.id == place_id).first()
        if place_obj:
            recommended_details.append({
                "place": place_obj,
                "reason": "สถานที่นี้มีสไตล์และผู้เยี่ยมชมคล้ายคลึงกัน",
                "score": round(score, 4)
            })

    return {
        "status": "success",
        "target_place_id": target_place_id,
        "similar_places": recommended_details
    }
