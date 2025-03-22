"""Test configuration and shared fixtures."""
import json
from pathlib import Path
from typing import Dict
from unittest.mock import Mock

import pytest
import dspy
from click.testing import CliRunner

from synthlang.config import Config, ConfigManager

@pytest.fixture
def temp_env_file(tmp_path) -> Path:
    """Create a temporary .env file."""
    env_content = """
    OPENAI_API_KEY=sk-test
    SYNTHLANG_MODEL=gpt-4o-mini
    SYNTHLANG_ENV=testing
    SYNTHLANG_LOG_LEVEL=INFO
    """
    env_file = tmp_path / ".env"
    env_file.write_text(env_content)
    return env_file

@pytest.fixture
def temp_config_file(tmp_path) -> Path:
    """Create a temporary config file."""
    config = {
        "openai_api_key": "sk-test",
        "model": "gpt-4o-mini",
        "environment": "testing",
        "log_level": "INFO"
    }
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps(config))
    return config_path

@pytest.fixture
def config_manager() -> ConfigManager:
    """Create a ConfigManager instance."""
    return ConfigManager()

@pytest.fixture
def cli_runner() -> CliRunner:
    """Create a Click CLI test runner."""
    return CliRunner()

@pytest.fixture
def mock_openai_response() -> Dict:
    """Mock OpenAI API response."""
    return {
        "choices": [{
            "text": "Mocked response",
            "finish_reason": "stop"
        }]
    }

@pytest.fixture
def test_config() -> Config:
    """Create a test configuration."""
    return Config(
        openai_api_key="sk-test",
        model="gpt-4o-mini",
        environment="testing",
        log_level="INFO"
    )

@pytest.fixture
def test_source_code() -> str:
    """Sample source code for testing."""
    return """
    function example() {
        console.log("Hello World");
        return 42;
    }
    """

@pytest.fixture
def test_task_description() -> str:
    """Sample task description for testing."""
    return "Create an AI assistant that helps with code review"

@pytest.fixture
def test_system_prompt() -> str:
    """Sample system prompt for testing."""
    return """You are a helpful AI assistant that specializes in code review.
    You analyze code for:
    1. Best practices
    2. Potential bugs
    3. Performance issues
    4. Security concerns"""

@pytest.fixture
def mock_lm():
    """Mock DSPy language model for testing."""
    mock = Mock(spec=dspy.LM)
    mock.generate.return_value = {
        'choices': [{
            'finish_reason': 'stop',
            'index': 0,
            'message': {
                'content': {
                    'source': 'Original text', 
                    'target': 'Translated text',
                    'explanation': 'Translation explanation'
                },
                'role': 'assistant'
            }
        }],
        'created': 1677858242,
        'id': 'chatcmpl-123',
        'model': 'gpt-4o-mini',
        'object': 'chat.completion',
        'usage': {'completion_tokens': 100, 'prompt_tokens': 50, 'total_tokens': 150}
    }
    mock.kwargs = {'temperature': 0.0}
    return mock

def pytest_configure(config):
    """Configure test environment."""
    # Add custom markers
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
