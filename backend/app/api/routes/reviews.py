from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from app.database import get_db
from app import models, schemas

router = APIRouter(tags=["Reviews & Recommendations"])

# POST /reviews — submit a review
@router.post("/reviews")
def add_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    new_review = models.Interaction(
        user_id=review.user_id,
        place_id=review.place_id,
        rating=review.rating,
        comment=review.comment_text  # map from frontend field
    )
    db.add(new_review)
    db.commit()

    # Recalculate avg rating
    avg_rating = db.query(func.avg(models.Interaction.rating)).filter(
        models.Interaction.place_id == review.place_id
    ).scalar()
    place = db.query(models.Place).filter(models.Place.id == review.place_id).first()
    if place:
        place.rating_avg = round(float(avg_rating or 0), 1)
        db.commit()
    return {"message": "Review submitted successfully"}

# GET /places/{place_id}/comments — fetch reviews for a place
@router.get("/places/{place_id}/comments")
def get_place_comments(place_id: int, db: Session = Depends(get_db)):
    results = db.query(
        models.Interaction.id,
        models.Interaction.rating,
        models.Interaction.comment.label("comment_text"),
        models.Interaction.visited_at,
        models.User.username,
    ).join(models.User).filter(
        models.Interaction.place_id == place_id
    ).order_by(desc(models.Interaction.visited_at)).all()

    return [
        {
            "id": r.id,
            "rating": r.rating,
            "comment_text": r.comment_text,
            "username": r.username,
            "visited_at": r.visited_at,
        }
        for r in results
    ]

# GET /recommendations/{user_id}
@router.get("/recommendations/{user_id}")
def get_recommendations(user_id: int, db: Session = Depends(get_db)):
    user_reviewed_ids = db.query(models.Interaction.place_id).filter(
        models.Interaction.user_id == user_id
    ).all()
    reviewed_ids = [r[0] for r in user_reviewed_ids]

    return db.query(models.Place).filter(
        ~models.Place.id.in_(reviewed_ids) if reviewed_ids else True,
        models.Place.is_published == True
    ).order_by(desc(models.Place.rating_avg)).limit(5).all()


# GET /admin/all-comments — ดึงรีวิวทั้งหมดสำหรับหน้า Admin (JOIN ครบทั้งคนรีวิวและชื่อสถานที่)
@router.get("/admin/all-comments")
def get_admin_all_comments(db: Session = Depends(get_db)):
    try:
        # ใช้ JOIN เพื่อดึงข้อมูลจาก 3 ตาราง: Interaction, User, และ Place
        results = db.query(
            models.Interaction.id,
            models.Interaction.rating,
            models.Interaction.comment.label("comment_text"),
            models.Interaction.place_id,
            models.User.username,
            models.Place.name.label("place_name"),
            models.Place.image_url.label("place_image")
        ).join(
            models.User, models.Interaction.user_id == models.User.id
        ).join(
            models.Place, models.Interaction.place_id == models.Place.id
        ).all()

        return [
            {
                "id": r.id,
                "rating": r.rating,
                "comment_text": r.comment_text,
                "username": r.username,
                "place_id": r.place_id,
                "place_name": r.place_name,
                "place_image": r.place_image
            }
            for r in results
        ]
    except Exception as e:
        # ถ้าพัง จะแจ้งรายละเอียด Error ใน Terminal ของ FastAPI
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# DELETE /admin/comments/{comment_id} — สำหรับปุ่มลบในหน้า Admin
@router.delete("/admin/comments/{comment_id}")
def delete_review(comment_id: int, db: Session = Depends(get_db)):
    review = db.query(models.Interaction).filter(models.Interaction.id == comment_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    db.delete(review)
    db.commit()
    return {"message": "Review deleted successfully"}