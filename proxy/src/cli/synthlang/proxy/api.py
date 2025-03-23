"""API client for SynthLang Proxy service."""
import json
from typing import Dict, List, Optional, Union, Any

import httpx
from httpx import Response

from synthlang.proxy.config import get_proxy_config
from synthlang.utils.logger import get_logger

logger = get_logger(__name__)


class ProxyClient:
    """Client for interacting with SynthLang Proxy service."""
    
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        """Initialize client with base URL and optional API key.
        
        Args:
            base_url: Base URL for the proxy service
            api_key: API key for authentication
        """
        config = get_proxy_config()
        self.base_url = base_url or config.endpoint
        self.api_key = api_key or config.api_key
        self.headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        logger.debug(f"Initialized ProxyClient with endpoint: {self.base_url}")
    
    def _make_request(
        self, method: str, endpoint: str, data: Optional[Dict] = None, 
        params: Optional[Dict] = None, stream: bool = False
    ) -> Union[Response, Dict]:
        """Make a request to the proxy service.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            data: Request data (for POST, PUT, etc.)
            params: Query parameters
            stream: Whether to stream the response
            
        Returns:
            Response object or parsed JSON response
            
        Raises:
            httpx.HTTPError: If the request fails
        """
        url = f"{self.base_url}{endpoint}"
        logger.debug(f"Making {method} request to {url}")
        
        try:
            with httpx.Client(timeout=30.0) as client:
                if method.upper() == "GET":
                    response = client.get(
                        url, params=params, headers=self.headers, stream=stream
                    )
                elif method.upper() == "POST":
                    response = client.post(
                        url, json=data, params=params, headers=self.headers, stream=stream
                    )
                elif method.upper() == "PUT":
                    response = client.put(
                        url, json=data, params=params, headers=self.headers, stream=stream
                    )
                elif method.upper() == "DELETE":
                    response = client.delete(
                        url, params=params, headers=self.headers, stream=stream
                    )
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                response.raise_for_status()
                
                if stream:
                    return response
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"HTTP error: {str(e)}")
            if hasattr(e, "response") and e.response is not None:
                try:
                    error_data = e.response.json()
                    logger.error(f"Error response: {json.dumps(error_data)}")
                except Exception:
                    logger.error(f"Error response text: {e.response.text}")
            raise
    
    def chat_completion(
        self, messages: List[Dict], model: Optional[str] = None, 
        stream: bool = False, **kwargs
    ) -> Dict:
        """Send a chat completion request to the proxy.
        
        Args:
            messages: List of message objects
            model: Model to use for completion
            stream: Whether to stream the response
            **kwargs: Additional parameters for the request
            
        Returns:
            Chat completion response
        """
        config = get_proxy_config()
        endpoint = "/v1/chat/completions"
        
        payload = {
            "model": model or config.default_model,
            "messages": messages,
            "stream": stream,
            **kwargs
        }
        
        return self._make_request("POST", endpoint, data=payload, stream=stream)
    
    def translate(self, source: str, framework: str) -> Dict:
        """Translate text using the proxy service.
        
        Args:
            source: Source text to translate
            framework: Target framework
            
        Returns:
            Translation result
        """
        endpoint = "/v1/translate"
        payload = {
            "source": source,
            "framework": framework
        }
        
        return self._make_request("POST", endpoint, data=payload)
    
    def optimize(self, prompt: str, **kwargs) -> Dict:
        """Optimize a prompt using the proxy service.
        
        Args:
            prompt: Prompt to optimize
            **kwargs: Additional parameters for optimization
            
        Returns:
            Optimization result
        """
        endpoint = "/v1/optimize"
        payload = {
            "prompt": prompt,
            **kwargs
        }
        
        return self._make_request("POST", endpoint, data=payload)
    
    def compress(self, text: str, use_gzip: bool = False) -> Dict:
        """Compress text using the proxy service.
        
        Args:
            text: Text to compress
            use_gzip: Whether to use gzip compression
            
        Returns:
            Compression result
        """
        endpoint = "/v1/compress"
        payload = {
            "text": text,
            "use_gzip": use_gzip
        }
        
        return self._make_request("POST", endpoint, data=payload)
    
    def decompress(self, compressed_text: str) -> Dict:
        """Decompress text using the proxy service.
        
        Args:
            compressed_text: Compressed text
            
        Returns:
            Decompression result
        """
        endpoint = "/v1/decompress"
        payload = {
            "text": compressed_text
        }
        
        return self._make_request("POST", endpoint, data=payload)
    
    def health_check(self) -> Dict:
        """Check the health of the proxy service.
        
        Returns:
            Health check result
        """
        endpoint = "/health"
        return self._make_request("GET", endpoint)