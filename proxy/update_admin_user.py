#!/usr/bin/env python3
"""
Update admin user in the database.

This script updates the admin user in the database with the API key from the .env file.
"""
import os
import sys
import asyncio
import logging
from argparse import ArgumentParser
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("update_admin_user")

async def find_user_by_api_key(api_key):
    """
    Find a user by API key.
    
    Args:
        api_key: The API key to look up
        
    Returns:
        The user object if found, None otherwise
    """
    from src.app.database import SessionLocal, User
    from sqlalchemy import select
    
    try:
        async with SessionLocal() as session:
            query = select(User).where(User.api_key == api_key)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            return user
    except Exception as e:
        logger.error(f"Error finding user by API key: {e}")
        return None

async def update_admin_user(user_id, api_key):
    """
    Update or create an admin user in the database.
    
    Args:
        user_id: The user ID for the admin user
        api_key: The API key for the admin user
    """
    from src.app.database import SessionLocal, User, Role, UserRole
    from sqlalchemy import select, update
    
    logger.info(f"Updating admin user: {user_id}")
    
    try:
        # First, check if the API key is already in use
        existing_user = await find_user_by_api_key(api_key)
        if existing_user and existing_user.user_id != user_id:
            logger.warning(f"API key is already in use by user '{existing_user.user_id}'")
            logger.info(f"Updating user '{existing_user.user_id}' to have admin role instead")
            user_id = existing_user.user_id
        
        async with SessionLocal() as session:
            # Check if user exists
            user_query = select(User).where(User.user_id == user_id)
            user_result = await session.execute(user_query)
            user = user_result.scalar_one_or_none()
            
            if not user:
                # Create new user
                new_user = User(
                    user_id=user_id,
                    api_key=api_key
                )
                session.add(new_user)
                await session.commit()
                
                # Refresh to get the ID
                await session.refresh(new_user)
                user = new_user
                logger.info(f"Created user: {user_id}")
            else:
                # Update API key if it changed and not already in use by another user
                if user.api_key != api_key and not existing_user:
                    user.api_key = api_key
                    await session.commit()
                    logger.info(f"Updated API key for user: {user_id}")
                else:
                    logger.info(f"User already exists: {user_id}")
            
            # Get admin role
            role_query = select(Role).where(Role.name == "admin")
            role_result = await session.execute(role_query)
            admin_role = role_result.scalar_one_or_none()
            
            if not admin_role:
                logger.error("Admin role not found")
                return False
            
            # Check if user already has admin role
            user_role_query = select(UserRole).where(
                UserRole.user_id == user.id,
                UserRole.role_id == admin_role.id
            )
            user_role_result = await session.execute(user_role_query)
            user_role = user_role_result.scalar_one_or_none()
            
            if not user_role:
                # Assign admin role to user
                new_user_role = UserRole(
                    user_id=user.id,
                    role_id=admin_role.id
                )
                session.add(new_user_role)
                await session.commit()
                logger.info(f"Assigned admin role to user: {user_id}")
            else:
                logger.info(f"User already has admin role: {user_id}")
        
        logger.info(f"Admin user {user_id} updated successfully")
        return True
    except Exception as e:
        logger.error(f"Error updating admin user: {e}")
        return False

async def main():
    """Main function to update the admin user."""
    parser = ArgumentParser(description="Update admin user in the database")
    parser.add_argument("--user", default="admin", help="Admin user ID (default: admin)")
    parser.add_argument("--key", help="Admin API key (default: from .env)")
    args = parser.parse_args()
    
    # Get admin API key from arguments or .env
    api_key = args.key
    if not api_key:
        # Try to get from .env
        from src.app.config import ADMIN_API_KEY, API_KEY
        api_key = ADMIN_API_KEY or API_KEY
        
        if not api_key:
            logger.error("No API key provided and none found in .env")
            return False
    
    logger.info(f"Using API key: {api_key[:5]}...")
    
    # Update admin user
    if not await update_admin_user(args.user, api_key):
        return False
    
    logger.info("Admin user updated successfully")
    return True

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)