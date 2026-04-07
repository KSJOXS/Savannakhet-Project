import torch
import torch.nn.functional as F
from torch_geometric.nn import SAGEConv, to_hetero
from app.services.gnn_service import build_gnn_graph

# --- โครงสร้าง AI ---
class BaseGNN(torch.nn.Module):
    def __init__(self, hidden_channels):
        super().__init__()
        self.conv1 = SAGEConv((-1, -1), hidden_channels)
        self.conv2 = SAGEConv((-1, -1), hidden_channels)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index).relu()
        x = self.conv2(x, edge_index)
        return x

class SavannakhetRecommender(torch.nn.Module):
    def __init__(self, hidden_channels, num_users, num_places, data_metadata):
        super().__init__()
        self.user_emb = torch.nn.Embedding(num_users, hidden_channels)
        self.place_emb = torch.nn.Embedding(num_places, hidden_channels)
        self.gnn = to_hetero(BaseGNN(hidden_channels), metadata=data_metadata)

    def forward(self, edge_index_dict):
        x_dict = {
            'user': self.user_emb.weight,
            'place': self.place_emb.weight
        }
        return self.gnn(x_dict, edge_index_dict)

    def recommend_places(self, user_id, updated_x_dict, top_k=5):
        user_features = updated_x_dict['user'][user_id]
        all_place_features = updated_x_dict['place']
        
        # คำนวณคะแนนความชอบ
        scores = torch.matmul(all_place_features, user_features)
        
        # ป้องกัน Error ถ้าขอ top_k มากกว่าจำนวนสถานที่ที่มี
        actual_k = min(top_k, all_place_features.size(0))
        top_scores, top_place_indices = torch.topk(scores, k=actual_k)
        
        return top_place_indices.tolist(), top_scores.tolist()

# --- ฟังก์ชันหลักสำหรับเรียกใช้งาน ---
def get_recommendations_for_user(db, user_id_from_db, top_k=5):
    data, user_map, place_map = build_gnn_graph(db)
    
    if user_id_from_db not in user_map:
        return {"status": "error", "message": "ไม่พบผู้ใช้งานนี้ หรือยังไม่มีข้อมูลเพียงพอ (Cold Start)"}
        
    # ป้องกัน Error กรณีกราฟยังไม่มีการกด Like หรือ Comment ใดๆ เลย
    if not data.edge_index_dict:
         return {"status": "error", "message": "ระบบยังไม่มีข้อมูลการกด Like ของใครเลย กรุณาเพิ่มข้อมูลจำลองก่อน"}

    mapped_user_id = user_map[user_id_from_db]

    model = SavannakhetRecommender(
        hidden_channels=64,
        num_users=data['user'].num_nodes,
        num_places=data['place'].num_nodes,
        data_metadata=data.metadata()
    )
    
    model.eval()
    with torch.no_grad():
        updated_features = model(data.edge_index_dict)
        recommended_indices, scores = model.recommend_places(mapped_user_id, updated_features, top_k)
        
    reverse_place_map = {v: k for k, v in place_map.items()}
    recommended_place_ids = [reverse_place_map[idx] for idx in recommended_indices]
    
    return {
        "status": "success",
        "user_id": user_id_from_db,
        "recommended_place_ids": recommended_place_ids,
        "scores": [round(s, 4) for s in scores] # ปัดเศษทศนิยมให้ดูง่าย
    }