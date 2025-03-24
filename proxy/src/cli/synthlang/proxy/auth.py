"""Authentication utilities for SynthLang Proxy."""
import json
import os
from pathlib import Path
from typing import Dict, Optional, Any

from synthlang.utils.logger import get_logger

logger = get_logger(__name__)


def get_credentials_path() -> Path:
    """Get path to credentials file.
    
    Returns:
        Path to credentials file
    """
    config_dir = Path.home() / ".synthlang"
    config_dir.mkdir(exist_ok=True)
    return config_dir / "credentials.json"


def save_credentials(api_key: str, endpoint: Optional[str] = None) -> None:
    """Save API key and endpoint to credentials file.
    
    Args:
        api_key: API key for authentication
        endpoint: Optional endpoint URL
    """
    creds_path = get_credentials_path()
    creds = {}
    
    # Load existing credentials if available
    if creds_path.exists():
        try:
            with open(creds_path) as f:
                creds = json.load(f)
        except json.JSONDecodeError:
            logger.warning(f"Invalid JSON in credentials file: {creds_path}")
            # Continue with empty credentials
    
    # Update credentials
    creds["api_key"] = api_key
    if endpoint:
        creds["endpoint"] = endpoint
    
    # Save credentials
    try:
        with open(creds_path, "w") as f:
            json.dump(creds, f, indent=2)
        logger.info(f"Credentials saved to {creds_path}")
    except Exception as e:
        logger.error(f"Error saving credentials: {str(e)}")
        raise


def clear_credentials() -> None:
    """Clear saved credentials."""
    creds_path = get_credentials_path()
    if creds_path.exists():
        try:
            creds_path.unlink()
            logger.info(f"Credentials cleared from {creds_path}")
        except Exception as e:
            logger.error(f"Error clearing credentials: {str(e)}")
            raise
    else:
        logger.info("No credentials file found to clear")


def get_credentials() -> Dict[str, Any]:
    """Get credentials from file or environment.
    
    Returns:
        Dictionary with credentials
    """
    creds = {}
    
    # Try to load from file
    creds_path = get_credentials_path()
    if creds_path.exists():
        try:
            with open(creds_path) as f:
                creds = json.load(f)
            logger.debug(f"Loaded credentials from {creds_path}")
        except json.JSONDecodeError:
            logger.warning(f"Invalid JSON in credentials file: {creds_path}")
    
    # Override with environment variables if present
    api_key = os.environ.get("SYNTHLANG_API_KEY")
    if api_key:
        creds["api_key"] = api_key
        logger.debug("Using API key from environment variable")
    
    endpoint = os.environ.get("SYNTHLANG_ENDPOINT")
    if endpoint:
        creds["endpoint"] = endpoint
        logger.debug(f"Using endpoint from environment variable: {endpoint}")
    
    return creds


def validate_api_key(api_key: str) -> bool:
    """Validate API key format.
    
    Args:
        api_key: API key to validate
        
    Returns:
        True if valid, False otherwise
    """
    # Simple validation - can be enhanced based on actual key format
    return bool(api_key and len(api_key) >= 8)