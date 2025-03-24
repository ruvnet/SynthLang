"""
Tool registry for agent tools.

This module provides functions for registering and retrieving agent tools.
"""
import logging
from typing import Dict, List, Any, Optional, Callable

# Configure logging
logger = logging.getLogger(__name__)

# Tool registry
_tools = {}


def register_tool(
    name: str,
    description: str,
    function: Callable,
    parameters: Dict[str, Any],
    required_role: str = "basic"
) -> None:
    """
    Register a tool in the registry.
    
    Args:
        name: Tool name
        description: Tool description
        function: Tool function
        parameters: Tool parameters schema
        required_role: Required role to use this tool
    """
    global _tools
    
    _tools[name] = {
        "name": name,
        "description": description,
        "function": function,
        "parameters": parameters,
        "required_role": required_role
    }
    
    logger.info(f"Registered tool: {name}")


def get_tool(name: str) -> Optional[Dict[str, Any]]:
    """
    Get a tool from the registry.
    
    Args:
        name: Tool name
        
    Returns:
        Tool information if found, None otherwise
    """
    return _tools.get(name)


def list_tools() -> List[Dict[str, Any]]:
    """
    List all registered tools.
    
    Returns:
        List of tool information dictionaries
    """
    # Return a copy of the tools without the function
    return [
        {
            "name": tool["name"],
            "description": tool["description"],
            "parameters": tool["parameters"],
            "required_role": tool["required_role"]
        }
        for tool in _tools.values()
    ]