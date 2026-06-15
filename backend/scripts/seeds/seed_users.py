import sys
import os
import random
import string

# Ensure we can import app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from app.database import SessionLocal
from app.models import User
from app.core.security import get_password_hash

def generate_random_string(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def seed_users(count=30):
    db = SessionLocal()
    try:
        users_added = 0
        for i in range(count):
            # Generate a random username and email to avoid collisions
            rand_str = generate_random_string(5)
            username = f"user_{rand_str}_{i}"
            email = f"{username}@example.com"
            password = "password123" # Default password for seed users
            
            existing_user = db.query(User).filter(User.username == username).first()
            if not existing_user:
                new_user = User(
                    username=username,
                    email=email,
                    password_hash=get_password_hash(password),
                    role="user",
                    preferences=["culture", "nature", "food"],
                    post_permission_status="approved"
                )
                db.add(new_user)
                users_added += 1
                print(f"Added user: {username} | Email: {email} | Password: {password}")
            
        db.commit()
        print(f"Successfully added {users_added} users.")
    except Exception as e:
        print(f"Error seeding users: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_users(30)
