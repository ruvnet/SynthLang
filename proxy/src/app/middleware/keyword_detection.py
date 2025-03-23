"""
Keyword detection middleware for the SynthLang Proxy.

This module provides middleware for detecting keywords in user messages and invoking the appropriate tools.
"""
import logging
import re
import sys
import os
import traceback
from typing import Dict, Any, List, Optional, Tuple, Union

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    print(f"Added {project_root} to Python path in keyword_detection.py")

# Print current Python path for debugging
print(f"Python path in keyword_detection.py: {sys.path}")

try:
    print("Attempting to import from src.app.keywords.registry")
    from src.app.keywords.registry import KEYWORD_REGISTRY, KeywordPattern
    print("Successfully imported from src.app.keywords.registry")
except ImportError as e:
    print(f"Error importing from src.app.keywords.registry: {e}")
    print(f"Traceback: {traceback.format_exc()}")
    try:
        print("Attempting to import from app.keywords.registry")
        from app.keywords.registry import KEYWORD_REGISTRY, KeywordPattern
        print("Successfully imported from app.keywords.registry")
    except ImportError as e2:
        print(f"Error importing from app.keywords.registry: {e2}")
        print(f"Traceback: {traceback.format_exc()}")
        raise e

try:
    print("Attempting to import from src.app.agents.registry")
    from src.app.agents.registry import get_tool
    print("Successfully imported from src.app.agents.registry")
except ImportError as e:
    print(f"Error importing from src.app.agents.registry: {e}")
    print(f"Traceback: {traceback.format_exc()}")
    try:
        print("Attempting to import from app.agents.registry")
        from app.agents.registry import get_tool
        print("Successfully imported from app.agents.registry")
    except ImportError as e2:
        print(f"Error importing from app.agents.registry: {e2}")
        print(f"Traceback: {traceback.format_exc()}")
        raise e

try:
    print("Attempting to import from src.app.auth.roles")
    from src.app.auth.roles import get_user_roles
    print("Successfully imported from src.app.auth.roles")
except ImportError as e:
    print(f"Error importing from src.app.auth.roles: {e}")
    print(f"Traceback: {traceback.format_exc()}")
    try:
        print("Attempting to import from app.auth.roles")
        from app.auth.roles import get_user_roles
        print("Successfully imported from app.auth.roles")
    except ImportError as e2:
        print(f"Error importing from app.auth.roles: {e2}")
        print(f"Traceback: {traceback.format_exc()}")
        raise e

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
            print(f"Matched pattern '{pattern.name}' for user '{user_id}'")
            
            # Get the tool
            tool_func = get_tool(pattern.tool)
            if not tool_func:
                logger.error(f"Tool '{pattern.tool}' not found for pattern '{pattern.name}'")
                print(f"Tool '{pattern.tool}' not found for pattern '{pattern.name}'")
                continue
            
            try:
                # Extract named groups from the match
                kwargs = match.groupdict()
                
                # Add the original message and user ID
                kwargs['user_message'] = message
                kwargs['user_id'] = user_id
                
                # Call the tool with the extracted parameters
                logger.info(f"Invoking tool '{pattern.tool}' with parameters: {kwargs}")
                print(f"Invoking tool '{pattern.tool}' with parameters: {kwargs}")
                result = await tool_func(**kwargs)
                
                # Add metadata to the result
                if isinstance(result, dict):
                    result.setdefault('pattern_name', pattern.name)
                    result.setdefault('tool', pattern.tool)
                
                return result
            except Exception as e:
                logger.exception(f"Error invoking tool '{pattern.tool}': {str(e)}")
                print(f"Error invoking tool '{pattern.tool}': {str(e)}")
                print(f"Traceback: {traceback.format_exc()}")
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
    # Check if keyword detection is enabled - import here to get the current value
    try:
        print("Attempting to import ENABLE_KEYWORD_DETECTION from src.app.keywords.registry")
        from src.app.keywords.registry import ENABLE_KEYWORD_DETECTION
        print(f"Successfully imported ENABLE_KEYWORD_DETECTION: {ENABLE_KEYWORD_DETECTION}")
    except ImportError as e:
        print(f"Error importing ENABLE_KEYWORD_DETECTION from src.app.keywords.registry: {e}")
        try:
            print("Attempting to import ENABLE_KEYWORD_DETECTION from app.keywords.registry")
            from app.keywords.registry import ENABLE_KEYWORD_DETECTION
            print(f"Successfully imported ENABLE_KEYWORD_DETECTION: {ENABLE_KEYWORD_DETECTION}")
        except ImportError as e2:
            print(f"Error importing ENABLE_KEYWORD_DETECTION from app.keywords.registry: {e2}")
            # Default to enabled if we can't import
            ENABLE_KEYWORD_DETECTION = True
            print(f"Using default value for ENABLE_KEYWORD_DETECTION: {ENABLE_KEYWORD_DETECTION}")
    
    if not ENABLE_KEYWORD_DETECTION:
        logger.debug("Keyword detection is disabled")
        print("Keyword detection is disabled")
        return None
        
    # Get the last user message
    last_message = get_last_user_message(messages)
    if not last_message:
        return None
    
    # Process the message with keywords
    return await process_message_with_keywords(last_message, user_id)