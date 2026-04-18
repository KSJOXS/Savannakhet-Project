from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

# ดึงฟังก์ชันที่เราเพิ่งเขียนมาใช้
from app.services.gnn_service import build_gnn_graph
from app import models, schemas

router = APIRouter()

@router.post("/log")
def log_interaction(payload: schemas.InteractionLogCreate, db: Session = Depends(get_db)):
    """
    เก็บ Log การใช้งาน (view, like, review) และคำนวณเป็น weight
    """
    weight = 1.0
    if payload.action_type == 'like':
        weight = 5.0
    elif payload.action_type == 'review' and payload.score is not None:
        if payload.score == 1: weight = -5.0
        elif payload.score == 2: weight = -2.0
        elif payload.score == 3: weight = 1.0
        elif payload.score == 4: weight = 3.0
        elif payload.score == 5: weight = 5.0

    new_log = models.InteractionLog(
        user_id=payload.user_id,
        place_id=payload.place_id,
        action_type=payload.action_type,
        interaction_weight=weight
    )
    db.add(new_log)
    db.commit()
    return {"status": "success", "message": "Interaction logged successfully", "weight_assigned": weight}

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