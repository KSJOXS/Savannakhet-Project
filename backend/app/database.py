from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# เปลี่ยน 'password' เป็นรหัสผ่าน MySQL ของคุณ
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:jojo2025@localhost:3306/savannakhet_db"
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://avnadmin:GHw_R~3Wb3g.g@mysql-xxxx.aivencloud.com:12345/defaultdb"
SQLALCHEMY_DATABASE_URL = f"clickhouse+http://default:GHw_R~3Wb3g.g@jj7nhi33yg.ap-southeast-1.aws.clickhouse.cloud:8443/default?secure=true"

# engine = create_engine(SQLALCHEMY_DATABASE_URL)
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