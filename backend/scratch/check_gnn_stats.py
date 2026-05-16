from app.database import SessionLocal
from app.models import InteractionLog, Place, Category

def check_stats():
    db = SessionLocal()
    logs = db.query(InteractionLog).all()
    counts = {}
    for l in logs:
        p = db.query(Place).filter(Place.id == l.place_id).first()
        if p:
            c = db.query(Category).filter(Category.id == p.category_id).first()
            if c:
                pt = c.parent_type
                counts[pt] = counts.get(pt, 0) + 1
    print(f"Total Logs: {len(logs)}")
    print("Category Distribution in Logs:")
    for pt, count in counts.items():
        print(f" - {pt}: {count}")
    db.close()

if __name__ == "__main__":
    check_stats()
