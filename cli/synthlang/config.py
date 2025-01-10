"""Configuration management for SynthLang CLI."""
import json
from pathlib import Path
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, validator

from synthlang.utils.env import load_env_file

class Config(BaseModel):
    """Configuration model."""
    openai_api_key: str = Field(..., min_length=1)
    model: str = Field(default="gpt-4o-mini")
    environment: str = Field(default="development")
    log_level: str = Field(default="INFO")

    @validator("model")
    def validate_model(cls, v: str) -> str:
        """Validate model name."""
        allowed_models = ["gpt-4o-mini", "gpt-4", "gpt-3.5-turbo"]
        if v not in allowed_models:
            raise ValueError(f"Model must be one of: {allowed_models}")
        return v

    @validator("environment")
    def validate_environment(cls, v: str) -> str:
        """Validate environment name."""
        allowed_environments = ["development", "production", "testing"]
        if v not in allowed_environments:
            raise ValueError(f"Environment must be one of: {allowed_environments}")
        return v

    @validator("log_level")
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        allowed_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v = v.upper()
        if v not in allowed_levels:
            raise ValueError(f"Log level must be one of: {allowed_levels}")
        return v

class ConfigManager:
    """Configuration manager."""

    def load(self, config_path: Path) -> Config:
        """Load configuration from file."""
        # Handle .env files
        if config_path.name == ".env":
            env_vars = load_env_file(config_path)
            return Config(
                openai_api_key=env_vars.get("OPENAI_API_KEY", ""),
                model=env_vars.get("SYNTHLANG_MODEL", "gpt-4o-mini"),
                environment=env_vars.get("SYNTHLANG_ENV", "development"),
                log_level=env_vars.get("SYNTHLANG_LOG_LEVEL", "INFO")
            )

        # Handle JSON config files
        if config_path.exists():
            with open(config_path) as f:
                config_data = json.load(f)
        else:
            config_data = {}

        # Override with environment variables if present
        import os
        if "OPENAI_API_KEY" in os.environ:
            config_data["openai_api_key"] = os.environ["OPENAI_API_KEY"]
        if "SYNTHLANG_MODEL" in os.environ:
            config_data["model"] = os.environ["SYNTHLANG_MODEL"]
        if "SYNTHLANG_ENV" in os.environ:
            config_data["environment"] = os.environ["SYNTHLANG_ENV"]
        if "SYNTHLANG_LOG_LEVEL" in os.environ:
            config_data["log_level"] = os.environ["SYNTHLANG_LOG_LEVEL"]

        return Config(**config_data)

    def save(self, config: Config, config_path: Path) -> None:
        """Save configuration to file."""
        config_data = config.model_dump()
        with open(config_path, "w") as f:
            json.dump(config_data, f, indent=2)

    def update(self, config_path: Path, updates: Dict[str, Any]) -> Config:
        """Update configuration with new values."""
        config = self.load(config_path)
        config_data = config.model_dump()
        config_data.update(updates)
        updated_config = Config(**config_data)
        self.save(updated_config, config_path)
        return updated_config
