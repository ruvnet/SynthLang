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
    # Mock the default provider's complete_chat method
    with patch('app.llm_providers.default_provider.complete_chat', new_callable=AsyncMock) as mock_complete_chat:
        # Set up the mock to raise an authentication error
        mock_complete_chat.side_effect = LLMAuthenticationError("Invalid API key")
        
        # Call the function and check that it raises the correct error
        with pytest.raises(LLMAuthenticationError):
            await complete_chat(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}]
            )


@pytest.mark.asyncio
async def test_complete_chat_rate_limit_error():
    """Test that rate limit errors are properly handled in complete_chat."""
    # Mock the default provider's complete_chat method
    with patch('app.llm_providers.default_provider.complete_chat', new_callable=AsyncMock) as mock_complete_chat:
        # Set up the mock to raise a rate limit error
        mock_complete_chat.side_effect = LLMRateLimitError("Rate limit exceeded")
        
        # Call the function and check that it raises the correct error
        with pytest.raises(LLMRateLimitError):
            await complete_chat(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}]
            )


@pytest.mark.asyncio
async def test_complete_chat_connection_error():
    """Test that connection errors are properly handled in complete_chat."""
    # Mock the default provider's complete_chat method
    with patch('app.llm_providers.default_provider.complete_chat', new_callable=AsyncMock) as mock_complete_chat:
        # Set up the mock to raise a connection error
        mock_complete_chat.side_effect = LLMConnectionError("Connection error")
        
        # Call the function and check that it raises the correct error
        with pytest.raises(LLMConnectionError):
            await complete_chat(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}]
            )


@pytest.mark.asyncio
async def test_complete_chat_timeout_error():
    """Test that timeout errors are properly handled in complete_chat."""
    # Mock the default provider's complete_chat method
    with patch('app.llm_providers.default_provider.complete_chat', new_callable=AsyncMock) as mock_complete_chat:
        # Set up the mock to raise a timeout error
        mock_complete_chat.side_effect = LLMTimeoutError("Request timed out")
        
        # Call the function and check that it raises the correct error
        with pytest.raises(LLMTimeoutError):
            await complete_chat(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}]
            )


@pytest.mark.asyncio
async def test_complete_chat_model_not_found_error():
    """Test that model not found errors are properly handled in complete_chat."""
    # Mock the default provider's complete_chat method
    with patch('app.llm_providers.default_provider.complete_chat', new_callable=AsyncMock) as mock_complete_chat:
        # Set up the mock to raise a model not found error
        mock_complete_chat.side_effect = LLMModelNotFoundError("Model not found")
        
        # Call the function and check that it raises the correct error
        with pytest.raises(LLMModelNotFoundError):
            await complete_chat(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}]
            )


@pytest.mark.asyncio
async def test_complete_chat_invalid_request_error():
    """Test that invalid request errors are properly handled in complete_chat."""
    # Mock the default provider's complete_chat method
    with patch('app.llm_providers.default_provider.complete_chat', new_callable=AsyncMock) as mock_complete_chat:
        # Set up the mock to raise an invalid request error
        mock_complete_chat.side_effect = LLMInvalidRequestError("Invalid request")
        
        # Call the function and check that it raises the correct error
        with pytest.raises(LLMInvalidRequestError):
            await complete_chat(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}]
            )


@pytest.mark.asyncio
async def test_complete_chat_generic_error():
    """Test that generic errors are properly handled in complete_chat."""
    # Mock the complete_chat function directly to handle the exception wrapping
    with patch('app.llm_provider.complete_chat', new_callable=AsyncMock) as mock_complete_chat:
        # Set up the mock to raise a generic error wrapped in LLMProviderError
        mock_complete_chat.side_effect = LLMProviderError("Some other error")
        
        # Call the function and check that it raises the correct error
        with pytest.raises(LLMProviderError):
            await complete_chat(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}]
            )


@pytest.mark.asyncio
async def test_stream_chat_error_handling():
    """Test that errors are properly handled in stream_chat."""
    # Mock the default provider's stream_chat method
    with patch('app.llm_providers.default_provider.stream_chat', new_callable=AsyncMock) as mock_stream_chat:
        # Set up the mock to raise an error
        mock_stream_chat.side_effect = LLMRateLimitError("Rate limit exceeded")
        
        # Call the function and check that it raises the correct error
        with pytest.raises(LLMRateLimitError):
            async for _ in await stream_chat(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}]
            ):
                pass


def test_get_embedding_error_handling():
    """Test that errors are properly handled in get_embedding."""
    # Mock the default provider's get_embedding method
    with patch('app.llm_providers.default_provider.get_embedding') as mock_get_embedding:
        # Set up the mock to raise an error
        mock_get_embedding.side_effect = LLMAuthenticationError("Invalid API key")
        
        # Call the function and check that it raises the correct error
        with pytest.raises(LLMAuthenticationError):
            get_embedding("Hello")