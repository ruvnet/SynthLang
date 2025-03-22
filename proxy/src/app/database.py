"""
Database models and connection setup.

This module defines SQLAlchemy models and database connection setup
for persisting interaction data.
"""
import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, String, Integer, Boolean, LargeBinary, DateTime, func
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Get database configuration from environment variables
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "synthlang_proxy")

# Construct the database URL
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# For testing or development, allow SQLite
if os.getenv("USE_SQLITE", "0") == "1":
    SQLITE_PATH = os.getenv("SQLITE_PATH", "sqlite+aiosqlite:///./synthlang_proxy.db")
    DATABASE_URL = SQLITE_PATH
    logger.info(f"Using SQLite database at {SQLITE_PATH}")
else:
    logger.info(f"Using PostgreSQL database at {DB_HOST}:{DB_PORT}/{DB_NAME}")

# Create engine with echo for debugging if needed
DEBUG_SQL = os.getenv("DEBUG_SQL", "0") == "1"
engine = create_async_engine(DATABASE_URL, echo=DEBUG_SQL)
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


async def init_db():
    """
    Initialize the database by creating all tables.
    
    This function should be called during application startup.
    """
    try:
        async with engine.begin() as conn:
            # Create tables if they don't exist
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")
        return True
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        return False