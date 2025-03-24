"""
Tests for the configuration module.

This module contains tests for the configuration loading functionality.
"""
import os
import pytest
import importlib
from unittest.mock import patch


def test_config_required_variables():
    """Test that required configuration variables are loaded correctly."""
    # Mock environment variables
    mock_env = {
        "OPENAI_API_KEY": "test-api-key",
        "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        "ENCRYPTION_KEY": "test-encryption-key"
    }
    
    with patch.dict(os.environ, mock_env, clear=True):
        # Force reload of the module
        import app.config
        importlib.reload(app.config)
        
        # Check required variables
        assert app.config.OPENAI_API_KEY == "test-api-key"
        assert app.config.DATABASE_URL == "postgresql+asyncpg://user:pass@localhost/db"
        assert app.config.ENCRYPTION_KEY == "test-encryption-key"


def test_config_optional_variables_defaults():
    """Test that optional configuration variables use default values when not set."""
    # Mock environment with only required variables
    mock_env = {
        "OPENAI_API_KEY": "test-api-key",
        "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        "ENCRYPTION_KEY": "test-encryption-key"
    }
    
    with patch.dict(os.environ, mock_env, clear=True):
        # Force reload of the module
        import app.config
        importlib.reload(app.config)
        
        # Check default values for optional variables
        assert app.config.USE_SYNTHLANG is True
        assert app.config.MASK_PII_BEFORE_LLM is False
        assert app.config.MASK_PII_IN_LOGS is True
        assert app.config.DEFAULT_RATE_LIMIT_QPM == 60


def test_config_optional_variables_custom():
    """Test that optional configuration variables can be customized."""
    # Mock environment with custom values
    mock_env = {
        "OPENAI_API_KEY": "test-api-key",
        "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        "ENCRYPTION_KEY": "test-encryption-key",
        "USE_SYNTHLANG": "0",
        "MASK_PII_BEFORE_LLM": "1",
        "MASK_PII_IN_LOGS": "0",
        "DEFAULT_RATE_LIMIT_QPM": "120"
    }
    
    with patch.dict(os.environ, mock_env, clear=True):
        # Force reload of the module
        import app.config
        importlib.reload(app.config)
        
        # Check custom values
        assert app.config.USE_SYNTHLANG is False
        assert app.config.MASK_PII_BEFORE_LLM is True
        assert app.config.MASK_PII_IN_LOGS is False
        assert app.config.DEFAULT_RATE_LIMIT_QPM == 120


def test_config_model_provider():
    """Test that the MODEL_PROVIDER dictionary is correctly defined."""
    import app.config
    
    # Check that the MODEL_PROVIDER dictionary exists and has expected entries
    assert isinstance(app.config.MODEL_PROVIDER, dict)
    assert "gpt-4o-search-preview" in app.config.MODEL_PROVIDER
    assert "gpt-4o-mini-search-preview" in app.config.MODEL_PROVIDER
    assert "o3-mini" in app.config.MODEL_PROVIDER
    
    # Check values
    assert app.config.MODEL_PROVIDER["gpt-4o-search-preview"] == "openai"
    assert app.config.MODEL_PROVIDER["gpt-4o-mini-search-preview"] == "openai"
    assert app.config.MODEL_PROVIDER["o3-mini"] == "openai"