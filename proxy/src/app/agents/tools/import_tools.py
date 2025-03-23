"""
Import tools module for the SynthLang Proxy.

This module explicitly imports all tools to ensure they are registered.
"""
import logging
import sys
import os
import traceback

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    print(f"Added {project_root} to Python path in import_tools.py")

# Print current Python path for debugging
print(f"Python path in import_tools.py: {sys.path}")

# Logger for this module
logger = logging.getLogger(__name__)

def import_all_tools():
    """
    Import all tools to ensure they are registered.
    
    This function should be called during application startup.
    """
    logger.info("Importing all tools...")
    print("Importing all tools...")
    
    tool_count = 0
    
    # Try importing with src.app prefix
    try:
        print("Attempting to import tools with src.app prefix")
        from src.app.agents.tools.web_search import perform_web_search
        from src.app.agents.tools.weather import get_weather
        from src.app.agents.tools.calculator import calculate
        print("Successfully imported tools with src.app prefix")
        tool_count = 3
        
        # Try to import file_search if it exists
        try:
            from src.app.agents.tools.file_search import search_files
            tool_count = 4
            print("Successfully imported file_search tool")
        except ImportError as e:
            print(f"File search tool not available: {e}")
    except ImportError as e:
        print(f"Error importing tools with src.app prefix: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        
        # Try importing with app prefix
        try:
            print("Attempting to import tools with app prefix")
            from app.agents.tools.web_search import perform_web_search
            from app.agents.tools.weather import get_weather
            from app.agents.tools.calculator import calculate
            print("Successfully imported tools with app prefix")
            tool_count = 3
            
            # Try to import file_search if it exists
            try:
                from app.agents.tools.file_search import search_files
                tool_count = 4
                print("Successfully imported file_search tool")
            except ImportError as e:
                print(f"File search tool not available: {e}")
        except ImportError as e2:
            print(f"Error importing tools with app prefix: {e2}")
            print(f"Traceback: {traceback.format_exc()}")
            logger.error(f"Failed to import tools from any known path: {e2}")
    except Exception as e:
        print(f"Unexpected error importing tools: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        logger.error(f"Unexpected error importing tools: {e}")
    
    # Log success
    if tool_count > 0:
        logger.info(f"Successfully imported {tool_count} tools")
        print(f"Successfully imported {tool_count} tools")
    else:
        logger.warning("No tools were imported")
        print("No tools were imported")
    
    # Return the number of tools imported
    return tool_count