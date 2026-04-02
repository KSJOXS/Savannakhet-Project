from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# เปลี่ยน 'password' เป็นรหัสผ่าน MySQL ของคุณ
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:jojo2025@localhost:3306/savannakhet_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ฟังก์ชันสำหรับเปิด/ปิด Database Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()