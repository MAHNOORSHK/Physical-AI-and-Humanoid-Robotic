"""
Database models and connection for Neon Postgres
"""

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

Base = declarative_base()


class Conversation(Base):
    """Conversation history table"""
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(255), index=True, nullable=False)
    user_message = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)
    context = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class QueryLog(Base):
    """Query logs for analytics"""
    __tablename__ = "query_logs"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(255), index=True)
    query = Column(Text, nullable=False)
    response_time = Column(Float, nullable=True)
    success = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)


# Database connection
def get_database():
    """Get database session"""
    if not settings.DATABASE_URL:
        return None

    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create tables
    Base.metadata.create_all(bind=engine)

    return SessionLocal()
