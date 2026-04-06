from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app import schemas
from typing import List

router = APIRouter(tags=["Admin Dashboard"])

# --- Category Management ---

@router.get("/categories", response_model=List[schemas.CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    """Get all categories (public endpoint)."""
    return db.query(models.Category).all()

@router.post("/admin/categories")
def create_category(cat: schemas.CategoryCreate, db: Session = Depends(get_db)):
    """Create a new category (admin only)."""
    new_cat = models.Category(name=cat.name)
    db.add(new_cat)
    db.commit()
    db.refresh(new_cat)
    return {"message": "Category created successfully.", "id": new_cat.id}

# --- Review / Comment Management ---

@router.get("/admin/all-comments")
def get_all_reviews_admin(db: Session = Depends(get_db)):
    """Fetch all reviews for admin table view."""
    return db.query(
        models.Interaction.id,
        models.Interaction.rating,
        models.Interaction.comment.label("comment_text"),
        models.User.username,
        models.Place.name.label("place_name")
    ).join(models.User).join(models.Place).all()

@router.delete("/comments/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    """Delete a review by ID (admin only)."""
    comment = db.query(models.Interaction).filter(models.Interaction.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Review not found.")
    db.delete(comment)
    db.commit()
    return {"message": "Review deleted successfully."}

# --- System Statistics ---

@router.get("/admin/stats")
def get_system_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics."""
    return {
        "total_users": db.query(models.User).count(),
        "total_places": db.query(models.Place).count(),
        "total_reviews": db.query(models.Interaction).count()
    }

# --- Category Delete ---

@router.delete("/admin/categories/{cat_id}")
def delete_category(cat_id: int, db: Session = Depends(get_db)):
    cat = db.query(models.Category).filter(models.Category.id == cat_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found.")
    db.delete(cat)
    db.commit()
    return {"message": "Category deleted successfully."}