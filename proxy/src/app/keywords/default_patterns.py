"""
Default keyword patterns for the SynthLang Proxy.

This module registers default keyword patterns for common tools.
"""
import os
import sys
import traceback
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    logger.debug(f"Added {project_root} to Python path")

try:
    from src.app.keywords.registry import KeywordPattern, register_pattern
    logger.debug("Successfully imported from src.app.keywords.registry")
except ImportError as e:
    logger.error(f"Error importing from src.app.keywords.registry: {e}")
    try:
        from app.keywords.registry import KeywordPattern, register_pattern
        logger.debug("Successfully imported from app.keywords.registry")
    except ImportError as e2:
        logger.error(f"Error importing from app.keywords.registry: {e2}")
        # Re-raise the original exception
        raise e

# Weather patterns
weather_pattern = KeywordPattern(
    name="weather_query",
    pattern=r"(?:what's|what is|how's|how is|get|check|tell me about)\s+(?:the)?\s*(?:weather|temperature|forecast)\s+(?:in|at|for)?\s+(?P<location>.+)",
    tool="weather",
    description="Detects requests for weather information",
    priority=100
)

# Web search patterns
web_search_pattern = KeywordPattern(
    name="web_search_query",
    pattern=r"(?:search|google|look up|find|research)\s+(?:for|about)?\s+(?P<query>.+)",
    tool="web_search",
    description="Detects requests for web searches",
    priority=90
)

# Calculator patterns
calculator_pattern = KeywordPattern(
    name="calculator_query",
    pattern=r"(?:calculate|compute|what is|solve|evaluate)\s+(?P<expression>.+)",
    tool="calculator",
    description="Detects requests for calculations",
    priority=80
)

# Admin patterns (requires admin role)
admin_pattern = KeywordPattern(
    name="admin_query",
    pattern=r"(?:admin|system|configure|setup|manage)\s+(?:the|this)?\s*(?:system|server|application|app|service)\s+(?:to|for)?\s+(?P<action>.+)",
    tool="system_admin",
    description="Detects requests for system administration tasks",
    priority=200,
    required_role="admin"
)

# Register all patterns
def register_default_patterns():
    """Register all default keyword patterns."""
    logger.info("Registering default patterns...")
    register_pattern(weather_pattern)
    register_pattern(web_search_pattern)
    register_pattern(calculator_pattern)
    register_pattern(admin_pattern)
    logger.info("Default patterns registered successfully")

# Register patterns when this module is imported
try:
    register_default_patterns()
    logger.debug("Default patterns registered on import")
except Exception as e:
    logger.error(f"Error registering default patterns on import: {e}")