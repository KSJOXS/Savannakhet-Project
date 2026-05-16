from app.database import SessionLocal
from app.models import User, InteractionLog, Place, Category
from app.core.security import get_password_hash
import json
import os
import subprocess

def setup_and_test():
    db = SessionLocal()
    try:
        # 1. Create a clean user 'test_ai'
        existing = db.query(User).filter(User.username == 'test_ai').first()
        if existing:
            db.query(InteractionLog).filter(InteractionLog.user_id == existing.id).delete()
            db.delete(existing)
            db.commit()
            print("Cleaned up old test_ai user.")

        u = User(
            username='test_ai',
            email='test_ai@example.com',
            password_hash=get_password_hash('password123'),
            preferences=json.dumps(['nature']),
            role='user'
        )
        db.add(u)
        db.commit()
        db.refresh(u)
        print(f"Created user 'test_ai' with preference: Nature")

        # 2. Simulate interactions with Nature places
        # Find some nature places
        nature_places = db.query(Place).join(Category).filter(Category.parent_type == 'nature').all()
        if not nature_places:
            print("No nature places found in DB!")
            return

        print(f"Logging 5 views on nature places for 'test_ai'...")
        for p in nature_places[:3]:
            log = InteractionLog(
                user_id=u.id,
                place_id=p.id,
                action_type='view',
                interaction_weight=1.0
            )
            db.add(log)
        
        # Add one LIKE to a nature place (Weight 5.0)
        like_log = InteractionLog(
            user_id=u.id,
            place_id=nature_places[0].id,
            action_type='like',
            interaction_weight=5.0
        )
        db.add(like_log)
        
        db.commit()
        print("Data seeded successfully.")

    finally:
        db.close()

    # 3. Modify demo_gnn.py temporarily to test this user
    # (Actually I'll just run it with an argument or similar if possible, 
    # but I'll just edit it to use 'test_ai')
    demo_path = os.path.join(os.getcwd(), 'ai_demo', 'demo_gnn.py')
    with open(demo_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content.replace('filter(User.username == "how")', 'filter(User.username == "test_ai")')
    
    with open(demo_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("\n--- RUNNING GNN DEMO FOR test_ai ---")
    result = subprocess.run(['..\\.venv\\Scripts\\python.exe', 'ai_demo/demo_gnn.py'], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)

if __name__ == "__main__":
    setup_and_test()
