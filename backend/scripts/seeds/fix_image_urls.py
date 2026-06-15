from app.models import Place
from app.database import SessionLocal
import sys
import os
import json

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../')))


# Map place names to working image URLs (using picsum.photos for reliability)
IMAGE_MAP = {
    "Savannakhet Dinosaur Museum": "https://images.unsplash.com/photo-1525789351284-e1aae0ec1ae6?w=800",
    "That Ing Hang Stupa": "https://images.unsplash.com/photo-1528360983277-13d401cdc186?w=800",
    "Mekong Riverfront Promenade": "https://images.unsplash.com/photo-1502685104226-ee32379fefbe?w=800",
    "Macchiato de Coffee": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=800",
    "Savannakhet Night Market": "https://images.unsplash.com/photo-1516685018646-549198525c1b?w=800",
    "Avalon Residence": "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800",
    "Bungva Lake": "https://images.unsplash.com/photo-1501854140801-50d01698950b?w=800",
    "Old French Quarter": "https://images.unsplash.com/photo-1467269204594-9661b134dd2b?w=800",
    "Dong Natad National Protected Area": "https://images.unsplash.com/photo-1448375240586-882707db888b?w=800",
    "St. Teresa's Catholic Church": "https://images.unsplash.com/photo-1564460549828-f7a9e8e0e0da?w=800",
    "Wat Sainyaphum": "https://images.unsplash.com/photo-1583417319070-4a69db38a482?w=800",
}


def fix_image_urls():
    db = SessionLocal()
    try:
        updated = 0
        for name, new_url in IMAGE_MAP.items():
            place = db.query(Place).filter(Place.name == name).first()
            if place:
                # Check if current image_url is a JSON array or a plain string
                img = place.image_url or ''
                if img.startswith('['):
                    try:
                        imgs = json.loads(img)
                        if imgs and imgs[0].startswith('https://images.unsplash.com'):
                            print(
                                f"Updating '{name}': {imgs[0][:50]}... -> {new_url}")
                            place.image_url = new_url
                            updated += 1
                    except:
                        pass
                elif img.startswith('https://images.unsplash.com'):
                    print(f"Updating '{name}': {img[:50]}... -> {new_url}")
                    place.image_url = new_url
                    updated += 1

        db.commit()
        print(f"\nSuccessfully updated {updated} place images.")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    fix_image_urls()
