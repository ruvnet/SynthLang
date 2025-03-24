"""Tests for configuration management."""
import os
import pytest
from pydantic import ValidationError

from synthlang.config import Config, ConfigManager

def test_config_validation():
    """Test configuration validation."""
    # Test with environment variables
    os.environ["OPENAI_API_KEY"] = "sk-test"
    os.environ["SYNTHLANG_MODEL"] = "gpt-4o-mini"
    os.environ["SYNTHLANG_ENV"] = "development"
    os.environ["SYNTHLANG_LOG_LEVEL"] = "INFO"

    config = Config()
    assert config.openai_api_key == "sk-test"
    assert config.model == "gpt-4o-mini"
    assert config.environment == "development"
    assert config.log_level == "INFO"

    # Clean up
    del os.environ["OPENAI_API_KEY"]
    del os.environ["SYNTHLANG_MODEL"]
    del os.environ["SYNTHLANG_ENV"]
    del os.environ["SYNTHLANG_LOG_LEVEL"]

def test_config_defaults():
    """Test configuration defaults."""
    config = Config()
    assert config.openai_api_key == ""  # Empty default
    assert config.model == "gpt-4o-mini"
    assert config.environment == "production"
    assert config.log_level == "INFO"

def test_config_manager_load():
    """Test ConfigManager load functionality."""
    os.environ["OPENAI_API_KEY"] = "sk-test"
    os.environ["SYNTHLANG_MODEL"] = "gpt-4o-mini"
    
    config_manager = ConfigManager()
    config = config_manager.load()

    assert config.openai_api_key == "sk-test"
    assert config.model == "gpt-4o-mini"
    assert config.environment == "production"  # Default value
    assert config.log_level == "INFO"  # Default value

    # Clean up
    del os.environ["OPENAI_API_KEY"]
    del os.environ["SYNTHLANG_MODEL"]

def test_config_manager_update():
    """Test ConfigManager update functionality."""
    os.environ["OPENAI_API_KEY"] = "sk-test"
    config_manager = ConfigManager()
    
    # Update config
    updates = {"model": "gpt-3.5-turbo", "log_level": "DEBUG"}
    updated_config = config_manager.update(updates)

    assert updated_config.model == "gpt-3.5-turbo"
    assert updated_config.log_level == "DEBUG"
    assert updated_config.openai_api_key == "sk-test"
    assert updated_config.environment == "production"  # Default value

    # Verify environment variables were updated
    assert os.environ["SYNTHLANG_MODEL"] == "gpt-3.5-turbo"
    assert os.environ["SYNTHLANG_LOG_LEVEL"] == "DEBUG"

    # Clean up
    del os.environ["OPENAI_API_KEY"]
    del os.environ["SYNTHLANG_MODEL"]
    del os.environ["SYNTHLANG_LOG_LEVEL"]

def test_invalid_config_update():
    """Test invalid configuration updates."""
    config_manager = ConfigManager()
    
    # Test invalid key
    with pytest.raises(ValueError, match="Invalid configuration key"):
        config_manager.update({"invalid_key": "value"})
