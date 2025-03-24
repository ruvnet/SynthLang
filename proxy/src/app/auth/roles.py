"""
Role-based access control for the SynthLang Proxy.

This module provides functions for managing user roles and permissions.
"""
import os
import logging
from typing import Dict, List, Set, Optional
import asyncio
from sqlalchemy import select, insert, delete, update, text
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.database import SessionLocal, User, Role, UserRole

# Logger for this module
logger = logging.getLogger(__name__)

# In-memory cache of user roles for performance
USER_ROLES: Dict[str, List[str]] = {}

# Default roles for all users
DEFAULT_ROLES = ["basic"]

# Role hierarchy: role -> list of included roles
ROLE_HIERARCHY: Dict[str, List[str]] = {
    "admin": ["premium", "basic"],
    "premium": ["basic"],
    "basic": []
}

async def init_user_roles() -> None:
    """
    Initialize user roles from the database.
    
    This function loads role assignments from the database and caches them
    in memory for faster access.
    """
    try:
        # Clear the in-memory cache
        USER_ROLES.clear()
        
        # Load roles from database
        async with SessionLocal() as session:
            # Query all users and their roles
            query = text("""
                SELECT u.user_id, r.name 
                FROM users u
                JOIN user_roles ur ON u.id = ur.user_id
                JOIN roles r ON ur.role_id = r.id
            """)
            result = await session.execute(query)
            rows = result.fetchall()
            
            # Populate the in-memory cache
            for user_id, role_name in rows:
                if user_id not in USER_ROLES:
                    USER_ROLES[user_id] = []
                USER_ROLES[user_id].append(role_name)
        
        # Load admin users from environment variable for backward compatibility
        admin_users = os.getenv("ADMIN_USERS", "").split(",")
        for user in admin_users:
            if user.strip():
                if user.strip() not in USER_ROLES:
                    USER_ROLES[user.strip()] = ["admin"]
                elif "admin" not in USER_ROLES[user.strip()]:
                    USER_ROLES[user.strip()].append("admin")
                logger.info(f"Initialized admin role for user from env: {user.strip()}")
        
        # Load premium users from environment variable for backward compatibility
        premium_users = os.getenv("PREMIUM_USERS", "").split(",")
        for user in premium_users:
            if user.strip():
                if user.strip() not in USER_ROLES:
                    USER_ROLES[user.strip()] = ["premium"]
                elif "premium" not in USER_ROLES[user.strip()]:
                    USER_ROLES[user.strip()].append("premium")
                logger.info(f"Initialized premium role for user from env: {user.strip()}")
        
        logger.info(f"Initialized roles for {len(USER_ROLES)} users from database and environment")
    except Exception as e:
        logger.error(f"Error initializing user roles: {e}")
        # Ensure we have at least an empty cache
        USER_ROLES.clear()

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
    roles = get_user_roles(user_id)
    has_role = role in roles
    logger.info(f"Checking if user '{user_id}' has role '{role}': {has_role} (user roles: {roles})")
    return has_role

async def add_user_role_db(user_id: str, role: str) -> bool:
    """
    Add a role to a user in the database.
    
    Args:
        user_id: The user ID to add the role to
        role: The role name to add
        
    Returns:
        True if the role was added successfully, False otherwise
    """
    try:
        async with SessionLocal() as session:
            # Get the user
            user_query = select(User).where(User.user_id == user_id)
            user_result = await session.execute(user_query)
            user = user_result.scalar_one_or_none()
            
            if not user:
                logger.warning(f"User '{user_id}' not found in database")
                return False
            
            # Get the role
            role_query = select(Role).where(Role.name == role)
            role_result = await session.execute(role_query)
            role_obj = role_result.scalar_one_or_none()
            
            if not role_obj:
                logger.warning(f"Role '{role}' not found in database")
                return False
            
            # Check if the user already has this role
            user_role_query = select(UserRole).where(
                UserRole.user_id == user.id,
                UserRole.role_id == role_obj.id
            )
            user_role_result = await session.execute(user_role_query)
            user_role = user_role_result.scalar_one_or_none()
            
            if user_role:
                logger.info(f"User '{user_id}' already has role '{role}'")
                return True
            
            # Add the role to the user
            new_user_role = UserRole(user_id=user.id, role_id=role_obj.id)
            session.add(new_user_role)
            await session.commit()
            
            # Update in-memory cache
            if user_id not in USER_ROLES:
                USER_ROLES[user_id] = [role]
            elif role not in USER_ROLES[user_id]:
                USER_ROLES[user_id].append(role)
            
            logger.info(f"Added role '{role}' to user '{user_id}' in database")
            return True
    except Exception as e:
        logger.error(f"Error adding role '{role}' to user '{user_id}': {e}")
        return False

def add_user_role(user_id: str, role: str) -> None:
    """
    Add a role to a user.
    
    This function updates both the in-memory cache and the database.
    
    Args:
        user_id: The user ID to add the role to
        role: The role name to add
    """
    if role not in ROLE_HIERARCHY and role != "basic":
        logger.warning(f"Adding unknown role '{role}' to user '{user_id}'")
    
    # Update in-memory cache immediately
    if user_id not in USER_ROLES:
        USER_ROLES[user_id] = DEFAULT_ROLES.copy()
    
    if role not in USER_ROLES[user_id]:
        USER_ROLES[user_id].append(role)
        logger.info(f"Added role '{role}' to user '{user_id}' in memory")
    
    # Schedule database update asynchronously
    asyncio.create_task(add_user_role_db(user_id, role))

async def remove_user_role_db(user_id: str, role: str) -> bool:
    """
    Remove a role from a user in the database.
    
    Args:
        user_id: The user ID to remove the role from
        role: The role name to remove
        
    Returns:
        True if the role was removed successfully, False otherwise
    """
    try:
        async with SessionLocal() as session:
            # Get the user
            user_query = select(User).where(User.user_id == user_id)
            user_result = await session.execute(user_query)
            user = user_result.scalar_one_or_none()
            
            if not user:
                logger.warning(f"User '{user_id}' not found in database")
                return False
            
            # Get the role
            role_query = select(Role).where(Role.name == role)
            role_result = await session.execute(role_query)
            role_obj = role_result.scalar_one_or_none()
            
            if not role_obj:
                logger.warning(f"Role '{role}' not found in database")
                return False
            
            # Remove the role from the user
            delete_query = delete(UserRole).where(
                UserRole.user_id == user.id,
                UserRole.role_id == role_obj.id
            )
            await session.execute(delete_query)
            await session.commit()
            
            logger.info(f"Removed role '{role}' from user '{user_id}' in database")
            return True
    except Exception as e:
        logger.error(f"Error removing role '{role}' from user '{user_id}': {e}")
        return False

def remove_user_role(user_id: str, role: str) -> None:
    """
    Remove a role from a user.
    
    This function updates both the in-memory cache and the database.
    
    Args:
        user_id: The user ID to remove the role from
        role: The role name to remove
    """
    # Update in-memory cache immediately
    if user_id in USER_ROLES and role in USER_ROLES[user_id]:
        USER_ROLES[user_id].remove(role)
        logger.info(f"Removed role '{role}' from user '{user_id}' in memory")
        
        # If user has no roles left, assign default roles
        if not USER_ROLES[user_id]:
            USER_ROLES[user_id] = DEFAULT_ROLES.copy()
            logger.info(f"Assigned default roles to user '{user_id}' in memory")
    
    # Schedule database update asynchronously
    asyncio.create_task(remove_user_role_db(user_id, role))

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
            # Extract API key from kwargs
            api_key = kwargs.get("api_key")
            
            if not api_key:
                # Try to get it from the request
                request = None
                for arg in args:
                    if hasattr(arg, "headers"):
                        request = arg
                        break
                
                if not request and "request" in kwargs:
                    request = kwargs["request"]
                
                if not request:
                    raise ValueError("Request object not found")
                
                # Get API key from authorization header
                auth_header = request.headers.get("Authorization", "")
                if not auth_header:
                    raise ValueError("Missing Authorization header")
                
                parts = auth_header.split()
                if len(parts) != 2 or parts[0].lower() != "bearer":
                    raise ValueError("Invalid Authorization header format")
                
                api_key = parts[1]
            
            # Get user ID from API key
            from src.app.auth.api_keys import get_user_id
            user_id = get_user_id(api_key)
            
            if not user_id:
                raise ValueError(f"Invalid API key: {api_key}")
            
            # Check if user has the required role
            if not has_role(user_id, required_role):
                raise PermissionError(f"User '{user_id}' does not have required role '{required_role}'")
            
            # User has the required role, proceed with the function
            return await func(*args, **kwargs)
        
        return wrapper
    
    return decorator