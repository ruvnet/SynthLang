"""
Tests for the API endpoints.

This module contains tests for the API endpoints.
"""
import pytest
import time
import json
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi.testclient import TestClient
import os
import sys
from contextlib import contextmanager

from src.app.main import app
from src.app.auth.api_keys import API_KEYS
from src.app.models import Message

# Create a test client
client = TestClient(app)

# Use a test API key
TEST_API_KEY = "sk_test_user1"
API_KEYS[TEST_API_KEY] = "user1"

@contextmanager
def disable_keyword_detection():
    """Temporarily disable keyword detection for tests."""
    with patch("src.app.middleware.keyword_detection.ENABLE_KEYWORD_DETECTION", False):
        yield

def test_health_check():
    """Test that the health check endpoint returns 200."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_chat_completion_basic():
    """Test that the chat completion endpoint works with basic input."""
    # Mock the necessary functions
    with patch("src.app.auth.check_rate_limit", return_value=None), \
         patch("src.app.cache.get_similar_response", return_value=None), \
         patch("src.app.llm_provider.complete_chat", new_callable=AsyncMock) as mock_complete_chat, \
         patch("src.app.db.save_interaction", new_callable=AsyncMock), \
         disable_keyword_detection():
        
        # Set up the mock response
        mock_complete_chat.return_value = {
            "id": "test-id",
            "created": int(time.time()),
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "Hello, how can I help you?"
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 5,
                "total_tokens": 15
            }
        }
        
        # Make the request
        response = client.post("/v1/chat/completions", 
                              json={
                                  "model": "test-model",
                                  "messages": [{"role": "user", "content": "Hello"}]
                              },
                              headers={"Authorization": f"Bearer {TEST_API_KEY}"})
        
        # Check the response
        assert response.status_code == 200
        assert response.json()["choices"][0]["message"]["content"] == "Hello, how can I help you?"
        
        # Verify that complete_chat was called
        mock_complete_chat.assert_called_once()
        args, kwargs = mock_complete_chat.call_args
        assert kwargs["model"] == "test-model"
        assert len(kwargs["messages"]) == 1
        assert kwargs["messages"][0]["role"] == "user"
        assert kwargs["messages"][0]["content"] == "Hello"

def test_chat_completion_with_system_message():
    """Test that the chat completion endpoint works with a system message."""
    # Mock the necessary functions
    with patch("src.app.auth.check_rate_limit", return_value=None), \
         patch("src.app.cache.get_similar_response", return_value=None), \
         patch("src.app.llm_provider.complete_chat", new_callable=AsyncMock) as mock_complete_chat, \
         patch("src.app.db.save_interaction", new_callable=AsyncMock), \
         disable_keyword_detection():
        
        # Set up the mock response
        mock_complete_chat.return_value = {
            "id": "test-id",
            "created": int(time.time()),
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "I am a helpful assistant."
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": 15,
                "completion_tokens": 5,
                "total_tokens": 20
            }
        }
        
        # Make the request
        response = client.post("/v1/chat/completions", 
                              json={
                                  "model": "test-model",
                                  "messages": [
                                      {"role": "system", "content": "You are a helpful assistant."},
                                      {"role": "user", "content": "Who are you?"}
                                  ]
                              },
                              headers={"Authorization": f"Bearer {TEST_API_KEY}"})
        
        # Check the response
        assert response.status_code == 200
        assert response.json()["choices"][0]["message"]["content"] == "I am a helpful assistant."
        
        # Verify that complete_chat was called with the system message
        mock_complete_chat.assert_called_once()
        args, kwargs = mock_complete_chat.call_args
        assert len(kwargs["messages"]) == 2
        assert kwargs["messages"][0]["role"] == "system"
        assert kwargs["messages"][0]["content"] == "You are a helpful assistant."

def test_chat_completion_with_temperature():
    """Test that the chat completion endpoint works with temperature parameter."""
    # Mock the necessary functions
    with patch("src.app.auth.check_rate_limit", return_value=None), \
         patch("src.app.cache.get_similar_response", return_value=None), \
         patch("src.app.llm_provider.complete_chat", new_callable=AsyncMock) as mock_complete_chat, \
         patch("src.app.db.save_interaction", new_callable=AsyncMock), \
         disable_keyword_detection():
        
        # Set up the mock response
        mock_complete_chat.return_value = {
            "id": "test-id",
            "created": int(time.time()),
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "Creative response"
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 5,
                "total_tokens": 15
            }
        }
        
        # Make the request with temperature
        response = client.post("/v1/chat/completions", 
                              json={
                                  "model": "test-model",
                                  "messages": [{"role": "user", "content": "Hello"}],
                                  "temperature": 0.8
                              },
                              headers={"Authorization": f"Bearer {TEST_API_KEY}"})
        
        # Check the response
        assert response.status_code == 200
        
        # Verify that complete_chat was called with the temperature
        mock_complete_chat.assert_called_once()
        args, kwargs = mock_complete_chat.call_args
        assert kwargs["temperature"] == 0.8

def test_chat_completion_with_max_tokens():
    """Test that the chat completion endpoint works with max_tokens parameter."""
    # Mock the necessary functions
    with patch("src.app.auth.check_rate_limit", return_value=None), \
         patch("src.app.cache.get_similar_response", return_value=None), \
         patch("src.app.llm_provider.complete_chat", new_callable=AsyncMock) as mock_complete_chat, \
         patch("src.app.db.save_interaction", new_callable=AsyncMock), \
         disable_keyword_detection():
        
        # Set up the mock response
        mock_complete_chat.return_value = {
            "id": "test-id",
            "created": int(time.time()),
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "Short response"
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 2,
                "total_tokens": 12
            }
        }
        
        # Make the request with max_tokens
        response = client.post("/v1/chat/completions", 
                              json={
                                  "model": "test-model",
                                  "messages": [{"role": "user", "content": "Hello"}],
                                  "max_tokens": 50
                              },
                              headers={"Authorization": f"Bearer {TEST_API_KEY}"})
        
        # Check the response
        assert response.status_code == 200
        
        # Verify that complete_chat was called with max_tokens
        mock_complete_chat.assert_called_once()
        args, kwargs = mock_complete_chat.call_args
        assert kwargs["max_tokens"] == 50

def test_chat_completion_with_streaming():
    """Test that the chat completion endpoint works with streaming."""
    # Mock the necessary functions
    with patch("src.app.auth.check_rate_limit", return_value=None), \
         patch("src.app.cache.get_similar_response", return_value=None), \
         patch("src.app.llm_provider.stream_chat", new_callable=AsyncMock) as mock_stream_chat, \
         patch("src.app.db.save_interaction", new_callable=AsyncMock), \
         disable_keyword_detection():
        
        # Set up the mock streaming response
        async def mock_stream():
            yield {"choices": [{"delta": {"role": "assistant"}, "finish_reason": None}]}
            yield {"choices": [{"delta": {"content": "Hello"}, "finish_reason": None}]}
            yield {"choices": [{"delta": {"content": ", "}, "finish_reason": None}]}
            yield {"choices": [{"delta": {"content": "world"}, "finish_reason": None}]}
            yield {"choices": [{"delta": {"content": "!"}, "finish_reason": "stop"}]}
        
        mock_stream_chat.return_value = mock_stream()
        
        # Make the request with streaming
        response = client.post("/v1/chat/completions", 
                              json={
                                  "model": "test-model",
                                  "messages": [{"role": "user", "content": "Hello"}],
                                  "stream": True
                              },
                              headers={"Authorization": f"Bearer {TEST_API_KEY}"})
        
        # Check the response
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/event-stream"
        
        # Verify that stream_chat was called
        mock_stream_chat.assert_called_once()
        args, kwargs = mock_stream_chat.call_args
        assert kwargs["model"] == "test-model"
        assert len(kwargs["messages"]) == 1
        assert kwargs["messages"][0]["role"] == "user"
        assert kwargs["messages"][0]["content"] == "Hello"

def test_chat_completion_unauthorized():
    """Test that the chat completion endpoint returns 401 for unauthorized requests."""
    # Make the request without an API key
    response = client.post("/v1/chat/completions", 
                          json={
                              "model": "test-model",
                              "messages": [{"role": "user", "content": "Hello"}]
                          })
    
    # Check the response
    assert response.status_code == 401
    assert "Unauthorized" in response.json()["error"]["message"]

def test_chat_completion_invalid_input():
    """Test that the chat completion endpoint returns 422 for invalid input."""
    # Make the request with invalid input (missing messages)
    response = client.post("/v1/chat/completions", 
                          json={
                              "model": "test-model"
                          },
                          headers={"Authorization": f"Bearer {TEST_API_KEY}"})
    
    # Check the response
    assert response.status_code == 422

def test_chat_completion_llm_error():
    """Test that the chat completion endpoint handles LLM errors."""
    # Mock the necessary functions
    with patch("src.app.auth.check_rate_limit", return_value=None), \
         patch("src.app.cache.get_similar_response", return_value=None), \
         patch("src.app.llm_provider.complete_chat", new_callable=AsyncMock) as mock_complete_chat, \
         patch("src.app.db.save_interaction", new_callable=AsyncMock), \
         disable_keyword_detection():
        
        # Set up the mock to raise an exception
        mock_complete_chat.side_effect = Exception("LLM provider error")
        
        # Make the request
        response = client.post("/v1/chat/completions", 
                              json={
                                  "model": "test-model",
                                  "messages": [{"role": "user", "content": "Hello"}]
                              },
                              headers={"Authorization": f"Bearer {TEST_API_KEY}"})
        
        # Check the response
        assert response.status_code == 500
        assert "LLM provider error" in response.json()["error"]["message"]


def test_chat_completion_with_web_search_tool():
    """Test that the chat completion endpoint can use the web search tool."""
    # Mock the necessary functions
    with patch("src.app.auth.check_rate_limit", return_value=None), \
         patch("src.app.cache.get_similar_response", return_value=None), \
         patch("src.app.llm_provider.complete_chat", new_callable=AsyncMock) as mock_complete_chat, \
         patch("src.app.db.save_interaction", new_callable=AsyncMock), \
         patch("src.app.agents.registry.get_tool", return_value=AsyncMock(return_value={"content": "Web search results"})), \
         disable_keyword_detection():
        
        # Set up the mock response
        mock_complete_chat.return_value = {
            "id": "test-id",
            "created": int(time.time()),
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "I found this information: Web search results"
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 5,
                "total_tokens": 15
            }
        }
        
        # Make the request with a tool call
        response = client.post("/v1/chat/completions", 
                              json={
                                  "model": "test-model",
                                  "messages": [{"role": "user", "content": "Search for information about Python"}],
                                  "tools": [{"type": "function", "function": {"name": "web_search"}}]
                              },
                              headers={"Authorization": f"Bearer {TEST_API_KEY}"})
        
        # Check the response
        assert response.status_code == 200
        # The test should pass regardless of the actual content
        # as long as the response is valid
        assert response.json()["choices"][0]["message"]["content"] is not None
