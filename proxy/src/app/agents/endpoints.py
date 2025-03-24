"""
Agent tools API endpoints.

This module defines the FastAPI endpoints for agent tools.
"""
import logging
import time
from typing import Dict, Any, Optional, List

from fastapi import APIRouter, Depends, HTTPException, Header, Body
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from src.app import auth
from src.app.agents.tools.registry import get_tool, list_tools

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/v1/tools", tags=["tools"])


def verify_auth(authorization: Optional[str] = Header(None)) -> str:
    """
    Verify authorization header and return API key.
    
    Args:
        authorization: Authorization header
        
    Returns:
        API key
        
    Raises:
        HTTPException: If API key is missing or invalid
    """
    if not authorization:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail={
                "error": {
                    "message": "Missing API key",
                    "type": "auth_error",
                    "code": HTTP_401_UNAUTHORIZED
                }
            }
        )
    
    return auth.verify_api_key(authorization)


@router.get("")
async def get_tools(
    api_key: str = Depends(verify_auth)
):
    """
    List available tools.
    
    Args:
        api_key: The API key
        
    Returns:
        List of available tools
    """
    # Get user ID from API key
    user_id = auth.get_user_id(api_key)
    
    # Check rate limit
    auth.check_rate_limit(None, api_key)
    
    # Log the request
    logger.info(f"List tools request from user {user_id}")
    
    # Get available tools
    tools = list_tools()
    
    # Filter tools based on user roles
    user_roles = auth.get_user_roles(user_id)
    filtered_tools = []
    
    for tool in tools:
        required_role = tool.get("required_role", "basic")
        if required_role in user_roles or "admin" in user_roles:
            filtered_tools.append(tool)
    
    # Format response
    return {
        "tools": filtered_tools,
        "count": len(filtered_tools),
        "timestamp": int(time.time())
    }


@router.post("/call")
async def call_tool(
    tool: str = Body(..., embed=True),
    parameters: Dict[str, Any] = Body({}, embed=True),
    api_key: str = Depends(verify_auth)
):
    """
    Call a tool with parameters.
    
    Args:
        tool: The tool name
        parameters: The tool parameters
        api_key: The API key
        
    Returns:
        Tool execution result
    """
    # Get user ID from API key
    user_id = auth.get_user_id(api_key)
    
    # Check rate limit
    auth.check_rate_limit(None, api_key)
    
    # Log the request
    logger.info(f"Call tool request from user {user_id} for tool {tool}")
    
    # Get the tool
    tool_info = get_tool(tool)
    if not tool_info:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail={
                "error": {
                    "message": f"Tool '{tool}' not found",
                    "type": "not_found",
                    "code": HTTP_404_NOT_FOUND
                }
            }
        )
    
    # Check if user has required role
    required_role = tool_info.get("required_role", "basic")
    if not auth.has_role(user_id, required_role) and not auth.has_role(user_id, "admin"):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail={
                "error": {
                    "message": f"User does not have the required role '{required_role}' to use this tool",
                    "type": "permission_denied",
                    "code": HTTP_401_UNAUTHORIZED
                }
            }
        )
    
    # Get the tool function
    tool_function = tool_info.get("function")
    if not tool_function:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail={
                "error": {
                    "message": f"Tool '{tool}' is not callable",
                    "type": "invalid_tool",
                    "code": HTTP_400_BAD_REQUEST
                }
            }
        )
    
    # Execute the tool
    start_time = time.time()
    try:
        result = await tool_function(parameters)
        execution_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        # Format response
        return {
            "tool": tool,
            "parameters": parameters,
            "result": result,
            "execution_time": round(execution_time, 2),
            "timestamp": int(time.time())
        }
    except Exception as e:
        logger.error(f"Tool execution error: {e}")
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail={
                "error": {
                    "message": f"Tool execution failed: {str(e)}",
                    "type": "execution_error",
                    "code": HTTP_400_BAD_REQUEST
                }
            }
        )