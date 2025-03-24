"""Tool registry for SynthLang agents."""
import inspect
import json
from typing import Dict, Callable, Any, List, Optional, Union, get_type_hints

from synthlang.utils.logger import get_logger

logger = get_logger(__name__)

# Global registry of tools
_TOOLS: Dict[str, Callable] = {}
_TOOL_SCHEMAS: Dict[str, Dict[str, Any]] = {}


def register_tool(name: Optional[str] = None, description: Optional[str] = None) -> Callable:
    """Register a tool in the global registry.
    
    This can be used as a decorator to register functions as tools.
    
    Args:
        name: Optional name for the tool (defaults to function name)
        description: Optional description of the tool
        
    Returns:
        Decorator function
    """
    def decorator(func: Callable) -> Callable:
        nonlocal name, description
        
        # Use function name if no name provided
        tool_name = name or func.__name__
        
        # Use docstring if no description provided
        tool_description = description or inspect.getdoc(func) or ""
        
        # Get function signature
        sig = inspect.signature(func)
        type_hints = get_type_hints(func)
        
        # Build schema for the tool
        parameters = {}
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
                
            param_type = type_hints.get(param_name, Any).__name__
            param_default = None if param.default is inspect.Parameter.empty else param.default
            param_required = param.default is inspect.Parameter.empty
            
            parameters[param_name] = {
                "type": param_type,
                "required": param_required
            }
            
            if param_default is not None:
                parameters[param_name]["default"] = param_default
        
        # Store tool schema
        _TOOL_SCHEMAS[tool_name] = {
            "name": tool_name,
            "description": tool_description,
            "parameters": parameters,
            "return_type": type_hints.get("return", Any).__name__
        }
        
        # Register the tool
        _TOOLS[tool_name] = func
        logger.debug(f"Registered tool: {tool_name}")
        
        return func
    
    # Handle case where decorator is used without parentheses
    if callable(name):
        func, name = name, None
        return decorator(func)
    
    return decorator


def get_tool(name: str) -> Callable:
    """Get a tool from the registry.
    
    Args:
        name: Name of the tool
        
    Returns:
        Tool function
        
    Raises:
        ValueError: If tool not found
    """
    if name not in _TOOLS:
        raise ValueError(f"Tool '{name}' not found in registry")
    return _TOOLS[name]


def get_tool_schema(name: str) -> Dict[str, Any]:
    """Get the schema for a tool.
    
    Args:
        name: Name of the tool
        
    Returns:
        Tool schema
        
    Raises:
        ValueError: If tool not found
    """
    if name not in _TOOL_SCHEMAS:
        raise ValueError(f"Tool schema for '{name}' not found in registry")
    return _TOOL_SCHEMAS[name]


def list_tools() -> List[str]:
    """List all registered tools.
    
    Returns:
        List of tool names
    """
    return list(_TOOLS.keys())


def get_all_tool_schemas() -> Dict[str, Dict[str, Any]]:
    """Get schemas for all registered tools.
    
    Returns:
        Dictionary of tool schemas
    """
    return _TOOL_SCHEMAS


def call_tool(name: str, **kwargs) -> Any:
    """Call a tool by name with arguments.
    
    Args:
        name: Name of the tool
        **kwargs: Arguments to pass to the tool
        
    Returns:
        Tool result
        
    Raises:
        ValueError: If tool not found
    """
    tool = get_tool(name)
    try:
        return tool(**kwargs)
    except Exception as e:
        logger.error(f"Error calling tool '{name}': {str(e)}")
        raise


def call_tool_with_json(name: str, json_args: str) -> Any:
    """Call a tool by name with JSON-encoded arguments.
    
    Args:
        name: Name of the tool
        json_args: JSON-encoded arguments
        
    Returns:
        Tool result
        
    Raises:
        ValueError: If tool not found or JSON is invalid
    """
    try:
        kwargs = json.loads(json_args)
        return call_tool(name, **kwargs)
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON arguments: {json_args}")
        raise ValueError(f"Invalid JSON arguments: {json_args}")


# Register some built-in tools
@register_tool(description="Get the current time")
def get_current_time() -> str:
    """Get the current time.
    
    Returns:
        Current time as a string
    """
    import datetime
    return datetime.datetime.now().isoformat()


@register_tool(description="Perform a simple calculation")
def calculate(expression: str) -> float:
    """Perform a simple calculation.
    
    Args:
        expression: Mathematical expression to evaluate
        
    Returns:
        Result of the calculation
        
    Raises:
        ValueError: If expression is invalid
    """
    # Use safer eval with restricted globals
    import math
    allowed_names = {
        k: v for k, v in math.__dict__.items() 
        if not k.startswith('__')
    }
    allowed_names.update({
        'abs': abs,
        'round': round,
        'min': min,
        'max': max
    })
    
    try:
        return eval(expression, {"__builtins__": {}}, allowed_names)
    except Exception as e:
        raise ValueError(f"Invalid expression: {str(e)}")