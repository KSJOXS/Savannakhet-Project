from app.models import Place, User
from app.database import SessionLocal
import sys
import os
import random
sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../')))


def reassign_owners():
    db = SessionLocal()
    try:
        # Get all non-admin users
        regular_users = db.query(User).filter(User.role != 'admin').all()
        if not regular_users:
            print("No regular users found!")
            return

        print(f"Found {len(regular_users)} regular users to assign from.")

        # Get all pending places (currently owned by admin/jame or NULL)
        places = db.query(Place).filter(Place.status == 'pending').all()

        for place in places:
            # Assign a random regular user as owner
            chosen_user = random.choice(regular_users)
            print(f"  {place.name[:35]:35s} -> {chosen_user.username}")
            place.owner_id = chosen_user.id

        db.commit()
        print(
            f"\nSuccessfully reassigned {len(places)} places to random regular users.")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    reassign_owners()
