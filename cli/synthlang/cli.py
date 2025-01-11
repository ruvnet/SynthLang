"""Command-line interface for SynthLang."""
import json
import os
import sys
from pathlib import Path
from typing import Optional

import click
import dspy

from synthlang import __version__
from synthlang.config import Config, ConfigManager
from synthlang.core.modules import FrameworkTranslator, SystemPromptGenerator

def load_config(config_path: Path) -> Config:
    """Load configuration from file."""
    if not config_path.exists():
        raise click.ClickException("Configuration file not found")
    try:
        config_manager = ConfigManager()
        return config_manager.load(config_path)
    except Exception as e:
        raise click.ClickException(f"Error loading configuration: {str(e)}")

def get_api_key() -> str:
    """Get OpenAI API key from environment variable or root .env file."""
    # First check environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return api_key
        
    # Then check root .env file
    root_env = Path("/workspaces/SynthLang/.env")
    if root_env.exists():
        with open(root_env) as f:
            for line in f:
                if line.startswith("OPENAI_API_KEY="):
                    return line.strip().split("=", 1)[1]
                    
    raise click.ClickException(
        "OPENAI_API_KEY not found in environment or .env file"
    )

@click.group()
@click.version_option(version=__version__, prog_name="SynthLang CLI")
def main():
    """SynthLang CLI - Framework translation and prompt engineering tool."""
    pass

@main.command()
@click.option(
    "--config",
    type=click.Path(path_type=Path),
    required=True,
    help="Path to configuration file"
)
def init(config: Path):
    """Initialize configuration."""
    if config.exists():
        raise click.ClickException("Configuration file already exists")
    
    config_manager = ConfigManager()
    default_config = Config(
        model="gpt-4o-mini",
        environment="development",
        log_level="INFO"
    )
    config_manager.save(default_config, config)
    click.echo("Configuration initialized")

@main.command()
@click.option(
    "--config",
    type=click.Path(path_type=Path),
    required=True,
    help="Path to configuration file"
)
@click.option("--source", required=True, help="Natural language prompt to translate")
@click.option(
    "--target-framework",
    required=True,
    help="Target framework for translation (use 'synthlang' for SynthLang format)"
)
def translate(config: Path, source: str, target_framework: str):
    """Translate natural language prompts to SynthLang format.
    
    Example:
        synthlang translate --config config.json \\
            --source "analyze customer feedback and generate summary" \\
            --target-framework synthlang
    """
    if target_framework.lower() != "synthlang":
        raise click.ClickException(
            "Only 'synthlang' is supported as target framework"
        )
    
    config_data = load_config(config)
    api_key = get_api_key()
    
    translator = FrameworkTranslator(
        api_key=api_key,
        model=config_data.model
    )
    try:
        result = translator.translate(source)
        click.echo("Translation complete")
        click.echo("\nSource prompt:")
        click.echo(result["source"])
        click.echo("\nTranslated prompt:")
        click.echo(result["target"])
        click.echo("\nExplanation:")
        click.echo(result["explanation"])
    except Exception as e:
        raise click.ClickException(f"Translation failed: {str(e)}")

@main.command()
@click.option(
    "--config",
    type=click.Path(path_type=Path),
    required=True,
    help="Path to configuration file"
)
@click.option("--task", required=True, help="Task description")
def generate(config: Path, task: str):
    """Generate system prompts."""
    config_data = load_config(config)
    api_key = get_api_key()
    
    generator = SystemPromptGenerator(
        api_key=api_key,
        model=config_data.model
    )
    try:
        result = generator.generate(task)
        click.echo("System prompt generated")
        click.echo("\nPrompt:")
        click.echo(result["prompt"])
        click.echo("\nRationale:")
        click.echo(result["rationale"])
        click.echo("\nMetadata:")
        click.echo(json.dumps(result["metadata"], indent=2))
    except Exception as e:
        raise click.ClickException(f"Generation failed: {str(e)}")

@main.command()
@click.option(
    "--config",
    type=click.Path(path_type=Path),
    required=True,
    help="Path to configuration file"
)
@click.option("--prompt", required=True, help="Prompt to optimize")
def optimize(config: Path, prompt: str):
    """Optimize prompts using DSPy."""
    config_data = load_config(config)
    
    # TODO: Implement prompt optimization
    click.echo("Prompt optimized")
    click.echo("(Optimization functionality coming soon)")

@main.group()
def config():
    """Manage configuration."""
    pass

@config.command()
@click.option(
    "--config",
    type=click.Path(path_type=Path),
    required=True,
    help="Path to configuration file"
)
def show(config: Path):
    """Show current configuration."""
    config_data = load_config(config)
    click.echo("Current configuration:")
    click.echo(json.dumps(config_data.model_dump(), indent=2))

@config.command()
@click.option(
    "--config",
    type=click.Path(path_type=Path),
    required=True,
    help="Path to configuration file"
)
@click.option("--key", required=True, help="Configuration key to update")
@click.option("--value", required=True, help="New value")
def set(config: Path, key: str, value: str):
    """Update configuration value."""
    config_manager = ConfigManager()
    try:
        current_config = load_config(config)
        updated_config = config_manager.update(config, {key: value})
        click.echo("Configuration updated")
        click.echo(f"Set {key} = {value}")
    except Exception as e:
        raise click.ClickException(f"Failed to update configuration: {str(e)}")

if __name__ == "__main__":
    main()
