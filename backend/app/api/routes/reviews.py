from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from app.database import get_db
from app import models, schemas
from datetime import datetime
from typing import List, Optional
from fastapi import UploadFile, File, Form
import os
import shutil
import json

router = APIRouter(tags=["Reviews & Recommendations"])

# POST /reviews — submit a review with multiple images
UPLOAD_DIR_REVIEWS = "static/reviews"


@router.post("/reviews")
async def add_review(
    user_id: int = Form(...),
    place_id: Optional[int] = Form(None),
    rating: Optional[int] = Form(None),
    comment_text: Optional[str] = Form(None),
    images: List[UploadFile] = File([]),
    db: Session = Depends(get_db)
):
    # Save images
    image_urls = []
    if images:
        os.makedirs(UPLOAD_DIR_REVIEWS, exist_ok=True)
        for img in images:
            if not img.filename:
                continue
            file_path = f"{UPLOAD_DIR_REVIEWS}/{datetime.now().timestamp()}_{img.filename}"
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(img.file, buffer)
            image_urls.append(f"/{file_path}")

    new_review = models.Interaction(
        user_id=user_id,
        place_id=place_id,
        rating=rating,
        comment=comment_text,
        images=json.dumps(image_urls),
        liked_by=[]
    )
    db.add(new_review)
    db.commit()

    # Recalculate avg rating if place_id is provided
    if place_id is not None:
        avg_rating = db.query(func.avg(models.Interaction.rating)).filter(
            models.Interaction.place_id == place_id,
            models.Interaction.rating.isnot(None)
        ).scalar()
        place = db.query(models.Place).filter(
            models.Place.id == place_id).first()
        if place:
            place.rating_avg = round(float(avg_rating or 0), 1)
            db.commit()

    return {"message": "Review submitted successfully", "review_id": new_review.id}


def safe_json_load(data, default=[]):
    if not data:
        return default
    if isinstance(data, (list, dict)):
        return data
    try:
        if isinstance(data, str):
            # บางครั้งข้อมูลใน DB อาจถูกครอบด้วย double quotes ซ้ำ (เช่น ""[]"")
            loaded = json.loads(data)
            if isinstance(loaded, str):  # ถ้าโหลดแล้วยังเป็น string ให้โหลดอีกรอบ
                return json.loads(loaded)
            return loaded
        return data
    except:
        return default

# GET /places/{place_id}/comments — fetch reviews for a place


@router.get("/places/{place_id}/comments")
def get_place_comments(place_id: int, db: Session = Depends(get_db)):
    results = db.query(
        models.Interaction,
        models.User.username,
        models.User.profile_image,
    ).join(
        models.User, models.Interaction.user_id == models.User.id
    ).filter(
        models.Interaction.place_id == place_id
    ).order_by(desc(models.Interaction.visited_at)).all()

    output = []
    for r in results:
        try:
            output.append({
                "id": r.Interaction.id,
                "rating": r.Interaction.rating,
                "comment_text": r.Interaction.comment,
                "username": r.username,
                "profile_image": r.profile_image,
                "visited_at": r.Interaction.visited_at,
                "images": safe_json_load(r.Interaction.images),
                "liked_by": safe_json_load(r.Interaction.liked_by),
            })
        except Exception as e:
            print(f"Error processing review {r.Interaction.id}: {e}")
            continue
    return output

# GET /community/feed — fetch all reviews for community feed


@router.get("/community/feed")
def get_community_feed(db: Session = Depends(get_db)):
    results = db.query(
        models.Interaction,
        models.User.username,
        models.User.profile_image,
        models.Place.name.label("place_name")
    ).join(
        models.User, models.Interaction.user_id == models.User.id
    ).outerjoin(
        models.Place, models.Interaction.place_id == models.Place.id
    ).order_by(desc(models.Interaction.visited_at)).limit(50).all()

    output = []
    for r in results:
        try:
            db_comments = db.query(models.PostComment).filter(
                models.PostComment.post_id == r.Interaction.id).order_by(models.PostComment.created_at.asc()).all()
            comments_list = []
            for c in db_comments:
                comments_list.append({
                    "id": c.id,
                    "user_id": c.user_id,
                    "username": c.user.username,
                    "profile_image": c.user.profile_image,
                    "comment_text": c.comment_text,
                    "created_at": c.created_at
                })

            output.append({
                "id": r.Interaction.id,
                "user_id": r.Interaction.user_id,
                "place_id": r.Interaction.place_id,
                "place_name": getattr(r, "place_name", "Unknown Place") or "Unknown Place",
                "rating": r.Interaction.rating,
                "comment": r.Interaction.comment,
                "images": safe_json_load(r.Interaction.images),
                "liked_by": safe_json_load(r.Interaction.liked_by),
                "visited_at": r.Interaction.visited_at,
                "username": r.username,
                "profile_image": r.profile_image,
                "post_comments": comments_list,
            })
        except Exception as e:
            print(f"Error processing feed item: {e}")
            continue
    return output

# POST /reviews/{review_id}/comments — add comment to post


@router.post("/reviews/{review_id}/comments")
def add_post_comment(
    review_id: int,
    user_id: int = Form(...),
    comment_text: str = Form(...),
    db: Session = Depends(get_db)
):
    post = db.query(models.Interaction).filter(
        models.Interaction.id == review_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    new_comment = models.PostComment(
        post_id=review_id,
        user_id=user_id,
        comment_text=comment_text
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return {"message": "Comment added successfully", "comment_id": new_comment.id}

# DELETE /reviews/comments/{comment_id} — delete a comment


@router.delete("/reviews/comments/{comment_id}")
def delete_post_comment(comment_id: int, user_id: int, db: Session = Depends(get_db)):
    comment = db.query(models.PostComment).filter(
        models.PostComment.id == comment_id, models.PostComment.user_id == user_id).first()
    if not comment:
        raise HTTPException(
            status_code=404, detail="Comment not found or unauthorized")
    db.delete(comment)
    db.commit()
    return {"message": "Comment deleted successfully"}

# POST /reviews/{review_id}/like — toggle like


@router.post("/reviews/{review_id}/like")
def toggle_like(review_id: int, user_id: int, db: Session = Depends(get_db)):
    review = db.query(models.Interaction).filter(
        models.Interaction.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    liked_by = review.liked_by if review.liked_by else []
    if isinstance(liked_by, str):
        liked_by = json.loads(liked_by)
    if user_id in liked_by:
        liked_by.remove(user_id)
        status = "unliked"
    else:
        liked_by.append(user_id)
        status = "liked"

    review.liked_by = liked_by
    db.commit()
    return {"status": status, "likes_count": len(liked_by)}

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
    review = db.query(models.Interaction).filter(
        models.Interaction.id == comment_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    db.delete(review)
    db.commit()
    return {"message": "Review deleted successfully"}

# PUT /reviews/{review_id} — สำหรับ User แก้ไขคอมเมนต์ตัวเอง


@router.put("/reviews/{review_id}")
async def update_user_review(
    review_id: int,
    user_id: int = Form(...),
    rating: Optional[int] = Form(None),
    comment_text: Optional[str] = Form(None),
    existing_images: str = Form("[]"),  # JSON list of URLs to keep
    new_images: List[UploadFile] = File([]),
    db: Session = Depends(get_db)
):
    review = db.query(models.Interaction).filter(
        models.Interaction.id == review_id, models.Interaction.user_id == user_id).first()
    if not review:
        raise HTTPException(
            status_code=404, detail="Review not found or unauthorized")

    # 1. Start with existing images to keep
    try:
        keep_images = json.loads(existing_images)
    except:
        keep_images = []

    # 2. Save new images
    if new_images:
        os.makedirs(UPLOAD_DIR_REVIEWS, exist_ok=True)
        for img in new_images:
            if not img.filename:
                continue
            file_path = f"{UPLOAD_DIR_REVIEWS}/{datetime.now().timestamp()}_{img.filename}"
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(img.file, buffer)
            keep_images.append(f"/{file_path}")

    review.rating = rating
    review.comment = comment_text
    review.images = json.dumps(keep_images)
    db.commit()

    # Recalculate avg rating
    if review.place_id is not None:
        avg_rating = db.query(func.avg(models.Interaction.rating)).filter(
            models.Interaction.place_id == review.place_id,
            models.Interaction.rating.isnot(None)
        ).scalar()
        place = db.query(models.Place).filter(
            models.Place.id == review.place_id).first()
        if place:
            place.rating_avg = round(float(avg_rating or 0), 1)
            db.commit()

    return {"message": "Review updated successfully"}

# DELETE /reviews/{review_id} — สำหรับ User ลบคอมเมนต์ตัวเอง


@router.delete("/reviews/{review_id}")
def delete_user_review(review_id: int, user_id: int, db: Session = Depends(get_db)):
    review = db.query(models.Interaction).filter(
        models.Interaction.id == review_id, models.Interaction.user_id == user_id).first()
    if not review:
        raise HTTPException(
            status_code=404, detail="Review not found or unauthorized")

    place_id = review.place_id
    db.delete(review)
    db.commit()

    # Recalculate avg rating
    if place_id is not None:
        avg_rating = db.query(func.avg(models.Interaction.rating)).filter(
            models.Interaction.place_id == place_id,
            models.Interaction.rating.isnot(None)
        ).scalar()
        place = db.query(models.Place).filter(
            models.Place.id == place_id).first()
        if place:
            place.rating_avg = round(float(avg_rating or 0), 1)
            db.commit()

    return {"message": "Review deleted successfully"}
