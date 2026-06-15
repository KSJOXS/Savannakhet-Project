"""
export_data_for_colab.py
========================
รันสคริปต์นี้ที่เครื่องตัวเองก่อน แล้วนำไฟล์ที่ได้ไป Upload ใน Google Colab

วิธีรัน:
  cd c:/Users/ASUS/savannakhet-project/backend
  python scripts/export_data_for_colab.py

ไฟล์ที่จะได้:
  backend/docs/savannakhet_real_data.json   ← Upload นี้ขึ้น Colab
"""

import sys, os, json

# Force UTF-8 output on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# ── เพิ่ม path ──
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import User, Place, Interaction, InteractionLog, Category

CATEGORIES = ['nature', 'culture', 'restaurant', 'hotel',
              'shopping', 'nightlife', 'cafe', 'local_food', 'chill', 'landmark']

def export():
    db = SessionLocal()
    try:
        # ── 1. Users ──
        users_raw = db.query(User).filter(User.deleted_at == None).all()
        users = []
        for u in users_raw:
            prefs = u.preferences or []
            if isinstance(prefs, str):
                try:
                    prefs = json.loads(prefs)
                except:
                    prefs = []
            users.append({
                "id"         : u.id,
                "username"   : u.username,
                "preferences": prefs if isinstance(prefs, list) else [],
            })

        # ── 2. Places ──
        places_raw = db.query(Place).filter(Place.status == "approved").all()
        places = []
        for p in places_raw:
            cat_type = p.category.parent_type if p.category else "other"
            places.append({
                "id"           : p.id,
                "name"         : p.name,
                "category"     : cat_type,
                "rating"       : float(p.rating_avg) if p.rating_avg else 0.0,
                "location_name": p.location_name or "Savannakhet",
            })

        # ── 3. Interactions (review + like + view) ──
        logs_raw = db.query(InteractionLog).all()
        interactions = []
        for log in logs_raw:
            weight = float(log.interaction_weight) if log.interaction_weight else 1.0
            interactions.append({
                "user_id"   : log.user_id,
                "place_id"  : log.place_id,
                "action"    : log.action_type,
                "weight"    : weight,
            })

        # ── เพิ่ม interactions จากตาราง user_interactions (reviews) ──
        reviews_raw = db.query(Interaction).all()
        reviewed_pairs = set((r.user_id, r.place_id) for r in reviews_raw)
        for r in reviews_raw:
            # ถ้ายังไม่มีใน logs ให้เพิ่ม
            if not any(i["user_id"] == r.user_id and i["place_id"] == r.place_id
                       and i["action"] == "review" for i in interactions):
                interactions.append({
                    "user_id" : r.user_id,
                    "place_id": r.place_id,
                    "action"  : "review",
                    "weight"  : 3.0,
                })

        # ── สรุป ──
        output = {
            "categories"   : CATEGORIES,
            "users"        : users,
            "places"       : places,
            "interactions" : interactions,
            "stats": {
                "num_users"        : len(users),
                "num_places"       : len(places),
                "num_interactions" : len(interactions),
            }
        }

        # ── บันทึก JSON ──
        out_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "docs", "savannakhet_real_data.json"
        )
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        print("=" * 55)
        print("  [OK] Export ข้อมูลจริงสำเร็จ!")
        print("=" * 55)
        print(f"  Users        : {len(users)}")
        print(f"  Places       : {len(places)}")
        print(f"  Interactions : {len(interactions)}")
        print(f"  บันทึกที่    : {out_path}")
        print("=" * 55)
        print("\n  ขั้นตอนต่อไป:")
        print("     1. เปิด Google Colab")
        print("     2. Upload ไฟล์  savannakhet_real_data.json")
        print("     3. รัน Notebook  Savannakhet_GNN_RealData.ipynb")

    finally:
        db.close()

if __name__ == "__main__":
    export()
