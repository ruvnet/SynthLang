#!/usr/bin/env python3
"""
Check user roles in the database.
"""
import asyncio
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set SQLite database path
os.environ["USE_SQLITE"] = "1"
os.environ["SQLITE_PATH"] = "sqlite+aiosqlite:///./synthlang_proxy.db"

from src.app.auth.roles import USER_ROLES, init_user_roles
from src.app.database import init_db
from src.app.auth.db_auth import load_api_keys_from_db

async def main():
    """Check user roles in the database."""
    try:
        # Initialize the database
        await init_db()
        print("Database initialized successfully")
        
        # Initialize user roles
        await init_user_roles()
        print("User roles initialized successfully")
        
        # Load API keys
        await load_api_keys_from_db()
        print("API keys loaded successfully")
        
        # Print user roles
        print("\nCurrent user roles:")
        for user_id, roles in USER_ROLES.items():
            print(f"  {user_id}: {roles}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())