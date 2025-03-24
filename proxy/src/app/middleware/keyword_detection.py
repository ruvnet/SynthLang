"""
Keyword detection middleware.

This module provides middleware for detecting keywords in messages.
"""
import logging
import re
from typing import Dict, List, Any, Optional, Set

from src.app.auth.roles import get_user_roles
from src.app.keywords.registry import list_patterns, ENABLE_KEYWORD_DETECTION, DETECTION_THRESHOLD
from src.app.agents.registry import get_tool

# Configure logging
logger = logging.getLogger(__name__)


def get_last_user_message(messages: List[Dict[str, str]]) -> Optional[str]:
    """
    Get the last user message from a list of messages.
    
    Args:
        messages: List of message dictionaries
        
    Returns:
        The content of the last user message, or None if no user messages
    """
    user_messages = [msg for msg in messages if msg.get("role") == "user"]
    if not user_messages:
        return None
    
    return user_messages[-1].get("content", "")


async def process_message_with_keywords(message: str, user_id: str) -> Optional[Dict[str, Any]]:
    """
    Process a message with keyword detection.
    
    Args:
        message: The message to process
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
    
    # Get user roles
    user_roles = get_user_roles(user_id)
    
    # Check each pattern
    for pattern_data in sorted_patterns:
        # Skip disabled patterns
        if not pattern_data.enabled:
            continue
        
        # Get pattern details
        tool_name = pattern_data.tool
        required_role = pattern_data.required_role
        
        # Skip if user doesn't have required role
        if required_role and required_role not in user_roles and "admin" not in user_roles:
            continue
        
        # Check if pattern matches
        try:
            match = pattern_data.match(message)
            if match:
                logger.info(f"Keyword pattern '{pattern_data.name}' matched for user {user_id}")
                
                # Get the tool
                tool = get_tool(tool_name)
                if not tool:
                    logger.warning(f"Tool '{tool_name}' not found for pattern '{pattern_data.name}'")
                    continue
                
                # Extract parameters from match
                parameters = pattern_data.extract_params(match)
                
                # Add the user message
                parameters["user_message"] = message
                
                # Add the user ID
                parameters["user_id"] = user_id
                
                # Execute the tool
                try:
                    result = await tool(**parameters)
                    return result
                except Exception as e:
                    logger.error(f"Tool execution error: {e}")
                    return {
                        "content": f"Error executing tool: {str(e)}",
                        "tool": tool_name,
                        "pattern": pattern_data.name,
                        "error": True
                    }
        except Exception as e:
            logger.error(f"Pattern matching error for '{pattern_data.name}': {e}")
            # Continue checking other patterns
    
    # No pattern matched
    return None


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
    # Import at runtime to allow for context managers to work correctly in tests
    from src.app.keywords.registry import ENABLE_KEYWORD_DETECTION
    
    # Check if keyword detection is enabled
    if not ENABLE_KEYWORD_DETECTION:
        return None
    
    # Get the last user message
    last_message = get_last_user_message(messages)
    if not last_message:
        return None
    
    # Process the message with keywords
    return await process_message_with_keywords(last_message, user_id)