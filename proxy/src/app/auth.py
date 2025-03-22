"""
Authentication module for API key verification and rate limiting.

This module provides functions for verifying API keys and
implementing rate limiting based on user identifiers.
"""
import time
import os
import logging
from typing import Dict, Tuple, Optional
from fastapi import Header, HTTPException, Request
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_429_TOO_MANY_REQUESTS

# Configure logging
logger = logging.getLogger(__name__)

# In-memory API key store (in production, replace with DB lookup)
# Format: {"api_key": {"user_id": "user_id", "rate_limit_qpm": 60}}
API_KEYS = {
    "sk_test_user1": {"user_id": "user1", "rate_limit_qpm": 60},
    "sk_test_user2": {"user_id": "user2", "rate_limit_qpm": 5},
}

# In-memory request counter for rate limiting
# Format: {"user_id": [timestamp, count]}
_request_counts: Dict[str, Tuple[float, int]] = {}


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
            detail="Missing API key"
        )
    
    if not authorization.startswith("Bearer "):
        logger.warning("Invalid Authorization format")
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header format"
        )
    
    api_key = authorization.split(" ", 1)[1]
    
    if api_key not in API_KEYS:
        logger.warning(f"Invalid API key: {api_key[:5]}...")
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    
    logger.debug(f"API key verified: {api_key[:5]}...")
    return api_key


def get_user_id(api_key: str) -> str:
    """
    Retrieve user identifier from API key.
    
    Args:
        api_key: The API key
        
    Returns:
        The user ID associated with the API key
    """
    return API_KEYS[api_key]["user_id"]


def get_rate_limit(api_key: str) -> int:
    """
    Get the rate limit for the given API key.
    
    Args:
        api_key: The API key
        
    Returns:
        The rate limit in requests per minute
    """
    return API_KEYS[api_key]["rate_limit_qpm"]


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
    
    if not allow_request(user_id):
        retry_after = 60  # Retry after 1 minute
        logger.warning(f"Rate limit exceeded for user {user_id}")
        raise HTTPException(
            status_code=HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded",
            headers={"Retry-After": str(retry_after)}
        )


def allow_request(user_id: str) -> bool:
    """
    Check if a request should be allowed based on rate limits.
    
    Args:
        user_id: The user identifier
        
    Returns:
        True if the request should be allowed, False otherwise
    """
    global _request_counts
    
    # Find the API key for this user to get the rate limit
    rate_limit = None
    for key, data in API_KEYS.items():
        if data["user_id"] == user_id:
            rate_limit = data["rate_limit_qpm"]
            break
    
    if rate_limit is None:
        # Unknown user, reject the request
        return False
    
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
