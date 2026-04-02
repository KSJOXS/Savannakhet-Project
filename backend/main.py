from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import models
from database import engine
from app.routes import users, places, reviews, admin

# สร้างตารางใน DB
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Savannakhet Smart Travel API")

# CORS Settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ติดตั้ง Static Files สำหรับเรียกดูรูปภาพ
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- จดทะเบียน Route (เรียกใช้จากไฟล์ที่เราแยกไว้) ---
app.include_router(users.router)
app.include_router(places.router)
app.include_router(reviews.router)
app.include_router(admin.router)

@app.get("/")
def home():
    return {"message": "Welcome to Savannakhet Smart Travel API"}