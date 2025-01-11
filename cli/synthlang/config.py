"""Configuration management for SynthLang."""
import json
from pathlib import Path
from typing import Any, Dict, Optional

from pydantic import BaseModel

class Config(BaseModel):
    """Configuration model."""
    model: str = "gpt-4o-mini"
    environment: str = "production"
    log_level: str = "INFO"

class ConfigManager:
    """Configuration manager."""
    
    def load(self, path: Path) -> Config:
        """Load configuration from file.
        
        Args:
            path: Path to configuration file
            
        Returns:
            Loaded configuration
            
        Raises:
            FileNotFoundError: If configuration file not found
            ValueError: If configuration is invalid
        """
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {path}")
            
        with open(path) as f:
            try:
                data = json.load(f)
                return Config(**data)
            except Exception as e:
                raise ValueError(f"Invalid configuration: {str(e)}")
    
    def save(self, config: Config, path: Path) -> None:
        """Save configuration to file.
        
        Args:
            config: Configuration to save
            path: Path to save configuration to
        """
        with open(path, "w") as f:
            json.dump(config.model_dump(), f, indent=2)
    
    def update(self, path: Path, updates: Dict[str, Any]) -> Config:
        """Update configuration values.
        
        Args:
            path: Path to configuration file
            updates: Dictionary of updates to apply
            
        Returns:
            Updated configuration
            
        Raises:
            ValueError: If updates are invalid
        """
        config = self.load(path)
        
        # Update values
        for key, value in updates.items():
            if not hasattr(config, key):
                raise ValueError(f"Invalid configuration key: {key}")
            setattr(config, key, value)
            
        # Save updated config
        self.save(config, path)
        return config
