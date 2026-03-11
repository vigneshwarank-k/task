from sqlalchemy.orm import sessionmaker , declarative_base
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")
Base = declarative_base()
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine , autoflush=False , autocommit = False)

def get_db():
    try:
        db = SessionLocal()
        yield db
        print("\n\n database connected successfully.. \n\n")
    finally:
        db.close()