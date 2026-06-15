from app.models import Place
from app.database import SessionLocal
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


db = SessionLocal()

restaurants = [
    {
        "name": "Lin's Cafe",
        "category_id": 7,  # Coffee & Tea
        "description": "A popular cafe in Savannakhet known for its excellent locally sourced coffee and cozy atmosphere.",
        "latitude": 16.559, "longitude": 104.750,
        "address": "Ban Xayaphoum, Kaisone Phomvihane, Savannakhet",
        "rating_avg": 4.6, "price_level": 2,
        "images": ["https://images.unsplash.com/photo-1550966871-3ed3cdb5ed0c?w=800&q=80", "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=800&q=80"]
    },
    {
        "name": "Pilgrim's Kitchen & Inn",
        "category_id": 6,  # Restaurants
        "description": "Offering a diverse menu of Western, Asian and local Lao food. Great place to chill with friends.",
        "latitude": 16.558, "longitude": 104.752,
        "address": "Kaisone Phomvihane, Savannakhet",
        "rating_avg": 4.5, "price_level": 2,
        "images": ["https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800&q=80", "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800&q=80"]
    },
    {
        "name": "Savan Cafe",
        "category_id": 7,
        "description": "Historical French colonial style cafe serving breakfast, sandwiches, and amazing Lao coffee.",
        "latitude": 16.557, "longitude": 104.755,
        "address": "Old Town, Savannakhet",
        "rating_avg": 4.7, "price_level": 2,
        "images": ["https://images.unsplash.com/photo-1525648199074-cee30ba79a4a?w=800&q=80"]
    },
    {
        "name": "Dao Savanh Restaurant",
        "category_id": 6,
        "description": "Premium fine dining featuring authentic French cuisine in an elegant vintage colonial building.",
        "latitude": 16.550, "longitude": 104.751,
        "address": "Riverside, Savannakhet",
        "rating_avg": 4.8, "price_level": 4,
        "images": ["https://images.unsplash.com/photo-1414235077428-338988a2e8c0?w=800&q=80"]
    },
    {
        "name": "Mekong River Night Market",
        "category_id": 9,  # Street Food
        "description": "Bustling night market along the Mekong river offering delicious and affordable local street food.",
        "latitude": 16.561, "longitude": 104.745,
        "address": "Mekong Riverfront, Savannakhet",
        "rating_avg": 4.5, "price_level": 1,
        "images": ["https://images.unsplash.com/photo-1544148103-0773bf10d330?w=800&q=80"]
    },
    {
        "name": "White House Restaurant",
        "category_id": 6,
        "description": "A long-standing favorite for classic Lao and Thai cuisine with a family-friendly atmosphere.",
        "latitude": 16.565, "longitude": 104.748,
        "address": "Route 9, Savannakhet",
        "rating_avg": 4.2, "price_level": 3,
        "images": ["https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800&q=80"]
    },
    {
        "name": "Nang Lin Bar",
        "category_id": 8,  # Bars & Pubs
        "description": "Modern bar offering craft cocktails, cold local beers, and great music.",
        "latitude": 16.555, "longitude": 104.753,
        "address": "Downtown Savannakhet",
        "rating_avg": 4.4, "price_level": 2,
        "images": ["https://images.unsplash.com/photo-1533777857889-4be7c70b33f7?w=800&q=80"]
    },
    {
        "name": "Long Pizza Laos",
        "category_id": 6,
        "description": "The best wood-fired pizza in town with generous toppings and friendly service.",
        "latitude": 16.562, "longitude": 104.758,
        "address": "Talat Yen Plaza, Savannakhet",
        "rating_avg": 4.5, "price_level": 2,
        "images": ["https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=800&q=80"]
    },
    {
        "name": "Phosy Market Food Stalls",
        "category_id": 9,
        "description": "Experience authentic local life with traditional Lao breakfasts, noodles, and fresh snacks.",
        "latitude": 16.570, "longitude": 104.760,
        "address": "Phosy Market, Savannakhet",
        "rating_avg": 4.3, "price_level": 1,
        "images": ["https://images.unsplash.com/photo-1544148103-0773bf10d330?w=800&q=80"]
    },
    {
        "name": "Macchiato Coffee Savannakhet",
        "category_id": 7,
        "description": "Trendy coffee shop perfect for remote working, featuring specialty coffee beans and pastries.",
        "latitude": 16.552, "longitude": 104.749,
        "address": "Old Quarter, Savannakhet",
        "rating_avg": 4.6, "price_level": 2,
        "images": ["https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=800&q=80"]
    },
    {
        "name": "Sunset Bar Mekong",
        "category_id": 8,
        "description": "The perfect spot to grab a Beerlao and watch the beautiful sunset over the Mekong River.",
        "latitude": 16.548, "longitude": 104.745,
        "address": "Riverside, Savannakhet",
        "rating_avg": 4.8, "price_level": 2,
        "images": ["https://images.unsplash.com/photo-1470337458703-415120a41f67?w=800&q=80"]
    },
    {
        "name": "Sala Thai Restaurant",
        "category_id": 6,
        "description": "Authentic Thai food and spicy Lao salads in a comfortable, air-conditioned setting.",
        "latitude": 16.559, "longitude": 104.756,
        "address": "Center, Savannakhet",
        "rating_avg": 4.4, "price_level": 3,
        "images": ["https://images.unsplash.com/photo-1481833761820-0509d3217039?w=800&q=80"]
    }
]

nature_spots = [
    {
        "name": "Bung Va Lake",
        "category_id": 2,  # Nature
        "description": "A scenic natural lake outside the city, perfect for a relaxing afternoon walk or a local picnic.",
        "latitude": 16.580, "longitude": 104.800,
        "address": "Outskirts of Savannakhet",
        "rating_avg": 4.3, "price_level": 1,
        "images": ["https://images.unsplash.com/photo-1472214103451-9374bd1c798e?w=800&q=80", "https://images.unsplash.com/photo-1465146344425-f00d5f5c8f07?w=800&q=80"]
    },
    {
        "name": "Dong Natad National Protected Area",
        "category_id": 2,
        "description": "A beautiful ancient forest featuring massive dipterocarp trees and serene nature trails. A spiritual and natural sanctuary.",
        "latitude": 16.600, "longitude": 104.850,
        "address": "Nong Deun Village, Savannakhet",
        "rating_avg": 4.7, "price_level": 1,
        "images": ["https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800&q=80", "https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=800&q=80"]
    },
    {
        "name": "Tad Salaen Waterfall",
        "category_id": 2,
        "description": "A beautiful cascading waterfall surrounded by dense jungle. Best visited during the rainy season for full flow.",
        "latitude": 16.400, "longitude": 105.100,
        "address": "Phine District, Savannakhet",
        "rating_avg": 4.5, "price_level": 1,
        "images": ["https://images.unsplash.com/photo-1433086966358-54859d0ed716?w=800&q=80", "https://images.unsplash.com/photo-1510798831971-661eb04b3739?w=800&q=80"]
    },
    {
        "name": "Phou Xang Heae National Protected Area",
        "category_id": 2,
        "description": "An expansive mountainous national park featuring diverse wildlife, trekking routes, and stunning viewpoints.",
        "latitude": 16.700, "longitude": 105.500,
        "address": "Vilabouly District, Savannakhet",
        "rating_avg": 4.6, "price_level": 2,
        "images": ["https://images.unsplash.com/photo-1501854140801-50d01698950b?w=800&q=80"]
    },
    {
        "name": "Mekong River Bank Gardens",
        "category_id": 10,  # Nature & Parks
        "description": "A nicely paved and green riverfront park ideal for jogging, cycling, or enjoying the evening breeze.",
        "latitude": 16.550, "longitude": 104.745,
        "address": "Riverside Road, Savannakhet",
        "rating_avg": 4.4, "price_level": 1,
        "images": ["https://images.unsplash.com/photo-1586348943529-beaae6c28db9?w=800&q=80"]
    },
    {
        "name": "Nong Lom Lake",
        "category_id": 2,
        "description": "A peaceful natural lake area surrounded by lush green fields, great for bird watching and photography.",
        "latitude": 16.650, "longitude": 104.900,
        "address": "Champhone District, Savannakhet",
        "rating_avg": 4.2, "price_level": 1,
        "images": ["https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=800&q=80"]
    },
    {
        "name": "Tad Phouy Waterfall",
        "category_id": 2,
        "description": "A hidden gem waterfall offering a refreshing natural pool for swimming amid the tropical forest.",
        "latitude": 16.350, "longitude": 105.200,
        "address": "Thapangthong District, Savannakhet",
        "rating_avg": 4.6, "price_level": 1,
        "images": ["https://images.unsplash.com/photo-1433086966358-54859d0ed716?w=800&q=80"]
    },
    {
        "name": "Houay Ki Ecological Park",
        "category_id": 10,
        "description": "A community-managed ecological park showcasing local flora and providing a relaxing natural retreat.",
        "latitude": 16.580, "longitude": 104.850,
        "address": "Kaisone Phomvihane, Savannakhet",
        "rating_avg": 4.1, "price_level": 1,
        "images": ["https://images.unsplash.com/photo-1475924156734-496f6cac6ec1?w=800&q=80"]
    }
]

print("Adding Restaurants...")
for data in restaurants:
    # Check if exists
    existing = db.query(Place).filter(Place.name == data["name"]).first()
    if not existing:
        place = Place(
            name=data["name"],
            category_id=data["category_id"],
            description=data["description"],
            location_lat=data["latitude"],
            location_lng=data["longitude"],
            location_name=data["address"],
            rating_avg=data["rating_avg"],
            image_url=json.dumps(data["images"])
        )
        db.add(place)
        db.commit()
        db.refresh(place)

print("Adding Nature Spots...")
for data in nature_spots:
    # Check if exists
    existing = db.query(Place).filter(Place.name == data["name"]).first()
    if not existing:
        place = Place(
            name=data["name"],
            category_id=data["category_id"],
            description=data["description"],
            location_lat=data["latitude"],
            location_lng=data["longitude"],
            location_name=data["address"],
            rating_avg=data["rating_avg"],
            image_url=json.dumps(data["images"])
        )
        db.add(place)
        db.commit()
        db.refresh(place)

db.close()
print("Done seeding Nature and Restaurants!")
