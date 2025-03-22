"""
Tool registry for the agent SDK.

This module provides functionality for registering and retrieving tools
that can be invoked by the agent SDK.
"""
from typing import Dict, Any, Callable, Optional


# Tool registry dictionary to store registered tools
TOOL_REGISTRY: Dict[str, Callable] = {}


def register_tool(name: str, tool_callable: Callable) -> None:
    """
    Register a tool in the tool registry.
    
    Args:
        name: The name of the tool to register
        tool_callable: The function to execute when the tool is invoked
    """
    TOOL_REGISTRY[name] = tool_callable


def get_tool(name: str) -> Optional[Callable]:
    """
    Retrieve a tool from the registry by name.
    
    Args:
        name: The name of the tool to retrieve
        
    Returns:
        The tool callable if found, None otherwise
    """
    return TOOL_REGISTRY.get(name)


def list_tools() -> Dict[str, Callable]:
    """
    List all registered tools.
    
    Returns:
        A dictionary of all registered tools
    """
    return TOOL_REGISTRY.copy()