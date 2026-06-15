# seed_hotels.py - เพิ่มข้อมูลโรงแรม 20 แห่ง สำหรับแขวงสะหวันนะเขต
from app.models import Place
from app.database import SessionLocal
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


HOTEL_CATEGORY_ID = 11  # Hotel & Resort

hotels = [
    {
        "name": "Daosavanh Resort & Spa",
        "description": "โรงแรมระดับ 4 ดาว ตั้งอยู่ริมแม่น้ำโขง มีสปาและสระว่ายน้ำกลางแจ้ง วิวแม่น้ำสวยงาม เหมาะสำหรับคู่รักและครอบครัว",
        "location_lat": 16.5500, "location_lng": 104.7600,
        "best_months": "Nov - Feb", "ideal_stay": "2-3 nights", "daily_budget": "₭ 300,000 - 600,000",
        "location_name": "River Road, Savannakhet",
        "best_for": ["Couples", "Families", "Business Travelers"],
        "avoid_if": ["Budget travelers"],
        "booking_url": "https://www.booking.com/hotel/la/daosavanh-resort-spa.html",
        "agoda_url": "https://www.agoda.com/daosavanh-resort-spa",
        "rating_avg": 4.5,
        "opening_hours": {
            "mon": {"open": "00:00", "close": "23:59", "closed": False},
            "tue": {"open": "00:00", "close": "23:59", "closed": False},
            "wed": {"open": "00:00", "close": "23:59", "closed": False},
            "thu": {"open": "00:00", "close": "23:59", "closed": False},
            "fri": {"open": "00:00", "close": "23:59", "closed": False},
            "sat": {"open": "00:00", "close": "23:59", "closed": False},
            "sun": {"open": "00:00", "close": "23:59", "closed": False},
        },
        "image_url": json.dumps([
            "/static/places/Daosavanh-_Resort_Spa-_Hotel_Savanakhet.jpg",
            "/static/places/daosavanh-resort-spa.jpg",
        ]),
    },
    {
        "name": "Leena Guesthouse",
        "description": "เกสต์เฮ้าส์บรรยากาศอบอุ่น ราคาประหยัด ตั้งอยู่ใจกลางเมืองสะหวันนะเขต เดินไปสถานที่ท่องเที่ยวได้สะดวก",
        "location_lat": 16.5520, "location_lng": 104.7620,
        "best_months": "Year-round", "ideal_stay": "1-2 nights", "daily_budget": "₭ 80,000 - 150,000",
        "location_name": "City Center, Savannakhet",
        "best_for": ["Backpackers", "Solo Travelers", "Budget Travelers"],
        "avoid_if": ["Those needing luxury amenities"],
        "booking_url": None, "agoda_url": None,
        "rating_avg": 4.0,
        "opening_hours": {k: {"open": "00:00", "close": "23:59", "closed": False} for k in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]},
        "image_url": json.dumps(["/static/places/R.jpg"]),
    },
    {
        "name": "Phonevilay Hotel",
        "description": "โรงแรมสไตล์โมเดิร์น มีห้องพักสะอาดสบาย บริการอาหารเช้า พร้อมที่จอดรถฟรี ตั้งอยู่ใกล้ตลาดสด",
        "location_lat": 16.5545, "location_lng": 104.7585,
        "best_months": "Year-round", "ideal_stay": "1-3 nights", "daily_budget": "₭ 150,000 - 280,000",
        "location_name": "Market Area, Savannakhet",
        "best_for": ["Families", "Business Travelers"],
        "avoid_if": ["Party seekers"],
        "booking_url": None, "agoda_url": None,
        "rating_avg": 3.8,
        "opening_hours": {k: {"open": "00:00", "close": "23:59", "closed": False} for k in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]},
        "image_url": json.dumps(["/static/places/sl-2.jpg"]),
    },
    {
        "name": "Savannakhet Eco Lodge",
        "description": "ที่พักสไตล์อีโคที่แวดล้อมด้วยธรรมชาติ เหมาะสำหรับนักท่องเที่ยวที่รักธรรมชาติ มีกิจกรรม birdwatching และ jungle trek",
        "location_lat": 16.5200, "location_lng": 104.7900,
        "best_months": "Oct - Apr", "ideal_stay": "2-4 nights", "daily_budget": "₭ 200,000 - 400,000",
        "location_name": "Outskirts, Savannakhet",
        "best_for": ["Nature Lovers", "Eco Travelers", "Adventure Seekers"],
        "avoid_if": ["City-center seekers", "Luxury travelers"],
        "booking_url": None, "agoda_url": None,
        "rating_avg": 4.3,
        "opening_hours": {k: {"open": "00:00", "close": "23:59", "closed": False} for k in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]},
        "image_url": json.dumps(["/static/places/sl-3.jpg"]),
    },
    {
        "name": "Mekong Hotel Savannakhet",
        "description": "โรงแรมริมโขงที่มีวิวสวยงาม ห้องพักกว้างขวาง มีร้านอาหารที่เสิร์ฟอาหารลาวแท้ ติดกับท่าเรือข้ามฟาก",
        "location_lat": 16.5510, "location_lng": 104.7560,
        "best_months": "Nov - Mar", "ideal_stay": "2-3 nights", "daily_budget": "₭ 200,000 - 350,000",
        "location_name": "Mekong Riverside, Savannakhet",
        "best_for": ["Couples", "Families", "River View Lovers"],
        "avoid_if": ["Those sensitive to noise from the port"],
        "booking_url": None, "agoda_url": None,
        "rating_avg": 4.1,
        "opening_hours": {k: {"open": "00:00", "close": "23:59", "closed": False} for k in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]},
        "image_url": json.dumps(["/static/places/thumb-0.jpg"]),
    },
    {
        "name": "Inthira Savannakhet Hotel",
        "description": "โรงแรมบูทีคสไตล์โคโลเนียลฝรั่งเศส ตั้งอยู่ในย่านเมืองเก่า มีการตกแต่งที่งดงาม เหมาะสำหรับผู้ที่ชื่นชอบประวัติศาสตร์",
        "location_lat": 16.5530, "location_lng": 104.7610,
        "best_months": "Nov - Feb", "ideal_stay": "2-3 nights", "daily_budget": "₭ 350,000 - 550,000",
        "location_name": "Old Town Quarter, Savannakhet",
        "best_for": ["History Buffs", "Culture Lovers", "Couples"],
        "avoid_if": ["Budget travelers"],
        "booking_url": "https://www.booking.com/hotel/la/inthira-savannakhet.html",
        "agoda_url": None,
        "rating_avg": 4.6,
        "opening_hours": {k: {"open": "00:00", "close": "23:59", "closed": False} for k in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]},
        "image_url": json.dumps([
            "/static/places/laos-savannakhet-former-lao-chaleun-complex-built-in-the-1960s-included-a-cinema-bars-and-dance-floors-3AB01C6.jpg",
        ]),
    },
    {
        "name": "Hoongthip Hotel",
        "description": "โรงแรมราคากลางๆ บริการดี อาหารเช้าอร่อย มีสระว่ายน้ำ เหมาะสำหรับครอบครัวที่มาพักระยะสั้น",
        "location_lat": 16.5490, "location_lng": 104.7630,
        "best_months": "Year-round", "ideal_stay": "1-3 nights", "daily_budget": "₭ 180,000 - 320,000",
        "location_name": "Central District, Savannakhet",
        "best_for": ["Families", "Short Stays"],
        "avoid_if": ["Long-term stays"],
        "booking_url": None, "agoda_url": None,
        "rating_avg": 3.9,
        "opening_hours": {k: {"open": "00:00", "close": "23:59", "closed": False} for k in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]},
        "image_url": json.dumps(["/static/places/S__17817771-1.jpg"]),
    },
    {
        "name": "Southida Guesthouse",
        "description": "เกสต์เฮ้าส์ขนาดเล็ก บรรยากาศอบอุ่น เจ้าของใจดีและพูดภาษาอังกฤษได้ดี เหมาะสำหรับนักเดินทางเดี่ยว",
        "location_lat": 16.5535, "location_lng": 104.7595,
        "best_months": "Year-round", "ideal_stay": "1-2 nights", "daily_budget": "₭ 60,000 - 120,000",
        "location_name": "Near Bus Station, Savannakhet",
        "best_for": ["Solo Travelers", "Backpackers"],
        "avoid_if": ["Families with young children", "Luxury seekers"],
        "booking_url": None, "agoda_url": None,
        "rating_avg": 4.2,
        "opening_hours": {k: {"open": "00:00", "close": "23:59", "closed": False} for k in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]},
        "image_url": json.dumps(["/static/places/images.jpg"]),
    },
    {
        "name": "Savan Vegas Hotel & Casino",
        "description": "โรงแรมระดับ 5 ดาว พร้อมคาสิโน สปา และห้องพักหรูหรา มีสิ่งอำนวยความสะดวกครบครัน เป็นโรงแรมที่ใหญ่ที่สุดในแขวง",
        "location_lat": 16.5400, "location_lng": 104.7700,
        "best_months": "Year-round", "ideal_stay": "2-4 nights", "daily_budget": "₭ 800,000 - 2,000,000",
        "location_name": "Savan-SENO Special Economic Zone",
        "best_for": ["Luxury Travelers", "Business Travelers", "Entertainment Seekers"],
        "avoid_if": ["Budget travelers", "Families with children (casino area)"],
        "booking_url": "https://www.booking.com/hotel/la/savan-vegas.html",
        "agoda_url": "https://www.agoda.com/savan-vegas",
        "rating_avg": 4.4,
        "opening_hours": {k: {"open": "00:00", "close": "23:59", "closed": False} for k in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]},
        "image_url": json.dumps(["/static/places/DATN4.png"]),
    },
    {
        "name": "Vansana Savannakhet Hotel",
        "description": "โรงแรม 3 ดาว สะอาดและทันสมัย อยู่ใกล้สนามบิน เหมาะสำหรับนักธุรกิจที่ต้องการความสะดวกสบาย มีร้านอาหารและบาร์",
        "location_lat": 16.5560, "location_lng": 104.7550,
        "best_months": "Year-round", "ideal_stay": "1-2 nights", "daily_budget": "₭ 220,000 - 380,000",
        "location_name": "Airport Road, Savannakhet",
        "best_for": ["Business Travelers", "Short Stays"],
        "avoid_if": ["Tourists wanting city-center access"],
        "booking_url": None, "agoda_url": None,
        "rating_avg": 3.7,
        "opening_hours": {k: {"open": "00:00", "close": "23:59", "closed": False} for k in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]},
        "image_url": json.dumps(["/static/places/lao-lao-bao-savannakhet-vieng-chan-5n4d-62b433cc4c943.jpg"]),
    },
    {
        "name": "Khammouane Riverside Resort",
        "description": "รีสอร์ทริมน้ำที่มีบรรยากาศสงบ เหมาะสำหรับการพักผ่อน มีเรือล่องแม่น้ำ กิจกรรมตกปลา และอาหารทะเลน้ำจืดสด",
        "location_lat": 16.5300, "location_lng": 104.7800,
        "best_months": "Nov - Apr", "ideal_stay": "2-4 nights", "daily_budget": "₭ 250,000 - 450,000",
        "location_name": "Riverside Area, Savannakhet",
        "best_for": ["Nature Lovers", "Fishing Enthusiasts", "Families"],
        "avoid_if": ["City-center activities seekers"],
        "booking_url": None, "agoda_url": None,
        "rating_avg": 4.2,
        "opening_hours": {k: {"open": "00:00", "close": "23:59", "closed": False} for k in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]},
        "image_url": json.dumps(["/static/places/savannakhet-laos-travel-photo-20250720095434486-photo-thumb.jpg"]),
    },
    {
        "name": "Phonesavanh Hotel",
        "description": "โรงแรมท้องถิ่นราคาย่อมเยา สะอาดและปลอดภัย มีบริการซักรีด ร้านอาหาร และเช่าจักรยาน เดินทางสะดวกด้วยรถตุ๊กตุ๊ก",
        "location_lat": 16.5515, "location_lng": 104.7580,
        "best_months": "Year-round", "ideal_stay": "1-3 nights", "daily_budget": "₭ 100,000 - 200,000",
        "location_name": "Downtown Savannakhet",
        "best_for": ["Budget Travelers", "Backpackers"],
        "avoid_if": ["Business travelers needing high-speed wifi"],
        "booking_url": None, "agoda_url": None,
        "rating_avg": 3.6,
        "opening_hours": {k: {"open": "00:00", "close": "23:59", "closed": False} for k in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]},
        "image_url": json.dumps(["/static/places/caption.jpg"]),
    },
    {
        "name": "Lao Orchid Hotel",
        "description": "โรงแรมสวยงามกลางใจเมือง มีห้องพักสไตล์โมเดิร์น พร้อมระเบียงส่วนตัว ใกล้ศูนย์การค้าและร้านอาหาร",
        "location_lat": 16.5505, "location_lng": 104.7605,
        "best_months": "Year-round", "ideal_stay": "2-3 nights", "daily_budget": "₭ 250,000 - 420,000",
        "location_name": "Commercial District, Savannakhet",
        "best_for": ["Couples", "Solo Travelers"],
        "avoid_if": ["Large groups"],
        "booking_url": None, "agoda_url": None,
        "rating_avg": 4.0,
        "opening_hours": {k: {"open": "00:00", "close": "23:59", "closed": False} for k in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]},
        "image_url": json.dumps(["/static/places/doi-net-Chua-that-ing-hang-lao.jpg"]),
    },
    {
        "name": "Champa Garden Hotel",
        "description": "โรงแรมบูทีคท่ามกลางสวนดอกจำปา บรรยากาศร่มรื่น เงียบสงบ อาหารเช้าแบบบุฟเฟต์รสชาติดี ออกแบบสไตล์ลาวดั้งเดิม",
        "location_lat": 16.5480, "location_lng": 104.7650,
        "best_months": "Oct - Mar", "ideal_stay": "2-3 nights", "daily_budget": "₭ 280,000 - 500,000",
        "location_name": "Residential Area, Savannakhet",
        "best_for": ["Couples", "Culture Lovers", "Relaxation"],
        "avoid_if": ["Party seekers", "Late-night entertainment seekers"],
        "booking_url": None, "agoda_url": None,
        "rating_avg": 4.4,
        "opening_hours": {k: {"open": "00:00", "close": "23:59", "closed": False} for k in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]},
        "image_url": json.dumps(["/static/places/unnamed.webp"]),
    },
    {
        "name": "Phouthip Hotel",
        "description": "โรงแรมธุรกิจที่มีห้องประชุม สิ่งอำนวยความสะดวกสำหรับ corporate events บริการรับ-ส่งสนามบิน WiFi ความเร็วสูง",
        "location_lat": 16.5570, "location_lng": 104.7540,
        "best_months": "Year-round", "ideal_stay": "1-4 nights", "daily_budget": "₭ 300,000 - 500,000",
        "location_name": "Business District, Savannakhet",
        "best_for": ["Business Travelers", "Corporate Events"],
        "avoid_if": ["Leisure travelers", "Budget travelers"],
        "booking_url": None, "agoda_url": None,
        "rating_avg": 3.9,
        "opening_hours": {k: {"open": "00:00", "close": "23:59", "closed": False} for k in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]},
        "image_url": json.dumps(["/static/places/unnamed (1).webp"]),
    },
    {
        "name": "Savan Na Khet Heritage Hotel",
        "description": "โรงแรมสไตล์เฮอริเทจที่รักษาเสน่ห์สถาปัตยกรรมฝรั่งเศสดั้งเดิม ห้องพักตกแต่งด้วยของเก่าหายาก เป็นที่ชื่นชอบของนักถ่ายภาพ",
        "location_lat": 16.5525, "location_lng": 104.7615,
        "best_months": "Nov - Feb", "ideal_stay": "2-4 nights", "daily_budget": "₭ 400,000 - 700,000",
        "location_name": "Heritage Quarter, Savannakhet",
        "best_for": ["History Buffs", "Photographers", "Culture Enthusiasts"],
        "avoid_if": ["Budget travelers", "Those needing modern amenities"],
        "booking_url": None, "agoda_url": None,
        "rating_avg": 4.7,
        "opening_hours": {k: {"open": "00:00", "close": "23:59", "closed": False} for k in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]},
        "image_url": json.dumps([
            "/static/places/laos-savannakhet-lao-chaleun-square-night-market-located-within-the-grounds-of-the-former-lao-chaleun-complex-built-in-the-1960s-3AB00X1.jpg",
        ]),
    },
    {
        "name": "Riverside Villas Savannakhet",
        "description": "วิลล่าสุดหรูริมแม่น้ำโขง ห้องพักแบบ private villa มีสระว่ายน้ำส่วนตัว บริการ butler ตลอด 24 ชั่วโมง",
        "location_lat": 16.5490, "location_lng": 104.7555,
        "best_months": "Nov - Mar", "ideal_stay": "3-7 nights", "daily_budget": "₭ 1,200,000 - 3,000,000",
        "location_name": "Mekong Riverside, Savannakhet",
        "best_for": ["Luxury Travelers", "Honeymoon Couples", "Special Occasions"],
        "avoid_if": ["Budget travelers", "Group tours"],
        "booking_url": None, "agoda_url": None,
        "rating_avg": 4.9,
        "opening_hours": {k: {"open": "00:00", "close": "23:59", "closed": False} for k in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]},
        "image_url": json.dumps(["/static/places/unnamed (2).webp"]),
    },
    {
        "name": "Pakse-Savannakhet Transit Hotel",
        "description": "โรงแรมสะดวก ตั้งอยู่ใกล้สถานีขนส่ง เหมาะสำหรับนักเดินทางที่แวะพักก่อนเดินทางต่อ ราคาประหยัด เช็คอินตลอด 24 ชั่วโมง",
        "location_lat": 16.5580, "location_lng": 104.7530,
        "best_months": "Year-round", "ideal_stay": "1 night", "daily_budget": "₭ 70,000 - 130,000",
        "location_name": "Bus Terminal Area, Savannakhet",
        "best_for": ["Transit Travelers", "Budget Travelers"],
        "avoid_if": ["Long-stay guests", "Luxury seekers"],
        "booking_url": None, "agoda_url": None,
        "rating_avg": 3.5,
        "opening_hours": {k: {"open": "00:00", "close": "23:59", "closed": False} for k in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]},
        "image_url": json.dumps(["/static/places/iStock-1152768728.jpg"]),
    },
    {
        "name": "Savanhxai Boutique Hotel",
        "description": "บูทีคโฮเทลที่มีการออกแบบร่วมสมัย ผสมผสานศิลปะลาวและดีไซน์โมเดิร์น มีร้านกาแฟชั้นล่างที่ได้รับความนิยม",
        "location_lat": 16.5508, "location_lng": 104.7598,
        "best_months": "Year-round", "ideal_stay": "2-3 nights", "daily_budget": "₭ 280,000 - 480,000",
        "location_name": "Central Savannakhet",
        "best_for": ["Design Lovers", "Instagrammers", "Couples"],
        "avoid_if": ["Budget travelers"],
        "booking_url": None, "agoda_url": None,
        "rating_avg": 4.3,
        "opening_hours": {k: {"open": "00:00", "close": "23:59", "closed": False} for k in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]},
        "image_url": json.dumps(["/static/places/place-talat-yen-savannakhet-laos-900x600.webp"]),
    },
    {
        "name": "Golden Palace Hotel Savannakhet",
        "description": "โรงแรมสไตล์พระราชวัง ห้องพักหรูหราทุกห้อง มีสวนขนาดใหญ่ สนามเทนนิส ฟิตเนส และสปาครบครัน เหมาะสำหรับงาน wedding",
        "location_lat": 16.5455, "location_lng": 104.7680,
        "best_months": "Nov - Apr", "ideal_stay": "2-5 nights", "daily_budget": "₭ 600,000 - 1,500,000",
        "location_name": "Southern District, Savannakhet",
        "best_for": ["Luxury Travelers", "Wedding Parties", "Special Events"],
        "avoid_if": ["Budget travelers", "Solo travelers"],
        "booking_url": None, "agoda_url": None,
        "rating_avg": 4.6,
        "opening_hours": {k: {"open": "00:00", "close": "23:59", "closed": False} for k in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]},
        "image_url": json.dumps(["/static/places/16a1ac436d864c2c360d1ef7fa857492.jpg"]),
    },
]


def seed():
    db = SessionLocal()
    try:
        added = 0
        for h in hotels:
            place = Place(
                category_id=HOTEL_CATEGORY_ID,
                name=h["name"],
                description=h["description"],
                location_lat=h["location_lat"],
                location_lng=h["location_lng"],
                image_url=h["image_url"],
                opening_hours=h["opening_hours"],
                is_published=True,
                status="approved",
                rating_avg=h["rating_avg"],
                best_months=h["best_months"],
                ideal_stay=h["ideal_stay"],
                daily_budget=h["daily_budget"],
                location_name=h["location_name"],
                best_for=h["best_for"],
                avoid_if=h["avoid_if"],
                booking_url=h["booking_url"],
                agoda_url=h["agoda_url"],
            )
            db.add(place)
            added += 1
            print(f"  [OK] Added: {h['name']}")

        db.commit()
        print(f"\nDone! Added {added} hotels to the database.")
    except Exception as e:
        db.rollback()
        print(f"ERROR: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(
        encoding='utf-8', errors='replace') if hasattr(sys.stdout, 'reconfigure') else None
    print("Seeding hotel data for Savannakhet...\n")
    seed()
