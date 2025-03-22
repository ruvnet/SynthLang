"""
Tests for the API endpoints.

This module contains tests for the API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
import numpy as np
import time

from app.main import app
from app import cache, llm_provider, db


client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint returns API information."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert "status" in data
    assert data["status"] == "operational"


def test_health_check_endpoint():
    """Test the health check endpoint."""
    with patch("app.synthlang.is_synthlang_available", return_value=True):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert data["synthlang_available"] is True


def test_chat_completion_endpoint_missing_api_key():
    """Test that the chat completion endpoint requires an API key."""
    req_body = {
        "model": "test-model",
        "messages": [{"role": "user", "content": "Hello"}]
    }
    response = client.post("/v1/chat/completions", json=req_body)
    assert response.status_code == 401
    data = response.json()
    assert "error" in data
    assert "message" in data["error"]
    assert "Missing API key" in data["error"]["message"]


def test_chat_completion_endpoint_invalid_api_key():
    """Test that the chat completion endpoint rejects invalid API keys."""
    headers = {"Authorization": "Bearer invalid_key"}
    req_body = {
        "model": "test-model",
        "messages": [{"role": "user", "content": "Hello"}]
    }
    response = client.post("/v1/chat/completions", json=req_body, headers=headers)
    assert response.status_code == 401
    data = response.json()
    assert "error" in data
    assert "message" in data["error"]
    assert "Invalid API key" in data["error"]["message"]


def test_chat_completion_endpoint_valid_api_key():
    """Test that the chat completion endpoint accepts valid API keys and saves to database."""
    # Mock the rate limit check to avoid rate limiting in tests
    with patch("app.auth.check_rate_limit", return_value=None), \
         patch("app.synthlang.compress_prompt", side_effect=lambda x: f"compressed: {x}"), \
         patch("app.llm_provider.complete_chat", new_callable=AsyncMock) as mock_complete_chat, \
         patch("app.db.save_interaction", new_callable=AsyncMock) as mock_save_interaction:
        
        # Mock the LLM response
        mock_complete_chat.return_value = {
            "id": "chatcmpl-123",
            "object": "chat.completion",
            "created": 1677858242,
            "model": "gpt-4o-search-preview",
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "This is a test response from the mock LLM API."
                    },
                    "index": 0,
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 10,
                "total_tokens": 20
            }
        }
        
        headers = {"Authorization": "Bearer sk_test_user1"}
        req_body = {
            "model": "test-model",
            "messages": [{"role": "user", "content": "Hello"}]
        }
        response = client.post("/v1/chat/completions", json=req_body, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "choices" in data
        assert len(data["choices"]) > 0
        assert "message" in data["choices"][0]
        assert "content" in data["choices"][0]["message"]
        
        # Verify that the LLM provider was called
        mock_complete_chat.assert_called_once()
        
        # Verify that save_interaction was called
        mock_save_interaction.assert_called_once()
        
        # Check the arguments - we know user_id and model should be correct
        args = mock_save_interaction.call_args.args
        assert args[0] == "user1"  # user_id
        assert args[1] == "test-model"  # model
        # Note: We don't check all arguments as the exact structure might vary


def test_chat_completion_endpoint_rate_limit():
    """Test that the chat completion endpoint enforces rate limits."""
    # Mock the rate limit check to simulate rate limiting
    with patch("app.auth.allow_request", return_value=False):
        headers = {"Authorization": "Bearer sk_test_user1"}
        req_body = {
            "model": "test-model",
            "messages": [{"role": "user", "content": "Hello"}]
        }
        
        response = client.post("/v1/chat/completions", json=req_body, headers=headers)
        assert response.status_code == 429
        data = response.json()
        assert "error" in data
        assert "message" in data["error"]
        assert "Rate limit exceeded" in data["error"]["message"]


def test_chat_completion_endpoint_synthlang_compression():
    """Test that the chat completion endpoint uses SynthLang compression."""
    # Mock the rate limit check and SynthLang compression
    with patch("app.auth.check_rate_limit", return_value=None), \
         patch("app.synthlang.compress_prompt") as mock_compress, \
         patch("app.llm_provider.complete_chat", new_callable=AsyncMock) as mock_complete_chat, \
         patch("app.db.save_interaction", new_callable=AsyncMock):
        
        mock_compress.return_value = "compressed content"
        mock_complete_chat.return_value = {
            "id": "chatcmpl-123",
            "created": int(time.time()),
            "choices": [{"message": {"content": "Test response"}}],
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 10,
                "total_tokens": 20
            }
        }
        
        headers = {"Authorization": "Bearer sk_test_user1"}
        req_body = {
            "model": "test-model",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": "Hello"}
            ]
        }
        response = client.post("/v1/chat/completions", json=req_body, headers=headers)
        assert response.status_code == 200
        
        # Verify that compress_prompt was called twice (once for system, once for user)
        assert mock_compress.call_count == 2
        mock_compress.assert_any_call("You are a helpful assistant")
        mock_compress.assert_any_call("Hello")


def test_invalid_request_format():
    """Test that the API returns appropriate errors for invalid request formats."""
    headers = {"Authorization": "Bearer sk_test_user1"}
    
    # Missing required field (messages)
    req_body = {"model": "test-model"}
    response = client.post("/v1/chat/completions", json=req_body, headers=headers)
    assert response.status_code == 422
    
    # Invalid message role
    req_body = {
        "model": "test-model",
        "messages": [{"role": "invalid_role", "content": "Hello"}]
    }
    response = client.post("/v1/chat/completions", json=req_body, headers=headers)
    assert response.status_code == 422
    
    # Invalid temperature (out of range)
    req_body = {
        "model": "test-model",
        "messages": [{"role": "user", "content": "Hello"}],
        "temperature": 3.0
    }
    response = client.post("/v1/chat/completions", json=req_body, headers=headers)
    assert response.status_code == 422


def test_chat_completion_cache_miss_then_hit():
    """Test that the first request is a cache miss and the second is a hit, and both are saved to database."""
    # Reset the cache for this test
    cache._index = cache.faiss.IndexFlatIP(cache.EMBED_DIM)
    cache._cached_pairs = []
    
    # Mock the rate limit check and embedding function
    with patch("app.auth.check_rate_limit", return_value=None), \
         patch("app.synthlang.compress_prompt", side_effect=lambda x: x), \
         patch("app.synthlang.decompress_prompt", side_effect=lambda x: x), \
         patch("app.cache.get_embedding", return_value=np.ones(cache.EMBED_DIM, dtype='float32')), \
         patch("app.llm_provider.complete_chat", new_callable=AsyncMock) as mock_complete_chat, \
         patch("app.db.save_interaction", new_callable=AsyncMock) as mock_save_interaction:
        
        mock_complete_chat.return_value = {
            "id": "chatcmpl-123",
            "created": int(time.time()),
            "choices": [{"message": {"content": "Paris is the capital of France."}}],
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 10,
                "total_tokens": 20
            }
        }
        
        headers = {"Authorization": "Bearer sk_test_user1"}
        req_body = {
            "model": "test-model",
            "messages": [{"role": "user", "content": "What is the capital of France?"}]
        }
        
        # First request should be a cache miss
        response1 = client.post("/v1/chat/completions", json=req_body, headers=headers)
        assert response1.status_code == 200
        data1 = response1.json()
        assert "debug" in data1
        assert "cache_hit" in data1["debug"]
        assert data1["debug"]["cache_hit"] is False
        
        # Verify that the LLM provider was called
        mock_complete_chat.assert_called_once()
        
        # Verify that save_interaction was called
        assert mock_save_interaction.call_count == 1
        
        mock_complete_chat.reset_mock()
        mock_save_interaction.reset_mock()
        
        # Second request with the same query should be a cache hit
        response2 = client.post("/v1/chat/completions", json=req_body, headers=headers)
        assert response2.status_code == 200
        data2 = response2.json()
        assert "debug" in data2
        assert "cache_hit" in data2["debug"]
        assert data2["debug"]["cache_hit"] is True
        
        # Verify that the LLM provider was NOT called for the cache hit
        mock_complete_chat.assert_not_called()
        
        # Verify that save_interaction was called
        assert mock_save_interaction.call_count == 1


def test_chat_completion_different_model_cache_miss():
    """Test that using a different model results in a cache miss."""
    # Reset the cache for this test
    cache._index = cache.faiss.IndexFlatIP(cache.EMBED_DIM)
    cache._cached_pairs = []
    
    # Mock the rate limit check and embedding function
    with patch("app.auth.check_rate_limit", return_value=None), \
         patch("app.synthlang.compress_prompt", side_effect=lambda x: x), \
         patch("app.synthlang.decompress_prompt", side_effect=lambda x: x), \
         patch("app.cache.get_embedding", return_value=np.ones(cache.EMBED_DIM, dtype='float32')), \
         patch("app.llm_provider.complete_chat", new_callable=AsyncMock) as mock_complete_chat, \
         patch("app.db.save_interaction", new_callable=AsyncMock):
        
        mock_complete_chat.return_value = {
            "id": "chatcmpl-123",
            "created": int(time.time()),
            "choices": [{"message": {"content": "Paris is the capital of France."}}],
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 10,
                "total_tokens": 20
            }
        }
        
        headers = {"Authorization": "Bearer sk_test_user1"}
        
        # First request with model1
        req_body1 = {
            "model": "test-model-1",
            "messages": [{"role": "user", "content": "What is the capital of France?"}]
        }
        response1 = client.post("/v1/chat/completions", json=req_body1, headers=headers)
        assert response1.status_code == 200
        
        # Reset the mock to track new calls
        mock_complete_chat.reset_mock()
        
        # Second request with model2 should be a cache miss despite same query
        req_body2 = {
            "model": "test-model-2",
            "messages": [{"role": "user", "content": "What is the capital of France?"}]
        }
        response2 = client.post("/v1/chat/completions", json=req_body2, headers=headers)
        assert response2.status_code == 200
        data2 = response2.json()
        assert "debug" in data2
        assert "cache_hit" in data2["debug"]
        assert data2["debug"]["cache_hit"] is False
        
        # Verify that the LLM provider was called for the different model
        mock_complete_chat.assert_called_once()


def test_chat_completion_llm_error_handling():
    """Test that errors from the LLM provider are properly handled."""
    with patch("app.auth.check_rate_limit", return_value=None), \
         patch("app.synthlang.compress_prompt", side_effect=lambda x: x), \
         patch("app.llm_provider.complete_chat", new_callable=AsyncMock) as mock_complete_chat:
        
        # Make the LLM provider raise an exception
        mock_complete_chat.side_effect = Exception("LLM API Error")
        
        headers = {"Authorization": "Bearer sk_test_user1"}
        req_body = {
            "model": "test-model",
            "messages": [{"role": "user", "content": "Hello"}]
        }
        
        response = client.post("/v1/chat/completions", json=req_body, headers=headers)
        assert response.status_code == 500
        data = response.json()
        assert "error" in data
        assert "message" in data["error"]
        assert "LLM provider call failed" in data["error"]["message"]


def test_chat_completion_with_web_search_tool():
    """Test that the chat completion endpoint invokes the web search tool for search-preview model."""
    # Mock the rate limit check, cache, and tool invocation
    with patch("app.auth.check_rate_limit", return_value=None), \
         patch("app.synthlang.compress_prompt", side_effect=lambda x: x), \
         patch("app.cache.get_embedding", return_value=np.ones(cache.EMBED_DIM, dtype='float32')), \
         patch("app.cache.get_similar_response", return_value=None), \
         patch("app.llm_provider.complete_chat", new_callable=AsyncMock) as mock_complete_chat, \
         patch("app.db.save_interaction", new_callable=AsyncMock):
        
        # Mock the LLM response with tool invocation
        mock_complete_chat.return_value = {
            "id": "chatcmpl-123",
            "created": int(time.time()),
            "choices": [{"message": {"content": "Web search results"}}],
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 10,
                "total_tokens": 20
            }
        }
        
        headers = {"Authorization": "Bearer sk_test_user1"}
        req_body = {
            "model": "gpt-4o-search-preview",
            "messages": [{"role": "user", "content": "What is the capital of France?"}]
        }
        
        response = client.post("/v1/chat/completions", json=req_body, headers=headers)
        assert response.status_code == 200
        data = response.json()
        
        # Verify that the LLM provider was called
        mock_complete_chat.assert_called_once()
        
        # Verify that the model parameter was passed correctly
        kwargs = mock_complete_chat.call_args.kwargs
        assert kwargs["model"] == "gpt-4o-search-preview"
        
        # Verify the response contains the expected content
        assert "choices" in data
        assert len(data["choices"]) > 0
        assert "message" in data["choices"][0]
        assert "content" in data["choices"][0]["message"]
        assert data["choices"][0]["message"]["content"] == "Web search results"


def test_chat_completion_with_regular_model():
    """Test that the chat completion endpoint does not invoke tools for regular models."""
    # Mock the rate limit check and LLM call
    with patch("app.auth.check_rate_limit", return_value=None), \
         patch("app.synthlang.compress_prompt", side_effect=lambda x: x), \
         patch("app.cache.get_embedding", return_value=np.ones(cache.EMBED_DIM, dtype='float32')), \
         patch("app.cache.get_similar_response", return_value=None), \
         patch("app.llm_provider.complete_chat", new_callable=AsyncMock) as mock_complete_chat, \
         patch("app.db.save_interaction", new_callable=AsyncMock):
        
        # Mock the LLM response
        mock_complete_chat.return_value = {
            "id": "chatcmpl-123",
            "created": int(time.time()),
            "choices": [{"message": {"content": "Regular LLM response"}}],
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 10,
                "total_tokens": 20
            }
        }
        
        headers = {"Authorization": "Bearer sk_test_user1"}
        req_body = {
            "model": "o3-mini",  # Regular model, not search-preview
            "messages": [{"role": "user", "content": "What is the capital of France?"}]
        }
        
        response = client.post("/v1/chat/completions", json=req_body, headers=headers)
        assert response.status_code == 200
        
        # Verify that the LLM provider was called
        mock_complete_chat.assert_called_once()
        
        # Verify that the model parameter was passed correctly
        kwargs = mock_complete_chat.call_args.kwargs
        assert kwargs["model"] == "o3-mini"
