"""Configuration management for SynthLang."""
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

class Config(BaseModel):
    """Configuration model."""
    openai_api_key: str = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    model: str = Field(default="gpt-4o-mini")
    environment: str = Field(default="production")
    log_level: str = Field(default="INFO")

    class Config:
        env_file = ".env"

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
        """Update configuration values in environment.
        
        Args:
            updates: Dictionary of updates to apply
            
        Returns:
            Updated configuration
            
        Raises:
            ValueError: If updates are invalid
        """
        config = self.load()
        
        # Update values
        for key, value in updates.items():
            if not hasattr(config, key):
                raise ValueError(f"Invalid configuration key: {key}")
            os.environ[f"SYNTHLANG_{key.upper()}"] = str(value)
            setattr(config, key, value)
            
        return config
