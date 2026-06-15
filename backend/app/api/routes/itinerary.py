from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.database import get_db
from app import models, schemas
import random
import json
import re


def parse_budget_to_thb(budget_str):
    if not budget_str:
        return 0
    numbers = [int(n.replace(',', ''))
               for n in re.findall(r'\d+[,]?\d*', budget_str)]
    if not numbers:
        return 0
    avg_val = sum(numbers) / len(numbers)
    budget_upper = budget_str.upper()
    if '₭' in budget_upper or 'KIP' in budget_upper or 'LAK' in budget_upper:
        return avg_val / 600
    elif '$' in budget_upper or 'USD' in budget_upper:
        return avg_val * 35
    else:
        return avg_val


def get_budget_tier(budget_str):
    thb = parse_budget_to_thb(budget_str)
    if thb == 0:
        return 'any'
    if thb < 500:
        return 'low'
    elif thb <= 2000:
        return 'moderate'
    else:
        return 'luxury'


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


def get_season_boosts(month: int):
    if not month:
        return []
    if month in [11, 12, 1, 2]:  # Cool & Dry
        return ['nature', 'landmark']
    elif month in [3, 4, 5]:  # Hot
        return ['cafe', 'nightlife', 'chill', 'restaurant']
    elif month in [6, 7, 8, 9, 10]:  # Rainy
        return ['cafe', 'culture', 'shopping']
    return []


@router.post("/generate", response_model=Dict[str, List[Dict[str, Any]]])
def generate_itinerary(request: schemas.ItineraryRequest, db: Session = Depends(get_db)):
    user_prefs = request.preferences or []

    if not user_prefs and request.user_id:
        user = db.query(models.User).filter(
            models.User.id == request.user_id).first()
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

    season_boosts = get_season_boosts(request.month)

    for place, cat in places_query:
        ptype = cat.parent_type
        # Add slight boost if it matches user preference
        is_preferred = ptype in user_prefs
        season_boost = ptype in season_boosts

        place_data = {
            "place": place,
            "category": cat.name,
            "parent_type": ptype,
            "is_preferred": is_preferred,
            "season_boost": season_boost,
            "budget_match": request.budget == get_budget_tier(place.daily_budget) if request.budget and request.budget != 'any' else True,
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
        return sorted(spots, key=lambda x: (x['budget_match'], x['is_preferred'], x['season_boost'], x['rating'] + random.uniform(-1.0, 1.0)), reverse=True)

    morning_spots = sort_spots(morning_spots)
    afternoon_spots = sort_spots(afternoon_spots)
    evening_spots = sort_spots(evening_spots)

    itinerary = {}
    used_place_ids = set()

    for day in range(1, request.days + 1):
        day_plan = []

        # 1. Select Morning Spot
        morning_pick = next(
            (s for s in morning_spots if s['place'].id not in used_place_ids), None)
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
                    # new add best months to show on place trip
                    "best_months": morning_pick['place'].best_months,
                },
                "category_name": morning_pick['category'],
                "is_preferred": morning_pick['is_preferred'],
                "season_boost": morning_pick['season_boost']
            })

        # 2. Select Afternoon Spot
        afternoon_pick = next(
            (s for s in afternoon_spots if s['place'].id not in used_place_ids), None)
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
                    "best_months": afternoon_pick['place'].best_months,
                },
                "category_name": afternoon_pick['category'],
                "is_preferred": afternoon_pick['is_preferred'],
                "season_boost": afternoon_pick['season_boost']
            })

        # 3. Select Evening Spot
        evening_pick = next(
            (s for s in evening_spots if s['place'].id not in used_place_ids), None)
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
                    "best_months": evening_pick['place'].best_months,
                },
                "category_name": evening_pick['category'],
                "is_preferred": evening_pick['is_preferred'],
                "season_boost": evening_pick['season_boost']
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
    itinerary = db.query(models.Itinerary).filter(
        models.Itinerary.id == itinerary_id).first()
    if not itinerary:
        raise HTTPException(status_code=404, detail="Itinerary not found")

    db.delete(itinerary)
    db.commit()
    return {"message": "Itinerary deleted successfully"}


@router.post("/swap", response_model=Dict[str, Any])
def swap_itinerary_place(request: schemas.SwapPlaceRequest, db: Session = Depends(get_db)):
    user_prefs = request.preferences or []
    season_boosts = get_season_boosts(request.month)

    # Fetch all active places with their categories
    places_query = db.query(models.Place, models.Category).join(
        models.Category, models.Place.category_id == models.Category.id
    ).filter(models.Place.status == "approved").all()

    candidates = []

    for place, cat in places_query:
        # Skip if it's already used or it's the current place
        if place.id in request.used_place_ids or (request.current_place_id is not None and place.id == request.current_place_id):
            continue

        ptype = cat.parent_type

        # Check if it fits the time slot
        if request.time_slot == "Morning" and ptype not in ['nature', 'culture', 'landmark']:
            continue
        if request.time_slot == "Afternoon" and ptype not in ['cafe', 'landmark', 'culture', 'shopping']:
            continue
        if request.time_slot == "Evening" and ptype not in ['local_food', 'restaurant', 'chill', 'nightlife']:
            continue

        is_preferred = ptype in user_prefs
        season_boost = ptype in season_boosts

        candidates.append({
            "place": place,
            "category_name": cat.name,
            "is_preferred": is_preferred,
            "season_boost": season_boost,
            "budget_match": request.budget == get_budget_tier(place.daily_budget) if request.budget and request.budget != 'any' else True,
            "rating": float(place.rating_avg or 0.0)
        })

    if not candidates:
        raise HTTPException(
            status_code=404, detail="No suitable alternative places found")

    random.shuffle(candidates)
    candidates.sort(key=lambda x: (x['budget_match'], x['is_preferred'],
                    x['season_boost'], x['rating'] + random.uniform(-1.0, 1.0)), reverse=True)

    best_match = candidates[0]

    time_map = {"Morning": "09:00", "Afternoon": "14:00", "Evening": "19:00"}

    return {
        "time_slot": request.time_slot,
        "time": time_map.get(request.time_slot, "12:00"),
        "place": {
            "id": best_match['place'].id,
            "name": best_match['place'].name,
            "description": best_match['place'].description,
            "image_url": best_match['place'].image_url,
            "rating_avg": best_match['place'].rating_avg,
            "category_id": best_match['place'].category_id,
            "best_months": best_match['place'].best_months,
        },
        "category_name": best_match['category_name'],
        "is_preferred": best_match['is_preferred']
    }
