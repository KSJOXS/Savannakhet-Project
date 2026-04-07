from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

# ดึงฟังก์ชันที่เราเพิ่งเขียนมาใช้
from app.services.gnn_service import build_gnn_graph

router = APIRouter()

@router.get("/test-graph-data")
def test_build_graph(db: Session = Depends(get_db)):
    try:
        # เรียกใช้งาน Service
        data, user_map, place_map = build_gnn_graph(db)
        
        # คืนค่าเป็นสรุปผลให้เราดูง่ายๆ บนเบราว์เซอร์
        return {
            "status": "success",
            "message": "สร้าง Graph สำเร็จ!",
            "graph_summary": {
                "total_users": data['user'].num_nodes,
                "total_places": data['place'].num_nodes,
                "total_interactions_edges": data['user', 'interacts_with', 'place'].num_edges if 'interacts_with' in data['user'].keys() else 0,
                "total_favorites_edges": data['user', 'likes', 'place'].num_edges if 'likes' in data['user'].keys() else 0,
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}