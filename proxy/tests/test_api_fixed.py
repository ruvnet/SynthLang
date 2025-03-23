"""
Tests for the API endpoints with fixed mocking.

This module contains tests for the API endpoints with proper mocking.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
import time

from app.main import app

client = TestClient(app)


def test_chat_completion_endpoint_synthlang_compression():
    """Test that the chat completion endpoint uses SynthLang compression."""
    # Mock the rate limit check and SynthLang API compression
    with patch("app.auth.check_rate_limit", return_value=None), \
         patch("app.synthlang.api.synthlang_api.compress") as mock_compress, \
         patch("app.synthlang.api.synthlang_api.decompress") as mock_decompress, \
         patch("app.llm_provider.complete_chat", new_callable=AsyncMock) as mock_complete_chat, \
         patch("app.db.save_interaction", new_callable=AsyncMock):
        
        # Set up the mocks
        mock_compress.return_value = "compressed content"
        mock_decompress.return_value = "decompressed content"
        mock_complete_chat.return_value = {
            "id": "chatcmpl-123",
            "created": int(time.time()),
            "choices": [{"message": {"content": "Test response"}}],
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 10,
                "total_tokens": 20
            }
        }
        
        headers = {"Authorization": "Bearer sk_test_user1"}
        req_body = {
            "model": "test-model",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": "Hello"}
            ]
        }
        response = client.post("/v1/chat/completions", json=req_body, headers=headers)
        assert response.status_code == 200
        
        # Verify that compress was called twice (once for system, once for user)
        assert mock_compress.call_count == 2
        mock_compress.assert_any_call("You are a helpful assistant")
        mock_compress.assert_any_call("Hello")
        
        # Verify that decompress was called twice (once for system, once for user)
        assert mock_decompress.call_count == 2
        mock_decompress.assert_any_call("compressed content")