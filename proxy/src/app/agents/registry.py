"""
Tool registry for the agent SDK.

This module provides functionality for registering and retrieving tools
that can be invoked by the agent SDK.
"""
from typing import Dict, Any, Callable, Optional
import logging

# Configure logger
logger = logging.getLogger(__name__)

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
    logger.info(f"Registered tool '{name}' in the tool registry")


def get_tool(name: str) -> Optional[Callable]:
    """
    Retrieve a tool from the registry by name.
    
    Args:
        name: The name of the tool to retrieve
        
    Returns:
        The tool callable if found, None otherwise
    """
    tool = TOOL_REGISTRY.get(name)
    if tool:
        logger.debug(f"Found tool '{name}' in the registry")
    else:
        logger.warning(f"Tool '{name}' not found in the registry. Available tools: {list(TOOL_REGISTRY.keys())}")
    return tool


def list_tools() -> Dict[str, Callable]:
    """
    List all registered tools.
    
    Returns:
        A dictionary of all registered tools
    """
    tools = TOOL_REGISTRY.copy()
    logger.info(f"Available tools: {list(tools.keys())}")
    return tools