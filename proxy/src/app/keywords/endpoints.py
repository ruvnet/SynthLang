"""
Keyword pattern management API endpoints.

This module defines the FastAPI endpoints for managing keyword patterns.
"""
import logging
import time
from typing import Dict, Any, Optional, List

from fastapi import APIRouter, Depends, HTTPException, Header, Body, Path
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

from src.app import auth
from src.app.keywords.registry import (
    list_patterns,
    get_pattern,
    register_pattern,
    KeywordPattern,
    DETECTION_THRESHOLD,
    ENABLE_KEYWORD_DETECTION
)

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/v1/keywords", tags=["keywords"])


def verify_auth(authorization: Optional[str] = Header(None)) -> str:
    """
    Verify authorization header and return API key.
    
    Args:
        authorization: Authorization header
        
    Returns:
        API key
        
    Raises:
        HTTPException: If API key is missing or invalid
    """
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
    
    return auth.verify_api_key(authorization)


@router.get("/patterns")
async def get_patterns(
    api_key: str = Depends(verify_auth)
):
    """
    List all keyword patterns.
    
    Args:
        api_key: The API key
        
    Returns:
        List of keyword patterns
    """
    # Get user ID from API key
    user_id = auth.get_user_id(api_key)
    
    # Check rate limit
    auth.check_rate_limit(None, api_key)
    
    # Check if user has required role
    if not auth.has_role(user_id, "admin"):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail={
                "error": {
                    "message": f"User '{user_id}' does not have required role 'admin'",
                    "type": "permission_error",
                    "code": HTTP_403_FORBIDDEN
                }
            }
        )
    
    # Log the request
    logger.info(f"List patterns request from user {user_id}")
    
    # Get patterns and settings
    patterns = [p.to_dict() for p in list_patterns()]
    settings = get_settings()
    
    # Format response
    return {
        "patterns": patterns,
        "count": len(patterns),
        "settings": settings,
        "timestamp": int(time.time())
    }


@router.post("/patterns")
async def create_pattern(
    name: str = Body(...),
    pattern: str = Body(...),
    tool: str = Body(...),
    description: str = Body(...),
    priority: int = Body(50),
    required_role: str = Body("basic"),
    enabled: bool = Body(True),
    api_key: str = Depends(verify_auth)
):
    """
    Add a new keyword pattern.
    
    Args:
        name: Pattern name
        pattern: Regex pattern
        tool: Tool to invoke
        description: Pattern description
        priority: Pattern priority (higher = checked first)
        required_role: Required role to use this pattern
        enabled: Whether the pattern is enabled
        api_key: The API key
        
    Returns:
        Added pattern
    """
    # Get user ID from API key
    user_id = auth.get_user_id(api_key)
    
    # Check rate limit
    auth.check_rate_limit(None, api_key)
    
    # Check if user has required role
    if not auth.has_role(user_id, "admin"):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail={
                "error": {
                    "message": f"User '{user_id}' does not have required role 'admin'",
                    "type": "permission_error",
                    "code": HTTP_403_FORBIDDEN
                }
            }
        )
    
    # Log the request
    logger.info(f"Create pattern request from user {user_id}")
    
    # Validate priority
    if priority < 0 or priority > 100:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail={
                "error": {
                    "message": "Priority must be between 0 and 100",
                    "type": "validation_error",
                    "code": HTTP_400_BAD_REQUEST
                }
            }
        )
    
    # Add pattern
    try:
        pattern_obj = KeywordPattern(
            name=name,
            pattern=pattern,
            tool=tool,
            description=description,
            priority=priority,
            required_role=required_role,
            enabled=enabled
        )
        
        register_pattern(pattern_obj)
        
        # Format response
        return {
            "pattern": pattern_obj.to_dict(),
            "timestamp": int(time.time())
        }
    except Exception as e:
        logger.error(f"Failed to add pattern: {e}")
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail={
                "error": {
                    "message": f"Failed to add pattern: {str(e)}",
                    "type": "pattern_error",
                    "code": HTTP_400_BAD_REQUEST
                }
            }
        )


@router.put("/patterns/{name}")
async def update_pattern_endpoint(
    name: str = Path(...),
    pattern: Optional[str] = Body(None),
    tool: Optional[str] = Body(None),
    description: Optional[str] = Body(None),
    priority: Optional[int] = Body(None),
    required_role: Optional[str] = Body(None),
    enabled: Optional[bool] = Body(None),
    api_key: str = Depends(verify_auth)
):
    """
    Update an existing keyword pattern.
    
    Args:
        name: Pattern name
        pattern: Regex pattern
        tool: Tool to invoke
        description: Pattern description
        priority: Pattern priority (higher = checked first)
        required_role: Required role to use this pattern
        enabled: Whether the pattern is enabled
        api_key: The API key
        
    Returns:
        Updated pattern
    """
    # Get user ID from API key
    user_id = auth.get_user_id(api_key)
    
    # Check rate limit
    auth.check_rate_limit(None, api_key)
    
    # Check if user has required role
    if not auth.has_role(user_id, "admin"):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail={
                "error": {
                    "message": f"User '{user_id}' does not have required role 'admin'",
                    "type": "permission_error",
                    "code": HTTP_403_FORBIDDEN
                }
            }
        )
    
    # Log the request
    logger.info(f"Update pattern request from user {user_id}")
    
    # Validate priority
    if priority is not None and (priority < 0 or priority > 100):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail={
                "error": {
                    "message": "Priority must be between 0 and 100",
                    "type": "validation_error",
                    "code": HTTP_400_BAD_REQUEST
                }
            }
        )
    
    # Get existing pattern
    existing_pattern = get_pattern(name)
    if not existing_pattern:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail={
                "error": {
                    "message": f"Pattern '{name}' not found",
                    "type": "not_found",
                    "code": HTTP_404_NOT_FOUND
                }
            }
        )
    
    # Update pattern
    try:
        # Track updated fields
        updated_fields = []
        
        # Update fields
        if pattern is not None and pattern != existing_pattern.pattern:
            existing_pattern.pattern = pattern
            existing_pattern.compile_pattern()
            updated_fields.append("pattern")
        
        if tool is not None and tool != existing_pattern.tool:
            existing_pattern.tool = tool
            updated_fields.append("tool")
        
        if description is not None and description != existing_pattern.description:
            existing_pattern.description = description
            updated_fields.append("description")
        
        if priority is not None and priority != existing_pattern.priority:
            existing_pattern.priority = priority
            updated_fields.append("priority")
        
        if required_role is not None and required_role != existing_pattern.required_role:
            existing_pattern.required_role = required_role
            updated_fields.append("required_role")
        
        if enabled is not None and enabled != existing_pattern.enabled:
            existing_pattern.enabled = enabled
            updated_fields.append("enabled")
        
        # Format response
        return {
            "pattern": existing_pattern.to_dict(),
            "updated_fields": updated_fields,
            "timestamp": int(time.time())
        }
    except Exception as e:
        logger.error(f"Failed to update pattern: {e}")
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail={
                "error": {
                    "message": f"Failed to update pattern: {str(e)}",
                    "type": "pattern_error",
                    "code": HTTP_400_BAD_REQUEST
                }
            }
        )


@router.delete("/patterns/{name}")
async def delete_pattern_endpoint(
    name: str = Path(...),
    api_key: str = Depends(verify_auth)
):
    """
    Delete a keyword pattern.
    
    Args:
        name: Pattern name
        api_key: The API key
        
    Returns:
        Deletion result
    """
    # Get user ID from API key
    user_id = auth.get_user_id(api_key)
    
    # Check rate limit
    auth.check_rate_limit(None, api_key)
    
    # Check if user has required role
    if not auth.has_role(user_id, "admin"):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail={
                "error": {
                    "message": f"User '{user_id}' does not have required role 'admin'",
                    "type": "permission_error",
                    "code": HTTP_403_FORBIDDEN
                }
            }
        )
    
    # Log the request
    logger.info(f"Delete pattern request from user {user_id}")
    
    # Get existing pattern
    existing_pattern = get_pattern(name)
    if not existing_pattern:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail={
                "error": {
                    "message": f"Pattern '{name}' not found",
                    "type": "not_found",
                    "code": HTTP_404_NOT_FOUND
                }
            }
        )
    
    # Delete pattern
    try:
        # Remove from registry
        from src.app.keywords.registry import KEYWORD_REGISTRY
        if name in KEYWORD_REGISTRY:
            del KEYWORD_REGISTRY[name]
            
        # Format response
        return {
            "success": True,
            "name": name,
            "timestamp": int(time.time())
        }
    except Exception as e:
        logger.error(f"Failed to delete pattern: {e}")
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail={
                "error": {
                    "message": f"Failed to delete pattern: {str(e)}",
                    "type": "pattern_error",
                    "code": HTTP_400_BAD_REQUEST
                }
            }
        )


@router.get("/settings")
async def get_settings_endpoint(
    api_key: str = Depends(verify_auth)
):
    """
    Get keyword detection settings.
    
    Args:
        api_key: The API key
        
    Returns:
        Keyword detection settings
    """
    # Get user ID from API key
    user_id = auth.get_user_id(api_key)
    
    # Check rate limit
    auth.check_rate_limit(None, api_key)
    
    # Check if user has required role
    if not auth.has_role(user_id, "admin"):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail={
                "error": {
                    "message": f"User '{user_id}' does not have required role 'admin'",
                    "type": "permission_error",
                    "code": HTTP_403_FORBIDDEN
                }
            }
        )
    
    # Log the request
    logger.info(f"Get settings request from user {user_id}")
    
    # Get settings
    settings = get_settings()
    
    # Format response
    return {
        "settings": settings,
        "timestamp": int(time.time())
    }


@router.put("/settings")
async def update_settings_endpoint(
    enable_detection: Optional[bool] = Body(None),
    detection_threshold: Optional[float] = Body(None),
    default_role: Optional[str] = Body(None),
    api_key: str = Depends(verify_auth)
):
    """
    Update keyword detection settings.
    
    Args:
        enable_detection: Whether to enable keyword detection
        detection_threshold: Threshold for keyword detection
        default_role: Default role for users
        api_key: The API key
        
    Returns:
        Updated settings
    """
    # Get user ID from API key
    user_id = auth.get_user_id(api_key)
    
    # Check rate limit
    auth.check_rate_limit(None, api_key)
    
    # Check if user has required role
    if not auth.has_role(user_id, "admin"):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail={
                "error": {
                    "message": f"User '{user_id}' does not have required role 'admin'",
                    "type": "permission_error",
                    "code": HTTP_403_FORBIDDEN
                }
            }
        )
    
    # Log the request
    logger.info(f"Update settings request from user {user_id}")
    
    # Validate threshold
    if detection_threshold is not None and (detection_threshold < 0 or detection_threshold > 1):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail={
                "error": {
                    "message": "Detection threshold must be between 0 and 1",
                    "type": "validation_error",
                    "code": HTTP_400_BAD_REQUEST
                }
            }
        )
    
    # Update settings
    try:
        # Track updated fields
        updated_fields = []
        
        # Update settings
        global ENABLE_KEYWORD_DETECTION, DETECTION_THRESHOLD
        
        if enable_detection is not None and enable_detection != ENABLE_KEYWORD_DETECTION:
            ENABLE_KEYWORD_DETECTION = enable_detection
            updated_fields.append("enable_detection")
        
        if detection_threshold is not None and detection_threshold != DETECTION_THRESHOLD:
            DETECTION_THRESHOLD = detection_threshold
            updated_fields.append("detection_threshold")
        
        # Get updated settings
        settings = get_settings()
        
        # Format response
        return {
            "settings": settings,
            "updated_fields": updated_fields,
            "timestamp": int(time.time())
        }
    except Exception as e:
        logger.error(f"Failed to update settings: {e}")
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail={
                "error": {
                    "message": f"Failed to update settings: {str(e)}",
                    "type": "settings_error",
                    "code": HTTP_400_BAD_REQUEST
                }
            }
        )


def get_settings() -> Dict[str, Any]:
    """
    Get keyword detection settings.
    
    Returns:
        Dictionary of settings
    """
    return {
        "enable_detection": ENABLE_KEYWORD_DETECTION,
        "detection_threshold": DETECTION_THRESHOLD
    }