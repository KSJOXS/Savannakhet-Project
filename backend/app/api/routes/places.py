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
        query = query.filter(models.Place.is_published == True)
    if category_id:
        query = query.filter(models.Place.category_id == category_id)
    
    places = query.all()
    for p in places:
        p.review_count = len([i for i in p.interactions if i.comment])
    return places

@router.get("/places/{place_id}", response_model=schemas.PlaceResponse)
def get_place_detail(place_id: int, db: Session = Depends(get_db)):
    from sqlalchemy.orm import selectinload
    place = db.query(models.Place).options(selectinload(models.Place.interactions)).filter(models.Place.id == place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found.")
    place.review_count = len([i for i in place.interactions if i.comment])
    return place

# --- Admin: Create place ---
@router.post("/admin/places")
async def create_place(
    name: str = Form(...),
    description: str = Form(...),
    category_id: int = Form(...),
    location_lat: Optional[float] = Form(None), # เปลี่ยนชื่อให้ตรงกับ Frontend
    location_lng: Optional[float] = Form(None), # เปลี่ยนชื่อให้ตรงกับ Frontend
    is_published: int = Form(1), # รับค่าจาก Frontend (1=Published, 0=Draft)
    images: Optional[List[UploadFile]] = File(None), # รองรับการอัปโหลดหลายรูป
    db: Session = Depends(get_db)
):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    image_urls = []

    # จัดการอัปโหลดไฟล์หลายรูป
    if images:
        for file in images:
            if file.filename: # เช็คว่ามีไฟล์ส่งมาจริงๆ
                file_path = f"{UPLOAD_DIR}/{file.filename}"
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                # เซฟแค่ Path พอครับ (Frontend เรามีฟังก์ชันแปะ http://localhost:8000 ให้แล้ว)
                image_urls.append(f"/{file_path}")

    # แปลง List เป็น JSON String เพื่อเซฟลง Database (เช่น '["/static/1.jpg", "/static/2.jpg"]')
    image_url_data = json.dumps(image_urls) if image_urls else "[]"

    new_place = models.Place(
        name=name,
        description=description,
        category_id=category_id,
        location_lat=location_lat,
        location_lng=location_lng,
        image_url=image_url_data,
        is_published=bool(is_published),
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

    # ถ้ามีการอัปโหลดรูปภาพใหม่เข้ามาตอนแก้ไข ค่อยอัปเดตช่อง image_url
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