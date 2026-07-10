from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from app.database import get_db
from app import models, schemas
from typing import List
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(tags=["Contact"])

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "")       # your Gmail address
SMTP_PASS = os.getenv("SMTP_PASS", "")       # your Gmail App Password
SITE_NAME = os.getenv("SITE_NAME", "Savannakhet Tourism")


def send_email_reply(to_email: str, to_name: str, subject: str, reply_text: str):
    """Send actual email to user who submitted contact form"""
    if not SMTP_USER or not SMTP_PASS:
        print("⚠️  SMTP_USER or SMTP_PASS not set in .env — skipping real email send.")
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Re: {subject} — {SITE_NAME}"
    msg["From"] = f"{SITE_NAME} <{SMTP_USER}>"
    msg["To"] = to_email

    # Plain text fallback
    plain = f"Hello {to_name},\n\n{reply_text}\n\nBest regards,\n{SITE_NAME} Team"

    # HTML body
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f0f4f8; margin: 0; padding: 0; }}
        .wrapper {{ max-width: 600px; margin: 40px auto; background: white; border-radius: 16px;
                   overflow: hidden; box-shadow: 0 4px 24px rgba(0,0,0,0.08); }}
        .header {{ background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
                   padding: 32px 40px; text-align: center; }}
        .header h1 {{ color: white; margin: 0; font-size: 22px; font-weight: 700; letter-spacing: 0.5px; }}
        .header p {{ color: rgba(255,255,255,0.8); margin: 6px 0 0; font-size: 13px; }}
        .body {{ padding: 36px 40px; }}
        .greeting {{ font-size: 16px; color: #1e293b; font-weight: 600; margin-bottom: 16px; }}
        .reply-box {{ background: #f8fafc; border-left: 4px solid #3b82f6; border-radius: 8px;
                      padding: 20px 24px; margin: 20px 0; color: #334155; font-size: 15px;
                      line-height: 1.75; white-space: pre-wrap; }}
        .original-label {{ font-size: 12px; color: #94a3b8; margin-top: 28px; margin-bottom: 8px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }}
        .footer {{ background: #f8fafc; padding: 20px 40px; text-align: center; border-top: 1px solid #e2e8f0; }}
        .footer p {{ color: #94a3b8; font-size: 12px; margin: 0; }}
        .badge {{ display: inline-block; background: #dbeafe; color: #1d4ed8; padding: 4px 12px;
                  border-radius: 20px; font-size: 12px; font-weight: 600; margin-top: 8px; }}
      </style>
    </head>
    <body>
      <div class="wrapper">
        <div class="header">
          <h1>🌏 {SITE_NAME}</h1>
          <p>Official Reply to Your Message</p>
        </div>
        <div class="body">
          <p class="greeting">Hello, {to_name} 👋</p>
          <p style="color:#475569;font-size:14px;margin-bottom:4px;">Thank you for reaching out to us. Here is our reply to your message:</p>

          <div class="reply-box">{reply_text}</div>

          <p style="color:#64748b;font-size:14px;margin-top:20px;">
            If you have any further questions, feel free to reply to this email or visit our website.
          </p>
          <div class="badge">✉️ Re: {subject}</div>
        </div>
        <div class="footer">
          <p>© {SITE_NAME} · This is an official reply to your contact form submission.</p>
        </div>
      </div>
    </body>
    </html>
    """

    msg.attach(MIMEText(plain, "plain"))
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, to_email, msg.as_string())
        print(f"✅ Email reply sent to {to_email}")
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        raise


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
    count = db.query(models.ContactMessage).filter(
        models.ContactMessage.is_read == False).count()
    return {"unread_count": count}

# --- ADMIN: Mark as read ---


@router.put("/api/admin/messages/{msg_id}/read")
def mark_as_read(msg_id: int, db: Session = Depends(get_db)):
    msg = db.query(models.ContactMessage).filter(
        models.ContactMessage.id == msg_id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found.")
    msg.is_read = True
    db.commit()
    return {"message": "Marked as read."}

# --- ADMIN: Reply — Send actual email to user ---


@router.post("/api/admin/messages/{msg_id}/reply")
def reply_to_message(msg_id: int, reply_text: str = Form(...), db: Session = Depends(get_db)):
    from datetime import datetime, timezone
    msg = db.query(models.ContactMessage).filter(
        models.ContactMessage.id == msg_id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found.")

    email_sent = False
    try:
        email_sent = send_email_reply(
            to_email=msg.email,
            to_name=msg.name,
            subject=msg.subject,
            reply_text=reply_text
        )
    except Exception as e:
        # Still mark as replied but log warning
        msg.is_replied = True
        msg.reply_text = reply_text
        msg.replied_at = datetime.now(timezone.utc)
        db.commit()
        raise HTTPException(
            status_code=500, detail=f"Failed to send email: {str(e)}")

    msg.is_replied = True
    msg.reply_text = reply_text
    msg.replied_at = datetime.now(timezone.utc)
    db.commit()
    return {
        "message": f"Reply sent to {msg.email}",
        "email_sent": email_sent
    }
