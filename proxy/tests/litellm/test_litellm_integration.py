"""
Integration tests for LiteLLM with FastAPI endpoints.

This module tests the integration of LiteLLM with the FastAPI endpoints,
focusing on handling various request formats including complex JSON and raw text.
"""
import pytest
import json
import sys
import os
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock

# Add the src directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.app.main import app

@pytest.fixture
def client():
    """Fixture for a FastAPI test client."""
    return TestClient(app)

@pytest.fixture
def auth_headers():
    """Fixture for authentication headers."""
    return {"Authorization": "Bearer test-key"}

@pytest.fixture
def mock_process_chat_completion():
    """Fixture to mock the process_chat_completion function."""
    mock_response = {
        "id": "chatcmpl-123",
        "object": "chat.completion",
        "created": 1677652288,
        "model": "gpt-4o-mini",
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "I'm doing well, thank you for asking!"
            },
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": 20,
            "completion_tokens": 17,
            "total_tokens": 37
        }
    }
    
    with patch("src.app.main.process_chat_completion", new=AsyncMock(return_value=mock_response)) as mock:
        yield mock

def test_json_request(client, auth_headers, mock_process_chat_completion):
    """Test standard JSON request."""
    response = client.post(
        "/chat/completions",
        headers={"Content-Type": "application/json", **auth_headers},
        json={
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": "Hello"}]
        }
    )
    
    assert response.status_code == 200
    assert "choices" in response.json()
    assert mock_process_chat_completion.called

def test_raw_text_request(client, auth_headers, mock_process_chat_completion):
    """Test raw text request."""
    response = client.post(
        "/chat/completions?model=gpt-4o-mini",
        headers={"Content-Type": "text/plain", **auth_headers},
        data="Hello, this is a raw text request"
    )
    
    assert response.status_code == 200
    assert "choices" in response.json()
    assert mock_process_chat_completion.called
    
    # Verify the message was correctly constructed
    call_args = mock_process_chat_completion.call_args[0]
    assert call_args[0].messages[0].role == "user"
    assert call_args[0].messages[0].content == "Hello, this is a raw text request"

def test_complex_json_request(client, auth_headers, mock_process_chat_completion):
    """Test complex JSON request with nested structures."""
    complex_data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": {
                "main_text": "This is a complex message with nested structure",
                "metadata": {
                    "source": "user interface",
                    "timestamp": 1677652288,
                    "client_info": {"browser": "Chrome", "version": "98.0.4758.102"}
                },
                "attachments": [
                    {"title": "Document 1", "content": "Some content here"},
                    {"title": "Document 2", "content": "More content here"}
                ]
            }}
        ]
    }
    
    # This would normally fail with validation errors before LiteLLM integration
    response = client.post(
        "/chat/completions",
        headers={"Content-Type": "application/json", **auth_headers},
        json=complex_data
    )
    
    assert response.status_code == 200
    assert "choices" in response.json()
    assert mock_process_chat_completion.called

def test_malformed_json_fallback(client, auth_headers, mock_process_chat_completion):
    """Test malformed JSON falls back to raw text handling."""
    response = client.post(
        "/chat/completions?model=gpt-4o-mini",
        headers={"Content-Type": "application/json", **auth_headers},
        data="This is not valid JSON but should be handled as raw text"
    )
    
    assert response.status_code == 200
    assert "choices" in response.json()
    assert mock_process_chat_completion.called
    
    # Verify the message was correctly constructed as raw text
    call_args = mock_process_chat_completion.call_args[0]
    assert call_args[0].messages[0].role == "user"
    assert call_args[0].messages[0].content == "This is not valid JSON but should be handled as raw text"

def test_query_parameters(client, auth_headers, mock_process_chat_completion):
    """Test query parameters are correctly parsed."""
    response = client.post(
        "/chat/completions?model=gpt-4&temperature=0.5&stream=true",
        headers={"Content-Type": "text/plain", **auth_headers},
        data="Testing query parameters"
    )
    
    assert response.status_code == 200
    
    # Verify query parameters were correctly parsed
    call_args = mock_process_chat_completion.call_args[0]
    assert call_args[0].model == "gpt-4"
    assert call_args[0].temperature == 0.5
    assert call_args[0].stream is True

def test_missing_authorization(client):
    """Test error handling for missing authorization."""
    response = client.post(
        "/chat/completions",
        headers={"Content-Type": "application/json"},
        json={
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": "Hello"}]
        }
    )
    
    assert response.status_code == 401
    assert "error" in response.json()

def test_invalid_temperature(client, auth_headers, mock_process_chat_completion):
    """Test handling of invalid temperature parameter."""
    response = client.post(
        "/chat/completions?model=gpt-4o-mini&temperature=invalid",
        headers={"Content-Type": "text/plain", **auth_headers},
        data="Testing invalid temperature"
    )
    
    # Should still work, with temperature defaulting to 1.0
    assert response.status_code == 200
    
    # Verify temperature defaulted to 1.0
    call_args = mock_process_chat_completion.call_args[0]
    assert call_args[0].temperature == 1.0

def test_empty_request_body(client, auth_headers, mock_process_chat_completion):
    """Test handling of empty request body."""
    response = client.post(
        "/chat/completions?model=gpt-4o-mini",
        headers={"Content-Type": "text/plain", **auth_headers},
        data=""
    )
    
    assert response.status_code == 200
    
    # Verify empty message was handled properly
    call_args = mock_process_chat_completion.call_args[0]
    assert call_args[0].messages[0].content == ""