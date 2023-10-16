import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    DATABASE_URL = 'postgresql://dbuser:dbpassword@db:5432/dbname'
    # raise Exception('Unable to read DATABASE_URL from system')

# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a Session class to instantiate database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()