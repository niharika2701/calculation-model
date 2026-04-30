from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@db:5432/fastapi_db"
)

class Base(DeclarativeBase):
    pass

def get_engine():
    return create_engine(DATABASE_URL)

def get_session_local():
    return sessionmaker(autocommit=False, autoflush=False, bind=get_engine())

def get_db():
    SessionLocal = get_session_local()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()