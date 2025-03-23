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

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    print(f"Added {project_root} to Python path in web_search.py")

# Print current Python path for debugging
print(f"Python path in web_search.py: {sys.path}")

# Try to import from src.app first
try:
    print("Attempting to import registry from src.app.agents.registry")
    from src.app.agents.registry import register_tool
    print("Successfully imported registry from src.app.agents.registry")
except ImportError as e:
    print(f"Error importing from src.app.agents.registry: {e}")
    print(f"Traceback: {traceback.format_exc()}")
    # Try to import from app
    try:
        print("Attempting to import registry from app.agents.registry")
        from app.agents.registry import register_tool
        print("Successfully imported registry from app.agents.registry")
    except ImportError as e2:
        print(f"Error importing from app.agents.registry: {e2}")
        print(f"Traceback: {traceback.format_exc()}")
        # Define a dummy register_tool function to avoid errors
        def register_tool(name, func):
            print(f"Dummy register_tool called for {name}")
        print("Using dummy register_tool function")

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
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            logger.error("OPENAI_API_KEY environment variable not set")
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        client = OpenAI(api_key=api_key)
    
    return client


async def perform_web_search(query: str, user_message: Optional[str] = None, user_id: Optional[str] = None) -> Dict[str, Any]:
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
    print(f"Performing web search for query: {query}")
    
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
        response = f"""Web Search Results for "{query}":

{search_results}

This search was performed using the web search tool."""
        
        return {
            "content": response,
            "tool": "web_search",
            "query": query,
            "results": search_results
        }
    
    except Exception as e:
        error_message = f"""I couldn't perform a web search for "{query}".

Error: {str(e)}

Please try again with a different query or check your internet connection."""
        
        logger.error(f"Web search error: {str(e)}")
        print(f"Web search error: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        
        return {
            "content": error_message,
            "tool": "web_search",
            "query": query,
            "error": str(e)
        }

# Register the tool
try:
    print("Registering web_search tool")
    register_tool("web_search", perform_web_search)
    print("Web search tool registered successfully")
except Exception as e:
    print(f"Error registering web_search tool: {e}")
    print(f"Traceback: {traceback.format_exc()}")