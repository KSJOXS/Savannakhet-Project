from sqlalchemy import create_engine, text
import sys
import os

# Add the project root to sys.path
sys.path.append(os.getcwd())

from app.database import SQLALCHEMY_DATABASE_URL

def migrate():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    with engine.connect() as connection:
        print("Checking for booking_url and agoda_url columns in places table...")
        
        # Check if booking_url exists
        result = connection.execute(text("SHOW COLUMNS FROM places LIKE 'booking_url'"))
        if not result.fetchone():
            print("Adding booking_url column...")
            connection.execute(text("ALTER TABLE places ADD COLUMN booking_url VARCHAR(500) AFTER avoid_if"))
            connection.commit()
        else:
            print("booking_url column already exists.")

        # Check if agoda_url exists
        result = connection.execute(text("SHOW COLUMNS FROM places LIKE 'agoda_url'"))
        if not result.fetchone():
            print("Adding agoda_url column...")
            connection.execute(text("ALTER TABLE places ADD COLUMN agoda_url VARCHAR(500) AFTER booking_url"))
            connection.commit()
        else:
            print("agoda_url column already exists.")
            
        print("Migration completed successfully!")

if __name__ == "__main__":
    migrate()
