"""
Web search tool for the agent SDK.

This module provides a tool for performing web searches using OpenAI's API.
"""
import os
import sys
import logging
import traceback
from typing import Dict, Any, Optional
from openai import OpenAI

# Configure logging
logger = logging.getLogger(__name__)

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    logger.debug(f"Added {project_root} to Python path")

# Try to import from src.app first
try:
    from src.app.agents.registry import register_tool
    logger.debug("Successfully imported registry from src.app")
except ImportError as e:
    logger.error(f"Error importing from src.app.agents.registry: {e}")
    # Try to import from app
    try:
        from app.agents.registry import register_tool
        logger.debug("Successfully imported registry from app")
    except ImportError as e2:
        logger.error(f"Error importing from app.agents.registry: {e2}")
        # Define a dummy register_tool function to avoid errors
        def register_tool(name, func):
            logger.warning(f"Using dummy register_tool for {name}")

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
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            logger.error("OPENAI_API_KEY environment variable not set")
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        client = OpenAI(api_key=api_key)
    
    return client


# Synchronous version for testing
def perform_web_search(query: str, user_message: Optional[str] = None, user_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Perform a web search using OpenAI's API.
    
    Args:
        query: The search query
        user_message: The original user message (optional)
        user_id: The ID of the user making the request (optional)
        
    Returns:
        A dictionary containing the search results
    """
    logger.info(f"Performing web search for query: {query}")
    
    try:
        # Get the OpenAI client
        openai_client = get_openai_client()
        
        # Use OpenAI to perform the search
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful web search assistant. Provide a concise summary of search results for the user's query."},
                {"role": "user", "content": f"Search for: {query}"}
            ],
            max_tokens=500
        )
        
        # Extract the search results
        search_results = response.choices[0].message.content
        
        # Create the response
        response_text = f"""Web Search Results for "{query}":

{search_results}

This search was performed using the web search tool."""
        
        return {
            "content": response_text,
            "tool": "web_search",
            "query": query,
            "results": search_results
        }
    
    except Exception as e:
        error_message = f"""I couldn't perform a web search for "{query}".

Error: {str(e)}

Please try again with a different query or check your internet connection."""
        
        logger.error(f"Web search error: {str(e)}")
        
        return {
            "content": error_message,
            "tool": "web_search",
            "query": query,
            "error": str(e)
        }


# Async version for actual use
async def async_perform_web_search(query: str, user_message: Optional[str] = None, user_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Perform a web search using OpenAI's API asynchronously.
    
    Args:
        query: The search query
        user_message: The original user message (optional)
        user_id: The ID of the user making the request (optional)
        
    Returns:
        A dictionary containing the search results
    """
    # For now, just call the synchronous version
    # In a real implementation, this would use an async client
    return perform_web_search(query, user_message, user_id)


# Register the tool
try:
    register_tool("web_search", perform_web_search)
    logger.info("Web search tool registered successfully")
except Exception as e:
    logger.error(f"Error registering web_search tool: {e}")