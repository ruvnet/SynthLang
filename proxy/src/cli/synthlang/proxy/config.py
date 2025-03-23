"""Configuration utilities for SynthLang Proxy."""
import json
import os
from pathlib import Path
from typing import Dict, Optional, Any, Union

from pydantic import BaseModel, Field

from synthlang.utils.logger import get_logger

logger = get_logger(__name__)


class ProxyConfig(BaseModel):
    """Configuration model for SynthLang Proxy."""
    
    # API settings
    api_key: Optional[str] = Field(None, description="API key for authentication")
    endpoint: str = Field("https://api.synthlang.org", description="Proxy endpoint URL")
    default_model: str = Field("gpt-4o-mini", description="Default model to use")
    
    # Server settings
    host: str = Field("127.0.0.1", description="Host to bind server to")
    port: int = Field(8000, description="Port to bind server to")
    
    # Cache settings
    cache_dir: str = Field(str(Path.home() / ".synthlang" / "cache"), description="Cache directory")
    cache_ttl: int = Field(3600, description="Cache TTL in seconds")
    
    # Security settings
    enable_encryption: bool = Field(False, description="Enable encryption")
    encryption_key: Optional[str] = Field(None, description="Encryption key")
    
    # Rate limiting
    rate_limit_enabled: bool = Field(True, description="Enable rate limiting")
    rate_limit_requests: int = Field(60, description="Requests per minute")
    
    # Streaming
    streaming_enabled: bool = Field(True, description="Enable streaming responses")
    
    # Logging
    log_level: str = Field("info", description="Logging level")
    log_file: Optional[str] = Field(None, description="Log file path")


def get_config_path() -> Path:
    """Get path to config file.
    
    Returns:
        Path to config file
    """
    config_dir = Path.home() / ".synthlang"
    config_dir.mkdir(exist_ok=True)
    return config_dir / "proxy_config.json"


def load_config() -> Dict[str, Any]:
    """Load configuration from file.
    
    Returns:
        Configuration dictionary
    """
    config_path = get_config_path()
    config = {}
    
    # Load from file if exists
    if config_path.exists():
        try:
            with open(config_path) as f:
                config = json.load(f)
            logger.debug(f"Loaded config from {config_path}")
        except json.JSONDecodeError:
            logger.warning(f"Invalid JSON in config file: {config_path}")
    
    return config


def save_config(config: Dict[str, Any]) -> None:
    """Save configuration to file.
    
    Args:
        config: Configuration dictionary
    """
    config_path = get_config_path()
    
    try:
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)
        logger.debug(f"Saved config to {config_path}")
    except Exception as e:
        logger.error(f"Error saving config: {str(e)}")
        raise


def update_config(updates: Dict[str, Any]) -> Dict[str, Any]:
    """Update configuration with new values.
    
    Args:
        updates: Dictionary with updates
        
    Returns:
        Updated configuration
    """
    config = load_config()
    config.update(updates)
    save_config(config)
    return config


def get_env_config() -> Dict[str, Any]:
    """Get configuration from environment variables.
    
    Returns:
        Configuration from environment
    """
    env_config = {}
    
    # Map environment variables to config keys
    env_mapping = {
        "SYNTHLANG_API_KEY": "api_key",
        "SYNTHLANG_ENDPOINT": "endpoint",
        "SYNTHLANG_DEFAULT_MODEL": "default_model",
        "SYNTHLANG_HOST": "host",
        "SYNTHLANG_PORT": "port",
        "SYNTHLANG_CACHE_DIR": "cache_dir",
        "SYNTHLANG_CACHE_TTL": "cache_ttl",
        "SYNTHLANG_ENABLE_ENCRYPTION": "enable_encryption",
        "SYNTHLANG_ENCRYPTION_KEY": "encryption_key",
        "SYNTHLANG_RATE_LIMIT_ENABLED": "rate_limit_enabled",
        "SYNTHLANG_RATE_LIMIT_REQUESTS": "rate_limit_requests",
        "SYNTHLANG_STREAMING_ENABLED": "streaming_enabled",
        "SYNTHLANG_LOG_LEVEL": "log_level",
        "SYNTHLANG_LOG_FILE": "log_file"
    }
    
    # Process environment variables
    for env_var, config_key in env_mapping.items():
        if env_var in os.environ:
            value = os.environ[env_var]
            
            # Convert types based on default values in ProxyConfig
            field_info = ProxyConfig.__fields__[config_key]
            if field_info.type_ == bool:
                value = value.lower() in ("true", "1", "yes", "y", "on")
            elif field_info.type_ == int:
                try:
                    value = int(value)
                except ValueError:
                    logger.warning(f"Invalid integer value for {env_var}: {value}")
                    continue
            
            env_config[config_key] = value
    
    return env_config


def get_proxy_config() -> ProxyConfig:
    """Get proxy configuration.
    
    This combines configuration from:
    1. Default values
    2. Configuration file
    3. Environment variables (highest priority)
    
    Returns:
        ProxyConfig object
    """
    # Start with defaults from the model
    config_dict = ProxyConfig().dict()
    
    # Update with file config
    file_config = load_config()
    config_dict.update(file_config)
    
    # Update with environment variables
    env_config = get_env_config()
    config_dict.update(env_config)
    
    # Create and return config object
    return ProxyConfig(**config_dict)