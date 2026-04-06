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