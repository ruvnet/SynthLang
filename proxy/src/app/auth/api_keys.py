"""
API key authentication and rate limiting for the SynthLang Proxy.

This module provides functions for verifying API keys and enforcing rate limits.
"""
import os
import time
import json
import logging
from typing import Dict, Tuple, Optional
from fastapi import HTTPException, Request

# Logger for this module
logger = logging.getLogger(__name__)

# Path to store API keys
API_KEYS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), ".api_keys.json")

# Dictionary of API keys: key -> user_id
API_KEYS: Dict[str, str] = {
    "sk_test_user1": "user1",
    "sk_test_user2": "user2"
}

# Dictionary of rate limits: user_id -> requests per minute
RATE_LIMITS: Dict[str, int] = {
    "user1": 60,  # 60 requests per minute
    "user2": 5    # 5 requests per minute
}

# Default rate limit for users not in RATE_LIMITS
DEFAULT_RATE_LIMIT = 10  # 10 requests per minute

# Dictionary to track request counts: user_id -> (timestamp, count)
_request_counts: Dict[str, Tuple[float, int]] = {}

def load_api_keys_from_file():
    """
    Load API keys from file.
    """
    global API_KEYS, RATE_LIMITS
    
    if os.path.exists(API_KEYS_FILE):
        try:
            with open(API_KEYS_FILE, "r") as f:
                data = json.load(f)
            
            # Update API keys and rate limits
            if "api_keys" in data:
                API_KEYS.update(data["api_keys"])
            
            if "rate_limits" in data:
                RATE_LIMITS.update(data["rate_limits"])
                
            logger.info(f"Loaded {len(data.get('api_keys', {}))} API keys from file")
        except Exception as e:
            logger.error(f"Error loading API keys from file: {e}")

# Load API keys from file on module import
load_api_keys_from_file()

# Also check for API key in environment
env_api_key = os.environ.get("API_KEY")
if env_api_key:
    # Add to API keys if not already present
    if env_api_key not in API_KEYS:
        API_KEYS[env_api_key] = "env_user"
        logger.info("Added API key from environment")

def verify_api_key(auth_header: Optional[str]) -> str:
    """
    Verify that the API key is valid.
    
    Args:
        auth_header: The Authorization header value
        
    Returns:
        The API key if valid
        
    Raises:
        HTTPException: If the API key is missing or invalid
    """
    if not auth_header:
        raise HTTPException(
            status_code=401,
            detail={"error": {"message": "Missing API key", "type": "auth_error", "code": 401}}
        )
    
    # Check format (should be "Bearer sk_...")
    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=401,
            detail={"error": {"message": "Invalid Authorization header format", "type": "auth_error"}}
        )
    
    api_key = parts[1]
    
    # Check if API key is valid
    if api_key not in API_KEYS:
        raise HTTPException(
            status_code=401,
            detail={"error": {"message": "Invalid API key", "type": "auth_error"}}
        )
    
    return api_key

def get_user_id(api_key: str) -> str:
    """
    Get the user ID associated with an API key.
    
    Args:
        api_key: The API key
        
    Returns:
        The user ID
    """
    return API_KEYS.get(api_key, "unknown")

def get_rate_limit(api_key: str) -> int:
    """
    Get the rate limit for an API key.
    
    Args:
        api_key: The API key
        
    Returns:
        The rate limit in requests per minute
    """
    user_id = get_user_id(api_key)
    return RATE_LIMITS.get(user_id, DEFAULT_RATE_LIMIT)

def check_rate_limit(request: Request, api_key: str) -> None:
    """
    Check if a request exceeds the rate limit.
    
    Args:
        request: The FastAPI request object
        api_key: The API key
        
    Raises:
        HTTPException: If the rate limit is exceeded
    """
    user_id = get_user_id(api_key)
    
    # Get current time
    current_time = time.time()
    
    # Get or initialize request count for this user
    if user_id not in _request_counts:
        _request_counts[user_id] = (current_time, 1)
        return
    
    # Get timestamp and count
    timestamp, count = _request_counts[user_id]
    
    # Check if the time window has expired (1 minute)
    if current_time - timestamp > 60:
        # Reset count for new time window
        _request_counts[user_id] = (current_time, 1)
        return
    
    # Get rate limit for this user
    rate_limit = get_rate_limit(api_key)
    
    # Check if rate limit is exceeded
    if count >= rate_limit:
        # Calculate time until reset
        reset_time = timestamp + 60 - current_time
        
        # Raise rate limit error
        raise HTTPException(
            status_code=429,
            detail={"error": {"message": "Rate limit exceeded", "type": "rate_limit_error"}},
            headers={"Retry-After": str(int(reset_time))}
        )
    
    # Increment request count
    _request_counts[user_id] = (timestamp, count + 1)

def allow_request(user_id: str) -> bool:
    """
    Check if a request is allowed based on rate limits.
    
    This is a simpler version of check_rate_limit that doesn't raise exceptions.
    
    Args:
        user_id: The user ID
        
    Returns:
        True if the request is allowed, False otherwise
    """
    # Get rate limit for this user
    rate_limit = RATE_LIMITS.get(user_id, DEFAULT_RATE_LIMIT)
    
    # Get current time
    current_time = time.time()
    
    # Get or initialize request count for this user
    if user_id not in _request_counts:
        _request_counts[user_id] = (current_time, 1)
        return True
    
    # Get timestamp and count
    timestamp, count = _request_counts[user_id]
    
    # Check if the time window has expired (1 minute)
    if current_time - timestamp > 60:
        # Reset count for new time window
        _request_counts[user_id] = (current_time, 1)
        return True
    
    # Check if rate limit is exceeded
    if count >= rate_limit:
        return False
    
    # Increment request count
    _request_counts[user_id] = (timestamp, count + 1)
    return True