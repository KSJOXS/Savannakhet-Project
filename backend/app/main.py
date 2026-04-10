from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app import models
from app.database import engine
from app.api.routes import users, places, reviews, admin, favorites, interactions, recommendations, settings

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
app.include_router(favorites.router)
app.include_router(recommendations.router, prefix="/api/recommendations", tags=["AI Recommendations"])

# ✅ แก้ไขจุดที่ 2: จดทะเบียน interactions router
app.include_router(interactions.router, prefix="/api/interactions", tags=["Interactions"])

# ✅ จดทะเบียน Settings Router
app.include_router(settings.router, prefix="/api/settings", tags=["Settings"])

@app.get("/")
def home():
    return {"message": "Welcome to Savannakhet Smart Travel API"}