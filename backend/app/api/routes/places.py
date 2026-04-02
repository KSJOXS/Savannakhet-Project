from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app import schemas
import shutil
import os
from typing import List, Optional

router = APIRouter(tags=["Places Management"])
UPLOAD_DIR = "static/places"

# --- General Access: แสดงผลหน้าแรก ---
@router.get("/places", response_model=List[schemas.PlaceResponse])
def get_places(
    category_id: Optional[int] = None, 
    include_drafts: bool = Query(False), 
    db: Session = Depends(get_db)
):
    query = db.query(models.Place)
    if not include_drafts:
        query = query.filter(models.Place.is_published == True)
    if category_id:
        query = query.filter(models.Place.category_id == category_id)
    return query.all()

@router.get("/places/{place_id}", response_model=schemas.PlaceResponse)
def get_place_detail(place_id: int, db: Session = Depends(get_db)):
    place = db.query(models.Place).filter(models.Place.id == place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="ไม่พบข้อมูลสถานที่")
    return place

# --- Admin Access: จัดการข้อมูลหลังบ้าน ---
@router.post("/admin/places")
async def create_place(
    name: str = Form(...), 
    description: str = Form(...), 
    category_id: int = Form(...),
    lat: float = Form(...), 
    lng: float = Form(...), 
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    new_place = models.Place(
        name=name, 
        description=description, 
        category_id=category_id,
        location_lat=lat,  # บันทึกพิกัดลง DB
        location_lng=lng,
        image_url=f"http://127.0.0.1:8000/{file_path}",
        is_published=True,
        rating_avg=0.0
    )
    db.add(new_place)
    db.commit()
    db.refresh(new_place)
    return {"message": "เพิ่มสถานที่สำเร็จ", "id": new_place.id}

@router.put("/admin/places/{place_id}")
def update_place(place_id: int, data: schemas.PlaceUpdate, db: Session = Depends(get_db)):
    db_place = db.query(models.Place).filter(models.Place.id == place_id).first()
    if not db_place:
        raise HTTPException(status_code=404, detail="ไม่พบสถานที่")
    
    db_place.name = data.name
    db_place.category_id = data.category_id
    db_place.description = data.description
    db_place.location_lat = data.location_lat
    db_place.location_lng = data.location_lng
    db_place.is_published = data.is_published
    db.commit()
    return {"message": "อัปเดตข้อมูลสำเร็จ"}

@router.delete("/admin/places/{place_id}")
def delete_place(place_id: int, db: Session = Depends(get_db)):
    place = db.query(models.Place).filter(models.Place.id == place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="ไม่พบสถานที่")
    db.delete(place)
    db.commit()
    return {"message": "ลบสถานที่เรียบร้อยแล้ว"}