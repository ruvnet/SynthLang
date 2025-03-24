"""Web tools for SynthLang agents."""
import json
from typing import Dict, Any, Optional, List, Union
from urllib.parse import urlparse

import httpx

from synthlang.proxy.agents.registry import register_tool
from synthlang.utils.logger import get_logger

logger = get_logger(__name__)


@register_tool(description="Fetch content from a URL")
def fetch_url(
    url: str, 
    method: str = "GET", 
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, str]] = None,
    data: Optional[Union[Dict[str, Any], str]] = None,
    timeout: int = 30
) -> Dict[str, Any]:
    """Fetch content from a URL.
    
    Args:
        url: URL to fetch
        method: HTTP method (GET, POST, etc.)
        headers: Optional HTTP headers
        params: Optional query parameters
        data: Optional request data (for POST, PUT, etc.)
        timeout: Request timeout in seconds
        
    Returns:
        Dictionary with response data
        
    Raises:
        httpx.HTTPError: If request fails
    """
    # Validate URL
    parsed_url = urlparse(url)
    if not parsed_url.scheme or not parsed_url.netloc:
        raise ValueError(f"Invalid URL: {url}")
    
    # Only allow http and https schemes
    if parsed_url.scheme not in ["http", "https"]:
        raise ValueError(f"Unsupported URL scheme: {parsed_url.scheme}")
    
    # Set default headers
    request_headers = {
        "User-Agent": "SynthLang/0.2.0 Agent"
    }
    if headers:
        request_headers.update(headers)
    
    try:
        with httpx.Client(timeout=timeout) as client:
            # Prepare request data
            request_data = None
            if data:
                if isinstance(data, dict):
                    request_data = data
                else:
                    request_data = data
            
            # Make request
            response = client.request(
                method=method.upper(),
                url=url,
                headers=request_headers,
                params=params,
                json=request_data if isinstance(request_data, dict) else None,
                content=request_data if isinstance(request_data, str) else None
            )
            
            # Raise for status
            response.raise_for_status()
            
            # Try to parse as JSON
            content_type = response.headers.get("content-type", "")
            if "application/json" in content_type:
                try:
                    json_data = response.json()
                    return {
                        "status_code": response.status_code,
                        "headers": dict(response.headers),
                        "content_type": content_type,
                        "json": json_data,
                        "text": None
                    }
                except json.JSONDecodeError:
                    pass
            
            # Return as text
            return {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "content_type": content_type,
                "json": None,
                "text": response.text
            }
    except httpx.HTTPError as e:
        logger.error(f"HTTP error fetching {url}: {str(e)}")
        
        # Include error response if available
        error_response = None
        if hasattr(e, "response") and e.response is not None:
            try:
                error_response = {
                    "status_code": e.response.status_code,
                    "headers": dict(e.response.headers),
                    "text": e.response.text
                }
            except Exception:
                pass
        
        raise ValueError(f"HTTP error: {str(e)}", error_response)


@register_tool(description="Search the web for information")
def web_search(
    query: str,
    num_results: int = 5
) -> List[Dict[str, Any]]:
    """Search the web for information.
    
    Note: This is a placeholder implementation. In a real implementation,
    this would use a search API like Google, Bing, or DuckDuckGo.
    
    Args:
        query: Search query
        num_results: Number of results to return
        
    Returns:
        List of search results
        
    Raises:
        ValueError: If search fails
    """
    # This is a placeholder - in a real implementation, you would use a search API
    logger.warning("web_search is a placeholder and doesn't perform real searches")
    
    return [
        {
            "title": f"Example search result for '{query}'",
            "url": f"https://example.com/search?q={query}",
            "snippet": f"This is a placeholder result for the query '{query}'. "
                      f"In a real implementation, this would use a search API."
        }
    ]


@register_tool(description="Extract main content from a webpage")
def extract_content(url: str) -> Dict[str, Any]:
    """Extract main content from a webpage.
    
    Note: This is a simplified implementation. In a real implementation,
    this would use more sophisticated content extraction techniques.
    
    Args:
        url: URL of the webpage
        
    Returns:
        Dictionary with extracted content
        
    Raises:
        ValueError: If extraction fails
    """
    try:
        # Fetch the webpage
        response = fetch_url(url)
        
        if response["text"] is None:
            raise ValueError("No text content found")
        
        # In a real implementation, you would use a library like newspaper3k,
        # readability, or trafilatura for better content extraction
        text = response["text"]
        
        # Simple extraction - remove HTML tags (very naive approach)
        import re
        content = re.sub(r'<[^>]+>', ' ', text)
        content = re.sub(r'\s+', ' ', content).strip()
        
        # Get title (naive approach)
        title_match = re.search(r'<title[^>]*>(.*?)</title>', text, re.IGNORECASE | re.DOTALL)
        title = title_match.group(1).strip() if title_match else "Unknown Title"
        
        return {
            "url": url,
            "title": title,
            "content": content[:1000] + ("..." if len(content) > 1000 else ""),
            "content_length": len(content)
        }
    except Exception as e:
        logger.error(f"Error extracting content from {url}: {str(e)}")
        raise ValueError(f"Content extraction failed: {str(e)}")