import torch
from torch_geometric.data import HeteroData
import models

def build_graph_from_db(interactions):
    data = HeteroData()

    # 1. จัดการ IDs (Mapping)
    # เนื่องจาก GNN ต้องการ index เริ่มจาก 0, 1, 2...
    user_ids = list(set([i.user_id for i in interactions]))
    place_ids = list(set([i.place_id for i in interactions]))

    user_map = {id: i for i, id in enumerate(user_ids)}
    place_map = {id: i for i, id in enumerate(place_ids)}

    # 2. สร้าง Node Features (แบบ Identity Matrix ง่ายๆ ไปก่อน)
    data['user'].x = torch.eye(len(user_ids))
    data['place'].x = torch.eye(len(place_ids))

    # 3. สร้าง Edge Index (เส้นเชื่อม)
    edge_index_user = [user_map[i.user_id] for i in interactions]
    edge_index_place = [place_map[i.place_id] for i in interactions]
    
    data['user', 'checks_out', 'place'].edge_index = torch.tensor(
        [edge_index_user, edge_index_place], dtype=torch.long
    )

    return data