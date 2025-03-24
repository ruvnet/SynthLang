#!/usr/bin/env python3
"""
Initialize database with default roles and admin user.

This script creates the necessary database tables and populates them with
default roles (basic, premium, admin) and an admin user.
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
logger = logging.getLogger("init_db_roles")

async def init_database():
    """Initialize the database tables."""
    from src.app.database import init_db
    
    logger.info("Initializing database tables...")
    result = await init_db()
    
    if result:
        logger.info("Database tables initialized successfully")
    else:
        logger.error("Failed to initialize database tables")
        return False
    
    return True

async def create_default_roles():
    """Create default roles in the database."""
    from src.app.database import SessionLocal, Role
    from sqlalchemy import select
    
    logger.info("Creating default roles...")
    
    try:
        async with SessionLocal() as session:
            # Define default roles
            default_roles = [
                {"name": "basic", "description": "Basic user with limited access"},
                {"name": "premium", "description": "Premium user with enhanced access"},
                {"name": "admin", "description": "Administrator with full access"}
            ]
            
            # Create roles if they don't exist
            for role_data in default_roles:
                # Check if role exists
                role_query = select(Role).where(Role.name == role_data["name"])
                role_result = await session.execute(role_query)
                role = role_result.scalar_one_or_none()
                
                if not role:
                    # Create new role
                    new_role = Role(
                        name=role_data["name"],
                        description=role_data["description"]
                    )
                    session.add(new_role)
                    logger.info(f"Created role: {role_data['name']}")
                else:
                    logger.info(f"Role already exists: {role_data['name']}")
            
            # Commit changes
            await session.commit()
        
        logger.info("Default roles created successfully")
        return True
    except Exception as e:
        logger.error(f"Error creating default roles: {e}")
        return False

async def create_admin_user(user_id, api_key):
    """
    Create an admin user in the database.
    
    Args:
        user_id: The user ID for the admin user
        api_key: The API key for the admin user
    """
    from src.app.database import SessionLocal, User, Role, UserRole
    from sqlalchemy import select
    
    logger.info(f"Creating admin user: {user_id}")
    
    try:
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
                # Update API key if it changed
                if user.api_key != api_key:
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
        
        logger.info(f"Admin user {user_id} created/updated successfully")
        return True
    except Exception as e:
        logger.error(f"Error creating admin user: {e}")
        return False

async def init_db_security():
    """Initialize database security measures."""
    try:
        from src.app.db_security import initialize_db_security
        
        logger.info("Initializing database security measures...")
        initialize_db_security()
        logger.info("Database security measures initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Error initializing database security: {e}")
        return False

async def main():
    """Main function to initialize the database and create roles and admin user."""
    parser = ArgumentParser(description="Initialize database with roles and admin user")
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
    
    # Initialize database
    if not await init_database():
        return False
    
    # Initialize database security
    if os.getenv("USE_SQLITE", "0") == "1":
        if not await init_db_security():
            logger.warning("Failed to initialize database security")
    
    # Create default roles
    if not await create_default_roles():
        return False
    
    # Create admin user
    if not await create_admin_user(args.user, api_key):
        return False
    
    logger.info("Database initialization completed successfully")
    return True

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)