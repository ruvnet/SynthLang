"""
Tests for the LLM provider module.

This module contains tests for the LLM provider integration.
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import time
import asyncio

from app import llm_provider


@pytest.mark.asyncio
async def test_complete_chat_regular_model():
    """Test that complete_chat calls the OpenAI API correctly for regular models."""
    # Create a mock response
    mock_response = MagicMock()
    mock_response.id = "chatcmpl-123"
    mock_response.object = "chat.completion"
    mock_response.created = int(time.time())
    mock_response.model = "o3-mini"
    
    # Mock the choices
    mock_choice = MagicMock()
    mock_choice.index = 0
    mock_choice.finish_reason = "stop"
    
    # Mock the message
    mock_message = MagicMock()
    mock_message.role = "assistant"
    mock_message.content = "This is a test response"
    mock_choice.message = mock_message
    
    mock_response.choices = [mock_choice]
    
    # Mock the usage
    mock_usage = MagicMock()
    mock_usage.prompt_tokens = 10
    mock_usage.completion_tokens = 20
    mock_usage.total_tokens = 30
    mock_response.usage = mock_usage
    
    # Mock the OpenAI client
    mock_client = MagicMock()
    mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
    
    # Mock the get_async_openai_client function
    with patch("app.llm_provider.get_async_openai_client", return_value=mock_client):
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
        
        # Verify the client was called with the correct parameters
        mock_client.chat.completions.create.assert_called_once()
        call_args = mock_client.chat.completions.create.call_args[1]
        assert call_args["model"] == "o3-mini"
        assert call_args["messages"] == [{"role": "user", "content": "Hello"}]
        assert call_args["stream"] is False
        assert call_args["user"] == "test_user"


@pytest.mark.asyncio
async def test_complete_chat_with_web_search_tool():
    """Test that complete_chat invokes the web search tool for search-preview models."""
    # Mock the web search tool
    mock_tool_response = {"content": "Web search results"}
    mock_web_search = MagicMock(return_value=mock_tool_response)
    
    # Mock the registry.get_tool function
    with patch("app.agents.registry.get_tool", return_value=mock_web_search):
        # Call the function
        response = await llm_provider.complete_chat(
            model="gpt-4o-search-preview",
            messages=[{"role": "user", "content": "What is the capital of France?"}],
            user_id="test_user"
        )
        
        # Verify the response
        assert "id" in response
        assert "choices" in response
        assert len(response["choices"]) == 1
        assert response["choices"][0]["message"] == mock_tool_response
        assert response["choices"][0]["finish_reason"] == "tool_invocation"
        assert "usage" in response
        
        # Verify the tool was called with the correct parameters
        mock_web_search.assert_called_once_with(user_message="What is the capital of France?")


@pytest.mark.asyncio
async def test_complete_chat_error_handling():
    """Test that complete_chat handles errors correctly."""
    # Mock the OpenAI client to raise an exception
    mock_client = MagicMock()
    mock_client.chat.completions.create = AsyncMock(side_effect=Exception("API error"))
    
    # Mock the get_async_openai_client function
    with patch("app.llm_provider.get_async_openai_client", return_value=mock_client):
        # Call the function and expect an exception
        with pytest.raises(Exception) as excinfo:
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
    chunk1 = MagicMock()
    chunk1.id = "chatcmpl-123"
    chunk1.object = "chat.completion.chunk"
    chunk1.created = int(time.time())
    chunk1.model = "o3-mini"
    
    # Mock the choices for chunk1
    mock_choice1 = MagicMock()
    mock_choice1.index = 0
    mock_choice1.finish_reason = None
    
    # Mock the delta for chunk1
    mock_delta1 = MagicMock()
    mock_delta1.content = "This "
    mock_choice1.delta = mock_delta1
    
    chunk1.choices = [mock_choice1]
    
    # Create another mock chunk
    chunk2 = MagicMock()
    chunk2.id = "chatcmpl-123"
    chunk2.object = "chat.completion.chunk"
    chunk2.created = int(time.time())
    chunk2.model = "o3-mini"
    
    # Mock the choices for chunk2
    mock_choice2 = MagicMock()
    mock_choice2.index = 0
    mock_choice2.finish_reason = "stop"
    
    # Mock the delta for chunk2
    mock_delta2 = MagicMock()
    mock_delta2.content = "is a test"
    mock_choice2.delta = mock_delta2
    
    chunk2.choices = [mock_choice2]
    
    # Create an async iterator mock with the chunks
    mock_stream = AsyncIteratorMock([chunk1, chunk2])
    
    # Mock the OpenAI client
    mock_client = MagicMock()
    mock_client.chat.completions.create = AsyncMock(return_value=mock_stream)
    
    # Mock the get_async_openai_client function
    with patch("app.llm_provider.get_async_openai_client", return_value=mock_client):
        # Call the function
        stream = await llm_provider.stream_chat(
            model="o3-mini",
            messages=[{"role": "user", "content": "Hello"}],
            user_id="test_user"
        )
        
        # Collect the chunks from the stream
        chunks = []
        async for chunk in stream:
            chunks.append(chunk)
        
        # Verify the chunks
        assert len(chunks) == 2
        assert chunks[0]["id"] == "chatcmpl-123"
        assert chunks[0]["object"] == "chat.completion.chunk"
        assert chunks[0]["model"] == "o3-mini"
        assert len(chunks[0]["choices"]) == 1
        assert chunks[0]["choices"][0]["delta"]["content"] == "This "
        assert chunks[0]["choices"][0]["finish_reason"] is None
        
        assert chunks[1]["id"] == "chatcmpl-123"
        assert chunks[1]["object"] == "chat.completion.chunk"
        assert chunks[1]["model"] == "o3-mini"
        assert len(chunks[1]["choices"]) == 1
        assert chunks[1]["choices"][0]["delta"]["content"] == "is a test"
        assert chunks[1]["choices"][0]["finish_reason"] == "stop"
        
        # Verify the client was called with the correct parameters
        mock_client.chat.completions.create.assert_called_once()
        call_args = mock_client.chat.completions.create.call_args[1]
        assert call_args["model"] == "o3-mini"
        assert call_args["messages"] == [{"role": "user", "content": "Hello"}]
        assert call_args["stream"] is True
        assert call_args["user"] == "test_user"


def test_get_embedding():
    """Test that get_embedding calls the OpenAI API correctly."""
    # Create a mock response
    mock_data = MagicMock()
    mock_data.embedding = [0.1, 0.2, 0.3]
    
    mock_response = MagicMock()
    mock_response.data = [mock_data]
    
    # Mock the OpenAI client
    mock_client = MagicMock()
    mock_client.embeddings.create = MagicMock(return_value=mock_response)
    
    # Mock the get_openai_client function
    with patch("app.llm_provider.get_openai_client", return_value=mock_client):
        # Call the function
        embedding = llm_provider.get_embedding("Hello")
        
        # Verify the embedding
        assert embedding == [0.1, 0.2, 0.3]
        
        # Verify the client was called with the correct parameters
        mock_client.embeddings.create.assert_called_once()
        call_args = mock_client.embeddings.create.call_args[1]
        assert call_args["model"] == "text-embedding-ada-002"
        assert call_args["input"] == "Hello"