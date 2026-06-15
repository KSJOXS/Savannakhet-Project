"""
seed_landmarks.py
รัน script นี้เพื่อเพิ่มข้อมูล Landmark categories และสถานที่ท่องเที่ยวลงฐานข้อมูล
Command: python seed_landmarks.py
"""
from app.models import Category, Place
from app.database import SessionLocal
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


db = SessionLocal()

# ============================================================
# 1. LANDMARK CATEGORIES
# ============================================================
landmark_categories_data = [
    {"name": "Temple & Pagoda",
        "description": "Buddhist temples, pagodas, and religious sites", "parent_type": "landmark"},
    {"name": "Museum",             "description": "Historical museums and cultural exhibitions",
        "parent_type": "landmark"},
    {"name": "Colonial Building",  "description": "French colonial era architecture",
        "parent_type": "landmark"},
    {"name": "Monument",           "description": "War memorials and commemorative monuments",
        "parent_type": "landmark"},
    {"name": "Market & Street",    "description": "Traditional markets and historic streets",
        "parent_type": "landmark"},
]

print("=== Creating Landmark Categories ===")
created_cats = {}
for cat_data in landmark_categories_data:
    # ตรวจสอบว่ามีอยู่แล้วหรือไม่
    existing = db.query(Category).filter(
        Category.name == cat_data["name"],
        Category.parent_type == "landmark"
    ).first()

    if existing:
        print(
            f"  [SKIP] Category already exists: {cat_data['name']} (id={existing.id})")
        created_cats[cat_data["name"]] = existing.id
    else:
        cat = Category(**cat_data)
        db.add(cat)
        db.flush()
        created_cats[cat_data["name"]] = cat.id
        print(f"  [OK]   Created: {cat_data['name']} (id={cat.id})")

db.commit()

# ============================================================
# 2. LANDMARK PLACES
# ============================================================
landmark_places_data = [
    {
        "name": "Wat Sainyaphum",
        "category_name": "Temple & Pagoda",
        "description": "One of the oldest and most revered temples in Savannakhet, dating back to the 16th century. The temple features stunning Lao-style architecture with intricate wood carvings and golden spires that shimmer in the sunlight.",
        "location_lat": 16.5567,
        "location_lng": 104.7620,
        "image_url": "https://images.unsplash.com/photo-1528360983277-13d401cdc186?w=800&q=80",
        "rating_avg": 4.7,
    },
    {
        "name": "Wat Xayaphoum",
        "category_name": "Temple & Pagoda",
        "description": "A peaceful Buddhist temple located in the heart of Savannakhet. Known for its beautiful garden, ancient Buddha statues, and serene atmosphere that draws both pilgrims and tourists.",
        "location_lat": 16.5540,
        "location_lng": 104.7590,
        "image_url": "https://images.unsplash.com/photo-1559628233-100c798642d8?w=800&q=80",
        "rating_avg": 4.5,
    },
    {
        "name": "Savannakhet Provincial Museum",
        "category_name": "Museum",
        "description": "The provincial museum houses an extensive collection of Lao artifacts, prehistoric fossils, and exhibits documenting the history of the Savannakhet province from ancient times to the present day.",
        "location_lat": 16.5560,
        "location_lng": 104.7600,
        "image_url": "https://images.unsplash.com/photo-1554907984-15263bfd63bd?w=800&q=80",
        "rating_avg": 4.3,
    },
    {
        "name": "Dinosaur Museum",
        "category_name": "Museum",
        "description": "A fascinating museum dedicated to the dinosaur fossils found in the Savannakhet region, one of Southeast Asia's richest paleontological sites. Features full-scale replicas and genuine fossil specimens.",
        "location_lat": 16.5530,
        "location_lng": 104.7610,
        "image_url": "https://images.unsplash.com/photo-1524492514790-8310bf594ea4?w=800&q=80",
        "rating_avg": 4.6,
    },
    {
        "name": "St. Teresa's Catholic Church",
        "category_name": "Colonial Building",
        "description": "A beautiful French colonial-era Catholic church built in the early 20th century. The church blends European Gothic architecture with local Lao artistic elements, creating a unique and stunning landmark.",
        "location_lat": 16.5550,
        "location_lng": 104.7575,
        "image_url": "https://images.unsplash.com/photo-1548625149-720f75ead27c?w=800&q=80",
        "rating_avg": 4.4,
    },
    {
        "name": "French Colonial Quarter",
        "category_name": "Colonial Building",
        "description": "A well-preserved district of French colonial buildings that give Savannakhet its distinctive charming character. Walking through these tree-lined streets feels like stepping back in time to 1900s Indochina.",
        "location_lat": 16.5545,
        "location_lng": 104.7580,
        "image_url": "https://images.unsplash.com/photo-1550159930-40066082a4fc?w=800&q=80",
        "rating_avg": 4.8,
    },
    {
        "name": "Savannakhet War Memorial",
        "category_name": "Monument",
        "description": "A solemn monument commemorating the soldiers and civilians who sacrificed their lives during the conflicts that shaped modern Laos. The memorial is a place of reflection and national pride.",
        "location_lat": 16.5518,
        "location_lng": 104.7595,
        "image_url": "https://images.unsplash.com/photo-1568430462989-44163eb1752f?w=800&q=80",
        "rating_avg": 4.2,
    },
    {
        "name": "Talat Yen (Night Market)",
        "category_name": "Market & Street",
        "description": "A vibrant night market in Savannakhet where locals and tourists gather in the evenings to enjoy street food, local crafts, and the lively atmosphere. A perfect place to experience authentic Lao culture.",
        "location_lat": 16.5510,
        "location_lng": 104.7600,
        "image_url": "https://images.unsplash.com/photo-1533900298318-6b8da08a523e?w=800&q=80",
        "rating_avg": 4.5,
    },
    {
        "name": "Savan-VEDC Monument",
        "category_name": "Monument",
        "description": "A prominent monument at the center of the city symbolizing the unity and development of Savannakhet. The surrounding plaza is a popular gathering spot for locals in the evenings.",
        "location_lat": 16.5535,
        "location_lng": 104.7555,
        "image_url": "https://images.unsplash.com/photo-1582139329536-e7284fece509?w=800&q=80",
        "rating_avg": 4.1,
    },
    {
        "name": "Cao Dai Temple",
        "category_name": "Temple & Pagoda",
        "description": "A unique Vietnamese Cao Dai temple reflecting the multicultural heritage of Savannakhet. Its colorful facade and distinctive religious iconography make it one of the most visually striking buildings in the city.",
        "location_lat": 16.5580,
        "location_lng": 104.7565,
        "image_url": "https://images.unsplash.com/photo-1588865258958-6c88a95c2b0f?w=800&q=80",
        "rating_avg": 4.3,
    },
]

print("\n=== Creating Landmark Places ===")
for place_data in landmark_places_data:
    cat_name = place_data.pop("category_name")
    cat_id = created_cats.get(cat_name)

    if not cat_id:
        print(f"  [WARN] Category not found: {cat_name}")
        continue

    existing = db.query(Place).filter(Place.name == place_data["name"]).first()
    if existing:
        print(
            f"  [UPDATE] Place exists, setting status to approved: {place_data['name']}")
        existing.status = "approved"
        continue

    place = Place(
        category_id=cat_id,
        is_published=True,
        status="approved",
        **place_data
    )
    db.add(place)
    print(f"  [OK]   Created: {place_data['name']}")

db.commit()
db.close()

print("\n✅ Landmark seed completed successfully!")
print(f"   Categories: {len(landmark_categories_data)}")
print(f"   Places:     {len(landmark_places_data)}")
