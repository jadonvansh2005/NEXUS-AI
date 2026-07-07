from sqlalchemy import create_engine, text
from app.settings import settings

def run_migration():
    print("Connecting to database using engine...")
    engine = create_engine(settings.DATABASE_URL)
    
    # We will use raw SQL ALTER TABLE commands to add columns safely if they do not exist
    # PostgreSQL supports 'ADD COLUMN IF NOT EXISTS'
    queries = [
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS is_verified BOOLEAN NOT NULL DEFAULT FALSE;",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS verification_otp VARCHAR(6);",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS otp_expiry TIMESTAMP;"
    ]
    
    with engine.begin() as conn:
        for q in queries:
            print(f"Executing: {q}")
            conn.execute(text(q))
            
    print("✅ Migration executed successfully!")

if __name__ == "__main__":
    run_migration()
