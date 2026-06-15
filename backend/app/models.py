from sqlalchemy import Column, Integer, String, Text, ForeignKey, Numeric, JSON, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import LONGTEXT  
from app.database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    parent_type = Column(String(50), default='other')  # 'nature', 'restaurant', 'hotel', 'other'

    # ความสัมพันธ์: หนึ่งหมวดหมู่มีได้หลายสถานที่
    places = relationship("Place", back_populates="category")

class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    name = Column(String(255), nullable=False)
    description = Column(Text)
    location_lat = Column(Numeric(10, 8)) 
    location_lng = Column(Numeric(11, 8))
    is_published = Column(Boolean, default=True)
    
    # แก้ไข: เปลี่ยนจาก String(255) เป็น LONGTEXT เพื่อแก้ Error 1406 (Data too long)
    image_url = Column(LONGTEXT) 
    
    opening_hours = Column(JSON, nullable=True)  # {"mon":{"open":"08:00","close":"17:00","closed":false}, ...}
    
    # User Submission
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(String(20), default="pending")  # 'pending', 'approved', 'rejected'
    
    rating_avg = Column(Numeric(3, 2), default=0)
    
    # Booking Links
    booking_url = Column(Text, nullable=True)
    agoda_url = Column(Text, nullable=True)
    
    # Premium Details
    best_months = Column(String(100), nullable=True)
    ideal_stay = Column(String(100), nullable=True)
    daily_budget = Column(String(100), nullable=True)
    location_name = Column(String(100), nullable=True)
    best_for = Column(JSON, nullable=True)  # List of strings
    avoid_if = Column(JSON, nullable=True)  # List of strings
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # ความสัมพันธ์
    category = relationship("Category", back_populates="places")
    interactions = relationship("Interaction", back_populates="place")
    favorites = relationship("Favorite", back_populates="place", cascade="all, delete")
    owner = relationship("User", back_populates="owned_places")
    sections = relationship("PlaceSection", back_populates="place", cascade="all, delete-orphan", order_by="PlaceSection.order_index")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    preferences = Column(JSON) # เก็บความชอบ เช่น ["culture", "food"]
    role = Column(String(20), default="user")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    deleted_at = Column(DateTime, nullable=True)
    profile_image = Column(String(255), nullable=True)
    post_permission_status = Column(String(20), default="none") # 'none', 'pending', 'approved'

    # เชื่อมไปที่ Interactions
    interactions = relationship("Interaction", back_populates="user", cascade="all, delete")
    favorites = relationship("Favorite", back_populates="user", cascade="all, delete")
    owned_places = relationship("Place", back_populates="owner")

class Interaction(Base):
    __tablename__ = "user_interactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    place_id = Column(Integer, ForeignKey("places.id"))
    rating = Column(Integer)
    comment = Column(Text)
    images = Column(LONGTEXT, nullable=True) # JSON array of image URLs
    liked_by = Column(JSON, nullable=True) # JSON array of user IDs
    visited_at = Column(DateTime(timezone=True), server_default=func.now())

    # เชื่อมกลับ
    user = relationship("User", back_populates="interactions")
    place = relationship("Place", back_populates="interactions")
    post_comments = relationship("PostComment", back_populates="post", cascade="all, delete-orphan")

class PostComment(Base):
    __tablename__ = "post_comments"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("user_interactions.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id"))
    comment_text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    post = relationship("Interaction", back_populates="post_comments")
    user = relationship("User", backref="post_comments")

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    place_id = Column(Integer, ForeignKey("places.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # เชื่อมกลับ
    user = relationship("User", back_populates="favorites")
    place = relationship("Place", back_populates="favorites")

class ContactMessage(Base):
    __tablename__ = "contact_messages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    subject = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    is_replied = Column(Boolean, default=False)
    reply_text = Column(Text, nullable=True)   # เก็บข้อความที่ admin ตอบกลับ
    replied_at = Column(DateTime(timezone=True), nullable=True)  # เวลาที่ตอบ
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SiteSetting(Base):
    __tablename__ = "site_settings"

    key_name = Column(String(100), primary_key=True, index=True)
    value = Column(LONGTEXT)
    description = Column(String(255))

class InteractionLog(Base):
    __tablename__ = "interaction_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    place_id = Column(Integer, ForeignKey("places.id", ondelete="CASCADE"))
    action_type = Column(String(50)) # 'view', 'like', 'review'
    interaction_weight = Column(Numeric(5, 2), default=1.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # เชื่อมกลับ
    user = relationship("User", backref="interaction_logs")
    place = relationship("Place", backref="interaction_logs")

class PlaceSection(Base):
    """Stores rich content sections for a place (image + description), like a travel article."""
    __tablename__ = "place_sections"

    id = Column(Integer, primary_key=True, index=True)
    place_id = Column(Integer, ForeignKey("places.id", ondelete="CASCADE"), nullable=False)
    image_url = Column(String(500), nullable=True)   # path to uploaded image
    description = Column(Text, nullable=True)         # rich text / paragraph
    order_index = Column(Integer, default=0)          # display order
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    place = relationship("Place", back_populates="sections")


class PasswordReset(Base):
    __tablename__ = "password_resets"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), index=True)
    token = Column(String(255), unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# --- Itinerary Models ---
class Itinerary(Base):
    __tablename__ = "itineraries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    days = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", backref="itineraries")
    items = relationship("ItineraryItem", back_populates="itinerary", cascade="all, delete-orphan")

class ItineraryItem(Base):
    __tablename__ = "itinerary_items"

    id = Column(Integer, primary_key=True, index=True)
    itinerary_id = Column(Integer, ForeignKey("itineraries.id", ondelete="CASCADE"), nullable=False)
    day = Column(Integer, nullable=False)
    time_slot = Column(String(50), nullable=False)  # Morning, Afternoon, Evening
    time = Column(String(20), nullable=False)       # 09:00, 14:00, 19:00
    place_id = Column(Integer, ForeignKey("places.id", ondelete="CASCADE"), nullable=False)
    
    itinerary = relationship("Itinerary", back_populates="items")
    place = relationship("Place")