import sys
import os
import random
import json

# Ensure we can import app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from app.database import SessionLocal
from app.models import Category, Place

places_data = [
    {
        "name": "Savannakhet Dinosaur Museum",
        "desc": "A museum exhibiting dinosaur fossils found in Savannakhet province.",
        "lat": 16.5562, "lng": 104.7520, "image": "https://images.unsplash.com/photo-1518998053401-878918451195?q=80&w=800", "parent_type": "other", "cat_name": "Museum"
    },
    {
        "name": "That Ing Hang Stupa",
        "desc": "One of the most sacred stupas in Central Laos, dating back to the 16th century.",
        "lat": 16.6333, "lng": 104.8333, "image": "https://images.unsplash.com/photo-1590273466185-36e7887702fb?q=80&w=800", "parent_type": "culture", "cat_name": "Temple"
    },
    {
        "name": "Wat Sainyaphum",
        "desc": "A beautiful and historic Buddhist temple near the Mekong River in the city center.",
        "lat": 16.5615, "lng": 104.7540, "image": "https://images.unsplash.com/photo-1601618216395-5384218a9fc8?q=80&w=800", "parent_type": "culture", "cat_name": "Temple"
    },
    {
        "name": "Mekong Riverfront Promenade",
        "desc": "A relaxing place for an evening walk, offering great sunset views over the Mekong River.",
        "lat": 16.5540, "lng": 104.7475, "image": "https://images.unsplash.com/photo-1543324632-475252d674cc?q=80&w=800", "parent_type": "nature", "cat_name": "Park"
    },
    {
        "name": "Lin's Cafe",
        "desc": "A popular cafe known for its excellent coffee and relaxed atmosphere.",
        "lat": 16.5590, "lng": 104.7510, "image": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?q=80&w=800", "parent_type": "restaurant", "cat_name": "Cafe"
    },
    {
        "name": "Macchiato de Coffee",
        "desc": "Cozy cafe with great pastries, local coffee blends, and air-conditioning.",
        "lat": 16.5620, "lng": 104.7550, "image": "https://images.unsplash.com/photo-1497935586351-b67a49e012bf?q=80&w=800", "parent_type": "restaurant", "cat_name": "Cafe"
    },
    {
        "name": "Savan Cafe",
        "desc": "Local cafe serving a mix of Lao dishes and western breakfast options.",
        "lat": 16.5630, "lng": 104.7565, "image": "https://images.unsplash.com/photo-1554118811-1e0d58224f24?q=80&w=800", "parent_type": "restaurant", "cat_name": "Cafe"
    },
    {
        "name": "White House Restaurant",
        "desc": "An elegant dining spot offering delicious Lao and Thai cuisine.",
        "lat": 16.5585, "lng": 104.7505, "image": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?q=80&w=800", "parent_type": "restaurant", "cat_name": "Restaurant"
    },
    {
        "name": "Savannakhet Night Market",
        "desc": "Vibrant night market with amazing local street food and snacks.",
        "lat": 16.5605, "lng": 104.7525, "image": "https://images.unsplash.com/photo-1533900298318-6b8da08a523e?q=80&w=800", "parent_type": "restaurant", "cat_name": "Market"
    },
    {
        "name": "Pilgrim's Kitchen & Inn",
        "desc": "Friendly restaurant and guesthouse known for its hearty meals.",
        "lat": 16.5650, "lng": 104.7580, "image": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?q=80&w=800", "parent_type": "restaurant", "cat_name": "Restaurant"
    },
    {
        "name": "Avalon Residence",
        "desc": "Comfortable and modern hotel located near the city center.",
        "lat": 16.5640, "lng": 104.7530, "image": "https://images.unsplash.com/photo-1566073771259-6a8506099945?q=80&w=800", "parent_type": "hotel", "cat_name": "Hotel"
    },
    {
        "name": "Bungva Lake",
        "desc": "A scenic lake perfect for picnics, relaxing, and eating fresh fish at local floating restaurants.",
        "lat": 16.5800, "lng": 104.7700, "image": "https://images.unsplash.com/photo-1437482078695-73f5af6ec827?q=80&w=800", "parent_type": "nature", "cat_name": "Lake"
    },
    {
        "name": "Dong Natad National Protected Area",
        "desc": "A sacred forest with a small lake, ideal for light trekking and nature observation.",
        "lat": 16.6500, "lng": 104.8500, "image": "https://images.unsplash.com/photo-1448375240586-882707db888b?q=80&w=800", "parent_type": "nature", "cat_name": "National Park"
    },
    {
        "name": "Old French Quarter",
        "desc": "Stroll down the streets filled with decaying but charming French colonial architecture.",
        "lat": 16.5560, "lng": 104.7480, "image": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?q=80&w=800", "parent_type": "culture", "cat_name": "Historical Landmark"
    },
    {
        "name": "St. Teresa's Catholic Church",
        "desc": "A beautifully preserved Catholic church built during the French colonial era.",
        "lat": 16.5575, "lng": 104.7495, "image": "https://images.unsplash.com/photo-1548625361-ecbaeb6fcc43?q=80&w=800", "parent_type": "culture", "cat_name": "Historical Landmark"
    }
]

def seed_15_places():
    db = SessionLocal()
    try:
        # Find admin user to assign as owner
        from app.models import User
        admin = db.query(User).filter(User.role == 'admin').first()
        owner_id = admin.id if admin else None

        places_added = 0
        for p in places_data:
            # Check or create category
            category = db.query(Category).filter(Category.name == p["cat_name"]).first()
            if not category:
                category = Category(name=p["cat_name"], parent_type=p["parent_type"])
                db.add(category)
                db.commit()
                db.refresh(category)

            # Check if place exists
            existing = db.query(Place).filter(Place.name == p["name"]).first()
            if not existing:
                new_place = Place(
                    name=p["name"],
                    description=p["desc"],
                    category_id=category.id,
                    location_lat=p["lat"],
                    location_lng=p["lng"],
                    is_published=True,
                    image_url=p["image"],
                    rating_avg=0.0,
                    owner_id=owner_id,
                    status="pending"
                )
                db.add(new_place)
                places_added += 1
                print(f"Added place: {new_place.name}")
        
        db.commit()
        print(f"Successfully added {places_added} places.")
    except Exception as e:
        print(f"Error seeding places: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_15_places()
