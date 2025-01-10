"""Tests for CLI interface."""
import json
from pathlib import Path
from typing import Dict

import pytest
from click.testing import CliRunner

from synthlang.cli import cli

@pytest.fixture
def runner():
    """CLI runner fixture."""
    return CliRunner()

@pytest.fixture
def config_file(tmp_path):
    """Sample config file fixture."""
    config = {
        "openai_api_key": "sk-test",
        "model": "gpt-4o-mini",
        "environment": "testing",
        "log_level": "INFO"
    }
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps(config))
    return config_path

def test_cli_version(runner):
    """Test version command."""
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "SynthLang CLI" in result.output

def test_cli_init(runner, tmp_path):
    """Test init command."""
    result = runner.invoke(cli, ["init", "--config", str(tmp_path / "config.json")])
    assert result.exit_code == 0
    assert "Configuration initialized" in result.output
    assert (tmp_path / "config.json").exists()

def test_cli_translate(runner, config_file):
    """Test translate command."""
    source_code = """
    function example() {
        console.log("Hello");
    }
    """
    result = runner.invoke(cli, [
        "translate",
        "--config", str(config_file),
        "--source", source_code,
        "--target-framework", "python"
    ])
    assert result.exit_code == 0
    assert "Translation complete" in result.output

def test_cli_generate(runner, config_file):
    """Test generate command."""
    task = "Create a chatbot assistant"
    result = runner.invoke(cli, [
        "generate",
        "--config", str(config_file),
        "--task", task
    ])
    assert result.exit_code == 0
    assert "System prompt generated" in result.output

def test_cli_optimize(runner, config_file):
    """Test optimize command."""
    prompt = "You are a helpful assistant"
    result = runner.invoke(cli, [
        "optimize",
        "--config", str(config_file),
        "--prompt", prompt
    ])
    assert result.exit_code == 0
    assert "Prompt optimized" in result.output

def test_cli_config_show(runner, config_file):
    """Test config show command."""
    result = runner.invoke(cli, [
        "config",
        "show",
        "--config", str(config_file)
    ])
    assert result.exit_code == 0
    assert "Current configuration" in result.output
    assert "gpt-4o-mini" in result.output

def test_cli_config_set(runner, config_file):
    """Test config set command."""
    result = runner.invoke(cli, [
        "config",
        "set",
        "--config", str(config_file),
        "--key", "log_level",
        "--value", "DEBUG"
    ])
    assert result.exit_code == 0
    assert "Configuration updated" in result.output

    # Verify update
    with open(config_file) as f:
        config = json.load(f)
        assert config["log_level"] == "DEBUG"

def test_cli_invalid_config(runner, tmp_path):
    """Test CLI with invalid config."""
    invalid_config = tmp_path / "invalid.json"
    invalid_config.write_text("invalid json")
    
    result = runner.invoke(cli, [
        "translate",
        "--config", str(invalid_config),
        "--source", "code",
        "--target-framework", "python"
    ])
    assert result.exit_code != 0
    assert "Error loading configuration" in result.output

def test_cli_missing_config(runner):
    """Test CLI with missing config."""
    result = runner.invoke(cli, [
        "translate",
        "--config", "nonexistent.json",
        "--source", "code",
        "--target-framework", "python"
    ])
    assert result.exit_code != 0
    assert "Configuration file not found" in result.output

def test_cli_help(runner):
    """Test help command."""
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output
    
    # Test subcommand help
    commands = ["init", "translate", "generate", "optimize", "config"]
    for cmd in commands:
        result = runner.invoke(cli, [cmd, "--help"])
        assert result.exit_code == 0
        assert "Usage:" in result.output
