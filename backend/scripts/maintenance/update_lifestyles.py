from sqlalchemy import text
from app.database import engine
import os
import sys
sys.path.append(os.getcwd())


def update_lifestyles():
    with engine.connect() as con:
        print("Updating categories for new lifestyle mapping...")

        # 1. ธรรมชาติ & ภูเขา (nature)
        con.execute(text("UPDATE categories SET parent_type = 'nature' WHERE name LIKE '%nature%' OR name LIKE '%park%' OR name LIKE '%ภูเขา%' OR name LIKE '%ป่า%' OR name LIKE '%น้ำตก%'"))

        # 2. วัด & ประวัติศาสตร์ (culture)
        con.execute(text("UPDATE categories SET parent_type = 'culture' WHERE name LIKE '%temple%' OR name LIKE '%pagoda%' OR name LIKE '%museum%' OR name LIKE '%ประวัติศาสตร์%' OR name LIKE '%วัด%'"))

        # 3. คาเฟ่ & ของหวาน (cafe)
        con.execute(text("UPDATE categories SET parent_type = 'cafe' WHERE name LIKE '%coffee%' OR name LIKE '%tea%' OR name LIKE '%cafe%' OR name LIKE '%คาเฟ่%' OR name LIKE '%เบเกอรี่%'"))

        # 4. อาหารท้องถิ่น (local_food)
        # Note: We include restaurants and food, but not cafe
        con.execute(text("UPDATE categories SET parent_type = 'local_food' WHERE name LIKE '%restaurant%' OR name LIKE '%food%' OR name LIKE '%market%' OR name LIKE '%อาหาร%' OR name LIKE '%ตลาด%'"))

        # 5. จุดถ่ายรูปสวย (landmark)
        con.execute(text("UPDATE categories SET parent_type = 'landmark' WHERE name LIKE '%monument%' OR name LIKE '%colonial%' OR name LIKE '%landmark%' OR name LIKE '%street art%'"))

        # 6. เดินเล่นชิลๆ (chill)
        # Includes bars, pubs, or generic chill spots
        con.execute(text("UPDATE categories SET parent_type = 'chill' WHERE name LIKE '%bar%' OR name LIKE '%pub%' OR name LIKE '%night%' OR name LIKE '%chill%' OR name LIKE '%เดินเล่น%'"))

        con.commit()
        print("Categories successfully updated!")


if __name__ == "__main__":
    update_lifestyles()
