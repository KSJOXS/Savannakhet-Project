import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.database import SessionLocal
from app.models import User, Place, InteractionLog, Category

db = SessionLocal()

# Check: How many cafe places exist vs total places?
total_places = db.query(Place).count()
cafe_places = db.query(Place).join(Category).filter(Category.parent_type == 'cafe').count()
print(f'Total places: {total_places}')
print(f'Cafe places: {cafe_places}')
print(f'Cafe ratio: {cafe_places}/{total_places} = {cafe_places/total_places*100:.1f}%')

# Check: dee's interactions - are they ONLY with cafe places?
dee = db.query(User).filter(User.username == 'dee').first()
logs = db.query(InteractionLog).filter(InteractionLog.user_id == dee.id).all()
print(f'\nDee has {len(logs)} interaction logs')

# Check: how many of these edges point to cafe?
dee_place_ids = set()
for log in logs:
    dee_place_ids.add(log.place_id)
print(f'Dee interacted with {len(dee_place_ids)} unique places')
for pid in dee_place_ids:
    p = db.query(Place).filter(Place.id == pid).first()
    c = p.category
    print(f'  Place ID {pid}: {p.name} -> {c.parent_type if c else "no cat"}')

# CRITICAL: Check if GNN is filtering already-interacted places
print('\n=== CRITICAL CHECK: Are cafe places already interacted? ===')
all_cafe_places = db.query(Place).join(Category).filter(Category.parent_type == 'cafe').all()
for cp in all_cafe_places:
    is_interacted = cp.id in dee_place_ids
    print(f'  {cp.name} (ID={cp.id}) -> Already interacted: {is_interacted}')

# Check: Does the demo exclude already-interacted places?
print('\n=== ANSWER: The demo does NOT exclude already-interacted places ===')
print('The demo recommends from ALL places including already-liked ones.')
print('But the real issue is: GNN message passing aggregates neighbors.')
print('With only 10 logs all to cafe, why does it recommend non-cafe?')

# Let's check other users' interactions - are other users interacting with the same cafe places?
print('\n=== OTHER USERS interacting with same cafe places as dee ===')
for pid in dee_place_ids:
    p = db.query(Place).filter(Place.id == pid).first()
    other_logs = db.query(InteractionLog).filter(
        InteractionLog.place_id == pid,
        InteractionLog.user_id != dee.id
    ).all()
    if other_logs:
        other_users = set()
        for ol in other_logs:
            u = db.query(User).filter(User.id == ol.user_id).first()
            other_users.add(u.username if u else str(ol.user_id))
        print(f'  {p.name}: also interacted by {other_users}')
    else:
        print(f'  {p.name}: NO other users interacted!')

# Check what jo and big (heavy users) interacted with
print('\n=== JO interactions summary ===')
jo = db.query(User).filter(User.username == 'jo').first()
jo_logs = db.query(InteractionLog).filter(InteractionLog.user_id == jo.id).all()
jo_cats = {}
for log in jo_logs:
    p = db.query(Place).filter(Place.id == log.place_id).first()
    c = p.category if p else None
    pt = c.parent_type if c else 'unknown'
    jo_cats[pt] = jo_cats.get(pt, 0) + 1
print(f'Jo categories: {jo_cats}')

print('\n=== BIG interactions summary ===')
big = db.query(User).filter(User.username == 'big').first()
big_logs = db.query(InteractionLog).filter(InteractionLog.user_id == big.id).all()
big_cats = {}
for log in big_logs:
    p = db.query(Place).filter(Place.id == log.place_id).first()
    c = p.category if p else None
    pt = c.parent_type if c else 'unknown'
    big_cats[pt] = big_cats.get(pt, 0) + 1
print(f'Big categories: {big_cats}')

db.close()
