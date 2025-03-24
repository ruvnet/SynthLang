"""
Tests for the authentication module.

This module contains tests for the API key authentication and rate limiting functions.
"""
import pytest
import time
from unittest.mock import patch, MagicMock
from fastapi import HTTPException, Request

from app.auth import (
    verify_api_key,
    get_user_id,
    get_rate_limit,
    check_rate_limit,
    allow_request,
    API_KEYS,
    _request_counts
)


def test_verify_api_key_valid():
    """Test that verify_api_key accepts valid API keys."""
    # Valid API key with Bearer prefix
    api_key = verify_api_key("Bearer sk_test_user1")
    assert api_key == "sk_test_user1"


def test_verify_api_key_missing():
    """Test that verify_api_key rejects missing API keys."""
    with pytest.raises(HTTPException) as excinfo:
        verify_api_key(None)
    
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail["error"]["message"] == "Missing API key"


def test_verify_api_key_invalid_format():
    """Test that verify_api_key rejects API keys with invalid format."""
    with pytest.raises(HTTPException) as excinfo:
        verify_api_key("sk_test_user1")  # Missing Bearer prefix
    
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail["error"]["message"] == "Invalid Authorization header format"


def test_verify_api_key_invalid_key():
    """Test that verify_api_key rejects invalid API keys."""
    with pytest.raises(HTTPException) as excinfo:
        verify_api_key("Bearer invalid_key")
    
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail["error"]["message"] == "Invalid API key"


def test_get_user_id():
    """Test that get_user_id returns the correct user ID for an API key."""
    user_id = get_user_id("sk_test_user1")
    assert user_id == "user1"
    
    user_id = get_user_id("sk_test_user2")
    assert user_id == "user2"


def test_get_rate_limit():
    """Test that get_rate_limit returns the correct rate limit for an API key."""
    rate_limit = get_rate_limit("sk_test_user1")
    assert rate_limit == 60
    
    rate_limit = get_rate_limit("sk_test_user2")
    assert rate_limit == 5


def test_check_rate_limit_first_request():
    """Test that check_rate_limit allows the first request for a user."""
    # Clear request counts
    _request_counts.clear()
    
    # Create a mock request
    mock_request = MagicMock(spec=Request)
    
    # This should not raise an exception
    check_rate_limit(mock_request, "sk_test_user1")
    
    # Verify request count was initialized
    assert "user1" in _request_counts
    assert _request_counts["user1"][1] == 1


def test_check_rate_limit_under_limit():
    """Test that check_rate_limit allows requests under the rate limit."""
    # Clear request counts
    _request_counts.clear()
    
    # Set up initial request count
    user_id = "user1"
    _request_counts[user_id] = [time.time(), 5]  # 5 requests so far
    
    # Create a mock request
    mock_request = MagicMock(spec=Request)
    
    # This should not raise an exception (limit is 60)
    check_rate_limit(mock_request, "sk_test_user1")
    
    # Verify request count was incremented
    assert _request_counts[user_id][1] == 6


def test_check_rate_limit_at_limit():
    """Test that check_rate_limit rejects requests at the rate limit."""
    # Clear request counts
    _request_counts.clear()
    
    # Set up initial request count at the limit
    user_id = "user2"
    _request_counts[user_id] = [time.time(), 5]  # 5 requests so far (limit is 5)
    
    # Create a mock request
    mock_request = MagicMock(spec=Request)
    
    # This should raise an exception
    with pytest.raises(HTTPException) as excinfo:
        check_rate_limit(mock_request, "sk_test_user2")
    
    assert excinfo.value.status_code == 429
    assert excinfo.value.detail["error"]["message"] == "Rate limit exceeded"
    assert "Retry-After" in excinfo.value.headers


def test_check_rate_limit_window_reset():
    """Test that check_rate_limit resets the count after the time window."""
    # Clear request counts
    _request_counts.clear()
    
    # Set up initial request count with an old timestamp
    user_id = "user1"
    _request_counts[user_id] = [time.time() - 61, 60]  # 60 requests, but window expired
    
    # Create a mock request
    mock_request = MagicMock(spec=Request)
    
    # This should not raise an exception
    check_rate_limit(mock_request, "sk_test_user1")
    
    # Verify window was reset
    assert _request_counts[user_id][1] == 1
    assert time.time() - _request_counts[user_id][0] < 1  # New timestamp


def test_allow_request_first_request():
    """Test that allow_request returns True for the first request."""
    # Clear request counts
    _request_counts.clear()
    
    # This should return True
    assert allow_request("user1") is True
    
    # Verify request count was initialized
    assert "user1" in _request_counts
    assert _request_counts["user1"][1] == 1


def test_allow_request_under_limit():
    """Test that allow_request returns True for requests under the limit."""
    # Clear request counts
    _request_counts.clear()
    
    # Set up initial request count
    user_id = "user1"
    _request_counts[user_id] = [time.time(), 5]  # 5 requests so far
    
    # This should return True (limit is 60)
    assert allow_request(user_id) is True
    
    # Verify request count was incremented
    assert _request_counts[user_id][1] == 6


def test_allow_request_at_limit():
    """Test that allow_request returns False for requests at the limit."""
    # Clear request counts
    _request_counts.clear()
    
    # Set up initial request count at the limit
    user_id = "user2"
    _request_counts[user_id] = [time.time(), 5]  # 5 requests so far (limit is 5)
    
    # This should return False
    assert allow_request(user_id) is False


def test_allow_request_window_reset():
    """Test that allow_request resets the count after the time window."""
    # Clear request counts
    _request_counts.clear()
    
    # Set up initial request count with an old timestamp
    user_id = "user1"
    _request_counts[user_id] = [time.time() - 61, 60]  # 60 requests, but window expired
    
    # This should return True
    assert allow_request(user_id) is True
    
    # Verify window was reset
    assert _request_counts[user_id][1] == 1
    assert time.time() - _request_counts[user_id][0] < 1  # New timestamp


def test_allow_request_unknown_user():
    """Test that allow_request returns False for unknown users."""
    # This should return True (using default rate limit)
    assert allow_request("unknown_user") is True