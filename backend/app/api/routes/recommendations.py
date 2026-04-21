from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.recommendation import get_recommendations_for_user, get_similar_places
from app import schemas

router = APIRouter()

@router.get("/{user_id}", response_model=schemas.RecommendationResponse)
def get_user_recommendations(user_id: int, top_k: int = 5, db: Session = Depends(get_db)):
    """
    ดึงข้อมูลสถานที่แนะนำสำหรับ User ID ที่ระบุ โดยใช้ AI (GNN Model)
    - top_k: จำนวนสถานที่ที่ต้องการให้แนะนำ (ค่าเริ่มต้นคือ 5)
    """
    result = get_recommendations_for_user(db, user_id_from_db=user_id, top_k=top_k)
    
    if result.get("status") == "error":
        raise HTTPException(status_code=404, detail=result.get("message"))
        
    return result

@router.get("/place/{place_id}/similar")
def get_similar_places_api(place_id: int, top_k: int = 3, db: Session = Depends(get_db)):
    """
    ดึงข้อมูลสถานที่ใกล้เคียง/คล้ายคลึงกับสถานที่ปัจจุบัน โดยใช้ GNN Embeddings
    """
    result = get_similar_places(db, target_place_id=place_id, top_k=top_k)
    
    if result.get("status") == "error":
        # In case of cold start or error, return empty list or fallback instead of throwing error
        return {
            "status": "success",
            "target_place_id": place_id,
            "similar_places": []
        }
        
    return result