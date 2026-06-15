from sqlalchemy import create_engine, inspect
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL", "mysql+pymysql://root:@localhost/savannakhet_db")
engine = create_engine(DATABASE_URL)

inspector = inspect(engine)
columns = [c['name'] for c in inspector.get_columns('places')]
print(f"Columns in 'places' table: {columns}")
