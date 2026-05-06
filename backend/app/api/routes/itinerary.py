from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.database import get_db
from app import models, schemas
import random
import json

router = APIRouter()

def parse_preferences(pref_data):
    if not pref_data:
        return []
    if isinstance(pref_data, str):
        try:
            return json.loads(pref_data)
        except:
            return []
    return pref_data

@router.post("/generate", response_model=Dict[str, List[Dict[str, Any]]])
def generate_itinerary(request: schemas.ItineraryRequest, db: Session = Depends(get_db)):
    user_prefs = request.preferences or []
    
    if not user_prefs and request.user_id:
        user = db.query(models.User).filter(models.User.id == request.user_id).first()
        if user:
            user_prefs = parse_preferences(user.preferences)

    # Fetch all active places with their categories
    places_query = db.query(models.Place, models.Category).join(
        models.Category, models.Place.category_id == models.Category.id
    ).filter(models.Place.status == "approved").all()

    # Categorize places based on time of day suitability
    morning_spots = []    # Nature, Culture, Landmark
    afternoon_spots = []  # Cafe, Culture, Landmark, Shopping
    evening_spots = []    # Local Food, Restaurant, Chill, Nightlife

    for place, cat in places_query:
        ptype = cat.parent_type
        # Add slight boost if it matches user preference
        is_preferred = ptype in user_prefs

        place_data = {
            "place": place,
            "category": cat.name,
            "parent_type": ptype,
            "is_preferred": is_preferred,
            "rating": float(place.rating_avg or 0.0)
        }

        if ptype in ['nature', 'culture', 'landmark']:
            morning_spots.append(place_data)
            
        if ptype in ['cafe', 'landmark', 'culture', 'shopping']:
            afternoon_spots.append(place_data)
            
        if ptype in ['local_food', 'restaurant', 'chill', 'nightlife']:
            evening_spots.append(place_data)

    # Helper function to sort by preference and rating + randomness
    def sort_spots(spots):
        random.shuffle(spots)
        return sorted(spots, key=lambda x: (x['is_preferred'], x['rating'] + random.uniform(-1.0, 1.0)), reverse=True)

    morning_spots = sort_spots(morning_spots)
    afternoon_spots = sort_spots(afternoon_spots)
    evening_spots = sort_spots(evening_spots)

    itinerary = {}
    used_place_ids = set()

    for day in range(1, request.days + 1):
        day_plan = []
        
        # 1. Select Morning Spot
        morning_pick = next((s for s in morning_spots if s['place'].id not in used_place_ids), None)
        if morning_pick:
            used_place_ids.add(morning_pick['place'].id)
            day_plan.append({
                "time_slot": "Morning",
                "time": "09:00",
                "place": {
                    "id": morning_pick['place'].id,
                    "name": morning_pick['place'].name,
                    "description": morning_pick['place'].description,
                    "image_url": morning_pick['place'].image_url,
                    "rating_avg": morning_pick['place'].rating_avg,
                    "category_id": morning_pick['place'].category_id,
                },
                "category_name": morning_pick['category'],
                "is_preferred": morning_pick['is_preferred']
            })

        # 2. Select Afternoon Spot
        afternoon_pick = next((s for s in afternoon_spots if s['place'].id not in used_place_ids), None)
        if afternoon_pick:
            used_place_ids.add(afternoon_pick['place'].id)
            day_plan.append({
                "time_slot": "Afternoon",
                "time": "14:00",
                "place": {
                    "id": afternoon_pick['place'].id,
                    "name": afternoon_pick['place'].name,
                    "description": afternoon_pick['place'].description,
                    "image_url": afternoon_pick['place'].image_url,
                    "rating_avg": afternoon_pick['place'].rating_avg,
                    "category_id": afternoon_pick['place'].category_id,
                },
                "category_name": afternoon_pick['category'],
                "is_preferred": afternoon_pick['is_preferred']
            })

        # 3. Select Evening Spot
        evening_pick = next((s for s in evening_spots if s['place'].id not in used_place_ids), None)
        if evening_pick:
            used_place_ids.add(evening_pick['place'].id)
            day_plan.append({
                "time_slot": "Evening",
                "time": "19:00",
                "place": {
                    "id": evening_pick['place'].id,
                    "name": evening_pick['place'].name,
                    "description": evening_pick['place'].description,
                    "image_url": evening_pick['place'].image_url,
                    "rating_avg": evening_pick['place'].rating_avg,
                    "category_id": evening_pick['place'].category_id,
                },
                "category_name": evening_pick['category'],
                "is_preferred": evening_pick['is_preferred']
            })

        itinerary[f"Day {day}"] = day_plan

    return itinerary

@router.post("/save", response_model=schemas.ItineraryResponse)
def save_itinerary(request: schemas.ItineraryCreate, db: Session = Depends(get_db)):
    try:
        new_itinerary = models.Itinerary(
            user_id=request.user_id,
            title=request.title,
            days=request.days
        )
        db.add(new_itinerary)
        db.flush()  # Get ID

        for item in request.items:
            new_item = models.ItineraryItem(
                itinerary_id=new_itinerary.id,
                day=item.day,
                time_slot=item.time_slot,
                time=item.time,
                place_id=item.place_id
            )
            db.add(new_item)
        
        db.commit()
        db.refresh(new_itinerary)
        return new_itinerary
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user/{user_id}", response_model=List[schemas.ItineraryResponse])
def get_user_itineraries(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Itinerary).filter(models.Itinerary.user_id == user_id).order_by(models.Itinerary.created_at.desc()).all()

@router.delete("/{itinerary_id}")
def delete_itinerary(itinerary_id: int, db: Session = Depends(get_db)):
    itinerary = db.query(models.Itinerary).filter(models.Itinerary.id == itinerary_id).first()
    if not itinerary:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    
    db.delete(itinerary)
    db.commit()
    return {"message": "Itinerary deleted successfully"}
