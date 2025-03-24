#!/usr/bin/env python3
"""
Fix the admin user issue by updating the environment variable.
"""
import os
import asyncio
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set SQLite database path
os.environ["USE_SQLITE"] = "1"
os.environ["SQLITE_PATH"] = "sqlite+aiosqlite:///./synthlang_proxy.db"

from src.app.database import init_db, SessionLocal, User
from sqlalchemy import select, update

async def main():
    """Fix the admin user issue."""
    try:
        # Initialize the database
        await init_db()
        print("Database initialized successfully")
        
        # Get the admin API key
        admin_api_key = os.environ.get("ADMIN_API_KEY") or os.environ.get("API_KEY")
        if not admin_api_key:
            print("No admin API key found in environment variables")
            return
        
        print(f"Using admin API key: {admin_api_key[:5]}...")
        
        # Check if there's a user with this API key
        async with SessionLocal() as session:
            query = select(User).where(User.api_key == admin_api_key)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            
            if user:
                print(f"Found user with API key: {user.user_id}")
                
                # Update the user_id to 'admin_user' if it's 'admin'
                if user.user_id == 'admin':
                    user.user_id = 'admin_user'
                    await session.commit()
                    print(f"Updated user_id from 'admin' to 'admin_user'")
                elif user.user_id == 'admin_user':
                    print("User already has the correct user_id 'admin_user'")
                else:
                    print(f"User has unexpected user_id: {user.user_id}")
            else:
                print("No user found with the admin API key")
                
                # Create a new admin user
                new_user = User(user_id='admin_user', api_key=admin_api_key)
                session.add(new_user)
                await session.commit()
                print("Created new admin user with user_id 'admin_user'")
        
        print("\nPlease restart the server for changes to take effect.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())