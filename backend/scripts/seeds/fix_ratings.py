import sys
import os
from sqlalchemy.sql import func

# Ensure we can import app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from app.database import SessionLocal
from app.models import Place, Interaction

def fix_ratings():
    db = SessionLocal()
    try:
        places = db.query(Place).all()
        updated_count = 0
        
        for place in places:
            # Get real rating from Interaction table
            # Assuming rating in Interaction is out of 5 and we take the average
            result = db.query(func.avg(Interaction.rating)).filter(
                Interaction.place_id == place.id,
                Interaction.rating.isnot(None)
            ).scalar()
            
            real_rating = round(float(result), 1) if result is not None else 0.0
            
            if place.rating_avg != real_rating:
                print(f"Updating '{place.name}': {place.rating_avg} -> {real_rating}")
                place.rating_avg = real_rating
                updated_count += 1
                
        db.commit()
        print(f"Successfully updated ratings for {updated_count} places.")
    except Exception as e:
        print(f"Error updating ratings: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_ratings()
