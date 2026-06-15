from app.models import Place
from app.database import SessionLocal
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


updates = {
    "Daosavanh Resort & Spa": "A 4-star hotel located along the Mekong River, featuring a spa and outdoor pool with stunning river views. Ideal for couples and families.",
    "Leena Guesthouse": "A cozy, budget-friendly guesthouse located in the heart of Savannakhet, within easy walking distance to tourist attractions.",
    "Phonevilay Hotel": "A modern hotel with clean, comfortable rooms, free breakfast, and free parking, located near the fresh market.",
    "Savannakhet Eco Lodge": "An eco-friendly lodge surrounded by nature. Perfect for nature lovers, offering activities like birdwatching and jungle trekking.",
    "Mekong Hotel Savannakhet": "A riverside hotel with beautiful views and spacious rooms. Features a restaurant serving authentic Lao cuisine, located next to the ferry terminal.",
    "Inthira Savannakhet Hotel": "A French colonial-style boutique hotel situated in the old town. Features exquisite decor and is perfect for history enthusiasts.",
    "Hoongthip Hotel": "A mid-range hotel with good service, delicious breakfast, and a swimming pool. Suitable for families on a short stay.",
    "Southida Guesthouse": "A small, warm guesthouse with friendly English-speaking owners. Ideal for solo travelers.",
    "Savan Vegas Hotel & Casino": "A 5-star hotel featuring a casino, spa, and luxurious rooms with full amenities. The largest hotel in the province.",
    "Vansana Savannakhet Hotel": "A clean and modern 3-star hotel located near the airport. Perfect for business travelers needing convenience, with an on-site restaurant and bar.",
    "Khammouane Riverside Resort": "A tranquil riverside resort ideal for relaxation. Offers river cruises, fishing activities, and fresh freshwater seafood.",
    "Phonesavanh Hotel": "An affordable, clean, and safe local hotel. Provides laundry service, a restaurant, and bicycle rentals, with easy tuk-tuk access.",
    "Lao Orchid Hotel": "A beautiful city-center hotel featuring modern rooms with private balconies, close to shopping centers and restaurants.",
    "Champa Garden Hotel": "A boutique hotel set amidst frangipani gardens. Offers a shady, peaceful atmosphere, a tasty buffet breakfast, and traditional Lao design.",
    "Phouthip Hotel": "A business hotel with meeting rooms and facilities for corporate events. Offers airport transfers and high-speed WiFi.",
    "Savan Na Khet Heritage Hotel": "A heritage hotel preserving the charm of original French architecture. Rooms are decorated with rare antiques, highly popular among photographers.",
    "Riverside Villas Savannakhet": "Luxurious villas along the Mekong River. Features private villa accommodations, private pools, and 24-hour butler service.",
    "Pakse-Savannakhet Transit Hotel": "A convenient hotel located near the bus terminal. Ideal for transit travelers making a stopover. Budget-friendly with 24-hour check-in.",
    "Savanhxai Boutique Hotel": "A contemporarily designed boutique hotel blending Lao art with modern design. Features a popular ground-floor cafe.",
    "Golden Palace Hotel Savannakhet": "A palace-style hotel with luxurious rooms. Features large gardens, a tennis court, a fitness center, and a full-service spa. Perfect for weddings."
}


def update():
    db = SessionLocal()
    try:
        updated = 0
        for name, desc in updates.items():
            place = db.query(Place).filter(Place.name == name).first()
            if place:
                place.description = desc
                updated += 1
                print(f"Updated: {name}")
        db.commit()
        print(f"Total updated: {updated}")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    update()
