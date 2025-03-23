"""
Configuration management module.

This module loads configuration settings from environment variables
and provides them as module-level constants for use throughout the application.
"""
import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Configure logging
logger = logging.getLogger(__name__)

# Load environment variables from .env file
env_path = Path(__file__).resolve().parent.parent.parent / '.env'
logger.info(f"Looking for .env file at: {env_path} (exists: {env_path.exists()})")

if env_path.exists():
    logger.info(f"Loading environment variables from {env_path}")
    load_dotenv(dotenv_path=env_path)
    # Debug: Print all environment variables (excluding sensitive values)
    for key in os.environ:
        if key == "OPENAI_API_KEY" and os.environ.get(key):
            logger.info(f"Environment variable {key} is set to: [REDACTED]")
        elif key not in ["OPENAI_API_KEY", "API_KEY", "ENCRYPTION_KEY"] and os.environ.get(key):
            logger.info(f"Environment variable {key} is set to: {os.environ.get(key)}")
else:
    logger.warning(f"No .env file found at {env_path}")
    # Try to load from current directory as fallback
    fallback_path = Path.cwd() / '.env'
    logger.info(f"Trying fallback .env location: {fallback_path} (exists: {fallback_path.exists()})")
    if fallback_path.exists():
        logger.info(f"Loading environment variables from fallback location: {fallback_path}")
        load_dotenv(dotenv_path=fallback_path)

# Required configuration variables
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.warning("OPENAI_API_KEY environment variable not set. API calls will likely fail.")
else:
    logger.info("OPENAI_API_KEY environment variable is set.")

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    logger.warning("DATABASE_URL environment variable not set. Database connections will likely fail.")

ENCRYPTION_KEY = os.environ.get("ENCRYPTION_KEY")
if not ENCRYPTION_KEY:
    logger.warning("ENCRYPTION_KEY environment variable not set. Encryption/decryption will likely fail.")

# Optional configuration variables with defaults
# Convert string values to appropriate types (bool, int)
# For booleans, we use int conversion (0=False, 1=True) to avoid Python's truthiness rules
USE_SYNTHLANG = bool(int(os.getenv("USE_SYNTHLANG", "1")))
MASK_PII_BEFORE_LLM = bool(int(os.getenv("MASK_PII_BEFORE_LLM", "0")))
MASK_PII_IN_LOGS = bool(int(os.getenv("MASK_PII_IN_LOGS", "1")))
DEFAULT_RATE_LIMIT_QPM = int(os.getenv("DEFAULT_RATE_LIMIT_QPM", "60"))

# Log configuration status
logger.info(f"Configuration loaded: USE_SYNTHLANG={USE_SYNTHLANG}, "
            f"MASK_PII_BEFORE_LLM={MASK_PII_BEFORE_LLM}, "
            f"MASK_PII_IN_LOGS={MASK_PII_IN_LOGS}, "
            f"DEFAULT_RATE_LIMIT_QPM={DEFAULT_RATE_LIMIT_QPM}")

# Model routing configuration
MODEL_PROVIDER = {
    "gpt-4o-search-preview": "openai",
    "gpt-4o-mini-search-preview": "openai",
    "o3-mini": "openai"
}

logger.info(f"Model provider configuration loaded with {len(MODEL_PROVIDER)} models")