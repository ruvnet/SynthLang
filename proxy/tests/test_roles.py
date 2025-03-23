"""
Tests for the role-based access control system.

This module contains tests for the role management functions.
"""
import pytest
from unittest.mock import patch
import os

from app.auth.roles import (
    init_user_roles,
    get_user_roles,
    has_role,
    add_user_role,
    remove_user_role,
    USER_ROLES,
    DEFAULT_ROLES,
    ROLE_HIERARCHY
)

@pytest.fixture
def reset_user_roles():
    """Reset USER_ROLES before and after tests."""
    # Save original
    original = USER_ROLES.copy()
    
    # Clear for test
    USER_ROLES.clear()
    
    yield
    
    # Restore original
    USER_ROLES.clear()
    USER_ROLES.update(original)

def test_init_user_roles():
    """Test that init_user_roles loads roles from environment variables."""
    with patch.dict(os.environ, {
        "ADMIN_USERS": "admin1,admin2",
        "PREMIUM_USERS": "premium1,premium2"
    }):
        # Clear existing roles
        USER_ROLES.clear()
        
        # Initialize roles
        init_user_roles()
        
        # Check admin users
        assert "admin1" in USER_ROLES
        assert "admin2" in USER_ROLES
        assert "admin" in USER_ROLES["admin1"]
        assert "admin" in USER_ROLES["admin2"]
        
        # Check premium users
        assert "premium1" in USER_ROLES
        assert "premium2" in USER_ROLES
        assert "premium" in USER_ROLES["premium1"]
        assert "premium" in USER_ROLES["premium2"]

def test_get_user_roles_direct(reset_user_roles):
    """Test that get_user_roles returns directly assigned roles."""
    # Assign roles
    USER_ROLES["test_user"] = ["admin"]
    
    # Get roles
    roles = get_user_roles("test_user")
    
    # Check roles
    assert "admin" in roles
    assert "premium" in roles  # Inherited from admin
    assert "basic" in roles    # Inherited from admin and premium

def test_get_user_roles_default(reset_user_roles):
    """Test that get_user_roles returns default roles for unknown users."""
    # Get roles for unknown user
    roles = get_user_roles("unknown_user")
    
    # Check roles
    assert roles == DEFAULT_ROLES

def test_get_user_roles_inheritance(reset_user_roles):
    """Test that get_user_roles includes inherited roles."""
    # Assign roles
    USER_ROLES["test_user"] = ["premium"]
    
    # Get roles
    roles = get_user_roles("test_user")
    
    # Check roles
    assert "premium" in roles
    assert "basic" in roles    # Inherited from premium
    assert "admin" not in roles  # Not assigned or inherited

def test_has_role_direct(reset_user_roles):
    """Test that has_role returns True for directly assigned roles."""
    # Assign roles
    USER_ROLES["test_user"] = ["admin"]
    
    # Check role
    assert has_role("test_user", "admin") is True

def test_has_role_inherited(reset_user_roles):
    """Test that has_role returns True for inherited roles."""
    # Assign roles
    USER_ROLES["test_user"] = ["admin"]
    
    # Check inherited roles
    assert has_role("test_user", "premium") is True
    assert has_role("test_user", "basic") is True

def test_has_role_missing(reset_user_roles):
    """Test that has_role returns False for missing roles."""
    # Assign roles
    USER_ROLES["test_user"] = ["basic"]
    
    # Check missing role
    assert has_role("test_user", "admin") is False
    assert has_role("test_user", "premium") is False

def test_add_user_role_new_user(reset_user_roles):
    """Test that add_user_role creates a new user entry if needed."""
    # Add role to new user
    add_user_role("new_user", "admin")
    
    # Check user and role
    assert "new_user" in USER_ROLES
    assert "admin" in USER_ROLES["new_user"]
    assert "basic" in USER_ROLES["new_user"]  # Default role should be included

def test_add_user_role_existing_user(reset_user_roles):
    """Test that add_user_role adds a role to an existing user."""
    # Create user
    USER_ROLES["test_user"] = ["basic"]
    
    # Add role
    add_user_role("test_user", "premium")
    
    # Check roles
    assert "basic" in USER_ROLES["test_user"]
    assert "premium" in USER_ROLES["test_user"]

def test_add_user_role_duplicate(reset_user_roles):
    """Test that add_user_role doesn't add duplicate roles."""
    # Create user with role
    USER_ROLES["test_user"] = ["admin"]
    
    # Add same role again
    add_user_role("test_user", "admin")
    
    # Check roles (should only have one instance of the role)
    assert USER_ROLES["test_user"].count("admin") == 1

def test_remove_user_role(reset_user_roles):
    """Test that remove_user_role removes a role from a user."""
    # Create user with roles
    USER_ROLES["test_user"] = ["admin", "premium"]
    
    # Remove role
    remove_user_role("test_user", "admin")
    
    # Check roles
    assert "admin" not in USER_ROLES["test_user"]
    assert "premium" in USER_ROLES["test_user"]

def test_remove_user_role_default_fallback(reset_user_roles):
    """Test that remove_user_role assigns default roles if all roles are removed."""
    # Create user with single role
    USER_ROLES["test_user"] = ["premium"]
    
    # Remove the role
    remove_user_role("test_user", "premium")
    
    # Check that default roles were assigned
    assert USER_ROLES["test_user"] == DEFAULT_ROLES

def test_remove_user_role_nonexistent(reset_user_roles):
    """Test that remove_user_role handles removing nonexistent roles."""
    # Create user with role
    USER_ROLES["test_user"] = ["basic"]
    
    # Remove nonexistent role (should not raise an error)
    remove_user_role("test_user", "admin")
    
    # Check roles are unchanged
    assert USER_ROLES["test_user"] == ["basic"]

def test_require_role_decorator():
    """Test the require_role decorator."""
    from app.auth.roles import require_role
    
    # Create a mock async function with the decorator
    @require_role("admin")
    async def mock_endpoint(user_id):
        return "Success"
    
    # Test with user that has the role
    with patch("app.auth.roles.has_role", return_value=True):
        # Should not raise an exception
        import asyncio
        result = asyncio.run(mock_endpoint(user_id="test_user"))
        assert result == "Success"
    
    # Test with user that doesn't have the role
    with patch("app.auth.roles.has_role", return_value=False):
        # Should raise a PermissionError
        with pytest.raises(PermissionError):
            asyncio.run(mock_endpoint(user_id="test_user"))