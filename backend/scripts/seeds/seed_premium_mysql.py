
import pymysql
import json

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "jojo2025",
    "database": "savannakhet_db",
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor
}

def update_place_16():
    try:
        conn = pymysql.connect(**db_config)
        with conn.cursor() as cursor:
            # Sample data matching the user's second image
            best_months = "Nov - Feb"
            ideal_stay = "4 - 7 days"
            daily_budget = "฿900 - ฿1,700"
            location_name = "Savannakhet (ZVK)"
            best_for = json.dumps(["Culture", "Education", "Family"])
            avoid_if = json.dumps(["No Interest in History"])
            
            sql = """
                UPDATE places 
                SET best_months = %s, 
                    ideal_stay = %s, 
                    daily_budget = %s, 
                    location_name = %s, 
                    best_for = %s, 
                    avoid_if = %s
                WHERE id = 16
            """
            cursor.execute(sql, (best_months, ideal_stay, daily_budget, location_name, best_for, avoid_if))
            
            # Also update place 7
            cursor.execute("""
                UPDATE places 
                SET best_months = %s, 
                    ideal_stay = %s, 
                    daily_budget = %s, 
                    location_name = %s, 
                    best_for = %s, 
                    avoid_if = %s
                WHERE id = 7
            """, ("Year-round", "1 - 2 hours", "₭20,000 - ₭50,000", "That Ing Hang", json.dumps(["Spirituality", "Photography"]), json.dumps(["Inappropriate Attire"])))
            
            conn.commit()
            print("Successfully updated Place 16 and Place 7 in MySQL.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    update_place_16()
