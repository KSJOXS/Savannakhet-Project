from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from app.database import get_db
from app import models, schemas
from typing import List

router = APIRouter(tags=["Contact"])

# --- PUBLIC: Submit contact message ---
@router.post("/api/contact", response_model=schemas.ContactMessageResponse)
def submit_contact(payload: schemas.ContactMessageCreate, db: Session = Depends(get_db)):
    msg = models.ContactMessage(
        name=payload.name,
        email=payload.email,
        subject=payload.subject,
        message=payload.message,
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg

# --- ADMIN: Get all messages (unread first, then newest) ---
@router.get("/api/admin/messages", response_model=List[schemas.ContactMessageResponse])
def get_all_messages(db: Session = Depends(get_db)):
    return db.query(models.ContactMessage).order_by(
        asc(models.ContactMessage.is_read),      # unread (False=0) first
        desc(models.ContactMessage.created_at)
    ).all()

# --- ADMIN: Get unread count ---
@router.get("/api/admin/messages/unread-count")
def get_unread_count(db: Session = Depends(get_db)):
    count = db.query(models.ContactMessage).filter(models.ContactMessage.is_read == False).count()
    return {"unread_count": count}

# --- ADMIN: Mark as read ---
@router.put("/api/admin/messages/{msg_id}/read")
def mark_as_read(msg_id: int, db: Session = Depends(get_db)):
    msg = db.query(models.ContactMessage).filter(models.ContactMessage.id == msg_id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found.")
    msg.is_read = True
    db.commit()
    return {"message": "Marked as read."}

# --- ADMIN: Reply (mock - just marks is_replied = True) ---
@router.post("/api/admin/messages/{msg_id}/reply")
def reply_to_message(msg_id: int, reply_text: str = Form(...), db: Session = Depends(get_db)):
    msg = db.query(models.ContactMessage).filter(models.ContactMessage.id == msg_id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found.")
    msg.is_replied = True
    db.commit()
    return {"message": f"Reply sent to {msg.email}. (Mock — no real email sent)"}
