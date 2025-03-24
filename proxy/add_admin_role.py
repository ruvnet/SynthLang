#!/usr/bin/env python3
"""
Add admin role to a user.
"""
import sys
from src.app.auth.roles import add_user_role, USER_ROLES

def main():
    """Add admin role to a user."""
    if len(sys.argv) < 2:
        print("Usage: python add_admin_role.py <user_id>")
        return
    
    user_id = sys.argv[1]
    add_user_role(user_id, "admin")
    print(f"Added admin role to user '{user_id}'")
    print(f"User roles: {USER_ROLES.get(user_id, [])}")

if __name__ == "__main__":
    main()