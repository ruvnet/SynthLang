"""
Tests for SynthLang integration.

This module contains tests for the SynthLang integration with the proxy.
"""
import os
import sys
import pytest
from unittest.mock import patch, MagicMock, Mock
import json
from fastapi.testclient import TestClient
from fastapi import HTTPException

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Create mock modules before importing app
mock_dspy = MagicMock()
mock_openai = MagicMock()
mock_openai_instance = MagicMock()
mock_openai.return_value = mock_openai_instance
sys.modules['dspy'] = mock_dspy
sys.modules['dspy.openai'] = MagicMock()
sys.modules['dspy.openai'].OpenAI = mock_openai

from app.main import app
from app.synthlang.api import synthlang_api

# Create test client
client = TestClient(app)

# Mock API key for tests
TEST_API_KEY = "test-api-key"
TEST_USER_ID = "test-user"


@pytest.fixture
def mock_auth():
    """Mock authentication for tests."""
    with patch("app.auth.verify_api_key") as mock_verify:
        mock_verify.return_value = TEST_API_KEY
        with patch("app.auth.get_user_id") as mock_get_user:
            mock_get_user.return_value = TEST_USER_ID
            with patch("app.auth.check_rate_limit") as mock_rate_limit:
                yield


@pytest.fixture
def mock_dspy_lm():
    """Mock DSPy language model for tests."""
    mock_lm = MagicMock()
    with patch("app.synthlang.utils.get_dspy_lm", return_value=mock_lm):
        # Set the language model on the API
        old_lm = synthlang_api.lm
        synthlang_api.lm = mock_lm
        yield mock_lm
        # Restore the original language model
        synthlang_api.lm = old_lm


def test_synthlang_api_initialization():
    """Test SynthLang API initialization."""
    # Test that the API is initialized
    assert synthlang_api is not None
    
    # Test that the API is enabled by default
    assert synthlang_api.is_enabled()
    
    # Test that the API can be disabled
    synthlang_api.set_enabled(False)
    assert not synthlang_api.is_enabled()
    
    # Reset for other tests
    synthlang_api.set_enabled(True)


def test_compression_functions():
    """Test SynthLang compression functions."""
    # Test compression
    original_text = "This is a test prompt that should be compressed."
    compressed_text = "↹ test•prompt ⊕ compress => result"
    
    # Mock the compress_prompt function to return a shorter string
    with patch("app.synthlang.api.compress_prompt") as mock_compress:
        mock_compress.return_value = compressed_text
        
        compressed = synthlang_api.compress(original_text)
        assert compressed == compressed_text
        assert len(compressed) < len(original_text)
    
    # Test decompression
    # Mock the decompress_prompt function to return the original text
    with patch("app.synthlang.api.decompress_prompt") as mock_decompress:
        mock_decompress.return_value = original_text
        
        decompressed = synthlang_api.decompress(compressed_text)
        assert decompressed == original_text


def test_health_endpoint_includes_synthlang():
    """Test that the health endpoint includes SynthLang availability."""
    # Mock SynthLang availability
    with patch("app.synthlang.is_synthlang_available") as mock_available:
        mock_available.return_value = True
        
        # Mock the import in main.py
        with patch("app.main.is_synthlang_available", return_value=True):
            response = client.get("/health")
            assert response.status_code == 200
            data = response.json()
            assert "synthlang_available" in data
            assert data["synthlang_available"] is True


@pytest.mark.parametrize(
    "endpoint,request_data",
    [
        (
            "/v1/synthlang/translate",
            {"text": "This is a test prompt", "instructions": None}
        ),
        (
            "/v1/synthlang/generate",
            {"task_description": "Create a system prompt for a chatbot"}
        ),
        (
            "/v1/synthlang/optimize",
            {"prompt": "This is a test prompt", "max_iterations": 3}
        ),
        (
            "/v1/synthlang/evolve",
            {"seed_prompt": "This is a seed prompt", "n_generations": 5}
        ),
        (
            "/v1/synthlang/classify",
            {"text": "This is a test prompt", "labels": ["category1", "category2"]}
        ),
        (
            "/v1/synthlang/prompts/save",
            {"name": "test-prompt", "prompt": "This is a test prompt", "metadata": {"test": True}}
        ),
        (
            "/v1/synthlang/prompts/load",
            {"name": "test-prompt"}
        ),
        (
            "/v1/synthlang/prompts/delete",
            {"name": "test-prompt"}
        ),
        (
            "/v1/synthlang/prompts/compare",
            {"name1": "prompt1", "name2": "prompt2"}
        ),
    ]
)
def test_synthlang_endpoints_require_auth(endpoint, request_data):
    """Test that SynthLang endpoints require authentication."""
    # Mock verify_auth to raise an exception
    with patch("app.synthlang.endpoints.verify_auth") as mock_verify:
        mock_verify.side_effect = HTTPException(status_code=401, detail="Unauthorized")
        
        # Test without auth header
        response = client.post(endpoint, json=request_data)
        assert response.status_code == 401
        
        # Test with invalid auth header
        response = client.post(
            endpoint,
            json=request_data,
            headers={"Authorization": "invalid-key"}
        )
        assert response.status_code == 401


@pytest.mark.parametrize(
    "endpoint,request_data,mock_method,mock_return",
    [
        (
            "/v1/synthlang/translate",
            {"text": "This is a test prompt", "instructions": None},
            "app.synthlang.api.synthlang_api.translate",
            {"source": "This is a test prompt", "target": "↹ test•prompt", "explanation": "Translated"}
        ),
        (
            "/v1/synthlang/generate",
            {"task_description": "Create a system prompt for a chatbot"},
            "app.synthlang.api.synthlang_api.generate",
            {"prompt": "↹ chatbot•system", "rationale": "Generated", "metadata": {}}
        ),
        (
            "/v1/synthlang/optimize",
            {"prompt": "This is a test prompt", "max_iterations": 3},
            "app.synthlang.api.synthlang_api.optimize",
            {"optimized": "↹ optimized•prompt", "improvements": ["Improved"], "metrics": {"clarity": 0.9}, "original": "This is a test prompt"}
        ),
        (
            "/v1/synthlang/evolve",
            {"seed_prompt": "This is a seed prompt", "n_generations": 5},
            "app.synthlang.api.synthlang_api.evolve",
            {"best_prompt": "↹ evolved•prompt", "fitness": {"overall": 0.9}, "generations": 5, "total_variants": 10, "successful_mutations": 3}
        ),
        (
            "/v1/synthlang/classify",
            {"text": "This is a test prompt", "labels": ["category1", "category2"]},
            "app.synthlang.api.synthlang_api.classify",
            {"input": "This is a test prompt", "label": "category1", "explanation": "Classified"}
        ),
        (
            "/v1/synthlang/prompts/save",
            {"name": "test-prompt", "prompt": "This is a test prompt", "metadata": {"test": True}},
            "app.synthlang.api.synthlang_api.save_prompt",
            None  # save_prompt doesn't return anything
        ),
        (
            "/v1/synthlang/prompts/load",
            {"name": "test-prompt"},
            "app.synthlang.api.synthlang_api.load_prompt",
            {"name": "test-prompt", "prompt": "This is a test prompt", "metadata": {}}
        ),
        (
            "/v1/synthlang/prompts/list",
            None,
            "app.synthlang.api.synthlang_api.list_prompts",
            [{"name": "test-prompt", "prompt": "This is a test prompt", "metadata": {}}]
        ),
        (
            "/v1/synthlang/prompts/delete",
            {"name": "test-prompt"},
            "app.synthlang.api.synthlang_api.delete_prompt",
            True
        ),
        (
            "/v1/synthlang/prompts/compare",
            {"name1": "prompt1", "name2": "prompt2"},
            "app.synthlang.api.synthlang_api.compare_prompts",
            {"prompts": {"prompt1": "Text 1", "prompt2": "Text 2"}, "metrics": {}, "differences": {}}
        ),
    ]
)
def test_synthlang_endpoints_with_auth(mock_auth, mock_dspy_lm, endpoint, request_data, mock_method, mock_return):
    """Test SynthLang endpoints with authentication."""
    # Mock the API method
    with patch(mock_method) as mock_api:
        if mock_return is not None:
            mock_api.return_value = mock_return
        
        # Mock verify_auth to return the test API key
        with patch("app.synthlang.endpoints.verify_auth", return_value=TEST_API_KEY):
            # Mock the is_enabled method to return True
            with patch("app.synthlang.api.synthlang_api.is_enabled", return_value=True):
                # Make the request
                if request_data is None:
                    # For GET endpoints
                    response = client.get(
                        endpoint,
                        headers={"Authorization": f"Bearer {TEST_API_KEY}"}
                    )
                else:
                    # For POST endpoints
                    response = client.post(
                        endpoint,
                        json=request_data,
                        headers={"Authorization": f"Bearer {TEST_API_KEY}"}
                    )
                
                # Check response
                assert response.status_code == 200
                
                # Verify the API method was called
                if request_data is None:
                    mock_api.assert_called_once()
                else:
                    mock_api.assert_called_once()
                
                # Check response data
                data = response.json()
                assert "version" in data
                assert "timestamp" in data


def test_chat_completion_uses_synthlang_api(mock_auth):
    """Test that chat completion endpoint uses SynthLang API."""
    # Mock the compress and decompress methods
    with patch("app.synthlang.api.synthlang_api.compress") as mock_compress:
        mock_compress.return_value = "compressed_content"
        
        with patch("app.synthlang.api.synthlang_api.decompress") as mock_decompress:
            mock_decompress.return_value = "decompressed_content"
            
            # Mock cache and LLM provider
            with patch("app.cache.get_similar_response") as mock_cache:
                mock_cache.return_value = None
                
                with patch("app.llm_provider.complete_chat") as mock_llm:
                    mock_llm.return_value = {
                        "id": "test-id",
                        "created": 1234567890,
                        "choices": [
                            {
                                "message": {
                                    "role": "assistant",
                                    "content": "This is a test response"
                                },
                                "finish_reason": "stop"
                            }
                        ],
                        "usage": {
                            "prompt_tokens": 10,
                            "completion_tokens": 5,
                            "total_tokens": 15
                        }
                    }
                    
                    # Mock database
                    with patch("app.db.save_interaction") as mock_db:
                        # Make the request
                        response = client.post(
                            "/v1/chat/completions",
                            json={
                                "model": "test-model",
                                "messages": [
                                    {"role": "system", "content": "You are a helpful assistant"},
                                    {"role": "user", "content": "Hello, world!"}
                                ]
                            },
                            headers={"Authorization": f"Bearer {TEST_API_KEY}"}
                        )
                        
                        # Check response
                        assert response.status_code == 200
                        
                        # Verify SynthLang API was used
                        assert mock_compress.call_count == 2  # system and user messages
                        assert mock_decompress.call_count == 2  # system and user messages


def test_get_dspy_lm_mocked():
    """Test get_dspy_lm function with mocked imports."""
    # Mock the DSPy module
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        with patch("importlib.util.find_spec") as mock_find_spec:
            mock_find_spec.return_value = MagicMock()
            
            # Mock the DSPy module
            mock_dspy = MagicMock()
            mock_openai = MagicMock()
            mock_openai_instance = MagicMock()
            mock_openai.return_value = mock_openai_instance
            
            # Set up the mock modules
            sys.modules['dspy'] = mock_dspy
            sys.modules['dspy.openai'] = MagicMock()
            sys.modules['dspy.openai'].OpenAI = mock_openai
            
            # Import the function after mocking
            from app.synthlang.utils import get_dspy_lm
            
            # Call the function
            lm = get_dspy_lm()
            
            # Check result
            assert lm is mock_openai_instance
            mock_openai.assert_called_once()


def test_synthlang_api_handles_missing_lm():
    """Test that SynthLang API handles missing language model."""
    # Save current LM
    current_lm = synthlang_api.lm
    
    try:
        # Set LM to None
        synthlang_api.lm = None
        
        # Test translate without LM
        result = synthlang_api.translate("Test prompt")
        assert "source" in result
        assert "target" in result
        assert "explanation" in result
        assert "Translation not available" in result["explanation"]
        
        # Test generate without LM
        result = synthlang_api.generate("Test task")
        assert "prompt" in result
        assert "rationale" in result
        assert "metadata" in result
        assert "Generation not available" in result["rationale"]
        
        # Test optimize without LM
        result = synthlang_api.optimize("Test prompt")
        assert "optimized" in result
        assert "improvements" in result
        assert "metrics" in result
        assert "original" in result
        assert result["optimized"] == "Test prompt"  # Should return original
        
        # Test evolve without LM
        result = synthlang_api.evolve("Test prompt")
        assert "best_prompt" in result
        assert "fitness" in result
        assert "generations" in result
        assert result["best_prompt"] == "Test prompt"  # Should return original
        
        # Test classify without LM
        result = synthlang_api.classify("Test prompt", ["label1", "label2"])
        assert "input" in result
        assert "label" in result
        assert "explanation" in result
        assert "Classification not available" in result["explanation"]
    finally:
        # Restore LM
        synthlang_api.lm = current_lm