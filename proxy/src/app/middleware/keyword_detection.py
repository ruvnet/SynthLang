"""
Keyword detection middleware.

This module provides middleware for detecting keywords in messages.
"""
import logging
import re
from typing import Dict, List, Any, Optional

from src.app import auth
from src.app.keywords.registry import list_patterns, ENABLE_KEYWORD_DETECTION, DETECTION_THRESHOLD
from src.app.agents.tools.registry import get_tool

# Configure logging
logger = logging.getLogger(__name__)


async def apply_keyword_detection(
    messages: List[Dict[str, str]],
    user_id: str
) -> Optional[Dict[str, Any]]:
    """
    Apply keyword detection to messages.
    
    Args:
        messages: List of message dictionaries
        user_id: User ID
        
    Returns:
        Tool response if a keyword is detected, None otherwise
    """
    # Check if keyword detection is enabled
    if not ENABLE_KEYWORD_DETECTION:
        return None
    
    # Get patterns
    patterns = list_patterns()
    
    # Sort patterns by priority (highest first)
    sorted_patterns = sorted(patterns, key=lambda p: p.priority, reverse=True)
    
    # Get the last user message
    user_messages = [msg for msg in messages if msg.get("role") == "user"]
    if not user_messages:
        return None
    
    last_user_message = user_messages[-1].get("content", "")
    
    # Check each pattern
    for pattern_data in sorted_patterns:
        # Skip disabled patterns
        if not pattern_data.enabled:
            continue
        
        # Get pattern details
        tool_name = pattern_data.tool
        required_role = pattern_data.required_role
        
        # Skip if user doesn't have required role
        if required_role and not auth.has_role(user_id, required_role) and not auth.has_role(user_id, "admin"):
            continue
        
        # Check if pattern matches
        try:
            match = pattern_data.match(last_user_message)
            if match:
                logger.info(f"Keyword pattern '{pattern_data.name}' matched for user {user_id}")
                
                # Get the tool
                tool_info = get_tool(tool_name)
                if not tool_info:
                    logger.warning(f"Tool '{tool_name}' not found for pattern '{pattern_data.name}'")
                    continue
                
                # Get the tool function
                tool_function = tool_info.get("function")
                if not tool_function:
                    logger.warning(f"Tool '{tool_name}' is not callable")
                    continue
                
                # Extract parameters from match
                parameters = pattern_data.extract_params(match)
                
                # Add the full match
                parameters["match"] = match.group(0)
                
                # Add the user message
                parameters["user_message"] = last_user_message
                
                # Execute the tool
                try:
                    result = await tool_function(parameters)
                    
                    # Format response
                    return {
                        "content": result.get("value", "I processed your request."),
                        "tool": tool_name,
                        "pattern": pattern_data.name
                    }
                except Exception as e:
                    logger.error(f"Tool execution error: {e}")
                    # Continue checking other patterns
        except Exception as e:
            logger.error(f"Pattern matching error for '{pattern_data.name}': {e}")
            # Continue checking other patterns
    
    # No pattern matched
    return None