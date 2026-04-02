from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models
from app import schemas, auth
from datetime import datetime

router = APIRouter(tags=["Users Management"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user: raise HTTPException(status_code=400, detail="Username นี้ถูกใช้งานแล้ว")
    new_user = models.User(
        username=user.username, email=user.email,
        password_hash=auth.get_password_hash(user.password), role="user" 
    )
    db.add(new_user)
    db.commit()
    return {"message": "ลงทะเบียนสำเร็จ"}

@router.post("/login")
def login(user_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == user_data.username).first()
    if not user or user.deleted_at is not None:
        raise HTTPException(status_code=401, detail="บัญชีถูกระงับหรือข้อมูลไม่ถูกต้อง")
    if not auth.verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
    
    token = auth.create_access_token(data={"sub": user.username, "id": user.id, "role": user.role})
    return {"access_token": token, "user": {"id": user.id, "username": user.username, "role": user.role}}

@router.get("/users", response_model=list[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@router.patch("/users/{user_id}/soft-delete")
def soft_delete(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user: raise HTTPException(status_code=404, detail="ไม่พบผู้ใช้งาน")
    user.deleted_at = datetime.utcnow()
    db.commit()
    return {"message": "ระงับการใช้งานสำเร็จ"}

@router.patch("/users/{user_id}/restore")
def restore(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user: raise HTTPException(status_code=404, detail="ไม่พบผู้ใช้งาน")
    user.deleted_at = None
    db.commit()
    return {"message": "กู้คืนผู้ใช้งานสำเร็จ"}