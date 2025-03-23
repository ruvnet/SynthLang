"""
Configuration module for keyword detection system.

This module provides functions for loading and saving keyword configurations
from TOML files.
"""
import os
import logging
import tomli
import tomli_w
import traceback
import sys
from typing import Dict, List, Any, Optional
from pathlib import Path

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    logging.getLogger(__name__).debug(f"Added {project_root} to Python path")

try:
    from src.app.keywords.registry import KeywordPattern, register_pattern, KEYWORD_REGISTRY
    logging.getLogger(__name__).debug("Successfully imported from src.app.keywords.registry")
except ImportError as e:
    logging.getLogger(__name__).error(f"Error importing from src.app.keywords.registry: {e}")
    try:
        from app.keywords.registry import KeywordPattern, register_pattern, KEYWORD_REGISTRY
        logging.getLogger(__name__).debug("Successfully imported from app.keywords.registry")
    except ImportError as e2:
        logging.getLogger(__name__).error(f"Error importing from app.keywords.registry: {e2}")
        # Re-raise the original exception
        raise e

# Logger for this module
logger = logging.getLogger(__name__)

# Default configuration directory
DEFAULT_CONFIG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config")

# Default configuration file
DEFAULT_CONFIG_FILE = os.path.join(DEFAULT_CONFIG_DIR, "keywords.toml")

def ensure_config_dir() -> str:
    """
    Ensure the configuration directory exists.
    
    Returns:
        The path to the configuration directory
    """
    config_dir = os.environ.get("SYNTHLANG_CONFIG_DIR", DEFAULT_CONFIG_DIR)
    os.makedirs(config_dir, exist_ok=True)
    return config_dir

def get_config_file_path() -> str:
    """
    Get the path to the configuration file.
    
    Returns:
        The path to the configuration file
    """
    config_dir = ensure_config_dir()
    config_file = os.environ.get("SYNTHLANG_KEYWORDS_CONFIG", os.path.join(config_dir, "keywords.toml"))
    return config_file

def load_keyword_config(config_file: Optional[str] = None) -> Dict[str, Any]:
    """
    Load keyword configuration from a TOML file.
    
    Args:
        config_file: Path to the configuration file (optional)
        
    Returns:
        The configuration as a dictionary
    """
    config_file = config_file or get_config_file_path()
    
    try:
        if os.path.exists(config_file):
            with open(config_file, "rb") as f:
                config = tomli.load(f)
            logger.info(f"Loaded keyword configuration from {config_file}")
            return config
        else:
            logger.warning(f"Configuration file {config_file} not found, using defaults")
            return {}
    except Exception as e:
        logger.error(f"Error loading configuration from {config_file}: {e}")
        return {}

def save_keyword_config(config: Dict[str, Any], config_file: Optional[str] = None) -> bool:
    """
    Save keyword configuration to a TOML file.
    
    Args:
        config: The configuration to save
        config_file: Path to the configuration file (optional)
        
    Returns:
        True if successful, False otherwise
    """
    config_file = config_file or get_config_file_path()
    
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        
        # Save configuration
        with open(config_file, "wb") as f:
            tomli_w.dump(config, f)
        
        logger.info(f"Saved keyword configuration to {config_file}")
        return True
    except Exception as e:
        logger.error(f"Error saving configuration to {config_file}: {e}")
        return False

def pattern_to_toml(pattern: KeywordPattern) -> Dict[str, Any]:
    """
    Convert a KeywordPattern to a TOML-compatible dictionary.
    
    Args:
        pattern: The pattern to convert
        
    Returns:
        A dictionary representation of the pattern
    """
    data = {
        "name": pattern.name,
        "pattern": pattern.pattern,
        "tool": pattern.tool,
        "description": pattern.description,
        "priority": pattern.priority,
        "enabled": pattern.enabled
    }
    
    # Only include required_role if it's set
    if pattern.required_role:
        data["required_role"] = pattern.required_role
    
    return data

def toml_to_pattern(data: Dict[str, Any]) -> KeywordPattern:
    """
    Convert a TOML dictionary to a KeywordPattern.
    
    Args:
        data: The dictionary to convert
        
    Returns:
        A KeywordPattern instance
    """
    return KeywordPattern(
        name=data["name"],
        pattern=data["pattern"],
        tool=data["tool"],
        description=data["description"],
        required_role=data.get("required_role"),
        priority=data.get("priority", 0),
        enabled=data.get("enabled", True)
    )

def export_patterns_to_toml() -> Dict[str, Any]:
    """
    Export all registered patterns to a TOML-compatible dictionary.
    
    Returns:
        A dictionary containing all patterns
    """
    config = {
        "settings": {
            "enable_keyword_detection": os.environ.get("ENABLE_KEYWORD_DETECTION", "1").lower() in ("1", "true", "yes"),
            "detection_threshold": float(os.environ.get("KEYWORD_DETECTION_THRESHOLD", "0.7")),
            "default_role": "basic"
        },
        "patterns": {}
    }
    
    # Add all patterns
    for name, pattern in KEYWORD_REGISTRY.items():
        config["patterns"][name] = pattern_to_toml(pattern)
    
    return config

def import_patterns_from_toml(config: Dict[str, Any]) -> int:
    """
    Import patterns from a TOML configuration.
    
    Args:
        config: The configuration dictionary
        
    Returns:
        The number of patterns imported
    """
    count = 0
    
    # Update settings
    if "settings" in config:
        settings = config["settings"]
        if "enable_keyword_detection" in settings:
            os.environ["ENABLE_KEYWORD_DETECTION"] = "1" if settings["enable_keyword_detection"] else "0"
        
        if "detection_threshold" in settings:
            os.environ["KEYWORD_DETECTION_THRESHOLD"] = str(settings["detection_threshold"])
    
    # Import patterns
    if "patterns" in config:
        patterns = config["patterns"]
        for name, data in patterns.items():
            try:
                # Ensure name in data matches key
                data["name"] = name
                
                # Create and register pattern
                pattern = toml_to_pattern(data)
                register_pattern(pattern)
                count += 1
            except Exception as e:
                logger.error(f"Error importing pattern '{name}': {e}")
    
    logger.info(f"Imported {count} patterns from configuration")
    return count

def create_default_config() -> Dict[str, Any]:
    """
    Create a default configuration.
    
    Returns:
        A default configuration dictionary
    """
    # Import default patterns
    try:
        logger.debug("Attempting to import default patterns")
        from src.app.keywords.default_patterns import register_default_patterns
        logger.debug("Successfully imported from src.app.keywords.default_patterns")
        register_default_patterns()
    except ImportError as e:
        logger.error(f"Error importing from src.app.keywords.default_patterns: {e}")
        try:
            # Try alternative import path
            logger.debug("Attempting to import from app.keywords.default_patterns")
            from app.keywords.default_patterns import register_default_patterns
            logger.debug("Successfully imported from app.keywords.default_patterns")
            register_default_patterns()
        except ImportError as e2:
            logger.error(f"Error importing from app.keywords.default_patterns: {e2}")
            logger.error("Failed to import default patterns from any known path")
    
    # Export to TOML
    config = export_patterns_to_toml()
    
    return config

def initialize_from_config() -> int:
    """
    Initialize the keyword system from configuration.
    
    Returns:
        The number of patterns loaded
    """
    # Load configuration
    config = load_keyword_config()
    
    # If empty, create default configuration
    if not config:
        config = create_default_config()
        save_keyword_config(config)
        return len(KEYWORD_REGISTRY)
    
    # Import patterns
    return import_patterns_from_toml(config)