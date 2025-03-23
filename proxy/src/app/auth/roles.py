"""
Role-based access control for the SynthLang Proxy.

This module provides functions for managing user roles and permissions.
"""
import os
import logging
from typing import Dict, List, Set, Optional

# Logger for this module
logger = logging.getLogger(__name__)

# User roles dictionary: user_id -> list of roles
USER_ROLES: Dict[str, List[str]] = {}

# Default roles for all users
DEFAULT_ROLES = ["basic"]

# Role hierarchy: role -> list of included roles
ROLE_HIERARCHY: Dict[str, List[str]] = {
    "admin": ["premium", "basic"],
    "premium": ["basic"],
    "basic": []
}

def init_user_roles() -> None:
    """
    Initialize user roles from configuration.
    
    This function loads role assignments from environment variables or other
    configuration sources.
    """
    # Example: Load admin users from environment variable
    admin_users = os.getenv("ADMIN_USERS", "").split(",")
    for user in admin_users:
        if user.strip():
            USER_ROLES[user.strip()] = ["admin"]
            logger.info(f"Initialized admin role for user: {user.strip()}")
    
    # Example: Load premium users from environment variable
    premium_users = os.getenv("PREMIUM_USERS", "").split(",")
    for user in premium_users:
        if user.strip():
            USER_ROLES[user.strip()] = ["premium"]
            logger.info(f"Initialized premium role for user: {user.strip()}")
    
    logger.info(f"Initialized roles for {len(USER_ROLES)} users")

def get_user_roles(user_id: str) -> List[str]:
    """
    Get all roles assigned to a user, including inherited roles.
    
    Args:
        user_id: The user ID to get roles for
        
    Returns:
        A list of role names assigned to the user
    """
    # Get directly assigned roles, or default roles if none assigned
    direct_roles = USER_ROLES.get(user_id, DEFAULT_ROLES.copy())
    
    # Include all inherited roles
    all_roles = set(direct_roles)
    for role in direct_roles:
        # Add all roles inherited from this role
        inherited = _get_inherited_roles(role)
        all_roles.update(inherited)
    
    return list(all_roles)

def _get_inherited_roles(role: str) -> Set[str]:
    """
    Get all roles inherited from a given role.
    
    Args:
        role: The role to get inherited roles for
        
    Returns:
        A set of inherited role names
    """
    inherited = set()
    
    # Add directly inherited roles
    direct_inherited = ROLE_HIERARCHY.get(role, [])
    inherited.update(direct_inherited)
    
    # Recursively add roles inherited from those roles
    for inherited_role in direct_inherited:
        inherited.update(_get_inherited_roles(inherited_role))
    
    return inherited

def has_role(user_id: str, role: str) -> bool:
    """
    Check if a user has a specific role.
    
    Args:
        user_id: The user ID to check
        role: The role name to check for
        
    Returns:
        True if the user has the role, False otherwise
    """
    return role in get_user_roles(user_id)

def add_user_role(user_id: str, role: str) -> None:
    """
    Add a role to a user.
    
    Args:
        user_id: The user ID to add the role to
        role: The role name to add
    """
    if role not in ROLE_HIERARCHY and role != "basic":
        logger.warning(f"Adding unknown role '{role}' to user '{user_id}'")
    
    if user_id not in USER_ROLES:
        USER_ROLES[user_id] = DEFAULT_ROLES.copy()
    
    if role not in USER_ROLES[user_id]:
        USER_ROLES[user_id].append(role)
        logger.info(f"Added role '{role}' to user '{user_id}'")

def remove_user_role(user_id: str, role: str) -> None:
    """
    Remove a role from a user.
    
    Args:
        user_id: The user ID to remove the role from
        role: The role name to remove
    """
    if user_id in USER_ROLES and role in USER_ROLES[user_id]:
        USER_ROLES[user_id].remove(role)
        logger.info(f"Removed role '{role}' from user '{user_id}'")
        
        # If user has no roles left, assign default roles
        if not USER_ROLES[user_id]:
            USER_ROLES[user_id] = DEFAULT_ROLES.copy()
            logger.info(f"Assigned default roles to user '{user_id}'")

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
            # Extract user_id from kwargs or request
            user_id = kwargs.get("user_id")
            
            # If user_id not in kwargs, try to get it from request
            if not user_id and "request" in kwargs:
                # This assumes the request has a user_id attribute
                user_id = getattr(kwargs["request"], "user_id", None)
            
            if not user_id:
                raise ValueError("User ID not found in request")
            
            # Check if user has the required role
            if not has_role(user_id, required_role):
                raise PermissionError(f"User '{user_id}' does not have required role '{required_role}'")
            
            # User has the required role, proceed with the function
            return await func(*args, **kwargs)
        
        return wrapper
    
    return decorator