"""Tests for CLI interface."""
import json
import os
from pathlib import Path
from typing import Dict

import pytest
from click.testing import CliRunner

from synthlang.cli import main

@pytest.fixture
def runner():
    """CLI runner fixture."""
    return CliRunner()

@pytest.fixture
def env_vars():
    """Environment variables fixture."""
    os.environ["OPENAI_API_KEY"] = "sk-test"
    os.environ["SYNTHLANG_MODEL"] = "gpt-4o-mini"
    os.environ["SYNTHLANG_ENV"] = "testing"
    os.environ["SYNTHLANG_LOG_LEVEL"] = "INFO"
    os.environ["SYNTHLANG_TEMPERATURE"] = "0.7"
    os.environ["SYNTHLANG_MAX_TOKENS"] = "2048"
    os.environ["SYNTHLANG_CONTEXT_WINDOW"] = "4096"
    yield
    # Clean up
    del os.environ["OPENAI_API_KEY"]
    del os.environ["SYNTHLANG_MODEL"]
    del os.environ["SYNTHLANG_ENV"]
    del os.environ["SYNTHLANG_LOG_LEVEL"]
    del os.environ["SYNTHLANG_TEMPERATURE"]
    del os.environ["SYNTHLANG_MAX_TOKENS"]
    del os.environ["SYNTHLANG_CONTEXT_WINDOW"]

def test_cli_version(runner):
    """Test version command."""
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "SynthLang CLI" in result.output

def test_cli_translate(runner, env_vars, mock_lm):
    """Test translate command."""
    from flask import Flask, current_app

    # Set up Flask test app and context
    app = Flask(__name__) 
    app.test_mock_lm = mock_lm
    with app.app_context():
        # Configure mock LM response
        mock_lm.completion.return_value = "Translated code"
        
        source_code = """
        function example() {
            console.log("Hello");
        }
        """
        result = runner.invoke(main, [
            "translate",
            "--source", source_code,
            "--target-framework", "synthlang"
        ])
        print("\nTest output:", result.output)
        assert result.exit_code == 0
        assert "Translation complete" in result.output

    # Verify mock was used
    mock_lm.completion.assert_called_once()

def test_cli_generate(runner, env_vars):
    """Test generate command."""
    task = "Create a chatbot assistant"
    result = runner.invoke(main, [
        "generate",
        "--task", task
    ])
    assert result.exit_code == 0
    assert "System prompt generated" in result.output

def test_cli_optimize(runner, env_vars):
    """Test optimize command."""
    prompt = "You are a helpful assistant"
    result = runner.invoke(main, [
        "optimize",
        "--prompt", prompt
    ])
    assert result.exit_code == 0
    assert "Prompt optimized" in result.output

def test_cli_config_show(runner, env_vars):
    """Test config show command."""
    result = runner.invoke(main, [
        "config",
        "show"
    ])
    assert result.exit_code == 0
    assert "Current configuration" in result.output
    assert "gpt-4o-mini" in result.output

def test_cli_config_set(runner, env_vars):
    """Test config set command."""
    result = runner.invoke(main, [
        "config",
        "set",
        "--key", "log_level",
        "--value", "DEBUG"
    ])
    assert result.exit_code == 0
    assert "Configuration updated" in result.output
    assert os.environ["SYNTHLANG_LOG_LEVEL"] == "DEBUG"

def test_cli_missing_api_key(runner):
    """Test CLI with missing API key."""
    result = runner.invoke(main, [
        "translate",
        "--source", "code",
        "--target-framework", "python"
    ])
    assert result.exit_code != 0
    assert "OPENAI_API_KEY not found" in result.output

def test_cli_help(runner):
    """Test help command."""
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output
    
    # Test subcommand help
    commands = ["translate", "generate", "optimize", "config"]
    for cmd in commands:
        result = runner.invoke(main, [cmd, "--help"])
        assert result.exit_code == 0
        assert "Usage:" in result.output
