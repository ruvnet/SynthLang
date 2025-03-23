"""
Tests for the user roles database initialization.

This module contains tests to verify that user roles are properly loaded from the database.
"""
import pytest
import asyncio
from unittest.mock import patch, MagicMock

from app.auth.roles import USER_ROLES

@pytest.mark.asyncio
async def test_user_roles_loaded_on_startup():
    """Test that user roles are loaded during application startup."""
    from app.main import lifespan
    
    # Mock FastAPI app
    mock_app = MagicMock()
    
    # Patch the init_user_roles function
    with patch('app.auth.init_user_roles') as mock_init_roles, \
         patch('app.auth.load_api_keys_from_db') as mock_load_api_keys:
        
        # Call the lifespan function
        cm = lifespan(mock_app)
        # Run the startup code
        await cm.__aenter__()
        
        # Check that init_user_roles was called
        mock_init_roles.assert_called_once()
        
        # Check that load_api_keys_from_db was called
        mock_load_api_keys.assert_called_once()

@pytest.mark.asyncio
async def test_main_py_has_correct_initialization_code():
    """Test that main.py contains the code to initialize user roles and API keys."""
    import os
    
    # Read the main.py file
    main_py_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'app', 'main.py')
    with open(main_py_path, 'r') as f:
        main_py_content = f.read()
    
    # Check that the initialization code is present
    assert 'await auth.init_user_roles()' in main_py_content
    assert 'await auth.load_api_keys_from_db()' in main_py_content
    assert 'User roles initialized successfully' in main_py_content
    assert 'API keys loaded successfully' in main_py_content

if __name__ == "__main__":
    asyncio.run(pytest.main(["-xvs", __file__]))