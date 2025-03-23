"""
Default keyword patterns for the SynthLang Proxy.

This module registers default keyword patterns for common tools.
"""
import os
import sys
import traceback

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    print(f"Added {project_root} to Python path in default_patterns.py")

# Print current Python path for debugging
print(f"Python path in default_patterns.py: {sys.path}")

try:
    from src.app.keywords.registry import KeywordPattern, register_pattern
    print("Successfully imported from src.app.keywords.registry in default_patterns.py")
except ImportError as e:
    print(f"Error importing from src.app.keywords.registry in default_patterns.py: {e}")
    print(f"Traceback: {traceback.format_exc()}")
    try:
        from app.keywords.registry import KeywordPattern, register_pattern
        print("Successfully imported from app.keywords.registry in default_patterns.py")
    except ImportError as e2:
        print(f"Error importing from app.keywords.registry in default_patterns.py: {e2}")
        print(f"Traceback: {traceback.format_exc()}")
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
    print("Registering default patterns...")
    register_pattern(weather_pattern)
    register_pattern(web_search_pattern)
    register_pattern(calculator_pattern)
    register_pattern(admin_pattern)
    print("Default patterns registered successfully")

# Register patterns when this module is imported
try:
    register_default_patterns()
    print("Default patterns registered on import")
except Exception as e:
    print(f"Error registering default patterns on import: {e}")
    print(f"Traceback: {traceback.format_exc()}")