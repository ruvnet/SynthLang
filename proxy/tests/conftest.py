"""
Pytest configuration and fixtures.

This module contains pytest fixtures and configuration for testing.
"""
import pytest
from unittest.mock import patch, AsyncMock
import numpy as np
import os
import sys
from fastapi.testclient import TestClient

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from app.main import app
from app import cache


@pytest.fixture
def client():
    """
    Create a test client for the FastAPI app.
    
    Returns:
        TestClient: A test client for the FastAPI app
    """
    return TestClient(app)


@pytest.fixture
def reset_cache():
    """
    Reset the cache before and after a test.
    """
    # Reset before test
    cache._index = cache.faiss.IndexFlatIP(cache.EMBED_DIM)
    cache._cached_pairs = []
    
    yield
    
    # Reset after test
    cache._index = cache.faiss.IndexFlatIP(cache.EMBED_DIM)
    cache._cached_pairs = []


@pytest.fixture
def mock_auth():
    """
    Mock the authentication functions.
    """
    with patch("app.auth.verify_api_key", return_value="sk_test_user1"), \
         patch("app.auth.get_user_id", return_value="user1"), \
         patch("app.auth.check_rate_limit", return_value=None), \
         patch("app.auth.allow_request", return_value=True):
        yield


@pytest.fixture
def mock_synthlang():
    """
    Mock the SynthLang functions.
    """
    with patch("app.synthlang.compress_prompt", side_effect=lambda x: f"compressed: {x}"), \
         patch("app.synthlang.decompress_prompt", side_effect=lambda x: x.replace("compressed: ", "")), \
         patch("app.synthlang.is_synthlang_available", return_value=True):
        yield


@pytest.fixture
def mock_llm_provider():
    """
    Mock the LLM provider functions.
    """
    with patch("app.llm_provider.complete_chat", new_callable=AsyncMock) as mock_complete_chat, \
         patch("app.llm_provider.stream_chat", new_callable=AsyncMock) as mock_stream_chat, \
         patch("app.llm_provider.get_embedding", return_value=np.ones(cache.EMBED_DIM, dtype='float32')):
        
        # Set up the mock response for complete_chat
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
        
        # Set up the mock response for stream_chat
        async def mock_stream_generator():
            async def generator():
                yield {"choices": [{"delta": {"content": "Chunk 1"}}]}
                yield {"choices": [{"delta": {"content": "Chunk 2"}}]}
                yield {"choices": [{"delta": {}}]}  # End of content
            return generator
        
        mock_stream_chat.return_value = mock_stream_generator
        
        yield {
            "complete_chat": mock_complete_chat,
            "stream_chat": mock_stream_chat
        }


@pytest.fixture
def mock_db():
    """
    Mock the database functions.
    """
    with patch("app.db.save_interaction", new_callable=AsyncMock) as mock_save_interaction:
        yield mock_save_interaction


@pytest.fixture
def mock_cache():
    """
    Mock the cache functions.
    """
    with patch("app.cache.get_embedding", return_value=np.ones(cache.EMBED_DIM, dtype='float32')):
        yield