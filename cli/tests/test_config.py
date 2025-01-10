"""Tests for configuration management."""
import os
from pathlib import Path
from typing import Dict

import pytest
from pydantic import ValidationError

from synthlang.config import Config, ConfigManager
from synthlang.utils.env import load_env_file

def test_config_validation():
    """Test configuration validation."""
    valid_config = {
        "openai_api_key": "sk-test",
        "model": "gpt-4o-mini",
        "environment": "development",
        "log_level": "INFO"
    }
    config = Config(**valid_config)
    assert config.openai_api_key == "sk-test"
    assert config.model == "gpt-4"
    assert config.environment == "development"
    assert config.log_level == "INFO"

    # Test invalid config
    invalid_config = {
        "openai_api_key": "",  # Empty key
        "model": "invalid-model",
        "environment": "invalid",
        "log_level": "INVALID"
    }
    with pytest.raises(ValidationError):
        Config(**invalid_config)

def test_config_manager_load(tmp_path: Path):
    """Test ConfigManager load functionality."""
    # Create test .env file
    env_content = """
    OPENAI_API_KEY=sk-test
    SYNTHLANG_MODEL=gpt-4
    SYNTHLANG_ENV=development
    SYNTHLANG_LOG_LEVEL=INFO
    """
    env_file = tmp_path / ".env"
    env_file.write_text(env_content)

    # Test loading config from env file
    config_manager = ConfigManager()
    config = config_manager.load(env_file)

    assert config.openai_api_key == "sk-test"
    assert config.model == "gpt-4"
    assert config.environment == "development"
    assert config.log_level == "INFO"

def test_config_manager_save(tmp_path: Path):
    """Test ConfigManager save functionality."""
    config_file = tmp_path / "config.json"
    config = Config(
        openai_api_key="sk-test",
        model="gpt-4",
        environment="development",
        log_level="INFO"
    )

    config_manager = ConfigManager()
    config_manager.save(config, config_file)

    # Verify saved config
    assert config_file.exists()
    loaded_config = config_manager.load(config_file)
    assert loaded_config == config

def test_config_manager_update(tmp_path: Path):
    """Test ConfigManager update functionality."""
    config_file = tmp_path / "config.json"
    initial_config = Config(
        openai_api_key="sk-test",
        model="gpt-4",
        environment="development",
        log_level="INFO"
    )

    config_manager = ConfigManager()
    config_manager.save(initial_config, config_file)

    # Update config
    updates = {"model": "gpt-3.5-turbo", "log_level": "DEBUG"}
    updated_config = config_manager.update(config_file, updates)

    assert updated_config.model == "gpt-3.5-turbo"
    assert updated_config.log_level == "DEBUG"
    assert updated_config.openai_api_key == initial_config.openai_api_key
    assert updated_config.environment == initial_config.environment

def test_env_file_loading(tmp_path: Path):
    """Test environment file loading."""
    env_content = """
    OPENAI_API_KEY=sk-test
    SYNTHLANG_MODEL=gpt-4
    SYNTHLANG_ENV=development
    SYNTHLANG_LOG_LEVEL=INFO
    """
    env_file = tmp_path / ".env"
    env_file.write_text(env_content)

    env_vars = load_env_file(env_file)
    assert env_vars["OPENAI_API_KEY"] == "sk-test"
    assert env_vars["SYNTHLANG_MODEL"] == "gpt-4"
    assert env_vars["SYNTHLANG_ENV"] == "development"
    assert env_vars["SYNTHLANG_LOG_LEVEL"] == "INFO"

def test_config_environment_override(tmp_path: Path):
    """Test environment variable override of config values."""
    # Create base config
    config_file = tmp_path / "config.json"
    base_config = Config(
        openai_api_key="sk-base",
        model="gpt-4",
        environment="development",
        log_level="INFO"
    )
    
    config_manager = ConfigManager()
    config_manager.save(base_config, config_file)

    # Set environment variable to override
    os.environ["OPENAI_API_KEY"] = "sk-override"
    os.environ["SYNTHLANG_MODEL"] = "gpt-3.5-turbo"

    # Load config - should use environment values
    loaded_config = config_manager.load(config_file)
    assert loaded_config.openai_api_key == "sk-override"
    assert loaded_config.model == "gpt-3.5-turbo"

    # Clean up environment
    del os.environ["OPENAI_API_KEY"]
    del os.environ["SYNTHLANG_MODEL"]
