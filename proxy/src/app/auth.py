"""
Authentication module for API key verification and rate limiting.

This module provides functions for verifying API keys and
implementing rate limiting based on user identifiers.
"""
import time
import os
import logging
import asyncio
from typing import Dict, Tuple, Optional, List
from fastapi import Header, HTTPException, Request
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_429_TOO_MANY_REQUESTS, HTTP_403_FORBIDDEN
from sqlalchemy import select

from src.app.database import SessionLocal, User
from src.app.auth.roles import has_role, get_user_roles
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

# In-memory request counter for rate limiting
# Format: {"user_id": [timestamp, count]}
_request_counts: Dict[str, Tuple[float, int]] = {}


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


def verify_api_key(authorization: str = Header(...)) -> str:
    """
    Verify the provided API key and return the API key if valid.
    
    Args:
        authorization: The Authorization header containing the API key
        
    Returns:
        The API key if valid
        
    Raises:
        HTTPException: If the API key is missing or invalid
    """
    if not authorization:
        logger.warning("Missing Authorization header")
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail={
                "error": {
                    "message": "Missing API key",
                    "type": "auth_error",
                    "code": HTTP_401_UNAUTHORIZED
                }
            }
        )
    
    if not authorization.startswith("Bearer "):
        logger.warning("Invalid Authorization format")
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail={
                "error": {
                    "message": "Invalid Authorization header format",
                    "type": "auth_error",
                    "code": HTTP_401_UNAUTHORIZED
                }
            }
        )
    
    api_key = authorization.split(" ", 1)[1]
    
    # Check if API key is in cache
    if api_key in API_KEY_CACHE:
        logger.debug(f"API key verified from cache: {api_key[:5]}...")
        return api_key
    
    # Schedule a database lookup
    asyncio.create_task(get_user_by_api_key(api_key))
    
    # For now, accept the key if it's one of the default keys
    if api_key == DEFAULT_API_KEY or api_key == ADMIN_API_KEY:
        logger.debug(f"API key verified from defaults: {api_key[:5]}...")
        return api_key
    
    logger.warning(f"Invalid API key: {api_key[:5]}...")
    raise HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail={
            "error": {
                "message": "Invalid API key",
                "type": "auth_error",
                "code": HTTP_401_UNAUTHORIZED
            }
        }
    )


def get_user_id(api_key: str) -> str:
    """
    Retrieve user identifier from API key.
    
    Args:
        api_key: The API key
        
    Returns:
        The user ID associated with the API key
    """
    # Check if API key is in cache
    if api_key in API_KEY_CACHE:
        return API_KEY_CACHE[api_key]["user_id"]
    
    # Fall back to default values for backward compatibility
    if api_key == DEFAULT_API_KEY:
        return "default_user"
    if api_key == ADMIN_API_KEY:
        return "admin_user"
    
    # This should not happen if verify_api_key is called first
    logger.error(f"Unknown API key: {api_key[:5]}...")
    return "unknown_user"


def get_rate_limit(api_key: str) -> int:
    """
    Get the rate limit for the given API key.
    
    Args:
        api_key: The API key
        
    Returns:
        The rate limit in requests per minute
    """
    # Check if API key is in cache
    if api_key in API_KEY_CACHE:
        return API_KEY_CACHE[api_key]["rate_limit_qpm"]
    
    # Fall back to default values for backward compatibility
    if api_key == ADMIN_API_KEY:
        return PREMIUM_RATE_LIMIT_QPM
    
    return DEFAULT_RATE_LIMIT_QPM


def check_rate_limit(request: Request, api_key: str) -> None:
    """
    Check if the request exceeds the rate limit for the user.
    
    Args:
        request: The FastAPI request object
        api_key: The API key
        
    Raises:
        HTTPException: If the rate limit is exceeded
    """
    user_id = get_user_id(api_key)
    rate_limit = get_rate_limit(api_key)
    
    if not allow_request(user_id, rate_limit):
        retry_after = 60  # Retry after 1 minute
        logger.warning(f"Rate limit exceeded for user {user_id}")
        raise HTTPException(
            status_code=HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "error": {
                    "message": "Rate limit exceeded",
                    "type": "rate_limit_error",
                    "code": HTTP_429_TOO_MANY_REQUESTS
                }
            },
            headers={"Retry-After": str(retry_after)}
        )


def allow_request(user_id: str, rate_limit: int) -> bool:
    """
    Check if a request should be allowed based on rate limits.
    
    Args:
        user_id: The user identifier
        rate_limit: The rate limit in requests per minute
        
    Returns:
        True if the request should be allowed, False otherwise
    """
    global _request_counts
    
    current_time = time.time()
    
    # If this is the first request from this user, initialize the counter
    if user_id not in _request_counts:
        _request_counts[user_id] = (current_time, 1)
        return True
    
    last_request_time, count = _request_counts[user_id]
    
    # If the last request was more than a minute ago, reset the counter
    if current_time - last_request_time > 60:
        _request_counts[user_id] = (current_time, 1)
        return True
    
    # If the user has exceeded their rate limit, reject the request
    if count >= rate_limit:
        return False
    
    # Otherwise, increment the counter and allow the request
    _request_counts[user_id] = (last_request_time, count + 1)
    return True


def require_role(required_role: str):
    """
    Decorator for endpoints that require a specific role.
    
    Args:
        required_role: The role required to access the endpoint
        
    Returns:
        A decorator function that checks if the user has the required role
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Extract API key from request
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            
            if request is None and "request" in kwargs:
                request = kwargs["request"]
            
            if request is None:
                raise ValueError("Request object not found in function arguments")
            
            # Get authorization header
            authorization = request.headers.get("Authorization")
            if not authorization:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail={
                        "error": {
                            "message": "Missing API key",
                            "type": "auth_error",
                            "code": HTTP_401_UNAUTHORIZED
                        }
                    }
                )
            
            # Verify API key
            api_key = verify_api_key(authorization)
            
            # Get user ID
            user_id = get_user_id(api_key)
            
            # Check if user has the required role
            if not has_role(user_id, required_role):
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN,
                    detail={
                        "error": {
                            "message": f"User '{user_id}' does not have required role '{required_role}'",
                            "type": "permission_error",
                            "code": HTTP_403_FORBIDDEN
                        }
                    }
                )
            
            # User has the required role, proceed with the function
            return await func(*args, **kwargs)
        
        return wrapper
    
    return decorator
