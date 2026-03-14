# models.py — SQLAlchemy models
from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.sql import func

# FIXED IMPORT — no dot
from database import Base


class Paper(Base):
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True, index=True)
    pmid = Column(String, unique=True, index=True, nullable=False)
    title = Column(Text)
    abstract = Column(Text)
    journal = Column(String)
    year = Column(String)
    keyword = Column(String)
    group = Column(String)
    relevance = Column(Float, default=0.0)
    date_added = Column(DateTime(timezone=True), server_default=func.now())
