from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.database import get_db
from app import models, schemas
from typing import List

router = APIRouter(tags=["Admin Dashboard"])

# --- 0. Places Approval Management ---

@router.get("/admin/places/pending", response_model=List[schemas.PlaceResponse])
def get_pending_places(db: Session = Depends(get_db)):
    from sqlalchemy.orm import selectinload
    return db.query(models.Place).options(selectinload(models.Place.category)).filter(models.Place.status == "pending").all()

from fastapi import Form
@router.put("/admin/places/{place_id}/status")
def update_place_status(place_id: int, status: str = Form(...), db: Session = Depends(get_db)):
    place = db.query(models.Place).filter(models.Place.id == place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found.")
    
    place.status = status
    if status == 'approved':
        place.is_published = True
    elif status == 'rejected':
        place.is_published = False
        
    db.commit()
    return {"message": f"Place status updated to {status}"}

# --- 0.5 User Permissions Management ---

@router.get("/admin/users/pending-permissions", response_model=List[schemas.UserResponse])
def get_pending_user_permissions(db: Session = Depends(get_db)):
    return db.query(models.User).filter(models.User.post_permission_status == "pending").all()

@router.put("/admin/users/{user_id}/post-permission-status")
def update_user_post_permission(user_id: int, status: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    user.post_permission_status = status
    db.commit()
    return {"message": f"User post permission updated to {status}"}

# --- 1. Category Management ---

@router.get("/categories", response_model=List[schemas.CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(models.Category).all()

@router.post("/admin/categories")
def create_category(cat: schemas.CategoryCreate, db: Session = Depends(get_db)):
    # เพิ่มการเช็คชื่อซ้ำเบื้องต้น
    existing = db.query(models.Category).filter(models.Category.name == cat.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists.")
    
    new_cat = models.Category(name=cat.name, parent_type=cat.parent_type)
    db.add(new_cat)
    db.commit()
    db.refresh(new_cat)
    return {"message": "Category created successfully.", "id": new_cat.id}

@router.delete("/admin/categories/{cat_id}")
def delete_category(cat_id: int, db: Session = Depends(get_db)):
    cat = db.query(models.Category).filter(models.Category.id == cat_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found.")
    db.delete(cat)
    db.commit()
    return {"message": "Category deleted successfully."}

# --- 2. Review / Comment Management (สำหรับตาราง Admin) ---

@router.get("/admin/all-comments")
def get_all_reviews_admin(db: Session = Depends(get_db)):
    """ดึงรีวิวพร้อมข้อมูลสถานที่และรูปภาพ เพื่อแสดงในตาราง Admin"""
    results = db.query(
        models.Interaction.id,
        models.Interaction.rating,
        models.Interaction.comment.label("comment_text"),
        models.User.username,
        models.Place.id.label("place_id"),
        models.Place.name.label("place_name"),
        models.Place.image_url.label("place_image") # ดึงรูปมาโชว์ในตารางด้วย
    ).join(models.User).join(models.Place).all()
    
    return results

@router.delete("/admin/comments/{comment_id}") # เปลี่ยน path ให้เป็น /admin/ ตามมาตรฐาน
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(models.Interaction).filter(models.Interaction.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Review not found.")
    db.delete(comment)
    db.commit()
    return {"message": "Review deleted successfully."}

# --- 3. System Statistics (สำหรับหน้า Dashboard) ---

@router.get("/admin/stats")
def get_system_stats(db: Session = Depends(get_db)):
    try:
        # 1. นับจำนวนพื้นฐาน
        total_users = db.query(models.User).count()
        total_places = db.query(models.Place).count()
        # นับจากตาราง user_interactions ตามรูป DB ของคุณ
        total_reviews = db.query(models.Interaction).filter(models.Interaction.comment != None).count()

        # 2. ดึงสถิติหมวดหมู่ (ดึงมาโชว์ในกราฟ Progress Bar)
        cat_stats = db.query(
            models.Category.name,
            func.count(models.Place.id).label('count')
        ).join(models.Place, models.Place.category_id == models.Category.id).group_by(models.Category.name).all()

        # 3. ดึงสถานที่เรตติ้งสูงสุด 5 อันดับ
        top_places = db.query(
            models.Place.id,
            models.Place.name,
            models.Place.rating_avg.label("rating")
        ).order_by(desc(models.Place.rating_avg)).limit(5).all()

        # ส่งข้อมูลกลับไปในรูปแบบที่ Frontend เข้าใจง่าย
        return {
            "total_users": total_users,
            "total_places": total_places,
            "total_reviews": total_reviews,
            "categories": [{"name": r[0], "count": r[1]} for r in cat_stats],
            "top_places": [{"id": r.id, "name": r.name, "rating": r.rating} for r in top_places]
        }
    except Exception as e:
        print(f"ERROR Dashboard Stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Database Query Error")