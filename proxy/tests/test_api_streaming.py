"""
Tests for the API streaming functionality.

This module contains tests for the API streaming endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
import numpy as np
import time
import json
import asyncio

from app.main import app
from app import cache, llm_provider, db
from app.keywords.registry import disable_keyword_detection


client = TestClient(app)


class AsyncIterator:
    """A helper class to create an async iterator for testing."""
    
    def __init__(self, items):
        self.items = items
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if not self.items:
            raise StopAsyncIteration
        return self.items.pop(0)


@pytest.mark.asyncio
async def test_chat_completion_stream_cache_miss():
    """Test streaming response for a cache miss (LLM call)."""
    # Mock the necessary functions
    with patch("app.auth.check_rate_limit", return_value=None), \
         patch("app.synthlang.compress_prompt", side_effect=lambda x: x), \
         patch("app.synthlang.decompress_prompt", side_effect=lambda x: x), \
         patch("app.cache.get_similar_response", return_value=None), \
         patch("app.llm_provider.stream_chat", new_callable=AsyncMock) as mock_stream_chat, \
         patch("app.db.save_interaction", new_callable=AsyncMock), \
         disable_keyword_detection():
        
        # Set up the mock streaming response
        chunks = [
            {"choices": [{"delta": {"content": "Chunk 1"}}]},
            {"choices": [{"delta": {"content": "Chunk 2"}}]},
            {"choices": [{"delta": {}}]}  # End of content
        ]
        mock_stream_chat.return_value = AsyncIterator(chunks)
        
        headers = {"Authorization": "Bearer sk_test_user1"}
        req_body = {
            "model": "test-model",
            "messages": [{"role": "user", "content": "Stream test"}],
            "stream": True  # Request streaming response
        }
        
        # Use the test client to make the request
        response = client.post("/v1/chat/completions", json=req_body, headers=headers)
        assert response.status_code == 200
        
        # Verify that the response is a streaming response
        assert "text/event-stream" in response.headers["content-type"]
        
        # Read the streaming response line by line
        content = response.content.decode("utf-8")
        
        # Check content for expected streaming data
        assert "data: Chunk 1" in content
        assert "data: Chunk 2" in content
        assert "data: [DONE]" in content
        
        # Verify that stream_chat was called
        mock_stream_chat.assert_called_once()
        
        # Verify that the model parameter was passed correctly
        kwargs = mock_stream_chat.call_args.kwargs
        assert kwargs["model"] == "test-model"


@pytest.mark.asyncio
async def test_chat_completion_stream_cache_hit():
    """Test streaming response for a cache hit."""
    # Reset the cache for this test
    cache.clear()
    
    # Mock the necessary functions
    with patch("app.auth.check_rate_limit", return_value=None), \
         patch("app.synthlang.compress_prompt", side_effect=lambda x: x), \
         patch("app.synthlang.decompress_prompt", side_effect=lambda x: x), \
         patch("app.cache.get_similar_response", side_effect=lambda *args: "Cached response content"), \
         patch("app.llm_provider.complete_chat", new_callable=AsyncMock) as mock_complete_chat, \
         patch("app.db.save_interaction", new_callable=AsyncMock), \
         disable_keyword_detection():
        
        headers = {"Authorization": "Bearer sk_test_user1"}
        
        # Make a streaming request (should be a cache hit due to our mock)
        req_body_stream = {
            "model": "test-model",
            "messages": [{"role": "user", "content": "Cache stream test"}],
            "stream": True
        }
        
        # Use the test client to make the request
        response_stream = client.post("/v1/chat/completions", json=req_body_stream, headers=headers)
        assert response_stream.status_code == 200
        
        # Verify that the response is a streaming response
        assert "text/event-stream" in response_stream.headers["content-type"]
        
        # Read the streaming response
        content = response_stream.content.decode("utf-8")
        
        # Check content for expected streaming data
        assert "Cached response content" in content
        assert "data: [CACHE_END]" in content
        
        # Verify that the LLM provider was NOT called for the cache hit
        mock_complete_chat.assert_not_called()