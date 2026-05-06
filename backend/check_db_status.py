from app.database import engine
from sqlalchemy import text
import json

def check():
    with engine.connect() as con:
        # 1. Check Categories
        print("--- Categories ---")
        res = con.execute(text("SELECT id, name, parent_type FROM categories"))
        rows = res.fetchall()
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Parent: {row[2]}")
            
        # 2. Check Places count by parent_type
        print("\n--- Place Counts by Parent Type ---")
        res = con.execute(text("""
            SELECT c.parent_type, COUNT(p.id) 
            FROM places p 
            JOIN categories c ON p.category_id = c.id 
            WHERE p.status = 'approved' AND p.is_published = 1
            GROUP BY c.parent_type
        """))
        for row in res.fetchall():
            print(f"{row[0]}: {row[1]}")

        # 3. List some restaurants if any
        print("\n--- Approved Restaurants (first 5) ---")
        res = con.execute(text("""
            SELECT p.id, p.name, c.name, c.parent_type
            FROM places p
            JOIN categories c ON p.category_id = c.id
            WHERE c.parent_type IN ('restaurant', 'cafe', 'local_food')
            AND p.status = 'approved' AND p.is_published = 1
            LIMIT 5
        """))
        for row in res.fetchall():
            print(f"ID: {row[0]}, Name: {row[1]}, Cat: {row[2]}, Parent: {row[3]}")

if __name__ == "__main__":
    try:
        check()
    except Exception as e:
        print(f"Error: {e}")
