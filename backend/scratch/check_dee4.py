import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.database import SessionLocal
from app.models import User, Place, InteractionLog, Category

db = SessionLocal()

dee = db.query(User).filter(User.username == 'dee').first()
print(f"=== USER DEE (id={dee.id}) ===")
print(f"Preferences: {dee.preferences}")

# All cafe places
print(f"\n=== ALL CAFE PLACES ===")
cafe_places = db.query(Place).join(Category).filter(Category.parent_type == 'cafe').all()
for p in cafe_places:
    print(f"  ID={p.id} | {p.name} | cat={p.category.name}")

# Dee's interaction logs
print(f"\n=== DEE's INTERACTION LOGS ===")
logs = db.query(InteractionLog).filter(InteractionLog.user_id == dee.id).order_by(InteractionLog.created_at.desc()).all()
for log in logs:
    p = db.query(Place).filter(Place.id == log.place_id).first()
    cat = p.category if p else None
    print(f"  Place: {p.name if p else '?'} (ID={log.place_id}) | Action: {log.action_type} | Weight: {log.interaction_weight} | Cat: {cat.parent_type if cat else '?'} | Time: {log.created_at}")

# Dee's interacted place IDs
interacted_ids = set(log.place_id for log in logs)
print(f"\n=== DEE's INTERACTED PLACE IDs ===")
print(f"  {interacted_ids}")

# Which cafe places has dee NOT interacted with?
print(f"\n=== CAFE PLACES DEE HAS NOT INTERACTED WITH ===")
for p in cafe_places:
    if p.id not in interacted_ids:
        print(f"  ID={p.id} | {p.name} (NEW!)")
    else:
        print(f"  ID={p.id} | {p.name} (already visited)")

db.close()
