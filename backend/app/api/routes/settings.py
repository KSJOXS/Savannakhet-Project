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
# แนะนำให้เซฟเป็น Path สั้นลง DB จะปลอดภัยกว่าเวลาเปลี่ยน Domain
# STATIC_BASE_URL = "http://127.0.0.1:8000/static/hero_images"


@router.get("/", response_model=List[schemas.SiteSettingResponse])
def get_all_settings(db: Session = Depends(get_db)):
    """ดึงข้อมูลการตั้งค่าทั้งหมด"""
    return db.query(models.SiteSetting).all()


@router.get("/{key_name}", response_model=schemas.SiteSettingResponse)
def get_setting(key_name: str, db: Session = Depends(get_db)):
    """ดึงข้อมูลการตั้งค่าตาม key_name"""
    setting = db.query(models.SiteSetting).filter(
        models.SiteSetting.key_name == key_name).first()
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    return setting


@router.put("/{key_name}", response_model=schemas.SiteSettingResponse)
def upsert_setting(key_name: str, setting_data: schemas.SiteSettingUpdate, db: Session = Depends(get_db)):
    """เพิ่มหรืออัปเดตการตั้งค่า"""
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

# 🚨 แก้ไข: รับค่า key_name แบบ Form Data จาก Vue


@router.post("/hero-images/upload")
async def upload_hero_image(
    file: UploadFile = File(...),
    key_name: str = Form("hero_images_public"),  # <- ค่าเริ่มต้นถ้าไม่ส่งมา
    db: Session = Depends(get_db)
):
    """
    อัปโหลดรูปภาพ Hero ใหม่และบันทึก URL ลงในฐานข้อมูลแยกตามแท็บ (สูงสุด 10 รูป)
    """
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    # สร้างโฟลเดอร์ถ้าย้อนยังไม่มี
    os.makedirs(HERO_IMAGES_DIR, exist_ok=True)

    # Load current list of hero images ตาม key_name ที่ส่งมา
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

    # เซฟเป็น Relative Path ป้องกันบั๊กเรื่องโดเมน (Vue จะเอาไปเติม http://localhost:8000 ให้เอง)
    image_url = f"/static/hero_images/{filename}"
    current_images.append(image_url)

    # Update the setting
    if setting:
        setting.value = json.dumps(current_images)
    else:
        setting = models.SiteSetting(
            key_name=key_name,  # ใช้ key_name ที่รับมา
            value=json.dumps(current_images),
            description=f"Hero images for {key_name}"
        )
        db.add(setting)

    db.commit()
    return {"url": image_url, "all_images": current_images}


# 🚨 แก้ไข: รับค่า key_name แบบ Query Parameter ตอนลบรูปด้วย
@router.delete("/hero-images/remove")
def remove_hero_image(
    image_url: str,
    key_name: str = "hero_images_public",
    db: Session = Depends(get_db)
):
    # 1. ค้นหา Setting ตามคีย์ที่ส่งมา
    setting = db.query(models.SiteSetting).filter(
        models.SiteSetting.key_name == key_name).first()

    # 2. 🚨 Fallback: ถ้าหาไม่เจอ ให้ลองหาจากคีย์เก่า (hero_images) เผื่อเป็นรูปสมัยก่อน
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

    # 3. 🚨 พยายามเทียบ URL (เช็คแค่ส่วนท้ายของชื่อไฟล์ก็พอ ป้องกันปัญหาเรื่องโดเมน)
    target_image = next(
        (img for img in current_images if image_url in img), None)

    if not target_image:
        raise HTTPException(status_code=404, detail="Image URL not in list")

    # ลบออกจากลิสต์ใน DB
    current_images.remove(target_image)
    setting.value = json.dumps(current_images)
    db.commit()

    # ลบไฟล์ออกจากโฟลเดอร์จริงๆ
    try:
        filename = target_image.split("/")[-1]
        filepath = os.path.join(HERO_IMAGES_DIR, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
    except Exception as e:
        print(f"Warning: Could not delete file: {e}")

    return {"deleted": target_image, "all_images": current_images}
