"""
JSON validation fix for handling XML-like content in requests.

This module provides a function to safely parse JSON that might contain XML-like tags.
"""
import json
import logging

# Configure logging
logger = logging.getLogger("app.json_validation")

def safe_json_loads(json_str):
    """
    Safely parse JSON that might contain XML-like tags.
    
    This function escapes < and > characters before parsing JSON to prevent
    the parser from mistaking XML tags for JSON syntax.
    
    Args:
        json_str: The JSON string to parse
        
    Returns:
        The parsed JSON object
    """
    try:
        # First try normal parsing
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        # If it fails and contains < characters, try escaping them
        if '<' in json_str:
            logger.info("JSON parsing failed, attempting to escape XML-like tags")
            # Replace < and > with Unicode escape sequences
            safe_str = json_str.replace("<", "\\u003c").replace(">", "\\u003e")
            try:
                return json.loads(safe_str)
            except json.JSONDecodeError:
                # If it still fails, re-raise the original error
                logger.error(f"JSON parsing failed even after escaping XML-like tags: {e}")
                raise e
        else:
            # If there are no < characters, re-raise the original error
            raise e