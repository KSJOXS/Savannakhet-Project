from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app import schemas
import shutil
import os
import json
from typing import List, Optional

router = APIRouter(tags=["Places Management"])
UPLOAD_DIR = "static/places"

# --- Public: Get all places ---
@router.get("/places", response_model=List[schemas.PlaceResponse])
def get_places(
    category_id: Optional[int] = None,
    include_drafts: bool = Query(False),
    db: Session = Depends(get_db)
):
    from sqlalchemy.orm import selectinload
    query = db.query(models.Place).options(selectinload(models.Place.interactions))
    if not include_drafts:
        query = query.filter(models.Place.is_published == True, models.Place.status == 'approved')
    if category_id:
        query = query.filter(models.Place.category_id == category_id)
    
    places = query.all()
    for p in places:
        p.review_count = len([i for i in p.interactions if i.comment])
    return places

@router.get("/places/trending", response_model=List[schemas.PlaceResponse])
def get_trending_places(limit: int = 10, db: Session = Depends(get_db)):
    """
    ดึงสถานที่ที่เป็นที่นิยม (Trending) โดยคำนวณจาก InteractionLog
    """
    from sqlalchemy import func
    from sqlalchemy.orm import selectinload
    
    # คำนวณหา Place ID ที่มี Interaction Weight รวมสูงสุด
    popular_ids = db.query(
        models.InteractionLog.place_id,
        func.sum(models.InteractionLog.interaction_weight).label('total_weight')
    ).group_by(models.InteractionLog.place_id)\
     .order_by(func.sum(models.InteractionLog.interaction_weight).desc())\
     .limit(limit).all()
    
    if not popular_ids:
        # Fallback to top rating if no logs
        return db.query(models.Place).filter(models.Place.is_published == True, models.Place.status == 'approved').order_by(models.Place.rating_avg.desc()).limit(limit).all()
        
    ids = [p[0] for p in popular_ids]
    
    # ดึงข้อมูล Place ตาม ID ที่ได้
    places = db.query(models.Place)\
        .options(selectinload(models.Place.interactions))\
        .filter(models.Place.id.in_(ids))\
        .all()
    
    # เรียงลำดับตามความนิยมเดิม
    places_sorted = sorted(places, key=lambda x: ids.index(x.id))
    
    for p in places_sorted:
        p.review_count = len([i for i in p.interactions if i.comment])
        
    return places_sorted

@router.get("/places/{place_id}", response_model=schemas.PlaceResponse)
def get_place_detail(place_id: int, db: Session = Depends(get_db)):
    from sqlalchemy.orm import selectinload
    place = db.query(models.Place).options(selectinload(models.Place.interactions)).filter(models.Place.id == place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found.")
    place.review_count = len([i for i in place.interactions if i.comment])
    return place

@router.get("/places/{place_id}/fans", response_model=List[schemas.UserResponse])
def get_place_fans(place_id: int, limit: int = 5, db: Session = Depends(get_db)):
    """
    ดึงข้อมูลผู้ใช้ที่เคยมี Interaction กับสถานที่นี้ (Social Proof)
    """
    from sqlalchemy import desc
    fans = db.query(models.User).join(models.InteractionLog)\
             .filter(models.InteractionLog.place_id == place_id)\
             .order_by(desc(models.InteractionLog.created_at))\
             .distinct()\
             .limit(limit).all()
    return fans

# --- User: Submit place ---
@router.post("/places/submit")
async def submit_place(
    name: str = Form(...),
    description: str = Form(...),
    category_id: int = Form(...),
    location_lat: Optional[float] = Form(None),
    location_lng: Optional[float] = Form(None),
    user_id: int = Form(...),
    opening_hours: Optional[str] = Form(None),
    images: Optional[List[UploadFile]] = File(None),
    db: Session = Depends(get_db)
):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    image_urls = []

    if images:
        for file in images:
            if file.filename:
                file_path = f"{UPLOAD_DIR}/{file.filename}"
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                image_urls.append(f"/{file_path}")

    image_url_data = json.dumps(image_urls) if image_urls else "[]"

    parsed_hours = None
    if opening_hours:
        try:
            parsed_hours = json.loads(opening_hours)
        except Exception:
            parsed_hours = None

    new_place = models.Place(
        name=name,
        description=description,
        category_id=category_id,
        location_lat=location_lat,
        location_lng=location_lng,
        image_url=image_url_data,
        is_published=False,
        status="pending",
        owner_id=user_id,
        opening_hours=parsed_hours,
        rating_avg=0.0
    )
    db.add(new_place)
    db.commit()
    db.refresh(new_place)
    return {"message": "Place submitted successfully. Waiting for admin approval.", "id": new_place.id}

# --- Admin: Create place ---
@router.post("/admin/places")
async def create_place(
    name: str = Form(...),
    description: str = Form(...),
    category_id: int = Form(...),
    location_lat: Optional[float] = Form(None),
    location_lng: Optional[float] = Form(None),
    is_published: int = Form(1),
    opening_hours: Optional[str] = Form(None),  # JSON string
    images: Optional[List[UploadFile]] = File(None),
    db: Session = Depends(get_db)
):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    image_urls = []

    if images:
        for file in images:
            if file.filename:
                file_path = f"{UPLOAD_DIR}/{file.filename}"
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                image_urls.append(f"/{file_path}")

    image_url_data = json.dumps(image_urls) if image_urls else "[]"

    parsed_hours = None
    if opening_hours:
        try:
            parsed_hours = json.loads(opening_hours)
        except Exception:
            parsed_hours = None

    new_place = models.Place(
        name=name,
        description=description,
        category_id=category_id,
        location_lat=location_lat,
        location_lng=location_lng,
        image_url=image_url_data,
        is_published=bool(is_published),
        status="approved",
        opening_hours=parsed_hours,
        rating_avg=0.0
    )
    db.add(new_place)
    db.commit()
    db.refresh(new_place)
    return {"message": "Place created successfully.", "id": new_place.id}

# --- Admin: Update place ---
@router.put("/admin/places/{place_id}")
async def update_place(
    place_id: int, 
    name: str = Form(...),
    description: str = Form(...),
    category_id: int = Form(...),
    location_lat: Optional[float] = Form(None),
    location_lng: Optional[float] = Form(None),
    is_published: int = Form(1),
    opening_hours: Optional[str] = Form(None),  # JSON string
    images: Optional[List[UploadFile]] = File(None),
    db: Session = Depends(get_db)
):
    db_place = db.query(models.Place).filter(models.Place.id == place_id).first()
    if not db_place:
        raise HTTPException(status_code=404, detail="Place not found.")

    db_place.name = name
    db_place.category_id = category_id
    db_place.description = description
    db_place.location_lat = location_lat
    db_place.location_lng = location_lng
    db_place.is_published = bool(is_published)

    if opening_hours is not None:
        try:
            db_place.opening_hours = json.loads(opening_hours)
        except Exception:
            pass

    if images and images[0].filename:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        image_urls = []
        for file in images:
            if file.filename:
                file_path = f"{UPLOAD_DIR}/{file.filename}"
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                image_urls.append(f"/{file_path}")
        
        db_place.image_url = json.dumps(image_urls)

    db.commit()
    return {"message": "Place updated successfully."}

# --- Admin: Delete place ---
@router.delete("/admin/places/{place_id}")
def delete_place(place_id: int, db: Session = Depends(get_db)):
    place = db.query(models.Place).filter(models.Place.id == place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found.")
    db.delete(place)
    db.commit()
    return {"message": "Place deleted successfully."}