from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
import json
import uuid
import os
import shutil
from app import models, schemas
from app.database import get_db

router = APIRouter()

HERO_IMAGES_DIR = "static/hero_images"
# Recommend saving as short Path in DB, safer for Domain changes
# STATIC_BASE_URL = "http://127.0.0.1:8000/static/hero_images"


@router.get("/", response_model=List[schemas.SiteSettingResponse])
def get_all_settings(db: Session = Depends(get_db)):
    """Get all settings"""
    return db.query(models.SiteSetting).all()


@router.get("/{key_name}", response_model=schemas.SiteSettingResponse)
def get_setting(key_name: str, db: Session = Depends(get_db)):
    """Get setting by key_name"""
    setting = db.query(models.SiteSetting).filter(
        models.SiteSetting.key_name == key_name).first()
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    return setting


@router.put("/{key_name}", response_model=schemas.SiteSettingResponse)
def upsert_setting(key_name: str, setting_data: schemas.SiteSettingUpdate, db: Session = Depends(get_db)):
    """Add or update setting"""
    setting = db.query(models.SiteSetting).filter(
        models.SiteSetting.key_name == key_name).first()
    if setting:
        setting.value = setting_data.value
        if setting_data.description is not None:
            setting.description = setting_data.description
    else:
        setting = models.SiteSetting(
            key_name=key_name,
            value=setting_data.value,
            description=setting_data.description
        )
        db.add(setting)

    db.commit()
    db.refresh(setting)
    return setting

# 🚨 Fix: Receive key_name as Form Data from Vue


@router.post("/hero-images/upload")
async def upload_hero_image(
    file: UploadFile = File(...),
    key_name: str = Form("hero_images_public"),  # <- Default if not sent
    db: Session = Depends(get_db)
):
    """
    Upload new Hero images and save URL in DB by tab (max 10 images)
    """
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    # Create folder if not exists
    os.makedirs(HERO_IMAGES_DIR, exist_ok=True)

    # Load current list of hero images based on key_name
    setting = db.query(models.SiteSetting).filter(
        models.SiteSetting.key_name == key_name).first()

    current_images = []
    if setting and setting.value:
        try:
            current_images = json.loads(setting.value)
        except:
            current_images = []

    if len(current_images) >= 10:
        raise HTTPException(
            status_code=400, detail="Maximum 10 hero images allowed. Please remove one first.")

    # Save file with unique name
    ext = os.path.splitext(file.filename)[1] or ".jpg"
    filename = f"{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(HERO_IMAGES_DIR, filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Save as Relative Path to prevent domain bugs (Vue will append http://localhost:8000)
    image_url = f"/static/hero_images/{filename}"
    current_images.append(image_url)

    # Update the setting
    if setting:
        setting.value = json.dumps(current_images)
    else:
        setting = models.SiteSetting(
            key_name=key_name,  # Use received key_name
            value=json.dumps(current_images),
            description=f"Hero images for {key_name}"
        )
        db.add(setting)

    db.commit()
    return {"url": image_url, "all_images": current_images}


# 🚨 Fix: Receive key_name as Query Parameter when deleting image
@router.delete("/hero-images/remove")
def remove_hero_image(
    image_url: str,
    key_name: str = "hero_images_public",
    db: Session = Depends(get_db)
):
    # 1. Find Setting by key
    setting = db.query(models.SiteSetting).filter(
        models.SiteSetting.key_name == key_name).first()

    # 2. 🚨 Fallback: If not found, try old key (hero_images)
    if not setting and key_name == "hero_images_public":
        setting = db.query(models.SiteSetting).filter(
            models.SiteSetting.key_name == "hero_images").first()

    if not setting or not setting.value:
        raise HTTPException(
            status_code=404, detail="No hero images found for this category")

    try:
        current_images = json.loads(setting.value)
    except:
        current_images = []

    # 3. 🚨 Compare URL (check only end of filename to prevent domain issues)
    target_image = next(
        (img for img in current_images if image_url in img), None)

    if not target_image:
        raise HTTPException(status_code=404, detail="Image URL not in list")

    # Remove from list in DB
    current_images.remove(target_image)
    setting.value = json.dumps(current_images)
    db.commit()

    # Delete actual file from folder
    try:
        filename = target_image.split("/")[-1]
        filepath = os.path.join(HERO_IMAGES_DIR, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
    except Exception as e:
        print(f"Warning: Could not delete file: {e}")

    return {"deleted": target_image, "all_images": current_images}
