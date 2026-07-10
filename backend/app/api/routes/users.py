from typing import Optional
import shutil
import os
from fastapi import UploadFile, File, Form, APIRouter, Depends, HTTPException, status
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.database import get_db
from app import models
from app import schemas
from app.core import security as auth
from app.core.email_service import send_reset_password_email
from datetime import datetime
import json
import secrets

router = APIRouter(tags=["Users Management"])


@router.post("/forgot-password")
def forgot_password(request: schemas.ForgotPasswordRequest, db: Session = Depends(get_db)):
    """
    Request password reset by sending Email to get Token
    """
    user = db.query(models.User).filter(
        models.User.email == request.email).first()
    # Always send same message for safety (Prevent User Enumeration)
    # Always send success status for safety
    msg = {"status": "success", "message": "RESET_LINK_SENT"}

    if not user:
        return msg

    # Generate random Token
    token = secrets.token_urlsafe(32)

    # Save Token to DB
    new_reset = models.PasswordReset(email=request.email, token=token)
    db.add(new_reset)
    db.commit()

    # 📧 Send actual email
    success = send_reset_password_email(request.email, token)

    if success:
        print(f"✅ Email sent successfully to {request.email}")
    else:
        print(
            f"❌ Failed to send email to {request.email} (Check SMTP settings)")

    return msg


@router.post("/reset-password")
def reset_password(data: schemas.PasswordResetConfirm, db: Session = Depends(get_db)):
    """
    Confirm new password with Token
    """
    reset_entry = db.query(models.PasswordReset).filter(
        models.PasswordReset.token == data.token).first()
    if not reset_entry:
        raise HTTPException(
            status_code=400, detail="Invalid or expired Token")

    user = db.query(models.User).filter(
        models.User.email == reset_entry.email).first()
    if not user:
        raise HTTPException(
            status_code=404, detail="User not found for this Token")

    # Update new password (Hash with bcrypt)
    user.password_hash = auth.get_password_hash(data.new_password)

    # Delete used Token
    db.delete(reset_entry)
    db.commit()

    return {"message": "Password reset successful! You can now log in."}


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(
        models.User.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=400, detail="This username is already taken.")
    existing_email = db.query(models.User).filter(
        models.User.email == user.email).first()
    if existing_email:
        raise HTTPException(
            status_code=400, detail="This email is already registered.")
    new_user = models.User(
        username=user.username, email=user.email,
        password_hash=auth.get_password_hash(user.password),
        preferences=user.preferences,
        role="user"
    )
    db.add(new_user)
    db.commit()
    return {"message": "Registration successful."}


@router.post("/login")
def login(user_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.username == user_data.username).first()
    if not user or user.deleted_at is not None:
        raise HTTPException(
            status_code=401, detail="Account is suspended or does not exist.")
    if not auth.verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=401, detail="Invalid username or password.")

    token = auth.create_access_token(
        data={"sub": user.username, "id": user.id, "role": user.role})
    return {
        "access_token": token,
        "user": {
            "id": user.id,
            "username": user.username,
            "role": user.role,
            "profile_image": user.profile_image,
            "preferences": user.preferences
        }
    }


@router.get("/users", response_model=list[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@router.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user


UPLOAD_DIR_USERS = "static/users"


@router.patch("/users/{user_id}", response_model=schemas.UserResponse)
async def update_user_profile(
    user_id: int,
    username: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    preferences: Optional[str] = Form(None),
    profile_image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()

    # 📝 DEBUG LOGGING
    try:
        with open("debug.log", "a", encoding="utf-8") as f:
            import datetime
            f.write(f"[{datetime.datetime.now()}] UPDATING USER ID: {user_id}\n")
            f.write(f"  - Received Username: {username}\n")
            f.write(f"  - Received Email: {email}\n")
            f.write(f"  - Received Preferences: {preferences}\n")
            f.write(
                f"  - DB User Found: {db_user.username if db_user else 'NOT FOUND'}\n")
    except:
        pass

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")

    if username is not None:
        existing = db.query(models.User).filter(
            models.User.username == username,
            models.User.id != user_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=400, detail="This username is already taken.")
        db_user.username = username

    if email is not None:
        existing = db.query(models.User).filter(
            models.User.email == email,
            models.User.id != user_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=400, detail="This email is already registered.")
        db_user.email = email

    if password is not None and len(password) > 0:
        db_user.password_hash = auth.get_password_hash(password)

    if preferences is not None:
        try:
            # Parse and update preferences
            from sqlalchemy.orm.attributes import flag_modified
            prefs_list = json.loads(preferences)
            if not isinstance(prefs_list, list):
                prefs_list = [str(prefs_list)]

            db_user.preferences = prefs_list
            # Force SQLAlchemy to detect change in JSON column
            flag_modified(db_user, "preferences")
        except Exception as e:
            print(f"Error parsing preferences: {e}")

    if profile_image and profile_image.filename:
        os.makedirs(UPLOAD_DIR_USERS, exist_ok=True)
        file_path = f"{UPLOAD_DIR_USERS}/{profile_image.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(profile_image.file, buffer)
        db_user.profile_image = f"/{file_path}"

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

    if user.deleted_at:
        delta = datetime.utcnow() - user.deleted_at
        if delta.days >= 3:
            raise HTTPException(
                status_code=400, detail="Cannot restore account after 3 days of suspension.")

    user.deleted_at = None
    db.commit()
    return {"message": "User restored successfully."}


@router.post("/users/{user_id}/request-post-permission")
def request_post_permission(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    user.post_permission_status = "pending"
    db.commit()
    return {"message": "Permission requested successfully."}


def safe_json_load(data, default=[]):
    if not data:
        return default
    if isinstance(data, (list, dict)):
        return data
    try:
        if isinstance(data, str):
            loaded = json.loads(data)
            if isinstance(loaded, str):
                return json.loads(loaded)
            return loaded
        return data
    except:
        return default


@router.get("/users/{user_id}/reviews")
def get_user_reviews(user_id: int, db: Session = Depends(get_db)):
    results = db.query(
        models.Interaction.id,
        models.Interaction.rating,
        models.Interaction.comment.label("comment_text"),
        models.Interaction.images,
        models.Interaction.liked_by,
        models.Interaction.visited_at,
        models.Place.id.label("place_id"),
        models.Place.name.label("place_name"),
        models.Place.image_url.label("place_image")
    ).join(
        models.Place, models.Interaction.place_id == models.Place.id
    ).filter(
        models.Interaction.user_id == user_id
    ).order_by(desc(models.Interaction.visited_at)).all()

    output = []
    for r in results:
        try:
            output.append({
                "id": r.id,
                "rating": r.rating,
                "comment_text": r.comment_text,
                "images": safe_json_load(r.images),
                "liked_by": safe_json_load(r.liked_by),
                "visited_at": r.visited_at,
                "place_id": r.place_id,
                "place_name": r.place_name,
                "place_image": r.place_image
            })
        except:
            continue
    return output


@router.get("/users/{user_id}/places", response_model=list[schemas.PlaceResponse])
def get_user_places(user_id: int, db: Session = Depends(get_db)):
    from sqlalchemy.orm import selectinload
    return db.query(models.Place).options(selectinload(models.Place.category)).filter(models.Place.owner_id == user_id).all()
