from sqlalchemy import text
from app.database import engine

def migrate():
    with engine.connect() as conn:
        print("Adding 'post_permission_status' column to users...")
        try:
            conn.execute(text("ALTER TABLE users ADD COLUMN post_permission_status VARCHAR(20) DEFAULT 'none';"))
            conn.commit()
            print("Successfully added 'post_permission_status'.")
        except Exception as e:
            print(f"Error adding column (might already exist): {e}")

if __name__ == "__main__":
    migrate()
