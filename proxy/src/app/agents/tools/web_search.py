"""
Web search tool for the agent SDK.

This module provides a tool for performing web searches using OpenAI's API.
"""
import os
import logging
from typing import Dict, Any, Optional
from openai import OpenAI
from app.agents.registry import register_tool

# Configure logging
logger = logging.getLogger(__name__)

# Initialize OpenAI client with API key from environment variable
# We'll initialize this lazily to avoid errors during import
client = None


def get_openai_client():
    """
    Get or initialize the OpenAI client.
    
    Returns:
        The OpenAI client instance
    """
    global client
    if client is None:
        api_key = os.getenv("OPENAI_API_KEY", "dummy_key_for_testing")
        client = OpenAI(api_key=api_key)
    return client


def perform_web_search(user_message: str, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Perform a web search using OpenAI API.
    
    Args:
        user_message: The user's query message
        options: Optional dictionary of web search options
        
    Returns:
        A dictionary containing the response message from the web search
    """
    try:
        logger.info(f"Performing web search for: {user_message[:50]}...")
        
        # Use default empty dict if options is None
        search_options = options or {}
        
        # Get the OpenAI client
        openai_client = get_openai_client()
        
        # Call OpenAI API with web search enabled
        completion = openai_client.chat.completions.create(
            model="gpt-4o-search-preview",  # or "gpt-4o-mini-search-preview" based on context
            web_search_options=search_options,
            messages=[{"role": "user", "content": user_message}],
        )
        
        # Extract and return the message
        response = completion.choices[0].message
        logger.info(f"Web search completed successfully")
        
        return response
    except Exception as e:
        logger.error(f"Error performing web search: {str(e)}")
        # Return error message
        return {"content": f"Error performing web search: {str(e)}"}


# Register the web search tool in the registry
register_tool("web_search", perform_web_search)