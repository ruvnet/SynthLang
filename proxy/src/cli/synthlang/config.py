"""Configuration management for SynthLang."""
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

class Config(BaseModel):
    """Configuration model."""
    openai_api_key: str = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    model: str = Field(default_factory=lambda: os.getenv("SYNTHLANG_MODEL", "gpt-4o-mini"))
    environment: str = Field(default_factory=lambda: os.getenv("SYNTHLANG_ENVIRONMENT", "production"))
    log_level: str = Field(default_factory=lambda: os.getenv("SYNTHLANG_LOG_LEVEL", "INFO"))

    class Config:
        env_file = ".env"
        env_prefix = "SYNTHLANG_"

class ConfigManager:
    """Configuration manager."""
    
    def load(self) -> Config:
        """Load configuration from environment variables.
        
        Returns:
            Loaded configuration
            
        Raises:
            ValueError: If required environment variables are missing
        """
        try:
            return Config()
        except Exception as e:
            raise ValueError(f"Invalid configuration: {str(e)}")
    
    def update(self, updates: Dict[str, Any]) -> Config:
        """Update configuration values in environment and .env file.
        
        Args:
            updates: Dictionary of updates to apply
            
        Returns:
            Updated configuration
            
        Raises:
            ValueError: If updates are invalid
        """
        config = self.load()
        env_path = Path(".env")
        
        # Read existing .env content
        env_content = {}
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    if "=" in line:
                        key, value = line.strip().split("=", 1)
                        env_content[key] = value
        
        # Update values
        for key, value in updates.items():
            if not hasattr(config, key):
                raise ValueError(f"Invalid configuration key: {key}")
            env_key = f"SYNTHLANG_{key.upper()}"
            os.environ[env_key] = str(value)
            env_content[env_key] = str(value)
            setattr(config, key, value)
        
        # Write updated content back to .env
        with open(env_path, "w") as f:
            for key, value in env_content.items():
                f.write(f"{key}={value}\n")
            
        return config
