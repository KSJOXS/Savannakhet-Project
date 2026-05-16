from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from typing import List, Optional
import shutil, os

router = APIRouter(tags=["Place Sections"])
UPLOAD_DIR = "static/sections"


# ──────────────────────────────────────────────
# PUBLIC: ดึง sections ทั้งหมดของสถานที่
# ──────────────────────────────────────────────
@router.get("/places/{place_id}/sections", response_model=List[schemas.PlaceSectionResponse])
def get_sections(place_id: int, db: Session = Depends(get_db)):
    return (
        db.query(models.PlaceSection)
        .filter(models.PlaceSection.place_id == place_id)
        .order_by(models.PlaceSection.order_index)
        .all()
    )


# ──────────────────────────────────────────────
# ADMIN: เพิ่ม section ใหม่
# ──────────────────────────────────────────────
@router.post("/admin/places/{place_id}/sections", response_model=schemas.PlaceSectionResponse)
async def add_section(
    place_id: int,
    description: Optional[str] = Form(None),
    order_index: int = Form(0),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    place = db.query(models.Place).filter(models.Place.id == place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found.")

    image_url = None
    if image and image.filename:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        safe_name = f"section_{place_id}_{image.filename}"
        file_path = f"{UPLOAD_DIR}/{safe_name}"
        with open(file_path, "wb") as buf:
            shutil.copyfileobj(image.file, buf)
        image_url = f"/{file_path}"

    section = models.PlaceSection(
        place_id=place_id,
        image_url=image_url,
        description=description,
        order_index=order_index,
    )
    db.add(section)
    db.commit()
    db.refresh(section)
    return section


# ──────────────────────────────────────────────
# ADMIN: แก้ไข section
# ──────────────────────────────────────────────
@router.put("/admin/places/{place_id}/sections/{section_id}", response_model=schemas.PlaceSectionResponse)
async def update_section(
    place_id: int,
    section_id: int,
    description: Optional[str] = Form(None),
    order_index: Optional[int] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    section = db.query(models.PlaceSection).filter(
        models.PlaceSection.id == section_id,
        models.PlaceSection.place_id == place_id
    ).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found.")

    if description is not None:
        section.description = description
    if order_index is not None:
        section.order_index = order_index

    if image and image.filename:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        safe_name = f"section_{place_id}_{image.filename}"
        file_path = f"{UPLOAD_DIR}/{safe_name}"
        with open(file_path, "wb") as buf:
            shutil.copyfileobj(image.file, buf)
        section.image_url = f"/{file_path}"

    db.commit()
    db.refresh(section)
    return section


# ──────────────────────────────────────────────
# ADMIN: ลบ section
# ──────────────────────────────────────────────
@router.delete("/admin/places/{place_id}/sections/{section_id}")
def delete_section(place_id: int, section_id: int, db: Session = Depends(get_db)):
    section = db.query(models.PlaceSection).filter(
        models.PlaceSection.id == section_id,
        models.PlaceSection.place_id == place_id
    ).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found.")
    db.delete(section)
    db.commit()
    return {"message": "Section deleted."}
