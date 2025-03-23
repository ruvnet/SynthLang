"""
Database-backed authentication module.

This module provides functions for database-backed API key verification and user management.
"""
import time
import os
import logging
import asyncio
from typing import Dict, Tuple, Optional, List, Any
from sqlalchemy import select

from src.app.database import SessionLocal, User
from src.app.auth.roles import has_role
from src.app.config import DEFAULT_RATE_LIMIT_QPM, PREMIUM_RATE_LIMIT_QPM

# Configure logging
logger = logging.getLogger(__name__)

# In-memory API key cache for faster lookups
# Format: {"api_key": {"user_id": "user_id", "rate_limit_qpm": 60}}
API_KEY_CACHE: Dict[str, Dict[str, any]] = {}

# Default API keys from environment variables for backward compatibility
DEFAULT_API_KEY = os.environ.get("API_KEY")
ADMIN_API_KEY = os.environ.get("ADMIN_API_KEY", DEFAULT_API_KEY)

# Initialize default API keys in the cache
if DEFAULT_API_KEY:
    API_KEY_CACHE[DEFAULT_API_KEY] = {"user_id": "default_user", "rate_limit_qpm": DEFAULT_RATE_LIMIT_QPM}
if ADMIN_API_KEY and ADMIN_API_KEY != DEFAULT_API_KEY:
    API_KEY_CACHE[ADMIN_API_KEY] = {"user_id": "admin_user", "rate_limit_qpm": PREMIUM_RATE_LIMIT_QPM}


async def load_api_keys_from_db():
    """
    Load API keys from the database into the in-memory cache.
    
    This function should be called during application startup.
    """
    try:
        async with SessionLocal() as session:
            # Query all users and their API keys
            query = select(User)
            result = await session.execute(query)
            users = result.scalars().all()
            
            # Update the in-memory cache
            for user in users:
                # Determine rate limit based on user roles
                rate_limit = DEFAULT_RATE_LIMIT_QPM
                if has_role(user.user_id, "premium") or has_role(user.user_id, "admin"):
                    rate_limit = PREMIUM_RATE_LIMIT_QPM
                
                API_KEY_CACHE[user.api_key] = {
                    "user_id": user.user_id,
                    "rate_limit_qpm": rate_limit
                }
            
            logger.info(f"Loaded {len(users)} API keys from database")
    except Exception as e:
        logger.error(f"Error loading API keys from database: {e}")


async def get_user_by_api_key(api_key: str) -> Optional[Dict[str, any]]:
    """
    Get user information from an API key.
    
    This function first checks the in-memory cache, then falls back to the database.
    
    Args:
        api_key: The API key to look up
        
    Returns:
        A dictionary with user information, or None if the API key is invalid
    """
    # Check in-memory cache first
    if api_key in API_KEY_CACHE:
        return API_KEY_CACHE[api_key]
    
    # Fall back to database lookup
    try:
        async with SessionLocal() as session:
            query = select(User).where(User.api_key == api_key)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            
            if user:
                # Determine rate limit based on user roles
                rate_limit = DEFAULT_RATE_LIMIT_QPM
                if has_role(user.user_id, "premium") or has_role(user.user_id, "admin"):
                    rate_limit = PREMIUM_RATE_LIMIT_QPM
                
                # Update the in-memory cache
                user_info = {
                    "user_id": user.user_id,
                    "rate_limit_qpm": rate_limit
                }
                API_KEY_CACHE[api_key] = user_info
                return user_info
    except Exception as e:
        logger.error(f"Error looking up API key in database: {e}")
    
    return None