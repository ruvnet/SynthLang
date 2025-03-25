"""
End-to-end tests for LiteLLM integration.

This module tests the complete flow from request processing to response handling,
including integration with the existing functionality like compression and caching.
"""
import pytest
import asyncio
from unittest.mock import patch, AsyncMock, MagicMock
import os
import time

from src.app.litellm_provider import complete_chat, stream_chat
from src.app.models import Message, ChatRequest
from src.app import auth, cache

# Skip these tests in CI environments or when API key is not available
skip_reason = "OPENAI_API_KEY not set"
skip_real_api_calls = not os.environ.get("OPENAI_API_KEY")

@pytest.fixture
def chat_request():
    """Fixture for a sample chat request."""
    return ChatRequest(
        model="gpt-4o-mini",
        messages=[
            Message(role="system", content="You are a helpful assistant."),
            Message(role="user", content="Hello, how are you?")
        ],
        temperature=0.7
    )

@pytest.mark.asyncio
@pytest.mark.skipif(skip_real_api_calls, reason=skip_reason)
async def test_real_completion(chat_request):
    """
    Test making an actual API call if OPENAI_API_KEY is set.
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
@pytest.mark.skipif(skip_real_api_calls, reason=skip_reason)
async def test_real_streaming(chat_request):
    """
    Test making an actual streaming API call if OPENAI_API_KEY is set.
    Skip this in CI environments or when API key is not available.
    """
    chunks = []
    async for chunk in stream_chat(
        model=chat_request.model,
        messages=[msg.dict() for msg in chat_request.messages],
        temperature=chat_request.temperature
    ):
        chunks.append(chunk)
    
    assert len(chunks) > 0
    # At least some chunks should have content
    content_found = False
    for chunk in chunks:
        if "choices" in chunk and len(chunk["choices"]) > 0:
            choice = chunk["choices"][0]
            if "delta" in choice and "content" in choice["delta"] and choice["delta"]["content"]:
                content_found = True
                break
    assert content_found, "No content found in any streaming chunk"

@pytest.mark.asyncio
async def test_process_chat_completion_integration():
    """
    Test the complete flow from process_chat_completion using mocked provider.
    """
    from src.app.main import process_chat_completion
    
    chat_request = ChatRequest(
        model="gpt-4o-mini",
        messages=[
            Message(role="system", content="You are a helpful assistant."),
            Message(role="user", content="Hello, how are you?")
        ],
        temperature=0.7
    )
    
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
    
    # Mock the verify_api_key function
    with patch("src.app.auth.verify_api_key", return_value="test-api-key"), \
         patch("src.app.auth.get_user_id", return_value="test-user"), \
         patch("src.app.auth.check_rate_limit", return_value=None), \
         patch("src.app.middleware.keyword_detection.apply_keyword_detection", new=AsyncMock(return_value=None)), \
         patch("src.app.synthlang.api.synthlang_api.compress", return_value="compressed_content"), \
         patch("src.app.synthlang.api.synthlang_api.decompress", return_value="decompressed_content"), \
         patch("src.app.cache.make_cache_key", return_value="test-cache-key"), \
         patch("src.app.cache.get_similar_response", return_value=None), \
         patch("src.app.litellm_provider.complete_chat", new=AsyncMock(return_value=mock_response)), \
         patch("src.app.db.save_interaction", new=AsyncMock(return_value=None)), \
         patch("src.app.cache.store", return_value=None):
        
        response = await process_chat_completion(chat_request, "Bearer test-key")
        
        assert response is not None
        assert "choices" in response
        assert len(response["choices"]) > 0
        assert "message" in response["choices"][0]
        assert response["choices"][0]["message"]["content"] == "I'm the helpful assistant you requested!"

@pytest.mark.asyncio
async def test_compression_integration():
    """
    Test that LiteLLM integration works with SynthLang compression.
    """
    from src.app.main import process_chat_completion
    
    chat_request = ChatRequest(
        model="gpt-4o-mini",
        messages=[
            Message(role="system", content="You are a helpful assistant."),
            Message(role="user", content="This is a long message that should be compressed by SynthLang")
        ],
        temperature=0.7
    )
    
    mock_response = {
        "id": "chatcmpl-123",
        "object": "chat.completion",
        "created": 1677652288,
        "model": "gpt-4o-mini",
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "I've processed your compressed message!"
            },
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": 20,
            "completion_tokens": 17,
            "total_tokens": 37
        }
    }
    
    # Create a spy for compress/decompress to verify they're called
    compression_spy = MagicMock(return_value="compressed_content")
    decompression_spy = MagicMock(return_value="decompressed_content")
    
    # Mock the necessary functions
    with patch("src.app.auth.verify_api_key", return_value="test-api-key"), \
         patch("src.app.auth.get_user_id", return_value="test-user"), \
         patch("src.app.auth.check_rate_limit", return_value=None), \
         patch("src.app.middleware.keyword_detection.apply_keyword_detection", new=AsyncMock(return_value=None)), \
         patch("src.app.synthlang.api.synthlang_api.compress", compression_spy), \
         patch("src.app.synthlang.api.synthlang_api.decompress", decompression_spy), \
         patch("src.app.cache.make_cache_key", return_value="test-cache-key"), \
         patch("src.app.cache.get_similar_response", return_value=None), \
         patch("src.app.litellm_provider.complete_chat", new=AsyncMock(return_value=mock_response)), \
         patch("src.app.db.save_interaction", new=AsyncMock(return_value=None)), \
         patch("src.app.cache.store", return_value=None):
        
        response = await process_chat_completion(chat_request, "Bearer test-key")
        
        # Verify compression and decompression were called
        assert compression_spy.call_count == 2  # Once for system, once for user
        assert decompression_spy.call_count == 2  # Once for system, once for user
        
        # Verify response
        assert response is not None
        assert response["choices"][0]["message"]["content"] == "I've processed your compressed message!"

@pytest.mark.asyncio
async def test_cache_integration():
    """
    Test that LiteLLM integration works with the cache system.
    """
    from src.app.main import process_chat_completion
    
    chat_request = ChatRequest(
        model="gpt-4o-mini",
        messages=[
            Message(role="user", content="A question that should hit the cache")
        ],
        temperature=0.7
    )
    
    cached_response = "This is a cached response from a previous query"
    
    # Mock the necessary functions
    with patch("src.app.auth.verify_api_key", return_value="test-api-key"), \
         patch("src.app.auth.get_user_id", return_value="test-user"), \
         patch("src.app.auth.check_rate_limit", return_value=None), \
         patch("src.app.middleware.keyword_detection.apply_keyword_detection", new=AsyncMock(return_value=None)), \
         patch("src.app.synthlang.api.synthlang_api.compress", return_value="compressed_content"), \
         patch("src.app.cache.make_cache_key", return_value="test-cache-key"), \
         patch("src.app.cache.get_similar_response", return_value=cached_response), \
         patch("src.app.db.save_interaction", new=AsyncMock(return_value=None)), \
         patch("src.app.litellm_provider.complete_chat", new=AsyncMock()) as mock_complete_chat:
        
        response = await process_chat_completion(chat_request, "Bearer test-key")
        
        # Verify LiteLLM provider was NOT called (cache hit)
        mock_complete_chat.assert_not_called()
        
        # Verify response contains cached content
        assert response is not None
        assert "choices" in response
        assert response["choices"][0]["message"]["content"] == cached_response
        assert response.get("debug", {}).get("cache_hit", False) is True

@pytest.mark.asyncio
async def test_keyword_detection_integration():
    """
    Test that LiteLLM integration works with keyword detection.
    """
    from src.app.main import process_chat_completion
    
    chat_request = ChatRequest(
        model="gpt-4o-mini",
        messages=[
            Message(role="user", content="A message that should trigger keyword detection")
        ],
        temperature=0.7
    )
    
    keyword_response = {
        "content": "This response was generated by a keyword-triggered tool",
        "tool": "test-tool",
        "pattern": "test-pattern"
    }
    
    # Mock the necessary functions
    with patch("src.app.auth.verify_api_key", return_value="test-api-key"), \
         patch("src.app.auth.get_user_id", return_value="test-user"), \
         patch("src.app.auth.check_rate_limit", return_value=None), \
         patch("src.app.middleware.keyword_detection.apply_keyword_detection", 
               new=AsyncMock(return_value=keyword_response)), \
         patch("src.app.db.save_interaction", new=AsyncMock(return_value=None)), \
         patch("src.app.litellm_provider.complete_chat", new=AsyncMock()) as mock_complete_chat:
        
        response = await process_chat_completion(chat_request, "Bearer test-key")
        
        # Verify LiteLLM provider was NOT called (keyword detection handled it)
        mock_complete_chat.assert_not_called()
        
        # Verify response contains keyword-generated content
        assert response is not None
        assert "choices" in response
        assert response["choices"][0]["message"]["content"] == keyword_response["content"]
        assert response.get("debug", {}).get("keyword_detection", False) is True
        assert response.get("debug", {}).get("tool_used") == "test-tool"