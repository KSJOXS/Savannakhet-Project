from app.database import SessionLocal
from app.models import Category, Place


def fix_link():
    db = SessionLocal()
    try:
        hotel_cat = db.query(Category).filter(
            Category.parent_type == 'hotel').first()
        hotel = db.query(Place).filter(
            Place.name == "Daosavanh Resort & Spa").first()

        if not hotel_cat:
            print("No hotel category found!")
            return

        if not hotel:
            print("No hotel found!")
            return

        print(
            f"Fixing hotel {hotel.name} (currently {hotel.category_id}) -> {hotel_cat.name} (ID: {hotel_cat.id})")
        hotel.category_id = hotel_cat.id
        db.commit()
        print("Success!")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    fix_link()
