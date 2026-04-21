from sqlalchemy import Column, Integer, String, Text, ForeignKey, Numeric, JSON, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import LONGTEXT  # เพิ่มตัวนี้เพื่อรองรับ Base64 ยาวๆ
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
    
    rating_avg = Column(Numeric(3, 2), default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # ความสัมพันธ์
    category = relationship("Category", back_populates="places")
    interactions = relationship("Interaction", back_populates="place")
    favorites = relationship("Favorite", back_populates="place", cascade="all, delete")

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

    # เชื่อมไปที่ Interactions
    interactions = relationship("Interaction", back_populates="user", cascade="all, delete")
    favorites = relationship("Favorite", back_populates="user", cascade="all, delete")

class Interaction(Base):
    __tablename__ = "user_interactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    place_id = Column(Integer, ForeignKey("places.id"))
    rating = Column(Integer)
    comment = Column(Text)
    visited_at = Column(DateTime(timezone=True), server_default=func.now())

    # เชื่อมกลับ
    user = relationship("User", back_populates="interactions")
    place = relationship("Place", back_populates="interactions")

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    place_id = Column(Integer, ForeignKey("places.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # เชื่อมกลับ
    user = relationship("User", back_populates="favorites")
    place = relationship("Place", back_populates="favorites")

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