"""
Tests for the API endpoints with keyword detection disabled.

This module contains tests for the API endpoints with keyword detection disabled.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
import numpy as np
import time
import json
from fastapi import HTTPException

from app.main import app
from app import cache, llm_provider, db
from app.keywords.registry import disable_keyword_detection


client = TestClient(app)


def test_chat_completion_endpoint_rate_limit():
    """Test that the chat completion endpoint enforces rate limits."""
    # Mock the rate limit check to simulate rate limiting
    def mock_check_rate_limit(*args, **kwargs):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Please try again later.",
            headers={"Retry-After": "60"}
        )
    
    with patch("app.auth.check_rate_limit", side_effect=mock_check_rate_limit), \
         disable_keyword_detection():
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


def test_chat_completion_cache_miss_then_hit():
    """Test that the first request is a cache miss and the second is a hit, and both are saved to database."""
    # Reset the cache
    cache.clear()
    
    # Mock the rate limit check and LLM provider
    with patch("app.auth.check_rate_limit", return_value=None), \
         patch("app.synthlang.compress_prompt", side_effect=lambda x: x), \
         patch("app.synthlang.decompress_prompt", side_effect=lambda x: x), \
         patch("app.llm_provider.complete_chat", new_callable=AsyncMock) as mock_complete_chat, \
         patch("app.db.save_interaction", new_callable=AsyncMock) as mock_save_interaction, \
         disable_keyword_detection():
        
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
        
        # Check if debug contains compressed_messages (new format) or cache_hit (old format)
        if "compressed_messages" in data1["debug"]:
            assert data1["debug"]["compressed_messages"] is not None
        else:
            assert "cache_hit" in data1["debug"]
            assert data1["debug"]["cache_hit"] is False
        
        # Verify that the LLM provider was called
        mock_complete_chat.assert_called_once()
        
        # Verify that save_interaction was called
        assert mock_save_interaction.call_count == 1
        
        mock_complete_chat.reset_mock()
        mock_save_interaction.reset_mock()
        
        # Mock get_similar_response to simulate a cache hit
        with patch("app.cache.get_similar_response", return_value="Paris is the capital of France."):
            # Second request with the same query should be a cache hit
            response2 = client.post("/v1/chat/completions", json=req_body, headers=headers)
            assert response2.status_code == 200
            data2 = response2.json()
            assert "debug" in data2
            
            # Check if debug contains compressed_messages (new format) or cache_hit (old format)
            if "compressed_messages" in data2["debug"]:
                # For new format, we can't directly check cache_hit, but we can verify LLM wasn't called
                pass
            else:
                assert "cache_hit" in data2["debug"]
                assert data2["debug"]["cache_hit"] is True
            
            # Verify that the LLM provider was NOT called for the cache hit
            mock_complete_chat.assert_not_called()
            
            # Verify that save_interaction was called
            assert mock_save_interaction.call_count == 1


def test_chat_completion_different_model_cache_miss():
    """Test that using a different model results in a cache miss."""
    # Reset the cache
    cache.clear()
    
    # Mock the rate limit check and LLM provider
    with patch("app.auth.check_rate_limit", return_value=None), \
         patch("app.synthlang.compress_prompt", side_effect=lambda x: x), \
         patch("app.synthlang.decompress_prompt", side_effect=lambda x: x), \
         patch("app.llm_provider.complete_chat", new_callable=AsyncMock) as mock_complete_chat, \
         patch("app.db.save_interaction", new_callable=AsyncMock), \
         disable_keyword_detection():
        
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
        
        # Check if debug contains compressed_messages (new format) or cache_hit (old format)
        if "compressed_messages" in data2["debug"]:
            # For new format, we can't directly check cache_hit, but we can verify LLM was called
            pass
        else:
            assert "cache_hit" in data2["debug"]
            assert data2["debug"]["cache_hit"] is False
        
        # Verify that the LLM provider was called for the different model
        mock_complete_chat.assert_called_once()


def test_chat_completion_llm_error_handling():
    """Test that errors from the LLM provider are properly handled."""
    with patch("app.auth.check_rate_limit", return_value=None), \
         patch("app.synthlang.compress_prompt", side_effect=lambda x: x), \
         patch("app.llm_provider.complete_chat", new_callable=AsyncMock) as mock_complete_chat, \
         disable_keyword_detection():
        
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