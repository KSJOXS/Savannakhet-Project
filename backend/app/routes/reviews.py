from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from database import get_db
import models
from app import schemas

router = APIRouter(tags=["Reviews & Recommendations"])

@router.post("/reviews")
def add_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    new_review = models.Interaction(
        user_id=review.user_id, place_id=review.place_id,
        rating=review.rating, comment=review.comment
    )
    db.add(new_review)
    db.commit()
    
    # อัปเดตคะแนนเฉลี่ยของสถานที่
    avg_rating = db.query(func.avg(models.Interaction.rating)).filter(models.Interaction.place_id == review.place_id).scalar()
    place = db.query(models.Place).filter(models.Place.id == review.place_id).first()
    if place:
        place.rating_avg = round(float(avg_rating or 0), 1)
        db.commit()
    return {"message": "บันทึกรีวิวสำเร็จ"}

@router.get("/recommendations/{user_id}")
def get_recommendations(user_id: int, db: Session = Depends(get_db)):
    user_reviewed_ids = db.query(models.Interaction.place_id).filter(models.Interaction.user_id == user_id).all()
    reviewed_ids = [r[0] for r in user_reviewed_ids]
    
    return db.query(models.Place).filter(
        ~models.Place.id.in_(reviewed_ids) if reviewed_ids else True,
        models.Place.is_published == True
    ).order_by(desc(models.Place.rating_avg)).limit(5).all()