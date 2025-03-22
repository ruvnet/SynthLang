"""
Tests for error handling in the LLM provider.

This module contains tests for the error handling in the LLM provider.
"""
import pytest
from unittest.mock import patch, AsyncMock, MagicMock
import httpx

from app.llm_provider import (
    complete_chat,
    stream_chat,
    get_embedding,
    LLMAuthenticationError,
    LLMRateLimitError,
    LLMConnectionError,
    LLMTimeoutError,
    LLMModelNotFoundError,
    LLMInvalidRequestError,
    LLMProviderError
)


@pytest.mark.asyncio
async def test_complete_chat_authentication_error():
    """Test that authentication errors are properly handled in complete_chat."""
    # Mock the AsyncOpenAI client
    with patch('app.llm_provider.get_async_openai_client') as mock_get_client:
        # Set up the mock to raise an authentication error
        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(
            side_effect=Exception("Invalid API key")
        )
        mock_get_client.return_value = mock_client
        
        # Call the function and check that it raises the correct error
        with pytest.raises(LLMAuthenticationError):
            await complete_chat(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}]
            )


@pytest.mark.asyncio
async def test_complete_chat_rate_limit_error():
    """Test that rate limit errors are properly handled in complete_chat."""
    # Mock the AsyncOpenAI client
    with patch('app.llm_provider.get_async_openai_client') as mock_get_client:
        # Set up the mock to raise a rate limit error
        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(
            side_effect=Exception("Rate limit exceeded")
        )
        mock_get_client.return_value = mock_client
        
        # Call the function and check that it raises the correct error
        with pytest.raises(LLMRateLimitError):
            await complete_chat(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}]
            )


@pytest.mark.asyncio
async def test_complete_chat_connection_error():
    """Test that connection errors are properly handled in complete_chat."""
    # Mock the AsyncOpenAI client
    with patch('app.llm_provider.get_async_openai_client') as mock_get_client:
        # Set up the mock to raise a connection error
        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(
            side_effect=Exception("Connection error")
        )
        mock_get_client.return_value = mock_client
        
        # Call the function and check that it raises the correct error
        with pytest.raises(LLMConnectionError):
            await complete_chat(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}]
            )


@pytest.mark.asyncio
async def test_complete_chat_timeout_error():
    """Test that timeout errors are properly handled in complete_chat."""
    # Mock the AsyncOpenAI client
    with patch('app.llm_provider.get_async_openai_client') as mock_get_client:
        # Set up the mock to raise a timeout error
        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(
            side_effect=httpx.TimeoutException("Request timed out")
        )
        mock_get_client.return_value = mock_client
        
        # Call the function and check that it raises the correct error
        with pytest.raises(LLMTimeoutError):
            await complete_chat(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}]
            )


@pytest.mark.asyncio
async def test_complete_chat_model_not_found_error():
    """Test that model not found errors are properly handled in complete_chat."""
    # Mock the AsyncOpenAI client
    with patch('app.llm_provider.get_async_openai_client') as mock_get_client:
        # Set up the mock to raise a model not found error
        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(
            side_effect=Exception("Model not found")
        )
        mock_get_client.return_value = mock_client
        
        # Call the function and check that it raises the correct error
        with pytest.raises(LLMModelNotFoundError):
            await complete_chat(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}]
            )


@pytest.mark.asyncio
async def test_complete_chat_invalid_request_error():
    """Test that invalid request errors are properly handled in complete_chat."""
    # Mock the AsyncOpenAI client
    with patch('app.llm_provider.get_async_openai_client') as mock_get_client:
        # Set up the mock to raise an invalid request error
        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(
            side_effect=Exception("Invalid request")
        )
        mock_get_client.return_value = mock_client
        
        # Call the function and check that it raises the correct error
        with pytest.raises(LLMInvalidRequestError):
            await complete_chat(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}]
            )


@pytest.mark.asyncio
async def test_complete_chat_generic_error():
    """Test that generic errors are properly handled in complete_chat."""
    # Mock the AsyncOpenAI client
    with patch('app.llm_provider.get_async_openai_client') as mock_get_client:
        # Set up the mock to raise a generic error
        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(
            side_effect=Exception("Some other error")
        )
        mock_get_client.return_value = mock_client
        
        # Call the function and check that it raises the correct error
        with pytest.raises(LLMProviderError):
            await complete_chat(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}]
            )


@pytest.mark.asyncio
async def test_stream_chat_error_handling():
    """Test that errors are properly handled in stream_chat."""
    # Mock the AsyncOpenAI client
    with patch('app.llm_provider.get_async_openai_client') as mock_get_client:
        # Set up the mock to raise an error
        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(
            side_effect=Exception("Rate limit exceeded")
        )
        mock_get_client.return_value = mock_client
        
        # Call the function and check that it raises the correct error
        with pytest.raises(LLMRateLimitError):
            async for _ in await stream_chat(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}]
            ):
                pass


def test_get_embedding_error_handling():
    """Test that errors are properly handled in get_embedding."""
    # Mock the OpenAI client
    with patch('app.llm_provider.get_openai_client') as mock_get_client:
        # Set up the mock to raise an error
        mock_client = MagicMock()
        mock_client.embeddings.create = MagicMock(
            side_effect=Exception("Invalid API key")
        )
        mock_get_client.return_value = mock_client
        
        # Call the function and check that it raises the correct error
        with pytest.raises(LLMAuthenticationError):
            get_embedding("Hello")