from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app import schemas
from app.core import security as auth
from datetime import datetime

router = APIRouter(tags=["Users Management"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="This username is already taken.")
    existing_email = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="This email is already registered.")
    new_user = models.User(
        username=user.username, email=user.email,
        password_hash=auth.get_password_hash(user.password), role="user"
    )
    db.add(new_user)
    db.commit()
    return {"message": "Registration successful."}

@router.post("/login")
def login(user_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == user_data.username).first()
    if not user or user.deleted_at is not None:
        raise HTTPException(status_code=401, detail="Account is suspended or does not exist.")
    if not auth.verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password.")

    token = auth.create_access_token(data={"sub": user.username, "id": user.id, "role": user.role})
    return {"access_token": token, "user": {"id": user.id, "username": user.username, "role": user.role}}

@router.get("/users", response_model=list[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@router.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user

@router.patch("/users/{user_id}", response_model=schemas.UserResponse)
def update_user_profile(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")

    if user_update.username is not None:
        existing = db.query(models.User).filter(
            models.User.username == user_update.username,
            models.User.id != user_id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="This username is already taken.")
        db_user.username = user_update.username

    if user_update.email is not None:
        existing = db.query(models.User).filter(
            models.User.email == user_update.email,
            models.User.id != user_id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="This email is already registered.")
        db_user.email = user_update.email

    if user_update.password is not None and len(user_update.password) > 0:
        db_user.password_hash = auth.get_password_hash(user_update.password)

    db.commit()
    db.refresh(db_user)
    return db_user

@router.patch("/users/{user_id}/soft-delete")
def soft_delete(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    user.deleted_at = datetime.utcnow()
    db.commit()
    return {"message": "User suspended successfully."}

@router.patch("/users/{user_id}/restore")
def restore(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    user.deleted_at = None
    db.commit()
    return {"message": "User restored successfully."}