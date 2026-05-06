from app.database import engine
from sqlalchemy import text

def check_raw():
    with engine.connect() as con:
        res = con.execute(text("SELECT * FROM places LIMIT 1"))
        row = res.fetchone()
        print(f"Keys: {res.keys()}")
        print(f"First row: {row}")

if __name__ == "__main__":
    check_raw()
