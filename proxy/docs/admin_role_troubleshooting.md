# Admin Role Troubleshooting Guide

## Common Issue: "Admin role required" Error

If you encounter an "Admin role required" error when trying to access admin-only endpoints (like `/v1/cache/stats`), it's likely due to a mismatch between the user ID in the database and what the code is expecting.

## Understanding the Issue

The SynthLang proxy uses a role-based access control system:

1. User roles are stored in the database
2. When the application starts, it loads these roles into memory
3. The `db_auth.py` file contains default environment variable handling that expects an admin user with the ID 'admin_user'
4. If your database has a user with the 'admin' role but a different user ID, you'll get this error

## How to Fix It

### Option 1: Update the Database (Recommended)

You can update the user ID in the database to match what the code expects:

```python
# Create a script similar to fix_admin_user.py
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set SQLite database path
os.environ["USE_SQLITE"] = "1"
os.environ["SQLITE_PATH"] = "sqlite+aiosqlite:///./synthlang_proxy.db"

from src.app.database import init_db, SessionLocal, User
from sqlalchemy import select

async def main():
    # Initialize the database
    await init_db()
    
    # Get the admin API key
    admin_api_key = os.environ.get("ADMIN_API_KEY") or os.environ.get("API_KEY")
    
    # Update the user_id in the database
    async with SessionLocal() as session:
        query = select(User).where(User.api_key == admin_api_key)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        
        if user and user.user_id == 'admin':
            user.user_id = 'admin_user'
            await session.commit()
            print("Updated user_id from 'admin' to 'admin_user'")

if __name__ == "__main__":
    asyncio.run(main())
```

### Option 2: Update the Code

Alternatively, you can modify `src/app/auth/db_auth.py` to use 'admin' instead of 'admin_user':

```python
# Find this line in db_auth.py
API_KEY_CACHE[ADMIN_API_KEY] = {"user_id": "admin_user", "rate_limit_qpm": PREMIUM_RATE_LIMIT_QPM}

# Change it to:
API_KEY_CACHE[ADMIN_API_KEY] = {"user_id": "admin", "rate_limit_qpm": PREMIUM_RATE_LIMIT_QPM}
```

## Verifying the Fix

After applying either fix, restart the server and test the admin endpoint:

```bash
curl -s -X GET "http://localhost:8000/v1/cache/stats" -H "Authorization: Bearer YOUR_ADMIN_API_KEY" | jq
```

You should now see the cache statistics instead of the "Admin role required" error.

## Checking User Roles

If you need to check the current user roles in the database, you can use this script:

```python
#!/usr/bin/env python3
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set SQLite database path
os.environ["USE_SQLITE"] = "1"
os.environ["SQLITE_PATH"] = "sqlite+aiosqlite:///./synthlang_proxy.db"

from src.app.auth.roles import USER_ROLES, init_user_roles
from src.app.database import init_db
from src.app.auth.db_auth import load_api_keys_from_db

async def main():
    # Initialize the database
    await init_db()
    
    # Initialize user roles
    await init_user_roles()
    
    # Load API keys
    await load_api_keys_from_db()
    
    # Print user roles
    print("\nCurrent user roles:")
    for user_id, roles in USER_ROLES.items():
        print(f"  {user_id}: {roles}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Technical Details

The issue occurs because:

1. In `db_auth.py`, the default admin API key is associated with the user ID 'admin_user'
2. In the database, the user with the admin role might have a different user ID (like 'admin')
3. When the application checks if a user has the admin role, it looks up the user ID from the API key
4. If the user ID doesn't match what's in the database, the role check fails

The fix ensures that the user ID in the database matches what the code expects, allowing the admin role check to succeed.