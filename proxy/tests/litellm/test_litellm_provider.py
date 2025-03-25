"""
Unit tests for the LiteLLM provider.

This module contains tests for the LiteLLM provider functionality,
including completion, streaming, error handling, and model mapping.
"""
import pytest
import json
import os
from unittest.mock import patch, AsyncMock, MagicMock

from src.app.litellm_provider import (
    complete_chat,
    stream_chat,
    map_model_name
)

@pytest.fixture
def mock_messages():
    """Fixture for sample messages."""
    return [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how are you?"}
    ]

@pytest.fixture
def mock_response():
    """Fixture for a sample LLM response."""
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
    """Test the complete_chat function."""
    with patch('litellm.acompletion', new=AsyncMock(return_value=mock_response)) as mock_completion:
        response = await complete_chat("gpt-4o-mini", mock_messages)
        
        mock_completion.assert_called_once()
        assert response["choices"][0]["message"]["content"] == "I'm doing well, thank you for asking! How can I help you today?"
        assert response["model"] == "gpt-4o-mini"

@pytest.mark.asyncio
async def test_stream_chat(mock_messages):
    """Test the stream_chat function."""
    # Mock streaming response chunks
    chunks = [
        {"id": "chatcmpl-123", "object": "chat.completion.chunk", "created": 1677652288, "model": "gpt-4o-mini", 
         "choices": [{"index": 0, "delta": {"content": "I'm"}, "finish_reason": None}]},
        {"id": "chatcmpl-123", "object": "chat.completion.chunk", "created": 1677652288, "model": "gpt-4o-mini", 
         "choices": [{"index": 0, "delta": {"content": " doing"}, "finish_reason": None}]},
        {"id": "chatcmpl-123", "object": "chat.completion.chunk", "created": 1677652288, "model": "gpt-4o-mini", 
         "choices": [{"index": 0, "delta": {"content": " well"}, "finish_reason": "stop"}]}
    ]
    
    # Create a mock for the async generator
    mock_generator = AsyncMock()
    mock_generator.__aiter__.return_value = chunks
    
    with patch('litellm.acompletion', new=AsyncMock(return_value=mock_generator)) as mock_completion:
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
    """Test error handling in the complete_chat function."""
    with patch('litellm.acompletion', new=AsyncMock(side_effect=Exception("API Error"))) as mock_completion:
        with pytest.raises(Exception):
            await complete_chat("gpt-4o-mini", mock_messages)
        
        mock_completion.assert_called_once()

def test_model_mapping():
    """Test the model_mapping function."""
    assert map_model_name("gpt-4o-mini") == "openai/gpt-4o-mini"
    assert map_model_name("claude-3-opus") == "anthropic/claude-3-opus"
    assert "openai/gpt-4" in map_model_name("gpt-4")

@pytest.mark.asyncio
async def test_non_string_content(mock_response):
    """Test handling of non-string content in messages."""
    # Messages with non-string content
    complex_messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": {
            "text": "This is a complex message",
            "metadata": {"source": "test", "importance": "high"},
            "data": [1, 2, 3, 4, 5]
        }}
    ]
    
    with patch('litellm.acompletion', new=AsyncMock(return_value=mock_response)) as mock_completion:
        response = await complete_chat("gpt-4o-mini", complex_messages)
        
        # Check that the function was called
        mock_completion.assert_called_once()
        
        # Verify that the content was converted to string
        call_args = mock_completion.call_args[1]
        assert "messages" in call_args
        sent_messages = call_args["messages"]
        assert len(sent_messages) == 2
        assert isinstance(sent_messages[1]["content"], str)
        assert "complex message" in sent_messages[1]["content"]

@pytest.mark.asyncio
async def test_retry_config(mock_messages, mock_response):
    """Test that retry configuration is set correctly."""
    with patch('litellm.acompletion', new=AsyncMock(return_value=mock_response)) as mock_completion:
        await complete_chat("gpt-4o-mini", mock_messages)
        
        # Check that retry configuration was passed to acompletion
        call_kwargs = mock_completion.call_args[1]
        assert "max_retries" in call_kwargs
        assert "timeout" in call_kwargs