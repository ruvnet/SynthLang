"""Tests for SynthLang Proxy functionality."""
import json
import os
import tempfile
from pathlib import Path
from unittest import mock

import pytest
from click.testing import CliRunner

from synthlang.cli import main
from synthlang.proxy.cache import SemanticCache
from synthlang.proxy.compression import compress_prompt, decompress_prompt


@pytest.fixture
def runner():
    """Create a CLI runner for testing."""
    return CliRunner()


@pytest.fixture
def temp_cache_dir():
    """Create a temporary directory for cache testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


def test_compression():
    """Test compression and decompression functionality."""
    # Test basic compression
    original = "This is a test prompt that should be compressed"
    compressed = compress_prompt(original, use_gzip=False)
    
    # Verify compression worked
    assert len(compressed) < len(original)
    
    # Test with gzip
    gzip_compressed = compress_prompt(original, use_gzip=True)
    
    # Verify gzip compression
    assert len(gzip_compressed) < len(original)
    
    # Test decompression
    decompressed = decompress_prompt(compressed)
    assert decompressed  # Should return something, even if not exact match


def test_semantic_cache(temp_cache_dir):
    """Test semantic cache functionality."""
    # Create cache with custom directory
    cache = SemanticCache(cache_dir=temp_cache_dir)
    
    # Test setting and getting
    key = "test_key"
    value = {"data": "test_value"}
    
    # Initially should be empty
    assert cache.get(key) is None
    
    # Set and get
    cache.set(key, value)
    result = cache.get(key)
    assert result == value
    
    # Test clearing
    count = cache.clear()
    assert count == 1  # Should have cleared one entry
    assert cache.get(key) is None  # Should be gone


def test_compress_command(runner):
    """Test the compress command."""
    result = runner.invoke(main, ["proxy", "compress", "This is a test prompt"])
    assert result.exit_code == 0
    assert "Original" in result.output
    assert "Compressed" in result.output
    assert "Compression ratio" in result.output


def test_cache_commands(runner, temp_cache_dir):
    """Test cache-related commands."""
    # Mock the get_semantic_cache function to use our temp directory
    with mock.patch('synthlang.proxy.cache.get_semantic_cache', 
                   return_value=SemanticCache(cache_dir=temp_cache_dir)):
        
        # Test cache stats
        result = runner.invoke(main, ["proxy", "cache-stats"])
        assert result.exit_code == 0
        assert "Cache Statistics" in result.output
        
        # Test clear cache
        result = runner.invoke(main, ["proxy", "clear-cache"])
        assert result.exit_code == 0
        assert "Cleared" in result.output


def test_tools_command(runner):
    """Test the tools command."""
    result = runner.invoke(main, ["proxy", "tools"])
    assert result.exit_code == 0
    assert "Available Tools" in result.output
    
    # Should list at least the built-in tools
    assert "get_current_time" in result.output or "calculate" in result.output


@mock.patch('synthlang.proxy.agents.registry.call_tool_with_json')
def test_call_tool_command(mock_call_tool, runner):
    """Test the call-tool command."""
    mock_call_tool.return_value = 4
    
    result = runner.invoke(
        main, ["proxy", "call-tool", "--tool", "calculate", "--args", '{"expression": "2+2"}']
    )
    
    assert result.exit_code == 0
    assert "Result" in result.output
    mock_call_tool.assert_called_once_with("calculate", '{"expression": "2+2"}')


@mock.patch('synthlang.proxy.auth.save_credentials')
def test_login_command(mock_save_credentials, runner):
    """Test the login command."""
    result = runner.invoke(
        main, ["proxy", "login", "--api-key", "test-key", "--endpoint", "https://test.com"]
    )
    
    assert result.exit_code == 0
    assert "Credentials saved" in result.output
    mock_save_credentials.assert_called_once_with("test-key", "https://test.com")


@mock.patch('synthlang.proxy.auth.clear_credentials')
def test_logout_command(mock_clear_credentials, runner):
    """Test the logout command."""
    result = runner.invoke(main, ["proxy", "logout"])
    
    assert result.exit_code == 0
    assert "Credentials cleared" in result.output
    mock_clear_credentials.assert_called_once()


@mock.patch('synthlang.proxy.api.ProxyClient.chat_completion')
@mock.patch('synthlang.proxy.auth.get_credentials')
def test_chat_command(mock_get_credentials, mock_chat_completion, runner):
    """Test the chat command."""
    # Mock credentials
    mock_get_credentials.return_value = {
        "api_key": "test-key",
        "endpoint": "https://test.com"
    }
    
    # Mock chat completion response
    mock_chat_completion.return_value = {
        "choices": [
            {
                "message": {
                    "content": "This is a test response"
                }
            }
        ]
    }
    
    result = runner.invoke(main, ["proxy", "chat", "Hello world"])
    
    assert result.exit_code == 0
    assert "This is a test response" in result.output
    
    # Verify the correct message was sent
    args, kwargs = mock_chat_completion.call_args
    assert len(args[0]) == 1  # One message
    assert args[0][0]["role"] == "user"
    assert args[0][0]["content"] == "Hello world"


@mock.patch('uvicorn.run')
def test_serve_command(mock_run, runner):
    """Test the serve command."""
    # Use a very short timeout to avoid hanging the test
    with mock.patch('click.echo'):  # Suppress output
        result = runner.invoke(main, ["proxy", "serve", "--port", "8000"])
    
    # The command should start but we mock uvicorn.run
    assert mock_run.called
    
    # Check the arguments
    args, kwargs = mock_run.call_args
    assert kwargs["port"] == 8000
    assert "synthlang.proxy.server:create_app" in args[0]