from sqlalchemy import text
from app.database import engine

def migrate():
    with engine.connect() as con:
        # 1. Add column if it doesn't exist
        print("Checking/Adding parent_type column...")
        try:
            con.execute(text("ALTER TABLE categories ADD COLUMN parent_type VARCHAR(50) DEFAULT 'other'"))
            con.commit()
            print("Column added successfully.")
        except Exception as e:
            if "Duplicate column name" in str(e):
                print("Column already exists.")
            else:
                print(f"Error adding column: {e}")

        # 2. Update existing data to make it look nice
        print("Updating existing categories...")
        # Nature
        con.execute(text("UPDATE categories SET parent_type = 'nature' WHERE name LIKE '%nature%' OR name LIKE '%waterfall%' OR name LIKE '%cave%' OR name LIKE '%forest%' OR name LIKE '%ธรรมชาติ%'"))
        # Restaurant
        con.execute(text("UPDATE categories SET parent_type = 'restaurant' WHERE name LIKE '%restaurant%' OR name LIKE '%cafe%' OR name LIKE '%coffee%' OR name LIKE '%food%' OR name LIKE '%ร้านอาหาร%' OR name LIKE '%คาเฟ่%'"))
        # Hotel
        con.execute(text("UPDATE categories SET parent_type = 'hotel' WHERE name LIKE '%hotel%' OR name LIKE '%resort%' OR name LIKE '%ที่พัก%' OR name LIKE '%โรงแรม%'"))
        
        con.commit()
        print("Data update complete.")

if __name__ == "__main__":
    migrate()
