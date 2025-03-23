"""
Tools package for the SynthLang Proxy.

This package contains tools that can be invoked by the keyword detection system.
"""
# Import all tools to ensure they are registered
from app.agents.tools.web_search import perform_web_search
from app.agents.tools.weather import get_weather
from app.agents.tools.calculator import calculate