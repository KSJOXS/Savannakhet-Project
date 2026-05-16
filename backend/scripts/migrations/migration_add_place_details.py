from sqlalchemy import text
from app.database import engine

def run_migration():
    columns = [
        ("best_months", "VARCHAR(100)"),
        ("ideal_stay", "VARCHAR(100)"),
        ("daily_budget", "VARCHAR(100)"),
        ("location_name", "VARCHAR(100)"),
        ("best_for", "JSON"),
        ("avoid_if", "JSON")
    ]
    
    with engine.connect() as connection:
        for col_name, col_type in columns:
            try:
                # SQLAlchemy text() is safer
                connection.execute(text(f"ALTER TABLE places ADD COLUMN {col_name} {col_type}"))
                connection.commit()
                print(f"Added column {col_name}")
            except Exception as e:
                if "Duplicate column name" in str(e):
                    print(f"Column {col_name} already exists")
                else:
                    print(f"Error adding {col_name}: {e}")
        
    print("Migration completed successfully")

if __name__ == "__main__":
    run_migration()
