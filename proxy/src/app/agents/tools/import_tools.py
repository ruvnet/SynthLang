"""
Import all tools.

This module imports all tools to ensure they are registered.
"""
import logging
import importlib
import os
import pkgutil
from typing import List

# Configure logging
logger = logging.getLogger(__name__)


def import_all_tools() -> int:
    """
    Import all tools to ensure they are registered.
    
    Returns:
        Number of tools imported
    """
    # Get the directory of this file
    tools_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Get all Python files in the directory
    tool_modules = []
    for _, name, is_pkg in pkgutil.iter_modules([tools_dir]):
        if not is_pkg and name != "registry" and name != "import_tools":
            tool_modules.append(name)
    
    # Import each module
    imported_count = 0
    for module_name in tool_modules:
        try:
            importlib.import_module(f"src.app.agents.tools.{module_name}")
            imported_count += 1
            logger.debug(f"Imported tool module: {module_name}")
        except Exception as e:
            logger.error(f"Failed to import tool module {module_name}: {e}")
    
    logger.info(f"Imported {imported_count} tool modules")
    return imported_count