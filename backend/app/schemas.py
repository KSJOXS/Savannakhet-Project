from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime

class ItineraryRequest(BaseModel):
    days: int = Field(default=1, ge=1, le=5)
    user_id: Optional[int] = None
    preferences: Optional[List[str]] = None
    month: Optional[int] = Field(default=None, ge=1, le=12)
    budget: Optional[str] = None

# --- User ---
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    preferences: Optional[List[str]] = None

class UserLogin(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    preferences: Optional[List[str]] = None

class UserResponse(UserBase):
    id: int
    role: str
    deleted_at: Optional[datetime] = None
    profile_image: Optional[str] = None  
    preferences: Optional[List[str]] = None
    post_permission_status: Optional[str] = "none"
    
    @field_validator('preferences', mode='before')
    @classmethod
    def parse_preferences(cls, v):
        import json
        if isinstance(v, str):
            try:
                return json.loads(v)
            except:
                return [v]
        return v
        
    class Config: from_attributes = True

# --- Place ---
class PlaceBase(BaseModel):
    name: str
    description: Optional[str] = None
    category_id: int
    image_url: Optional[str] = None
    location_lat: Optional[float] = None
    location_lng: Optional[float] = None
    is_published: bool = True
    opening_hours: Optional[dict] = None
    owner_id: Optional[int] = None
    status: str = "pending"
    
    # Premium Details
    best_months: Optional[str] = None
    ideal_stay: Optional[str] = None
    daily_budget: Optional[str] = None
    location_name: Optional[str] = None
    best_for: Optional[List[str]] = None
    avoid_if: Optional[List[str]] = None
    booking_url: Optional[str] = None
    agoda_url: Optional[str] = None

class PlaceUpdate(PlaceBase):
    """ใช้สำหรับ PUT request ตอนแก้ไขข้อมูล"""
    pass

class PlaceResponse(PlaceBase):
    id: int
    rating_avg: float
    review_count: int = 0
    opening_hours: Optional[dict] = None
    class Config: from_attributes = True
    location_lat: Optional[float] = None
    location_lng: Optional[float] = None

class PlaceSectionResponse(BaseModel):
    id: int
    place_id: int
    image_url: Optional[str] = None
    description: Optional[str] = None
    order_index: int = 0
    class Config: from_attributes = True

# --- Category & Review ---
class CategoryCreate(BaseModel):
    name: str
    parent_type: str = 'other'

class CategoryResponse(BaseModel):
    id: int
    name: str
    parent_type: str
    class Config: from_attributes = True

class ReviewCreate(BaseModel):
    place_id: int
    user_id: int
    rating: int
    comment_text: Optional[str] = None
    images: Optional[List[str]] = []

class InteractionResponse(BaseModel):
    id: int
    user_id: int
    place_id: int
    rating: int
    comment: Optional[str] = None
    images: Optional[List[str]] = []
    liked_by: Optional[List[int]] = []
    visited_at: datetime
    username: Optional[str] = None
    profile_image: Optional[str] = None
    place_name: Optional[str] = None

    class Config: from_attributes = True

# --- Favorite ---
class FavoriteToggle(BaseModel):
    user_id: int
    place_id: int

class FavoriteResponse(BaseModel):
    id: int
    user_id: int
    place_id: int
    created_at: datetime
    place: PlaceResponse

    class Config: from_attributes = True

class UserInteractionCreate(BaseModel):
    place_id: int
    rating: Optional[float] = None
    comment: Optional[str] = None
    interaction_type: str  # เช่น 'click', 'like', 'visit'

# --- Site Settings ---
class SiteSettingBase(BaseModel):
    value: Optional[str] = None
    description: Optional[str] = None

class SiteSettingCreate(SiteSettingBase):
    pass

class SiteSettingUpdate(SiteSettingBase):
    pass

class SiteSettingResponse(BaseModel):
    key_name: str
    value: Optional[str] = None
    description: Optional[str] = None
    class Config: from_attributes = True

# --- Interaction Log (GNN) ---
class InteractionLogCreate(BaseModel):
    user_id: int
    place_id: int
    action_type: str # 'view', 'like', 'review'
    score: Optional[int] = None # ใช้กรณี review (1-5)

# --- Recommendation ---
class RecommendationDetail(BaseModel):
    place: PlaceResponse
    reason: str
    score: float

class RecommendationResponse(BaseModel):
    status: str
    user_id: int
    dynamic_hero_category: Optional[str] = None
    recommended_places: List[RecommendationDetail]

# --- Contact Messages ---
class ContactMessageCreate(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str

class ContactMessageResponse(BaseModel):
    id: int
    name: str
    email: str
    subject: str
    message: str
    is_read: bool
    is_replied: bool
    created_at: datetime
    class Config: from_attributes = True

# --- Password Reset ---
class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str

# --- Itinerary ---
class ItineraryItemCreate(BaseModel):
    day: int
    time_slot: str
    time: str
    place_id: int

class ItineraryCreate(BaseModel):
    user_id: int
    title: str
    days: int
    items: List[ItineraryItemCreate]

class ItineraryItemResponse(BaseModel):
    id: int
    day: int
    time_slot: str
    time: str
    place_id: int
    place: Optional[PlaceResponse] = None
    class Config: from_attributes = True

class ItineraryResponse(BaseModel):
    id: int
    user_id: int
    title: str
    days: int
    created_at: datetime
    items: List[ItineraryItemResponse]
    class Config: from_attributes = True

class SwapPlaceRequest(BaseModel):
    current_place_id: Optional[int] = None
    time_slot: str
    month: Optional[int] = None
    preferences: Optional[List[str]] = None
    budget: Optional[str] = None
    used_place_ids: List[int] = []