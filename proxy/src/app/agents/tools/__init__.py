"""
Tools package for the SynthLang Proxy.

This package contains tools that can be invoked by the keyword detection system.
"""
import sys
import os
import traceback

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    print(f"Added {project_root} to Python path in tools/__init__.py")

# Print current Python path for debugging
print(f"Python path in tools/__init__.py: {sys.path}")

# Import all tools to ensure they are registered
try:
    print("Attempting to import tools with src.app prefix in __init__.py")
    from src.app.agents.tools.web_search import perform_web_search
    from src.app.agents.tools.weather import get_weather
    from src.app.agents.tools.calculator import calculate
    print("Successfully imported tools with src.app prefix in __init__.py")
except ImportError as e:
    print(f"Error importing tools with src.app prefix in __init__.py: {e}")
    print(f"Traceback: {traceback.format_exc()}")
    try:
        print("Attempting to import tools with app prefix in __init__.py")
        from app.agents.tools.web_search import perform_web_search
        from app.agents.tools.weather import get_weather
        from app.agents.tools.calculator import calculate
        print("Successfully imported tools with app prefix in __init__.py")
    except ImportError as e2:
        print(f"Error importing tools with app prefix in __init__.py: {e2}")
        print(f"Traceback: {traceback.format_exc()}")