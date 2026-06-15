from sqlalchemy import text
from app.database import engine
import sys
import os
sys.path.append(os.getcwd())


def run_update():
    with engine.connect() as con:
        print("Updating categories...")
        # Culture
        con.execute(text("UPDATE categories SET parent_type = 'culture' WHERE name LIKE '%temple%' OR name LIKE '%museum%' OR name LIKE '%landmark%' OR name LIKE '%culture%' OR name LIKE '%ประวัติศาสตร์%' OR name LIKE '%วัด%' OR name LIKE '%พิพิธภัณฑ์%' OR name LIKE '%monument%' OR name LIKE '%building%'"))
        # Shopping
        con.execute(text("UPDATE categories SET parent_type = 'shopping' WHERE name LIKE '%market%' OR name LIKE '%shop%' OR name LIKE '%mall%' OR name LIKE '%ตลาด%' OR name LIKE '%ห้าง%'"))
        # Nightlife
        con.execute(text("UPDATE categories SET parent_type = 'nightlife' WHERE name LIKE '%bar%' OR name LIKE '%pub%' OR name LIKE '%night%' OR name LIKE '%club%' OR name LIKE '%เหล้า%' OR name LIKE '%บาร์%'"))
        con.commit()
        print("Success!")


if __name__ == "__main__":
    run_update()
