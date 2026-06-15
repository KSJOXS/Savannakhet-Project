
import sqlite3
import json

db_path = 'backend/app.db'


def update_place_16():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Sample data matching the user's second image
    best_months = "Nov - Feb"
    ideal_stay = "4 - 7 days"
    daily_budget = "฿900 - ฿1,700"
    location_name = "Savannakhet (ZVK)"
    best_for = json.dumps(["Culture", "Education", "Family"])
    avoid_if = json.dumps(["No Interest in History"])

    cursor.execute("""
        UPDATE places 
        SET best_months = ?, 
            ideal_stay = ?, 
            daily_budget = ?, 
            location_name = ?, 
            best_for = ?, 
            avoid_if = ?
        WHERE id = 16
    """, (best_months, ideal_stay, daily_budget, location_name, best_for, avoid_if))

    # Also update place 7 (That Ing Hang) for more variety
    cursor.execute("""
        UPDATE places 
        SET best_months = "Year-round", 
            ideal_stay = "1 - 2 hours", 
            daily_budget = "₭20,000 - ₭50,000", 
            location_name = "That Ing Hang", 
            best_for = ?, 
            avoid_if = ?
        WHERE id = 7
    """, (json.dumps(["Spirituality", "Photography"]), json.dumps(["Inappropriate Attire"])))

    conn.commit()
    conn.close()
    print("Updated Place 16 and Place 7 with premium details.")


if __name__ == "__main__":
    update_place_16()
