"""SynthLang Proxy module for advanced prompt engineering capabilities.

This module provides proxy functionality for SynthLang, including:
- API client for remote proxy services
- Local proxy server
- Semantic caching
- Advanced compression
- Authentication utilities
- Agent SDK and tool registry
"""

from synthlang.proxy.api import ProxyClient
from synthlang.proxy.auth import (
    get_credentials,
    save_credentials,
    clear_credentials,
    validate_api_key
)
from synthlang.proxy.cache import SemanticCache, get_semantic_cache
from synthlang.proxy.compression import (
    compress_prompt,
    decompress_prompt,
    compress_with_gzip,
    decompress_with_gzip,
    get_compression_stats
)
from synthlang.proxy.config import ProxyConfig, get_proxy_config
from synthlang.proxy.server import create_app, start_server

__all__ = [
    # API client
    "ProxyClient",
    
    # Authentication
    "get_credentials",
    "save_credentials",
    "clear_credentials",
    "validate_api_key",
    
    # Caching
    "SemanticCache",
    "get_semantic_cache",
    
    # Compression
    "compress_prompt",
    "decompress_prompt",
    "compress_with_gzip",
    "decompress_with_gzip",
    "get_compression_stats",
    
    # Configuration
    "ProxyConfig",
    "get_proxy_config",
    
    # Server
    "create_app",
    "start_server"
]

# Version of the proxy module
__version__ = "0.2.0"