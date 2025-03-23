"""
Tests for the keyword detection middleware.

This module contains tests for the keyword detection middleware.
"""
import pytest
from unittest.mock import patch, AsyncMock, MagicMock
import os

from src.app.middleware.keyword_detection import (
    process_message_with_keywords,
    get_last_user_message,
    apply_keyword_detection
)
from src.app.keywords.registry import KeywordPattern, register_pattern, KEYWORD_REGISTRY

@pytest.fixture
def reset_registry():
    """Reset the keyword registry before and after tests."""
    # Save original
    original = KEYWORD_REGISTRY.copy()
    
    # Clear for test
    KEYWORD_REGISTRY.clear()
    
    yield
    
    # Restore original
    KEYWORD_REGISTRY.clear()
    KEYWORD_REGISTRY.update(original)

def test_get_last_user_message():
    """Test that get_last_user_message returns the last user message."""
    # Test with no user messages
    messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "assistant", "content": "How can I help you?"}
    ]
    assert get_last_user_message(messages) is None
    
    # Test with one user message
    messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "How can I help you?"}
    ]
    assert get_last_user_message(messages) == "Hello"
    
    # Test with multiple user messages
    messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "How can I help you?"},
        {"role": "user", "content": "What's the weather like?"}
    ]
    assert get_last_user_message(messages) == "What's the weather like?"

@pytest.mark.asyncio
async def test_process_message_with_keywords(reset_registry):
    """Test that process_message_with_keywords detects keywords and invokes tools."""
    # Register a test pattern
    test_pattern = KeywordPattern(
        name="test_weather",
        pattern=r"(?:what's|what is|how's|how is|get|check|tell me about)\s+(?:the)?\s*(?:weather|temperature|forecast)\s+(?:in|at|for)?\s+(?P<location>[^?]+)",
        tool="weather",
        description="Detects requests for weather information",
        priority=100
    )
    register_pattern(test_pattern)
    
    # Mock the get_user_roles function
    with patch("src.app.middleware.keyword_detection.get_user_roles", return_value=["basic"]):
        # Mock the get_tool function
        with patch("src.app.middleware.keyword_detection.get_tool") as mock_get_tool:
            # Create a mock tool function
            mock_tool = AsyncMock(return_value={"content": "The weather in New York is sunny and 75°F."})
            mock_get_tool.return_value = mock_tool
            
            # Test with a matching message
            message = "What's the weather in New York?"
            result = await process_message_with_keywords(message, "test_user")
            
            # Verify the result
            assert result is not None
            assert "content" in result
            assert "The weather in New York is sunny and 75°F." in result["content"]
            
            # Verify the tool was called with the correct parameters
            mock_get_tool.assert_called_once_with("weather")
            mock_tool.assert_called_once()
            call_args = mock_tool.call_args[1]
            assert "location" in call_args
            # Allow for either "New York" or "New York?" as the location
            assert call_args["location"] in ["New York", "New York?"]
            assert call_args["user_message"] == message
            assert call_args["user_id"] == "test_user"

@pytest.mark.asyncio
async def test_process_message_with_keywords_no_match(reset_registry):
    """Test that process_message_with_keywords returns None when no pattern matches."""
    # Register a test pattern
    test_pattern = KeywordPattern(
        name="test_weather",
        pattern=r"(?:what's|what is|how's|how is|get|check|tell me about)\s+(?:the)?\s*(?:weather|temperature|forecast)\s+(?:in|at|for)?\s+(?P<location>[^?]+)",
        tool="weather",
        description="Detects requests for weather information",
        priority=100
    )
    register_pattern(test_pattern)
    
    # Mock the get_user_roles function
    with patch("src.app.middleware.keyword_detection.get_user_roles", return_value=["basic"]):
        # Test with a non-matching message
        message = "Tell me a joke"
        result = await process_message_with_keywords(message, "test_user")
        
        # Verify the result
        assert result is None

@pytest.mark.asyncio
async def test_process_message_with_keywords_role_restriction(reset_registry):
    """Test that process_message_with_keywords respects role restrictions."""
    # Register a test pattern with role restriction
    test_pattern = KeywordPattern(
        name="test_admin",
        pattern=r"(?:admin|system|configure|setup|manage)\s+(?:the|this)?\s*(?:system|server|application|app|service)\s+(?:to|for)?\s+(?P<action>[^?]+)",
        tool="system_admin",
        description="Detects requests for system administration tasks",
        priority=200,
        required_role="admin"
    )
    register_pattern(test_pattern)
    
    # Mock the get_user_roles function for a basic user
    with patch("src.app.middleware.keyword_detection.get_user_roles", return_value=["basic"]):
        # Test with a matching message but insufficient role
        message = "admin the system to restart the server"
        result = await process_message_with_keywords(message, "test_user")
        
        # Verify the result (should be None due to role restriction)
        assert result is None
    
    # Mock the get_user_roles function for an admin user
    with patch("src.app.middleware.keyword_detection.get_user_roles", return_value=["admin"]):
        # Mock the get_tool function
        with patch("src.app.middleware.keyword_detection.get_tool") as mock_get_tool:
            # Create a mock tool function
            mock_tool = AsyncMock(return_value={"content": "System restarted successfully."})
            mock_get_tool.return_value = mock_tool
            
            # Test with a matching message and sufficient role
            message = "admin the system to restart the server"
            result = await process_message_with_keywords(message, "admin_user")
            
            # Verify the result
            assert result is not None
            assert "content" in result
            assert "System restarted successfully." in result["content"]

@pytest.mark.asyncio
async def test_process_message_with_keywords_tool_error(reset_registry):
    """Test that process_message_with_keywords handles tool errors gracefully."""
    # Register a test pattern
    test_pattern = KeywordPattern(
        name="test_weather",
        pattern=r"(?:what's|what is|how's|how is|get|check|tell me about)\s+(?:the)?\s*(?:weather|temperature|forecast)\s+(?:in|at|for)?\s+(?P<location>[^?]+)",
        tool="weather",
        description="Detects requests for weather information",
        priority=100
    )
    register_pattern(test_pattern)
    
    # Mock the get_user_roles function
    with patch("src.app.middleware.keyword_detection.get_user_roles", return_value=["basic"]):
        # Mock the get_tool function
        with patch("src.app.middleware.keyword_detection.get_tool") as mock_get_tool:
            # Create a mock tool function that raises an exception
            mock_tool = AsyncMock(side_effect=Exception("Weather service unavailable"))
            mock_get_tool.return_value = mock_tool
            
            # Test with a matching message
            message = "What's the weather in New York?"
            result = await process_message_with_keywords(message, "test_user")
            
            # Verify the result contains an error message
            assert result is not None
            assert "content" in result
            assert "error" in result["content"].lower()
            assert "Weather service unavailable" in result["content"]

@pytest.mark.asyncio
async def test_apply_keyword_detection(reset_registry):
    """Test that apply_keyword_detection processes messages correctly."""
    # Register a test pattern
    test_pattern = KeywordPattern(
        name="test_weather",
        pattern=r"(?:what's|what is|how's|how is|get|check|tell me about)\s+(?:the)?\s*(?:weather|temperature|forecast)\s+(?:in|at|for)?\s+(?P<location>[^?]+)",
        tool="weather",
        description="Detects requests for weather information",
        priority=100
    )
    register_pattern(test_pattern)
    
    # Mock the get_user_roles function
    with patch("src.app.middleware.keyword_detection.get_user_roles", return_value=["basic"]):
        # Mock the get_tool function
        with patch("src.app.middleware.keyword_detection.get_tool") as mock_get_tool:
            # Create a mock tool function
            mock_tool = AsyncMock(return_value={"content": "The weather in New York is sunny and 75°F."})
            mock_get_tool.return_value = mock_tool
            
            # Test with a matching message
            messages = [
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": "Hello"},
                {"role": "assistant", "content": "How can I help you?"},
                {"role": "user", "content": "What's the weather in New York?"}
            ]
            result = await apply_keyword_detection(messages, "test_user")
            
            # Verify the result
            assert result is not None
            assert "content" in result
            assert "The weather in New York is sunny and 75°F." in result["content"]
            
            # Verify the tool was called with the correct parameters
            mock_get_tool.assert_called_once_with("weather")
            mock_tool.assert_called_once()
            call_args = mock_tool.call_args[1]
            assert "location" in call_args
            # Allow for either "New York" or "New York?" as the location
            assert call_args["location"] in ["New York", "New York?"]