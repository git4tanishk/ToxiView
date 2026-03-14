# database.py — SQLAlchemy setup (SQLite for MVP)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os


DB_FILE = os.getenv('TOXIVIEW_DB', 'toxiview.db')
SQLALCHEMY_DATABASE_URL = f'sqlite:///{DB_FILE}'


engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()