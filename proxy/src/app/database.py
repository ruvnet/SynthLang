"""
Database models and connection setup.

This module defines SQLAlchemy models and database connection setup
for persisting interaction data.
"""
import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, String, Integer, Boolean, LargeBinary, DateTime, func

# Database URL (placeholder, will be configured via env var later)
# Use a valid URL format with numeric port
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@host:5432/database_name")
engine = create_async_engine(DATABASE_URL, echo=False)  # Set echo=True for debugging SQL
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


class Interaction(Base):
    """
    SQLAlchemy model for storing interaction data.
    
    Attributes:
        id: Primary key
        user_id: User identifier
        model: LLM model used
        prompt_enc: Encrypted prompt data
        response_enc: Encrypted response data
        cache_hit: Whether the response was from cache
        prompt_tokens: Number of tokens in the prompt
        response_tokens: Number of tokens in the response
        timestamp: When the interaction occurred
    """
    __tablename__ = "interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    model = Column(String)
    prompt_enc = Column(LargeBinary)
    response_enc = Column(LargeBinary)
    cache_hit = Column(Boolean)
    prompt_tokens = Column(Integer)
    response_tokens = Column(Integer)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())