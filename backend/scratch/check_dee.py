import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.database import SessionLocal
from app.models import User, Place, InteractionLog, Favorite, Category, Interaction

db = SessionLocal()

# 1. Check user dee
dee = db.query(User).filter(User.username == 'dee').first()
if dee:
    print(f'=== USER DEE ===')
    print(f'ID: {dee.id}')
    print(f'Preferences: {dee.preferences}')
    print(f'Type of preferences: {type(dee.preferences)}')
    
    # 2. Check dee's interaction_logs
    logs = db.query(InteractionLog).filter(InteractionLog.user_id == dee.id).all()
    print(f'\n=== INTERACTION LOGS ({len(logs)}) ===')
    for log in logs:
        place = db.query(Place).filter(Place.id == log.place_id).first()
        cat = place.category if place else None
        cat_info = f'{cat.name} (parent_type={cat.parent_type})' if cat else 'No category'
        print(f'  Place: {place.name if place else "?"} | Action: {log.action_type} | Weight: {log.interaction_weight} | Category: {cat_info}')
    
    # 3. Check dee's favorites
    favs = db.query(Favorite).filter(Favorite.user_id == dee.id).all()
    print(f'\n=== FAVORITES ({len(favs)}) ===')
    for fav in favs:
        place = db.query(Place).filter(Place.id == fav.place_id).first()
        cat = place.category if place else None
        cat_info = f'{cat.name} (parent_type={cat.parent_type})' if cat else 'No category'
        print(f'  Place: {place.name if place else "?"} | Category: {cat_info}')
    
    # 4. Check dee's reviews/interactions
    reviews = db.query(Interaction).filter(Interaction.user_id == dee.id).all()
    print(f'\n=== REVIEWS ({len(reviews)}) ===')
    for r in reviews:
        place = db.query(Place).filter(Place.id == r.place_id).first()
        cat = place.category if place else None
        cat_info = f'{cat.name} (parent_type={cat.parent_type})' if cat else 'No category'
        print(f'  Place: {place.name if place else "?"} | Rating: {r.rating} | Category: {cat_info}')

else:
    print('User dee not found!')

# 5. Check all categories
print(f'\n=== ALL CATEGORIES ===')
cats = db.query(Category).all()
for c in cats:
    print(f'  ID: {c.id} | Name: {c.name} | parent_type: {c.parent_type}')

# 6. Check places that were recommended
print(f'\n=== RECOMMENDED PLACES CHECK ===')
for name in ['Savan-VEDC Monument', 'Dong Tao', 'Talat Yen (Night Market)', "Pilgrim's Kitchen & Inn", 'Dao hung 1', 'laos chaluen']:
    place = db.query(Place).filter(Place.name == name).first()
    if place:
        cat = place.category if place else None
        cat_info = f'{cat.name} (parent_type={cat.parent_type})' if cat else 'No category'
        print(f'  {place.name} | cat: {cat_info} | rating: {place.rating_avg}')

# 7. Check cafe places
print(f'\n=== CAFE PLACES ===')
cafe_cats = db.query(Category).filter(Category.parent_type == 'cafe').all()
for cc in cafe_cats:
    places = db.query(Place).filter(Place.category_id == cc.id).all()
    for p in places:
        print(f'  {p.name} | cat: {cc.name} (parent_type={cc.parent_type}) | rating: {p.rating_avg}')

# 8. Check all interaction_logs summary
print(f'\n=== ALL INTERACTION LOGS SUMMARY ===')
all_logs = db.query(InteractionLog).all()
print(f'Total logs: {len(all_logs)}')
user_ids = set(l.user_id for l in all_logs)
print(f'Unique users with logs: {user_ids}')
for uid in user_ids:
    u = db.query(User).filter(User.id == uid).first()
    count = len([l for l in all_logs if l.user_id == uid])
    print(f'  User: {u.username if u else uid} (id={uid}) -> {count} logs')

db.close()
