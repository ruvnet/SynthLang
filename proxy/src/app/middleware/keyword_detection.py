"""
Keyword detection middleware for the SynthLang Proxy.

This module provides middleware for detecting keywords in user messages and invoking the appropriate tools.
"""
import logging
import re
from typing import Dict, Any, List, Optional, Tuple, Union

from app.keywords.registry import KEYWORD_REGISTRY, KeywordPattern
from app.agents.registry import get_tool
from app.auth.roles import get_user_roles

# Logger for this module
logger = logging.getLogger(__name__)

def get_last_user_message(messages: List[Dict[str, str]]) -> Optional[str]:
    """
    Extract the last user message from a list of messages.
    
    Args:
        messages: List of message dictionaries with 'role' and 'content' keys
        
    Returns:
        The content of the last user message, or None if no user message is found
    """
    for message in reversed(messages):
        if message.get('role') == 'user':
            return message.get('content')
    return None

async def process_message_with_keywords(message: str, user_id: str) -> Optional[Dict[str, Any]]:
    """
    Process a message to detect keywords and invoke the appropriate tool.
    
    Args:
        message: The message to process
        user_id: The ID of the user who sent the message
        
    Returns:
        The tool response if a keyword is detected, None otherwise
    """
    if not message or not user_id:
        return None
    
    # Get user roles
    user_roles = get_user_roles(user_id)
    
    # Sort patterns by priority (highest first)
    sorted_patterns = sorted(
        KEYWORD_REGISTRY.values(),
        key=lambda p: p.priority,
        reverse=True
    )
    
    # Check each pattern
    for pattern in sorted_patterns:
        # Skip if the pattern requires a role the user doesn't have
        if pattern.required_role and pattern.required_role not in user_roles:
            continue
        
        # Try to match the pattern
        match = re.search(pattern.pattern, message, re.IGNORECASE)
        if match:
            logger.info(f"Matched pattern '{pattern.name}' for user '{user_id}'")
            
            # Get the tool
            tool_func = get_tool(pattern.tool)
            if not tool_func:
                logger.error(f"Tool '{pattern.tool}' not found for pattern '{pattern.name}'")
                continue
            
            try:
                # Extract named groups from the match
                kwargs = match.groupdict()
                
                # Add the original message and user ID
                kwargs['user_message'] = message
                kwargs['user_id'] = user_id
                
                # Call the tool with the extracted parameters
                logger.info(f"Invoking tool '{pattern.tool}' with parameters: {kwargs}")
                result = await tool_func(**kwargs)
                
                # Add metadata to the result
                if isinstance(result, dict):
                    result.setdefault('pattern_name', pattern.name)
                    result.setdefault('tool', pattern.tool)
                
                return result
            except Exception as e:
                logger.exception(f"Error invoking tool '{pattern.tool}': {str(e)}")
                return {
                    "content": f"I encountered an error while trying to process your request: {str(e)}",
                    "pattern_name": pattern.name,
                    "tool": pattern.tool,
                    "error": str(e)
                }
    
    # No pattern matched
    return None

async def apply_keyword_detection(messages: List[Dict[str, str]], user_id: str) -> Optional[Dict[str, Any]]:
    """
    Apply keyword detection to a list of messages.
    
    Args:
        messages: List of message dictionaries with 'role' and 'content' keys
        user_id: The ID of the user who sent the messages
        
    Returns:
        The tool response if a keyword is detected, None otherwise
    """
    # Get the last user message
    last_message = get_last_user_message(messages)
    if not last_message:
        return None
    
    # Process the message with keywords
    return await process_message_with_keywords(last_message, user_id)