"""
Database models and connection setup.

This module defines SQLAlchemy models and database connection setup
for persisting interaction data.
"""
import os
import logging
import threading
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, String, Integer, Boolean, LargeBinary, DateTime, func, ForeignKey, Table, text
from sqlalchemy.orm import relationship
from sqlalchemy import event

from src.app.config import DATABASE_URL as CONFIG_DATABASE_URL

# Configure logging
logger = logging.getLogger(__name__)

# Use DATABASE_URL from config if available, otherwise construct from components
if CONFIG_DATABASE_URL:
    DATABASE_URL = CONFIG_DATABASE_URL
    logger.info("Using DATABASE_URL from configuration")
else:
    # Fallback to constructing from individual components
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "synthlang_proxy")
    
    # Construct the database URL
    DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    logger.warning("DATABASE_URL not found in configuration, constructed from components")

# For testing or development, allow SQLite
if os.getenv("USE_SQLITE", "0") == "1":
    SQLITE_PATH = os.getenv("SQLITE_PATH", "sqlite+aiosqlite:///./synthlang_proxy.db")
    DATABASE_URL = SQLITE_PATH
    logger.info(f"Using SQLite database at {SQLITE_PATH}")
    
    # Import the database security module for SQLite
    from src.app.db_security import initialize_db_security
    
    # Initialize database security for SQLite
    initialize_db_security()
else:
    logger.info(f"Using database at {DATABASE_URL}")

# Create engine with echo for debugging if needed
DEBUG_SQL = os.getenv("DEBUG_SQL", "0") == "1"

# Configure engine based on database type
if DATABASE_URL.startswith('sqlite'):
    # SQLite doesn't support connection pooling the same way
    engine = create_async_engine(
        DATABASE_URL, 
        echo=DEBUG_SQL,
        # SQLite-specific options
        connect_args={"check_same_thread": False},
    )
else:
    # PostgreSQL and other databases support connection pooling
    engine = create_async_engine(
        DATABASE_URL, 
        echo=DEBUG_SQL,
        # Connection pool settings for better security and performance
        pool_size=5,  # Default number of connections
        max_overflow=10,  # Maximum number of connections above pool_size
        pool_timeout=30,  # Timeout for getting a connection from the pool
        pool_recycle=1800,  # Recycle connections after 30 minutes
        pool_pre_ping=True,  # Check connection validity before using
    )

# Set up connection pool event listeners for security
@event.listens_for(engine.sync_engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Set SQLite pragmas for security on connection creation."""
    if DATABASE_URL.startswith('sqlite'):
        cursor = dbapi_connection.cursor()
        # Enable foreign key constraints
        cursor.execute("PRAGMA foreign_keys=ON")
        # Use Write-Ahead Logging for better concurrency and crash recovery
        cursor.execute("PRAGMA journal_mode=WAL")
        # Balance between safety and performance
        cursor.execute("PRAGMA synchronous=NORMAL")
        # Overwrite deleted data with zeros
        cursor.execute("PRAGMA secure_delete=ON")
        # Automatically vacuum the database
        cursor.execute("PRAGMA auto_vacuum=FULL")
        cursor.close()

# Create session factory
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Thread-local storage for session tracking
_session_registry = threading.local()
_session_registry.sessions = set()

# Base class for all models
Base = declarative_base()

# Session management functions
async def close_all_sessions():
    """Close all active sessions."""
    if hasattr(_session_registry, 'sessions'):
        for session in list(_session_registry.sessions):
            try:
                await session.close()
            except Exception as e:
                logger.error(f"Error closing session: {e}")
        _session_registry.sessions.clear()


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


class User(Base):
    """
    SQLAlchemy model for storing user data.
    
    Attributes:
        id: Primary key
        user_id: User identifier (e.g., email or username)
        api_key: API key for the user
        created_at: When the user was created
        updated_at: When the user was last updated
        roles: Relationship to UserRole
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True)
    api_key = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship to UserRole
    roles = relationship("UserRole", back_populates="user", cascade="all, delete-orphan")


class Role(Base):
    """
    SQLAlchemy model for storing role definitions.
    
    Attributes:
        id: Primary key
        name: Role name
        description: Role description
        created_at: When the role was created
        users: Relationship to UserRole
    """
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship to UserRole
    users = relationship("UserRole", back_populates="role", cascade="all, delete-orphan")


class UserRole(Base):
    """
    SQLAlchemy model for storing user-role associations.
    
    Attributes:
        id: Primary key
        user_id: Foreign key to User
        role_id: Foreign key to Role
        assigned_at: When the role was assigned
        user: Relationship to User
        role: Relationship to Role
    """
    __tablename__ = "user_roles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    role_id = Column(Integer, ForeignKey("roles.id"))
    assigned_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="roles")
    role = relationship("Role", back_populates="users")


async def init_db():
    """
    Initialize the database by creating all tables.
    
    This function should be called during application startup.
    """
    try:
        async with engine.begin() as conn:
            # Create tables if they don't exist
            await conn.run_sync(Base.metadata.create_all)
        
        # Initialize default roles if they don't exist
        await init_default_roles()
        
        logger.info("Database tables created successfully")
        return True
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        return False


async def init_default_roles():
    """
    Initialize default roles in the database.
    
    This function creates the basic, premium, and admin roles if they don't exist.
    """
    try:
        async with SessionLocal() as session:
            # Check if roles already exist
            for role_name, description in [
                ("basic", "Basic user with limited access"),
                ("premium", "Premium user with enhanced access"),
                ("admin", "Administrator with full access")
            ]:
                # Check if role exists using proper text() function
                query = text(f"SELECT id FROM roles WHERE name = '{role_name}'")
                role_result = await session.execute(query)
                role = role_result.scalar_one_or_none()
                
                if not role:
                    # Create role if it doesn't exist using proper text() function
                    insert_query = text(f"INSERT INTO roles (name, description) VALUES ('{role_name}', '{description}')")
                    await session.execute(insert_query)
                    logger.info(f"Created default role: {role_name}")
            
            # Commit the transaction
            await session.commit()
        
        logger.info("Default roles initialized")
        return True
    except Exception as e:
        logger.error(f"Error initializing default roles: {e}")
        return False