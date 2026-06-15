from app.models import Place, User
from app.database import SessionLocal
import sys
sys.path.append('.')

db = SessionLocal()
places = db.query(Place).filter(Place.status == 'pending').all()
for p in places:
    owner = db.query(User).filter(
        User.id == p.owner_id).first() if p.owner_id else None
    username = owner.username if owner else "NULL"
    print(
        f"Place: {p.name[:30]:30s} | owner_id: {str(p.owner_id):5s} | username: {username}")
db.close()
