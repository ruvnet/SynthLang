# LiteLLM Integration Plan for SynthLang Proxy

## Overview

This plan outlines the integration of LiteLLM into the SynthLang proxy to handle complex JSON requests while maintaining all existing capabilities (compression, caching, keyword detection, etc.). LiteLLM will be used as the primary interface to LLM providers, replacing the current direct OpenAI implementation.

## Goals

1. Resolve complex JSON request parsing issues
2. Maintain all existing SynthLang proxy capabilities
3. Support multiple LLM providers through a unified interface
4. Add robust error handling and fallback mechanisms
5. Add thorough testing to ensure compatibility

## Implementation Steps

### 1. Add LiteLLM to Dependencies

Update the requirements.txt file:

```
litellm>=1.22.0
```

### 2. Create LiteLLM Provider Module

Create a new module at `src/app/litellm_provider.py` that will handle all interactions with LLM providers through LiteLLM.

### 3. Implement Core Provider Functions

This module will implement the following functions:
- `complete_chat` - For standard chat completions
- `stream_chat` - For streaming chat completions
- Supporting utilities for error handling, model mapping, etc.

### 4. Update Request Processing

Modify the chat completion endpoints to:
- Handle both JSON and raw text requests
- Use LiteLLM for all provider interactions
- Maintain compatibility with existing middleware

### 5. Add LiteLLM Configuration

Add a configuration system for LiteLLM that supports:
- Multiple providers
- Model fallbacks
- Retry mechanisms
- Logging

### 6. Add Tests

Create comprehensive tests in `/proxy/tests/litellm` to verify:
- Basic functionality
- Complex request handling
- Error cases
- Integration with existing features

### 7. Update Documentation

Update documentation to reflect the new capabilities and configuration options.

## Detailed Implementation

### 1. LiteLLM Provider Module

The LiteLLM provider module will include:

```python
# src/app/litellm_provider.py
import os
import time
import logging
from typing import List, Dict, Any, AsyncGenerator, Optional, Union
import litellm
from litellm.utils import Callback

logger = logging.getLogger("app.litellm_provider")

# Configure LiteLLM
litellm.set_verbose = False  # Set to True for debugging
litellm.drop_params = True  # Drop unsupported params instead of erroring
litellm.success_callback = ["langfuse"]  # Optional logging

# Configure API keys from environment
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

if OPENAI_API_KEY:
    litellm.set_api_key(OPENAI_API_KEY, "openai")
if ANTHROPIC_API_KEY:
    litellm.set_api_key(ANTHROPIC_API_KEY, "anthropic")

# Model fallbacks
MODEL_FALLBACKS = {
    "gpt-4o-mini": ["openai/gpt-4o-mini", "openai/gpt-3.5-turbo"]
}

# Model routing
def map_model_name(model: str) -> str:
    """
    Map internal model names to provider-specific model names.
    """
    model_map = {
        "gpt-4o-mini": "openai/gpt-4o-mini",
        "gpt-4o": "openai/gpt-4o",
        "gpt-4": "openai/gpt-4-turbo",
        "gpt-3.5-turbo": "openai/gpt-3.5-turbo",
        "claude-3-opus": "anthropic/claude-3-opus",
        "claude-3-sonnet": "anthropic/claude-3-sonnet",
        "claude-3-haiku": "anthropic/claude-3-haiku"
    }
    return model_map.get(model, model)

# Callback for logging and error handling
class SynthLangCallback(Callback):
    async def on_response(self, response):
        model = response.get("model", "unknown")
        logger.info(f"LiteLLM response from model {model}")
        
    async def on_error(self, error, model, messages, kwargs):
        logger.error(f"LiteLLM error with model {model}: {error}")

# Initialize callback
litellm.callbacks = [SynthLangCallback()]

async def complete_chat(
    model: str, 
    messages: List[Dict[str, str]], 
    temperature: float = 1.0, 
    top_p: float = 1.0, 
    n: int = 1, 
    max_tokens: Optional[int] = None,
    user_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Send a chat completion request to the LLM provider using LiteLLM.
    
    Args:
        model: The model to use
        messages: The conversation messages
        temperature: Controls randomness (higher = more random)
        top_p: Controls diversity via nucleus sampling
        n: How many completions to generate
        max_tokens: Maximum number of tokens to generate
        user_id: A unique identifier for the end-user
        
    Returns:
        The chat completion response
    """
    try:
        # Map model name
        provider_model = map_model_name(model)
        
        # Configure retry parameters
        retry_config = {
            "max_retries": 3,
            "timeout": 60,
        }
        
        # Make the API call through LiteLLM
        response = await litellm.acompletion(
            model=provider_model,
            messages=messages,
            temperature=temperature,
            top_p=top_p,
            n=n,
            max_tokens=max_tokens,
            user=user_id,
            fallbacks=MODEL_FALLBACKS.get(model, []),
            **retry_config
        )
        
        # Ensure the response format is consistent with your existing API
        normalized_response = {
            "id": response.get("id", f"chatcmpl-{int(time.time())}"),
            "object": "chat.completion",
            "created": response.get("created", int(time.time())),
            "model": model,
            "choices": response.get("choices", []),
            "usage": response.get("usage", {})
        }
        
        return normalized_response
    except Exception as e:
        logger.error(f"LiteLLM completion error: {e}")
        raise

async def stream_chat(
    model: str, 
    messages: List[Dict[str, str]], 
    temperature: float = 1.0, 
    top_p: float = 1.0, 
    n: int = 1,
    max_tokens: Optional[int] = None,
    user_id: Optional[str] = None
) -> AsyncGenerator[Dict[str, Any], None]:
    """
    Stream a chat completion from the LLM provider using LiteLLM.
    
    Args:
        model: The model to use
        messages: The conversation messages
        temperature: Controls randomness (higher = more random)
        top_p: Controls diversity via nucleus sampling
        n: How many completions to generate
        max_tokens: Maximum number of tokens to generate
        user_id: A unique identifier for the end-user
        
    Yields:
        Streaming chunks of the chat completion response
    """
    try:
        # Map model name
        provider_model = map_model_name(model)
        
        # Configure retry parameters
        retry_config = {
            "max_retries": 3,
            "timeout": 60,
        }
        
        # Make the streaming API call through LiteLLM
        response_stream = await litellm.acompletion(
            model=provider_model,
            messages=messages,
            temperature=temperature,
            top_p=top_p,
            n=n,
            max_tokens=max_tokens,
            user=user_id,
            stream=True,
            fallbacks=MODEL_FALLBACKS.get(model, []),
            **retry_config
        )
        
        # Stream the response chunks
        async for chunk in response_stream:
            # Ensure consistent chunk format
            normalized_chunk = {
                "id": chunk.get("id", f"chatcmpl-{int(time.time())}"),
                "object": "chat.completion.chunk",
                "created": chunk.get("created", int(time.time())),
                "model": model,
                "choices": chunk.get("choices", [])
            }
            yield normalized_chunk
    except Exception as e:
        logger.error(f"LiteLLM streaming error: {e}")
        raise
```

### 2. Update Chat Completions Endpoint

Update the chat completions endpoint in `src/app/main.py` to handle both JSON and raw text:

```python
@app.post("/chat/completions")
async def create_chat_completion(
    request: Request,
    authorization: str = Header(None)
):
    """
    Create a chat completion (non-versioned endpoint).
    
    This endpoint accepts both JSON and raw text input. If the request
    content type is application/json, it will be parsed as a ChatRequest.
    Otherwise, it will be treated as raw text and processed as a user message.
    
    Args:
        request: The FastAPI request object
        authorization: The Authorization header containing the API key
        
    Returns:
        The chat completion response
    """
    content_type = request.headers.get("content-type", "").lower()
    
    # Check if the request is JSON
    if "application/json" in content_type:
        try:
            # Parse as JSON
            body = await request.json()
            # Convert to ChatRequest model
            chat_request = ChatRequest(**body)
            return await process_chat_completion(chat_request, authorization)
        except Exception as e:
            logger.error(f"Error parsing JSON request: {e}")
            # Fall through to raw text handling if JSON parsing fails
    
    # Handle as raw text
    try:
        # Read raw body
        raw_body = await request.body()
        text_content = raw_body.decode(errors='replace')
        
        # Get query parameters
        model = request.query_params.get("model", "gpt-4o-mini")
        temperature_str = request.query_params.get("temperature", "1.0")
        stream_str = request.query_params.get("stream", "false")
        max_tokens_str = request.query_params.get("max_tokens", None)
        
        # Parse parameters
        try:
            temperature = float(temperature_str)
            if temperature < 0 or temperature > 2:
                temperature = 1.0
        except ValueError:
            temperature = 1.0
            
        try:
            stream = stream_str.lower() in ("true", "1", "yes")
        except:
            stream = False
            
        try:
            max_tokens = int(max_tokens_str) if max_tokens_str else None
        except ValueError:
            max_tokens = None
        
        # Create a ChatRequest object
        chat_request = ChatRequest(
            model=model,
            messages=[Message(role="user", content=text_content)],
            temperature=temperature,
            stream=stream,
            max_tokens=max_tokens
        )
        
        logger.info(f"Processing raw text request as user message (length: {len(text_content)} chars)")
        return await process_chat_completion(chat_request, authorization)
    except Exception as e:
        logger.error(f"Error processing raw text request: {e}")
        raise HTTPException(
            status_code=400,
            detail={
                "error": {
                    "message": f"Failed to process request: {str(e)}",
                    "type": "request_error",
                    "code": 400
                }
            }
        )
```

### 3. Update Configuration

Update the configuration in `src/app/config.py` to include LiteLLM settings:

```python
# LiteLLM configuration
LITELLM_ENABLED = os.getenv("LITELLM_ENABLED", "true").lower() in ("true", "1", "yes")
LITELLM_CACHE = os.getenv("LITELLM_CACHE", "true").lower() in ("true", "1", "yes")
LITELLM_VERBOSE = os.getenv("LITELLM_VERBOSE", "false").lower() in ("true", "1", "yes")
LITELLM_TIMEOUT = int(os.getenv("LITELLM_TIMEOUT", "30"))
LITELLM_MAX_RETRIES = int(os.getenv("LITELLM_MAX_RETRIES", "3"))
```

### 4. Test Files

Create the following test files:

#### Basic Functionality Tests

```python
# /proxy/tests/litellm/test_litellm_provider.py
import pytest
import json
import os
from unittest.mock import patch, AsyncMock

from src.app.litellm_provider import (
    complete_chat,
    stream_chat,
    map_model_name
)

@pytest.fixture
def mock_messages():
    return [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how are you?"}
    ]

@pytest.fixture
def mock_response():
    return {
        "id": "chatcmpl-123",
        "object": "chat.completion",
        "created": 1677652288,
        "model": "gpt-4o-mini",
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "I'm doing well, thank you for asking! How can I help you today?"
            },
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": 20,
            "completion_tokens": 17,
            "total_tokens": 37
        }
    }

@pytest.mark.asyncio
async def test_complete_chat(mock_messages, mock_response):
    with patch('litellm.acompletion', new=AsyncMock(return_value=mock_response)) as mock_completion:
        response = await complete_chat("gpt-4o-mini", mock_messages)
        
        mock_completion.assert_called_once()
        assert response["choices"][0]["message"]["content"] == "I'm doing well, thank you for asking! How can I help you today?"
        assert response["model"] == "gpt-4o-mini"

@pytest.mark.asyncio
async def test_stream_chat(mock_messages):
    # Mock streaming response chunks
    chunks = [
        {"id": "chatcmpl-123", "object": "chat.completion.chunk", "created": 1677652288, "model": "gpt-4o-mini", 
         "choices": [{"index": 0, "delta": {"content": "I'm"}, "finish_reason": None}]},
        {"id": "chatcmpl-123", "object": "chat.completion.chunk", "created": 1677652288, "model": "gpt-4o-mini", 
         "choices": [{"index": 0, "delta": {"content": " doing"}, "finish_reason": None}]},
        {"id": "chatcmpl-123", "object": "chat.completion.chunk", "created": 1677652288, "model": "gpt-4o-mini", 
         "choices": [{"index": 0, "delta": {"content": " well"}, "finish_reason": "stop"}]}
    ]
    
    with patch('litellm.acompletion', new=AsyncMock(return_value=AsyncMock(__aiter__=AsyncMock(return_value=chunks)))) as mock_completion:
        response_chunks = []
        async for chunk in stream_chat("gpt-4o-mini", mock_messages):
            response_chunks.append(chunk)
        
        mock_completion.assert_called_once()
        assert len(response_chunks) == 3
        assert "I'm" in str(response_chunks[0])
        assert "doing" in str(response_chunks[1])
        assert "well" in str(response_chunks[2])

@pytest.mark.asyncio
async def test_error_handling(mock_messages):
    with patch('litellm.acompletion', new=AsyncMock(side_effect=Exception("API Error"))) as mock_completion:
        with pytest.raises(Exception):
            await complete_chat("gpt-4o-mini", mock_messages)
        
        mock_completion.assert_called_once()

def test_model_mapping():
    assert map_model_name("gpt-4o-mini") == "openai/gpt-4o-mini"
    assert map_model_name("claude-3-opus") == "anthropic/claude-3-opus"
    assert "openai/gpt-4-" in map_model_name("gpt-4")
```

#### Integration Tests

```python
# /proxy/tests/litellm/test_litellm_integration.py
import pytest
import json
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

from src.app.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_process_chat_completion():
    with patch("src.app.main.process_chat_completion") as mock:
        mock.return_value = {
            "id": "chatcmpl-123",
            "object": "chat.completion",
            "created": 1677652288,
            "model": "gpt-4o-mini",
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "I'm doing well, thank you for asking!"
                },
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": 20,
                "completion_tokens": 17,
                "total_tokens": 37
            }
        }
        yield mock

def test_json_request(client, mock_process_chat_completion):
    # Test a standard JSON request
    response = client.post(
        "/chat/completions",
        headers={"Content-Type": "application/json", "Authorization": "Bearer test-key"},
        json={
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": "Hello"}]
        }
    )
    
    assert response.status_code == 200
    assert "choices" in response.json()
    assert mock_process_chat_completion.called

def test_raw_text_request(client, mock_process_chat_completion):
    # Test a raw text request
    response = client.post(
        "/chat/completions?model=gpt-4o-mini",
        headers={"Content-Type": "text/plain", "Authorization": "Bearer test-key"},
        data="Hello, this is a raw text request"
    )
    
    assert response.status_code == 200
    assert "choices" in response.json()
    assert mock_process_chat_completion.called

def test_complex_json_request(client, mock_process_chat_completion):
    # Test a complex JSON request with nested structures
    complex_data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": {
                "main_text": "This is a complex message with nested structure",
                "metadata": {
                    "source": "user interface",
                    "timestamp": 1677652288,
                    "client_info": {"browser": "Chrome", "version": "98.0.4758.102"}
                },
                "attachments": [
                    {"title": "Document 1", "content": "Some content here"},
                    {"title": "Document 2", "content": "More content here"}
                ]
            }}
        ]
    }
    
    # Before implementing LiteLLM, this would fail with validation errors
    # After implementation, it should handle this by converting to string
    response = client.post(
        "/chat/completions",
        headers={"Content-Type": "application/json", "Authorization": "Bearer test-key"},
        json=complex_data
    )
    
    assert response.status_code == 200
    assert "choices" in response.json()
    assert mock_process_chat_completion.called

def test_malformed_json_fallback(client, mock_process_chat_completion):
    # Test that malformed JSON falls back to raw text handling
    response = client.post(
        "/chat/completions?model=gpt-4o-mini",
        headers={"Content-Type": "application/json", "Authorization": "Bearer test-key"},
        data="This is not valid JSON but should be handled as raw text"
    )
    
    assert response.status_code == 200
    assert "choices" in response.json()
    assert mock_process_chat_completion.called

def test_missing_authorization(client):
    # Test error handling for missing authorization
    response = client.post(
        "/chat/completions",
        headers={"Content-Type": "application/json"},
        json={
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": "Hello"}]
        }
    )
    
    assert response.status_code == 401
    assert "error" in response.json()
```

#### End-to-End Tests

```python
# /proxy/tests/litellm/test_litellm_e2e.py
import pytest
import asyncio
from unittest.mock import patch, AsyncMock
import os

from src.app.litellm_provider import complete_chat, stream_chat
from src.app.models import Message, ChatRequest
from src.app.main import process_chat_completion

@pytest.fixture
def chat_request():
    return ChatRequest(
        model="gpt-4o-mini",
        messages=[
            Message(role="system", content="You are a helpful assistant."),
            Message(role="user", content="Hello, how are you?")
        ],
        temperature=0.7
    )

@pytest.mark.asyncio
@pytest.mark.skipif(not os.environ.get("OPENAI_API_KEY"), reason="OPENAI_API_KEY not set")
async def test_real_completion(chat_request):
    """
    This test makes an actual API call if OPENAI_API_KEY is set.
    Skip this in CI environments or when API key is not available.
    """
    response = await complete_chat(
        model=chat_request.model,
        messages=[msg.dict() for msg in chat_request.messages],
        temperature=chat_request.temperature
    )
    
    assert response is not None
    assert "choices" in response
    assert len(response["choices"]) > 0
    assert "message" in response["choices"][0]
    assert "content" in response["choices"][0]["message"]

@pytest.mark.asyncio
async def test_process_chat_completion_integration(chat_request):
    """
    Test the complete flow from process_chat_completion using mocked provider.
    """
    mock_response = {
        "id": "chatcmpl-123",
        "object": "chat.completion",
        "created": 1677652288,
        "model": "gpt-4o-mini",
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "I'm the helpful assistant you requested!"
            },
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": 20,
            "completion_tokens": 17,
            "total_tokens": 37
        }
    }
    
    with patch("src.app.litellm_provider.complete_chat", new=AsyncMock(return_value=mock_response)):
        response = await process_chat_completion(chat_request, "Bearer test-key")
        
        assert response is not None
        assert "choices" in response
        assert len(response["choices"]) > 0
        assert "message" in response["choices"][0]
        assert response["choices"][0]["message"]["content"] == "I'm the helpful assistant you requested!"
```

### 5. Integration into Application

To switch from the current provider to LiteLLM, update the import in `main.py`:

```python
# Change:
from . import auth, cache, llm_provider, db

# To:
from . import auth, cache, litellm_provider as llm_provider, db
```

This approach lets you switch back and forth easily during testing.

### 6. Update Requirements

Add LiteLLM to your requirements.txt:

```
# Add to requirements.txt
litellm>=1.22.0
```

### 7. Deployment

1. Update the Dockerfile to install the new dependencies
2. Update environment variables in fly.toml:

```toml
[env]
  LITELLM_ENABLED = "true"
  LITELLM_VERBOSE = "false"
  LITELLM_TIMEOUT = "30"
  LITELLM_MAX_RETRIES = "3"
```

3. Deploy to fly.io:

```bash
fly deploy
```

## Conclusion

This implementation plan maintains all existing SynthLang proxy capabilities while adding LiteLLM integration to handle complex requests more robustly. The key improvements include:

1. Better handling of complex JSON structures
2. Fallback to raw text processing when JSON parsing fails
3. Improved error handling and retries
4. Multiple provider support through a unified interface
5. Comprehensive test coverage for the new functionality

This approach will resolve the validation errors seen in the logs while preserving all the existing features of the SynthLang proxy.