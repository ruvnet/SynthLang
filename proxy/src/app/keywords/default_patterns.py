"""
Default keyword patterns for the SynthLang Proxy.

This module registers default keyword patterns for common tools.
"""
from app.keywords.registry import KeywordPattern, register_pattern

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
    register_pattern(weather_pattern)
    register_pattern(web_search_pattern)
    register_pattern(calculator_pattern)
    register_pattern(admin_pattern)

# Register patterns when this module is imported
register_default_patterns()