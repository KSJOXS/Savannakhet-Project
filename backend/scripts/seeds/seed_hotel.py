from app.database import SessionLocal
from app.models import Category, Place


def seed_hotel():
    db = SessionLocal()
    try:
        # 1. Create Hotel Category
        hotel_cat = db.query(Category).filter(
            Category.name == "Hotel & Resort").first()
        if not hotel_cat:
            hotel_cat = Category(
                name="Hotel & Resort",
                description="Luxury and budget accommodations in Savannakhet",
                parent_type="hotel"
            )
            db.add(hotel_cat)
            db.commit()
            db.refresh(hotel_cat)
            print(f"Created category: {hotel_cat.name}")
        else:
            hotel_cat.parent_type = "hotel"
            db.commit()
            print(f"Updated category: {hotel_cat.name} to type 'hotel'")

        # 2. Create a Sample Hotel
        sample_hotel = db.query(Place).filter(
            Place.name == "Daosavanh Resort & Spa").first()
        if not sample_hotel:
            sample_hotel = Place(
                name="Daosavanh Resort & Spa",
                description="Experience the best resort in Savannakhet with a stunning view of the Mekong River and premium amenities.",
                category_id=hotel_cat.id,
                location_lat=16.5662,
                location_lng=104.7525,
                is_published=True,
                image_url="https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
                rating_avg=4.8
            )
            db.add(sample_hotel)
            db.commit()
            print(f"Created hotel: {sample_hotel.name}")
        else:
            print(f"Hotel {sample_hotel.name} already exists.")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_hotel()
