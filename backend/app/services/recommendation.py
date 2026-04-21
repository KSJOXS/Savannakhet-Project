import torch
import torch.nn.functional as F
from torch_geometric.nn import GraphConv, to_hetero
from sqlalchemy.sql import func
from app.services.gnn_service import build_gnn_graph
from app.models import InteractionLog, Place, Category
from sqlalchemy.orm import Session

# --- AI Structure ---
class BaseGNN(torch.nn.Module):
    def __init__(self, hidden_channels):
        super().__init__()
        self.conv1 = GraphConv((-1, -1), hidden_channels)
        self.conv2 = GraphConv((-1, -1), hidden_channels)

    def forward(self, x, edge_index, edge_weight=None):
        # GraphConv supports edge_weight naturally
        x = self.conv1(x, edge_index, edge_weight).relu()
        x = self.conv2(x, edge_index, edge_weight)
        return x

class SavannakhetRecommender(torch.nn.Module):
    def __init__(self, hidden_channels, num_users, num_places, data_metadata):
        super().__init__()
        self.user_emb = torch.nn.Embedding(num_users, hidden_channels)
        self.place_emb = torch.nn.Embedding(num_places, hidden_channels)
        self.gnn = to_hetero(BaseGNN(hidden_channels), metadata=data_metadata)

    def forward(self, edge_index_dict, edge_weight_dict=None):
        x_dict = {
            'user': self.user_emb.weight,
            'place': self.place_emb.weight
        }
        return self.gnn(x_dict, edge_index_dict, edge_weight_dict)

    def recommend_places(self, user_id, updated_x_dict, top_k=5):
        user_features = updated_x_dict['user'][user_id]
        all_place_features = updated_x_dict['place']
        
        scores = torch.matmul(all_place_features, user_features)
        actual_k = min(top_k, all_place_features.size(0))
        top_scores, top_place_indices = torch.topk(scores, k=actual_k)
        
        return top_place_indices.tolist(), top_scores.tolist()

# --- Helper functions ---
def get_user_favorite_category(db: Session, user_id: int):
    # Find most interacted category
    result = db.query(Category.parent_type, func.count(InteractionLog.id).label('total'))\
        .join(Place, InteractionLog.place_id == Place.id)\
        .join(Category, Place.category_id == Category.id)\
        .filter(InteractionLog.user_id == user_id)\
        .group_by(Category.parent_type)\
        .order_by(func.count(InteractionLog.id).desc())\
        .first()
    return result.parent_type if result else "nature"

def get_explainability(db: Session, user_id: int, recommended_place_id: int):
    # Simple Neighbor Logic: "Because you liked X"
    # Find a place the user heavily interacted with
    liked = db.query(Place.name)\
        .join(InteractionLog, InteractionLog.place_id == Place.id)\
        .filter(InteractionLog.user_id == user_id, InteractionLog.interaction_weight >= 3.0)\
        .order_by(InteractionLog.interaction_weight.desc())\
        .first()
    
    if liked:
        return f"Because you liked {liked[0]}"
    return "Popular choice in Savannakhet"

# --- Main logic ---
def get_recommendations_for_user(db: Session, user_id_from_db: int, top_k=5):
    data, user_map, place_map = build_gnn_graph(db)
    
    if user_id_from_db not in user_map:
        return {"status": "error", "message": "ไม่พบผู้ใช้งานนี้ หรือยังไม่มีข้อมูลเพียงพอ (Cold Start)"}
        
    if not data.edge_index_dict:
         return {"status": "error", "message": "ระบบยังไม่มีข้อมูล Interaction ใดๆ เลย กรุณาจำลองข้อมูลก่อน"}

    mapped_user_id = user_map[user_id_from_db]

    model = SavannakhetRecommender(
        hidden_channels=64,
        num_users=data['user'].num_nodes,
        num_places=data['place'].num_nodes,
        data_metadata=data.metadata()
    )
    
    model.eval()
    with torch.no_grad():
        edge_weight_dict = data.edge_weight_dict if hasattr(data, 'edge_weight_dict') else None
        updated_features = model(data.edge_index_dict, edge_weight_dict)
        recommended_indices, scores = model.recommend_places(mapped_user_id, updated_features, top_k)
        
    reverse_place_map = {v: k for k, v in place_map.items()}
    recommended_place_ids = [reverse_place_map[idx] for idx in recommended_indices]
    
    dynamic_cat = get_user_favorite_category(db, user_id_from_db)

    # Build detailed response
    recommended_details = []
    
    for idx, place_id in enumerate(recommended_place_ids):
        # Fetch Place data
        place_obj = db.query(Place).filter(Place.id == place_id).first()
        if place_obj:
            reason = get_explainability(db, user_id_from_db, place_id)
            recommended_details.append({
                "place": place_obj,
                "reason": reason,
                "score": round(scores[idx], 4)
            })
    
    return {
        "status": "success",
        "user_id": user_id_from_db,
        "dynamic_hero_category": dynamic_cat,
        "recommended_places": recommended_details
    }

def train_gnn_link_prediction(db: Session):
    # วางโครงสำหรับทำ Offline Training
    # (สามารถใช้ Celery หรือ Background task เรียกใช้งานฟังก์ชันนี้)
    # เช่น การเทรนโมเดลด้วย Negative Sampling เพื่อทำ Link Prediction จริงๆ
    pass

def get_similar_places(db: Session, target_place_id: int, top_k=3):
    """
    Find similar places based on GNN node embeddings (Item-Item Collaborative Filtering)
    """
    data, user_map, place_map = build_gnn_graph(db)
    
    if target_place_id not in place_map:
        return {"status": "error", "message": "ยังไม่มีข้อมูล Interaction ของสถานที่นี้มากพอ (Cold Start)"}
        
    if not data.edge_index_dict:
         return {"status": "error", "message": "ระบบยังไม่มีข้อมูล Interaction ใดๆ เลย"}

    mapped_target_id = place_map[target_place_id]

    model = SavannakhetRecommender(
        hidden_channels=64,
        num_users=data['user'].num_nodes,
        num_places=data['place'].num_nodes,
        data_metadata=data.metadata()
    )
    
    model.eval()
    with torch.no_grad():
        edge_weight_dict = data.edge_weight_dict if hasattr(data, 'edge_weight_dict') else None
        updated_features = model(data.edge_index_dict, edge_weight_dict)
        all_place_features = updated_features['place']
        
        # Get embedding of the target place
        target_feature = all_place_features[mapped_target_id].unsqueeze(0)
        
        # Calculate Cosine Similarity with all other places
        similarities = F.cosine_similarity(target_feature, all_place_features)
        
        # top_k + 1 to exclude the place itself
        actual_k = min(top_k + 1, all_place_features.size(0))
        top_scores, top_indices = torch.topk(similarities, k=actual_k)
        
    reverse_place_map = {v: k for k, v in place_map.items()}
    recommended_place_ids = []
    
    for i in range(actual_k):
        idx = top_indices[i].item()
        if idx == mapped_target_id:
            continue
        recommended_place_ids.append((reverse_place_map[idx], top_scores[i].item()))
        if len(recommended_place_ids) == top_k:
            break
            
    # Fetch data from DB
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