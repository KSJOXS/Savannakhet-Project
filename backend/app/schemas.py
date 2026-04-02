from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# --- User ---
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    role: str
    deleted_at: Optional[datetime] = None
    class Config: from_attributes = True

# --- Place ---
class PlaceBase(BaseModel):
    name: str
    description: Optional[str] = None
    category_id: int
    image_url: Optional[str] = None
    location_lat: float  # พิกัดละติจูด
    location_lng: float  # พิกัดลองจิจูด
    is_published: bool = True

class PlaceUpdate(PlaceBase):
    """ใช้สำหรับ PUT request ตอนแก้ไขข้อมูล"""
    pass

class PlaceResponse(PlaceBase):
    id: int
    rating_avg: float
    class Config: from_attributes = True

# --- Category & Review ---
class CategoryCreate(BaseModel):
    name: str

class CategoryResponse(BaseModel):
    id: int
    name: str
    class Config: from_attributes = True

class ReviewCreate(BaseModel):
    place_id: int
    user_id: int
    rating: int
    comment: Optional[str] = None