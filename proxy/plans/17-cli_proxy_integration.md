# CLI Proxy Integration Plan

## Overview

This plan outlines the integration of the SynthLang Proxy capabilities into the existing CLI. The goal is to enhance the CLI with the advanced features developed for the proxy service, creating a unified tool that can be used for both local prompt engineering and remote proxy operations.

## Objectives

1. Update the CLI to include all proxy capabilities
2. Maintain backward compatibility with existing CLI functionality
3. Add new commands for proxy-specific features
4. Implement proper testing for all new features
5. Update documentation to reflect the new capabilities

## Current State Analysis

### CLI Structure
- Command-line interface for mathematical prompt engineering
- Framework translation and optimization using symbolic notation
- Core commands: translate, evolve, optimize, classify
- Mathematical frameworks support
- Example scripts and tutorials

### Proxy Capabilities to Integrate
- Advanced prompt compression
- Semantic caching
- API endpoint functionality
- Authentication and rate limiting
- Database persistence
- Security features (encryption, PII protection)
- Agent SDK and tool registry
- Streaming support
- DSPy integration for advanced prompt engineering

## Implementation Plan

### Phase 1: Core Structure Updates

#### 1.1. Update Dependencies

Update `pyproject.toml` and `requirements.txt` to include proxy dependencies:

```toml
[tool.poetry.dependencies]
python = "^3.8"
dspy-ai = "^2.0.0"
click = "^8.1.7"
python-dotenv = "^1.0.0"
pydantic = "^2.5.2"
rich = "^13.7.0"
fastapi = "^0.104.1"
uvicorn = "^0.23.2"
sqlalchemy = "^2.0.23"
cryptography = "^41.0.5"
httpx = "^0.25.1"
python-jose = "^3.3.0"
```

#### 1.2. Create Proxy Module Structure

Create a new module structure for proxy capabilities:

```
synthlang/
├── proxy/
│   ├── __init__.py
│   ├── api.py             # API client for proxy service
│   ├── auth.py            # Authentication utilities
│   ├── cache.py           # Semantic caching functionality
│   ├── compression.py     # Advanced compression utilities
│   ├── config.py          # Proxy configuration
│   ├── db.py              # Database utilities
│   ├── security.py        # Security utilities
│   ├── server.py          # Local proxy server
│   └── agents/            # Agent SDK
│       ├── __init__.py
│       ├── registry.py    # Tool registry
│       └── tools/         # Built-in tools
```

#### 1.3. Update Version and Changelog

Update version in `__init__.py` and add new entries to `CHANGELOG.md`:

```python
# synthlang/__init__.py
__version__ = "0.2.0"
```

```markdown
## [0.2.0] - 2025-03-23

### Added
- Proxy service integration
- Advanced prompt compression
- Semantic caching
- Local proxy server
- API client for remote proxy
- Authentication and rate limiting
- Database persistence
- Security features
- Agent SDK and tool registry
- Streaming support
```

### Phase 2: Feature Implementation

#### 2.1. Proxy API Client

Create an API client for interacting with remote proxy services:

```python
# synthlang/proxy/api.py
"""API client for SynthLang Proxy service."""
import httpx
from typing import Dict, List, Optional, Union, Any

class ProxyClient:
    """Client for interacting with SynthLang Proxy service."""
    
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        """Initialize client with base URL and optional API key."""
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
        
    def chat_completion(self, messages: List[Dict], model: str, **kwargs) -> Dict:
        """Send a chat completion request to the proxy."""
        endpoint = f"{self.base_url}/v1/chat/completions"
        payload = {
            "model": model,
            "messages": messages,
            **kwargs
        }
        response = httpx.post(endpoint, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    # Add methods for other proxy endpoints
```

#### 2.2. Local Proxy Server

Implement a local proxy server that can be started from the CLI:

```python
# synthlang/proxy/server.py
"""Local proxy server implementation."""
import uvicorn
from fastapi import FastAPI
from typing import Dict, Optional

def create_app() -> FastAPI:
    """Create FastAPI application for proxy server."""
    # Import here to avoid circular imports
    from app.main import app
    return app

def start_server(host: str = "127.0.0.1", port: int = 8000, 
                 log_level: str = "info", reload: bool = False) -> None:
    """Start the proxy server."""
    uvicorn.run(
        "synthlang.proxy.server:create_app",
        host=host,
        port=port,
        log_level=log_level,
        reload=reload
    )
```

#### 2.3. Authentication Utilities

Implement authentication utilities for the CLI:

```python
# synthlang/proxy/auth.py
"""Authentication utilities for SynthLang Proxy."""
import os
import json
from pathlib import Path
from typing import Dict, Optional

def get_credentials_path() -> Path:
    """Get path to credentials file."""
    config_dir = Path.home() / ".synthlang"
    config_dir.mkdir(exist_ok=True)
    return config_dir / "credentials.json"

def save_credentials(api_key: str, endpoint: Optional[str] = None) -> None:
    """Save API key and endpoint to credentials file."""
    creds_path = get_credentials_path()
    creds = {}
    if creds_path.exists():
        with open(creds_path) as f:
            creds = json.load(f)
    
    creds["api_key"] = api_key
    if endpoint:
        creds["endpoint"] = endpoint
        
    with open(creds_path, "w") as f:
        json.dump(creds, f)
        
def get_credentials() -> Dict:
    """Get credentials from file or environment."""
    creds_path = get_credentials_path()
    creds = {}
    
    # Try to load from file
    if creds_path.exists():
        with open(creds_path) as f:
            creds = json.load(f)
            
    # Override with environment variables if present
    api_key = os.environ.get("SYNTHLANG_API_KEY")
    if api_key:
        creds["api_key"] = api_key
        
    endpoint = os.environ.get("SYNTHLANG_ENDPOINT")
    if endpoint:
        creds["endpoint"] = endpoint
        
    return creds
```

#### 2.4. Compression Utilities

Implement advanced compression utilities:

```python
# synthlang/proxy/compression.py
"""Advanced compression utilities for SynthLang Proxy."""
import gzip
import base64
from typing import Optional

def compress_with_gzip(text: str) -> str:
    """Compress text using gzip and encode as base64."""
    compressed = gzip.compress(text.encode("utf-8"))
    return base64.b64encode(compressed).decode("utf-8")

def decompress_with_gzip(compressed_text: str) -> str:
    """Decompress base64-encoded gzipped text."""
    compressed = base64.b64decode(compressed_text)
    return gzip.decompress(compressed).decode("utf-8")

def compress_prompt(prompt: str, use_gzip: bool = False) -> str:
    """Compress prompt using SynthLang compression and optionally gzip."""
    # First apply SynthLang compression
    from synthlang.core.translator import FrameworkTranslator
    translator = FrameworkTranslator(None)
    result = translator.translate(prompt)
    compressed = result["target"]
    
    # Optionally apply gzip compression
    if use_gzip:
        compressed = compress_with_gzip(compressed)
        
    return compressed

def decompress_prompt(compressed: str) -> str:
    """Decompress prompt, handling both SynthLang and gzip compression."""
    # Check if it's gzip compressed
    try:
        if "=" in compressed:  # Likely base64
            decompressed = decompress_with_gzip(compressed)
        else:
            decompressed = compressed
            
        # TODO: Implement SynthLang decompression
        return decompressed
    except Exception as e:
        return compressed  # Return as-is if decompression fails
```

#### 2.5. Semantic Caching

Implement semantic caching functionality:

```python
# synthlang/proxy/cache.py
"""Semantic caching functionality for SynthLang Proxy."""
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any
import time

class SemanticCache:
    """Simple semantic cache implementation."""
    
    def __init__(self, cache_dir: Optional[str] = None):
        """Initialize cache with optional directory."""
        if cache_dir:
            self.cache_dir = Path(cache_dir)
        else:
            self.cache_dir = Path.home() / ".synthlang" / "cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
    def _get_cache_path(self, key: str) -> Path:
        """Get path for cache entry."""
        hash_key = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{hash_key}.json"
        
    def get(self, key: str) -> Optional[Dict]:
        """Get item from cache."""
        cache_path = self._get_cache_path(key)
        if not cache_path.exists():
            return None
            
        with open(cache_path) as f:
            entry = json.load(f)
            
        # Check if entry is expired
        if entry.get("expires_at") and entry["expires_at"] < time.time():
            cache_path.unlink()
            return None
            
        return entry["value"]
        
    def set(self, key: str, value: Dict, ttl: Optional[int] = None) -> None:
        """Set item in cache with optional TTL in seconds."""
        cache_path = self._get_cache_path(key)
        
        entry = {
            "key": key,
            "value": value,
            "created_at": time.time()
        }
        
        if ttl:
            entry["expires_at"] = time.time() + ttl
            
        with open(cache_path, "w") as f:
            json.dump(entry, f)
            
    def clear(self) -> None:
        """Clear all cache entries."""
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()
```

#### 2.6. Agent SDK

Implement the agent SDK and tool registry:

```python
# synthlang/proxy/agents/registry.py
"""Tool registry for SynthLang agents."""
from typing import Dict, Callable, Any, List

# Global registry of tools
_TOOLS: Dict[str, Callable] = {}

def register_tool(name: str, func: Callable) -> None:
    """Register a tool in the global registry."""
    _TOOLS[name] = func
    
def get_tool(name: str) -> Callable:
    """Get a tool from the registry."""
    if name not in _TOOLS:
        raise ValueError(f"Tool '{name}' not found in registry")
    return _TOOLS[name]
    
def list_tools() -> List[str]:
    """List all registered tools."""
    return list(_TOOLS.keys())
```

### Phase 3: CLI Command Updates

#### 3.1. Add Proxy Commands

Update `cli.py` to add proxy-related commands:

```python
# synthlang/cli.py
"""Command-line interface for SynthLang."""
import click
from typing import Optional

@click.group()
@click.version_option()
def cli():
    """SynthLang CLI - Mathematical prompt engineering and proxy integration."""
    pass

# Existing commands...

@cli.group()
def proxy():
    """Commands for working with SynthLang Proxy."""
    pass
    
@proxy.command()
@click.option("--host", default="127.0.0.1", help="Host to bind to")
@click.option("--port", default=8000, help="Port to bind to")
@click.option("--reload", is_flag=True, help="Enable auto-reload")
def serve(host: str, port: int, reload: bool):
    """Start a local proxy server."""
    from synthlang.proxy.server import start_server
    click.echo(f"Starting proxy server on {host}:{port}")
    start_server(host=host, port=port, reload=reload)
    
@proxy.command()
@click.option("--api-key", required=True, help="API key for proxy service")
@click.option("--endpoint", default="https://api.synthlang.org", help="Proxy endpoint")
def login(api_key: str, endpoint: str):
    """Save credentials for proxy service."""
    from synthlang.proxy.auth import save_credentials
    save_credentials(api_key, endpoint)
    click.echo(f"Credentials saved for {endpoint}")
    
@proxy.command()
@click.option("--model", default="gpt-4o-mini", help="Model to use")
@click.option("--system", help="System message")
@click.argument("prompt")
def chat(model: str, system: Optional[str], prompt: str):
    """Send a chat request to the proxy."""
    from synthlang.proxy.api import ProxyClient
    from synthlang.proxy.auth import get_credentials
    
    creds = get_credentials()
    if "api_key" not in creds:
        click.echo("No API key found. Run 'synthlang proxy login' first.")
        return
        
    endpoint = creds.get("endpoint", "https://api.synthlang.org")
    client = ProxyClient(endpoint, creds["api_key"])
    
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    
    try:
        response = client.chat_completion(messages, model)
        click.echo(response["choices"][0]["message"]["content"])
    except Exception as e:
        click.echo(f"Error: {e}")
        
@proxy.command()
@click.option("--use-gzip", is_flag=True, help="Use gzip compression")
@click.argument("prompt")
def compress(use_gzip: bool, prompt: str):
    """Compress a prompt using SynthLang compression."""
    from synthlang.proxy.compression import compress_prompt
    compressed = compress_prompt(prompt, use_gzip)
    click.echo(f"Original: {len(prompt)} chars")
    click.echo(f"Compressed: {len(compressed)} chars")
    click.echo(compressed)
    
@proxy.command()
@click.argument("compressed")
def decompress(compressed: str):
    """Decompress a SynthLang-compressed prompt."""
    from synthlang.proxy.compression import decompress_prompt
    decompressed = decompress_prompt(compressed)
    click.echo(decompressed)
    
@proxy.command()
def clear_cache():
    """Clear the semantic cache."""
    from synthlang.proxy.cache import SemanticCache
    cache = SemanticCache()
    cache.clear()
    click.echo("Cache cleared")
```

#### 3.2. Update Existing Commands

Update existing commands to use proxy capabilities when available:

```python
# synthlang/cli.py

@cli.command()
@click.option("--source", required=True, help="Source text to translate")
@click.option("--framework", default="synthlang", help="Target framework")
@click.option("--use-proxy", is_flag=True, help="Use proxy service if available")
def translate(source: str, framework: str, use_proxy: bool):
    """Translate text to the specified framework."""
    if use_proxy:
        try:
            from synthlang.proxy.api import ProxyClient
            from synthlang.proxy.auth import get_credentials
            
            creds = get_credentials()
            if "api_key" in creds:
                endpoint = creds.get("endpoint", "https://api.synthlang.org")
                client = ProxyClient(endpoint, creds["api_key"])
                response = client.translate(source, framework)
                click.echo(response["target"])
                return
        except Exception:
            # Fall back to local implementation
            pass
            
    # Local implementation
    from synthlang.core.translator import FrameworkTranslator
    translator = FrameworkTranslator(None)
    result = translator.translate(source)
    click.echo(result["target"])
```

### Phase 4: Testing

#### 4.1. Unit Tests

Create unit tests for new functionality:

```python
# tests/proxy/test_compression.py
"""Tests for compression utilities."""
import pytest
from synthlang.proxy.compression import compress_with_gzip, decompress_with_gzip

def test_gzip_compression():
    """Test gzip compression and decompression."""
    original = "This is a test string that should be compressed"
    compressed = compress_with_gzip(original)
    decompressed = decompress_with_gzip(compressed)
    assert decompressed == original
    assert len(compressed) < len(original)
```

```python
# tests/proxy/test_cache.py
"""Tests for semantic cache."""
import pytest
import time
from synthlang.proxy.cache import SemanticCache

def test_cache_set_get():
    """Test setting and getting cache entries."""
    cache = SemanticCache()
    cache.clear()  # Start with clean cache
    
    key = "test_key"
    value = {"data": "test_value"}
    
    # Set and get
    cache.set(key, value)
    result = cache.get(key)
    assert result == value
    
    # Test TTL
    cache.set(key, value, ttl=1)  # 1 second TTL
    assert cache.get(key) == value
    time.sleep(1.1)  # Wait for expiration
    assert cache.get(key) is None
```

#### 4.2. Integration Tests

Create integration tests for CLI commands:

```python
# tests/test_cli_proxy.py
"""Integration tests for proxy CLI commands."""
import pytest
from click.testing import CliRunner
from synthlang.cli import cli

def test_compress_command():
    """Test the compress command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["proxy", "compress", "This is a test prompt"])
    assert result.exit_code == 0
    assert "Original:" in result.output
    assert "Compressed:" in result.output
    
def test_decompress_command():
    """Test the decompress command."""
    runner = CliRunner()
    compressed = "↹ test•prompt"
    result = runner.invoke(cli, ["proxy", "decompress", compressed])
    assert result.exit_code == 0
    assert result.output.strip()  # Should have some output
```

### Phase 5: Documentation Updates

#### 5.1. Update README.md

Update the CLI README.md to include proxy capabilities:

```markdown
# SynthLang CLI

A powerful command-line interface for mathematical prompt engineering, framework translation, optimization, and proxy integration.

## Installation

```bash
pip install synthlang
```

## Core Commands

| Command | Description | Example |
|---------|-------------|---------|
| `translate` | Convert natural language to SynthLang format | `synthlang translate --source "your prompt" --framework synthlang` |
| `evolve` | Improve prompts using genetic algorithms | `synthlang evolve --seed "initial prompt" --generations 5` |
| `optimize` | Optimize prompts for efficiency | `synthlang optimize --prompt "your prompt"` |
| `classify` | Analyze and categorize prompts | `synthlang classify predict --text "prompt" --labels "categories"` |

## Proxy Commands

| Command | Description | Example |
|---------|-------------|---------|
| `proxy serve` | Start a local proxy server | `synthlang proxy serve --port 8000` |
| `proxy login` | Save credentials for proxy service | `synthlang proxy login --api-key "your-key"` |
| `proxy chat` | Send a chat request to the proxy | `synthlang proxy chat "Hello, world"` |
| `proxy compress` | Compress a prompt | `synthlang proxy compress "Your prompt"` |
| `proxy decompress` | Decompress a prompt | `synthlang proxy decompress "↹ prompt"` |
| `proxy clear-cache` | Clear the semantic cache | `synthlang proxy clear-cache` |
```

#### 5.2. Create New Documentation

Create new documentation for proxy features:

```markdown
# Proxy Integration

SynthLang CLI now includes integration with SynthLang Proxy, allowing you to:

1. Run a local proxy server
2. Connect to remote proxy services
3. Use advanced compression and caching
4. Access all proxy features from the command line

## Starting a Local Server

```bash
synthlang proxy serve --port 8000
```

This starts a local proxy server that you can use for development and testing.

## Connecting to a Remote Proxy

```bash
synthlang proxy login --api-key "your-key" --endpoint "https://your-proxy.com"
```

This saves your credentials for connecting to a remote proxy service.

## Using the Proxy for Chat

```bash
synthlang proxy chat --model "gpt-4o" "What is the capital of France?"
```

This sends a chat request to the proxy service.

## Advanced Compression

```bash
synthlang proxy compress --use-gzip "Your long prompt here"
```

This compresses a prompt using SynthLang compression and optionally gzip.
```

### Phase 6: Release

#### 6.1. Update Version

Update version in `__init__.py`:

```python
# synthlang/__init__.py
__version__ = "0.2.0"
```

#### 6.2. Build and Publish

Build and publish the updated package:

```bash
poetry build
poetry publish
```

## Timeline

1. Phase 1 (Core Structure Updates): 1 day
2. Phase 2 (Feature Implementation): 3 days
3. Phase 3 (CLI Command Updates): 1 day
4. Phase 4 (Testing): 2 days
5. Phase 5 (Documentation Updates): 1 day
6. Phase 6 (Release): 1 day

Total: 9 days

## Dependencies

- Python 3.8+
- DSPy 2.0.0+
- FastAPI
- SQLAlchemy
- Cryptography
- HTTPX

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Breaking existing functionality | Comprehensive testing of all existing features |
| Dependency conflicts | Careful management of dependencies and version constraints |
| Performance issues | Profiling and optimization of critical paths |
| Security vulnerabilities | Security review of all new code |
| Compatibility issues | Support for multiple Python versions and platforms |

## Success Criteria

1. All existing CLI functionality continues to work
2. All proxy capabilities are accessible through the CLI
3. All tests pass
4. Documentation is complete and accurate
5. Package can be installed and used without errors