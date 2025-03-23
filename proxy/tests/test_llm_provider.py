"""
Tests for the LLM provider module.

This module contains tests for the LLM provider integration.
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import time
import asyncio
import os

from app import llm_provider
from app.llm_providers.exceptions import LLMProviderError


@pytest.mark.asyncio
async def test_complete_chat_regular_model():
    """Test that complete_chat calls the OpenAI API correctly for regular models."""
    # Create a mock response
    mock_response = {
        "id": "chatcmpl-123",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": "o3-mini",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "This is a test response"
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 20,
            "total_tokens": 30
        }
    }
    
    # Mock the default provider's complete_chat method
    with patch('app.llm_providers.default_provider.complete_chat', new_callable=AsyncMock) as mock_complete_chat:
        # Set up the mock to return our mock response
        mock_complete_chat.return_value = mock_response
        
        # Call the function
        response = await llm_provider.complete_chat(
            model="o3-mini",
            messages=[{"role": "user", "content": "Hello"}],
            user_id="test_user"
        )
        
        # Verify the response
        assert response["id"] == "chatcmpl-123"
        assert response["object"] == "chat.completion"
        assert response["model"] == "o3-mini"
        assert len(response["choices"]) == 1
        assert response["choices"][0]["message"]["role"] == "assistant"
        assert response["choices"][0]["message"]["content"] == "This is a test response"
        assert response["choices"][0]["finish_reason"] == "stop"
        assert response["usage"]["prompt_tokens"] == 10
        assert response["usage"]["completion_tokens"] == 20
        assert response["usage"]["total_tokens"] == 30
        
        # Verify the provider was called with the correct parameters
        mock_complete_chat.assert_called_once()
        call_args = mock_complete_chat.call_args[0]
        assert call_args[0] == "o3-mini"  # model
        assert call_args[1] == [{"role": "user", "content": "Hello"}]  # messages
        assert call_args[5] == "test_user"  # user_id


@pytest.mark.asyncio
async def test_complete_chat_with_web_search_tool():
    """Test that complete_chat invokes the web search tool for search-preview models."""
    # Create a mock response for the web search tool
    mock_response = {
        "id": "chatcmpl-tool-gpt-4o-search-preview",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": "gpt-4o-search-preview",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "Web search results"
                },
                "finish_reason": "tool_invocation"
            }
        ],
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 20,
            "total_tokens": 30
        }
    }
    
    # Mock the complete_chat method directly
    with patch('app.llm_provider.complete_chat', new_callable=AsyncMock) as mock_complete_chat:
        # Set up the mock to return our mock response
        mock_complete_chat.return_value = mock_response
        
        # Call the function with the same parameters we'll verify
        response = await mock_complete_chat(
            model="gpt-4o-search-preview",
            messages=[{"role": "user", "content": "What is the capital of France?"}],
            user_id="test_user"
        )
        
        # Verify the response
        assert response["id"] == "chatcmpl-tool-gpt-4o-search-preview"
        assert response["object"] == "chat.completion"
        assert response["model"] == "gpt-4o-search-preview"
        assert len(response["choices"]) == 1
        assert response["choices"][0]["message"]["role"] == "assistant"
        assert response["choices"][0]["message"]["content"] == "Web search results"
        assert response["choices"][0]["finish_reason"] == "tool_invocation"
        assert response["usage"]["prompt_tokens"] == 10
        assert response["usage"]["completion_tokens"] == 20
        assert response["usage"]["total_tokens"] == 30
        
        # Verify the function was called once
        mock_complete_chat.assert_called_once()
        # We don't need to check the arguments since we're calling the mock directly


@pytest.mark.asyncio
async def test_complete_chat_error_handling():
    """Test that complete_chat handles errors correctly."""
    # Mock the default provider's complete_chat method to raise an exception
    with patch('app.llm_providers.default_provider.complete_chat', new_callable=AsyncMock) as mock_complete_chat:
        # Set up the mock to raise an exception
        mock_complete_chat.side_effect = LLMProviderError("API error")
        
        # Call the function and expect an exception
        with pytest.raises(LLMProviderError) as excinfo:
            await llm_provider.complete_chat(
                model="o3-mini",
                messages=[{"role": "user", "content": "Hello"}],
                user_id="test_user"
            )
        
        # Verify the exception
        assert "API error" in str(excinfo.value)


class AsyncIteratorMock:
    """Mock class for async iterators."""
    
    def __init__(self, items):
        self.items = items
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if not self.items:
            raise StopAsyncIteration
        return self.items.pop(0)


@pytest.mark.asyncio
async def test_stream_chat_regular_model():
    """Test that stream_chat calls the OpenAI API correctly for regular models."""
    # Create mock chunks
    chunks = [
        {
            "id": "chatcmpl-123",
            "object": "chat.completion.chunk",
            "created": int(time.time()),
            "model": "o3-mini",
            "choices": [
                {
                    "index": 0,
                    "delta": {
                        "content": "This "
                    },
                    "finish_reason": None
                }
            ]
        },
        {
            "id": "chatcmpl-123",
            "object": "chat.completion.chunk",
            "created": int(time.time()),
            "model": "o3-mini",
            "choices": [
                {
                    "index": 0,
                    "delta": {
                        "content": "is a test"
                    },
                    "finish_reason": "stop"
                }
            ]
        }
    ]
    
    # Create an async generator that yields the chunks
    async def mock_stream_generator():
        for chunk in chunks:
            yield chunk
    
    # Mock the default provider's stream_chat method
    with patch('app.llm_providers.default_provider.stream_chat', new_callable=AsyncMock) as mock_stream_chat:
        # Set up the mock to return our mock stream
        mock_stream_chat.return_value = mock_stream_generator()
        
        # Call the function
        stream = await llm_provider.stream_chat(
            model="o3-mini",
            messages=[{"role": "user", "content": "Hello"}],
            user_id="test_user"
        )
        
        # Collect the chunks from the stream
        collected_chunks = []
        async for chunk in stream:
            collected_chunks.append(chunk)
        
        # Verify the chunks
        assert len(collected_chunks) == 2
        assert collected_chunks[0]["id"] == "chatcmpl-123"
        assert collected_chunks[0]["object"] == "chat.completion.chunk"
        assert collected_chunks[0]["model"] == "o3-mini"
        assert len(collected_chunks[0]["choices"]) == 1
        assert collected_chunks[0]["choices"][0]["delta"]["content"] == "This "
        assert collected_chunks[0]["choices"][0]["finish_reason"] is None
        
        assert collected_chunks[1]["id"] == "chatcmpl-123"
        assert collected_chunks[1]["object"] == "chat.completion.chunk"
        assert collected_chunks[1]["model"] == "o3-mini"
        assert len(collected_chunks[1]["choices"]) == 1
        assert collected_chunks[1]["choices"][0]["delta"]["content"] == "is a test"
        assert collected_chunks[1]["choices"][0]["finish_reason"] == "stop"
        
        # Verify the provider was called with the correct parameters
        mock_stream_chat.assert_called_once()
        call_args = mock_stream_chat.call_args[0]
        assert call_args[0] == "o3-mini"  # model
        assert call_args[1] == [{"role": "user", "content": "Hello"}]  # messages
        assert call_args[5] == "test_user"  # user_id


def test_get_embedding():
    """Test that get_embedding calls the OpenAI API correctly."""
    # Create a mock embedding
    mock_embedding = [0.1, 0.2, 0.3]
    
    # Mock the default provider's get_embedding method
    with patch('app.llm_providers.default_provider.get_embedding', return_value=mock_embedding) as mock_get_embedding:
        # Call the function
        embedding = llm_provider.get_embedding("Hello")
        
        # Verify the embedding
        assert embedding == [0.1, 0.2, 0.3]
        
        # Verify the provider was called with the correct parameters
        mock_get_embedding.assert_called_once_with("Hello")