"""Configuration management for SynthLang CLI."""
import os
from pathlib import Path
from typing import Dict, Any, Optional
import json

from pydantic import BaseModel

class Config(BaseModel):
    """Configuration model."""
    openai_api_key: Optional[str] = None
    model: str = "gpt-4o-mini"
    environment: str = "development"
    log_level: str = "INFO"

class ConfigManager:
    """Manages configuration loading and saving."""

    def load(self, config_path: Path) -> Config:
        """Load configuration from file and environment.
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            Config object with loaded configuration
            
        Note:
            Environment variables take precedence over file configuration.
            Required environment variables:
            - OPENAI_API_KEY: OpenAI API key
        """
        # Load from file if exists
        config_data = {}
        if config_path.exists():
            with open(config_path) as f:
                config_data = json.load(f)

        # Override with environment variables
        if os.getenv("OPENAI_API_KEY"):
            config_data["openai_api_key"] = os.getenv("OPENAI_API_KEY")
        if os.getenv("SYNTHLANG_MODEL"):
            config_data["model"] = os.getenv("SYNTHLANG_MODEL")
        if os.getenv("SYNTHLANG_ENV"):
            config_data["environment"] = os.getenv("SYNTHLANG_ENV")
        if os.getenv("SYNTHLANG_LOG_LEVEL"):
            config_data["log_level"] = os.getenv("SYNTHLANG_LOG_LEVEL")

        # Ensure API key is available
        if not config_data.get("openai_api_key"):
            raise ValueError(
                "OpenAI API key not found. Set OPENAI_API_KEY environment variable."
            )

        return Config(**config_data)

    def save(self, config: Config, config_path: Path) -> None:
        """Save configuration to file.
        
        Args:
            config: Configuration to save
            config_path: Path to save configuration to
            
        Note:
            Sensitive data like API keys are not saved to file.
        """
        # Create config directory if needed
        config_path.parent.mkdir(parents=True, exist_ok=True)

        # Save non-sensitive config
        config_data = config.model_dump()
        config_data.pop("openai_api_key", None)  # Don't save API key

        with open(config_path, "w") as f:
            json.dump(config_data, f, indent=2)

    def update(self, config_path: Path, updates: Dict[str, Any]) -> Config:
        """Update configuration values.
        
        Args:
            config_path: Path to configuration file
            updates: Dictionary of updates to apply
            
        Returns:
            Updated configuration
        """
        config = self.load(config_path)
        
        # Update config
        config_dict = config.model_dump()
        config_dict.update(updates)
        updated_config = Config(**config_dict)
        
        # Save updated config
        self.save(updated_config, config_path)
        
        return updated_config
