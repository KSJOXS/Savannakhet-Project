from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from app import schemas
from typing import List

# ถอด prefix="/admin" ออกจากระดับ Router เพื่อให้จัดการรายตัวได้แม่นยำขึ้น
router = APIRouter(tags=["Admin Dashboard"])

# --- Category Management ---

@router.get("/categories", response_model=List[schemas.CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    """ดึงหมวดหมู่ทั้งหมด (Frontend เรียกใช้ที่ /categories)"""
    return db.query(models.Category).all()

@router.post("/admin/categories")
def create_category(cat: schemas.CategoryCreate, db: Session = Depends(get_db)):
    """เพิ่มหมวดหมู่ใหม่ (Admin เรียกใช้ที่ /admin/categories)"""
    new_cat = models.Category(name=cat.name)
    db.add(new_cat)
    db.commit()
    db.refresh(new_cat)
    return {"message": "เพิ่มหมวดหมู่สำเร็จ", "id": new_cat.id}

# --- Review/Comment Management ---

@router.get("/admin/all-comments")
def get_all_reviews_admin(db: Session = Depends(get_db)):
    """ดึงรีวิวทั้งหมดมาแสดงในตาราง Admin (เรียกที่ /admin/all-comments)"""
    return db.query(
        models.Interaction.id, 
        models.Interaction.rating, 
        models.Interaction.comment.label("comment_text"),
        models.User.username, 
        models.Place.name.label("place_name")
    ).join(models.User).join(models.Place).all()

# --- System Statistics ---

@router.get("/admin/stats")
def get_system_stats(db: Session = Depends(get_db)):
    """ดึงตัวเลขสถิติไปโชว์ที่หน้า Dashboard (เรียกที่ /admin/stats)"""
    user_count = db.query(models.User).count()
    place_count = db.query(models.Place).count()
    review_count = db.query(models.Interaction).count()
    
    return {
        "total_users": user_count,
        "total_places": place_count,
        "total_reviews": review_count
    }

# --- ลบหมวดหมู่ (เพิ่มเติมเพื่อความครบถ้วน) ---
@router.delete("/admin/categories/{cat_id}")
def delete_category(cat_id: int, db: Session = Depends(get_db)):
    cat = db.query(models.Category).filter(models.Category.id == cat_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="ไม่พบหมวดหมู่")
    db.delete(cat)
    db.commit()
    return {"message": "ลบหมวดหมู่สำเร็จ"}