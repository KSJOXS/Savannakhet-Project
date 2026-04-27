from sqlalchemy import text
from app.database import engine

def migrate():
    with engine.connect() as conn:
        print("Adding 'owner_id' column...")
        try:
            conn.execute(text("ALTER TABLE places ADD COLUMN owner_id INT;"))
            conn.execute(text("ALTER TABLE places ADD CONSTRAINT fk_places_owner FOREIGN KEY (owner_id) REFERENCES users(id);"))
            print("Successfully added 'owner_id'.")
        except Exception as e:
            print(f"'owner_id' might already exist or error: {e}")

        print("Adding 'status' column...")
        try:
            conn.execute(text("ALTER TABLE places ADD COLUMN status VARCHAR(20) DEFAULT 'pending';"))
            print("Successfully added 'status'.")
        except Exception as e:
            print(f"'status' might already exist or error: {e}")

        print("Setting existing places to 'approved'...")
        try:
            conn.execute(text("UPDATE places SET status = 'approved' WHERE status IS NULL OR status = 'pending';"))
            conn.commit()
            print("Successfully updated existing places.")
        except Exception as e:
            print(f"Error updating existing places: {e}")

if __name__ == "__main__":
    migrate()
    print("Migration complete!")
