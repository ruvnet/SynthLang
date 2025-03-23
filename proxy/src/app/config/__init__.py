"""
Configuration package for the SynthLang Proxy.

This package contains configuration modules for the SynthLang Proxy.
"""
import os
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Required configuration variables
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.warning("OPENAI_API_KEY environment variable not set. API calls will likely fail.")

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    logger.warning("DATABASE_URL environment variable not set. Database connections will likely fail.")

ENCRYPTION_KEY = os.environ.get("ENCRYPTION_KEY")
if not ENCRYPTION_KEY:
    logger.warning("ENCRYPTION_KEY environment variable not set. Encryption/decryption will likely fail.")

# API keys
API_KEY = os.environ.get("API_KEY")
ADMIN_API_KEY = os.environ.get("ADMIN_API_KEY", API_KEY)  # Default to API_KEY if not set

# Optional configuration variables with defaults
# Convert string values to appropriate types (bool, int)
# For booleans, we use int conversion (0=False, 1=True) to avoid Python's truthiness rules
USE_SYNTHLANG = bool(int(os.getenv("USE_SYNTHLANG", "1")))
MASK_PII_BEFORE_LLM = bool(int(os.getenv("MASK_PII_BEFORE_LLM", "0")))
MASK_PII_IN_LOGS = bool(int(os.getenv("MASK_PII_IN_LOGS", "1")))
DEFAULT_RATE_LIMIT_QPM = int(os.getenv("DEFAULT_RATE_LIMIT_QPM", "60"))
PREMIUM_RATE_LIMIT_QPM = int(os.getenv("PREMIUM_RATE_LIMIT_QPM", "120"))

# SQLite configuration
USE_SQLITE = bool(int(os.getenv("USE_SQLITE", "0")))
SQLITE_PATH = os.getenv("SQLITE_PATH", "sqlite+aiosqlite:///./synthlang_proxy.db")

# Cache configuration
ENABLE_CACHE = bool(int(os.getenv("ENABLE_CACHE", "1")))
CACHE_SIMILARITY_THRESHOLD = float(os.getenv("CACHE_SIMILARITY_THRESHOLD", "0.95"))
CACHE_MAX_ITEMS = int(os.getenv("CACHE_MAX_ITEMS", "1000"))

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