from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
import json

db = SessionLocal()
try:
    place = db.query(models.Place).filter(models.Place.id == 7).first()
    if place:
        print(f"ID: {place.id}")
        print(f"Name: {place.name}")
        print(f"Best For: {place.best_for}")
        print(f"Avoid If: {place.avoid_if}")

        # Test serialization
        from app import schemas
        p_res = schemas.PlaceResponse.from_orm(place)
        print("Serialization successful")
    else:
        print("Place ID 7 not found")
except Exception as e:
    print(f"Error: {e}")
finally:
    db.close()
