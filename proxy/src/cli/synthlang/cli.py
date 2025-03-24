"""Command-line interface for SynthLang."""
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

import click
import dspy

from synthlang import __version__
from synthlang.config import Config, ConfigManager
from synthlang.core import (
    FrameworkTranslator, 
    SystemPromptGenerator, 
    PromptOptimizer,
    PromptEvolver,
    PromptManager,
    PromptClassifier
)
from synthlang.cli_proxy import register_proxy_commands


def load_config() -> Config:
    """Load configuration from environment."""
    try:
        config_manager = ConfigManager()
        return config_manager.load()
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
    """SynthLang CLI - Framework translation, prompt engineering, and proxy integration."""
    pass


@main.command()
@click.option("--source", required=True, help="Natural language prompt to translate")
@click.option("--framework", required=True, help="Target framework for translation (use 'synthlang' for SynthLang format)")
@click.option("--show-metrics", is_flag=True, help="Show token and cost metrics")
@click.option("--use-proxy", is_flag=True, help="Use proxy service if available")
def translate(source: str, framework: str, show_metrics: bool, use_proxy: bool):
    """Translate natural language prompts to SynthLang format.
    
    Example:
        synthlang translate \\
            --source "analyze customer feedback and generate summary" \\
            --framework synthlang \\
            --show-metrics
    """
    if framework.lower() != "synthlang":
        raise click.ClickException(
            "Only 'synthlang' is supported as target framework"
        )
    
    # Try to use proxy if requested
    if use_proxy:
        try:
            from synthlang.proxy.api import ProxyClient
            from synthlang.proxy.auth import get_credentials
            
            creds = get_credentials()
            if "api_key" in creds:
                endpoint = creds.get("endpoint", "https://api.synthlang.org")
                client = ProxyClient(endpoint, creds["api_key"])
                
                click.echo("Using proxy service for translation...")
                response = client.translate(source, framework)
                
                click.echo("Translation complete")
                click.echo("\nSource prompt:")
                click.echo(source)
                click.echo("\nTranslated prompt:")
                click.echo(response["target"])
                
                if "explanation" in response:
                    click.echo("\nExplanation:")
                    click.echo(response["explanation"])
                
                return
            else:
                click.echo("No API key found for proxy service. Falling back to local translation.")
        except Exception as e:
            click.echo(f"Error using proxy service: {str(e)}. Falling back to local translation.")
    
    # Local implementation
    config_data = load_config()
    api_key = get_api_key()
    
    # Create language model
    lm = dspy.LM(model=config_data.model, api_key=api_key)
    dspy.configure(lm=lm)

    # Set up translation instructions
    instructions = """SYNTHLANG TRANSLATION FORMAT:

RULES:
1. Use ONLY these symbols: ↹ (input), ⊕ (process), Σ (output)
2. NO quotes, arrows, or descriptions
3. Use • to join related items
4. Use => for transformations
5. Maximum 30 characters per line
6. Use mathematical operators (+, >, <, ^)
7. Break complex tasks into steps

IMPORTANT: Keep translations extremely concise!

GOOD EXAMPLES:
↹ data•source
⊕ condition>5 => action
Σ result + log

↹ input•stream, params
⊕ transform => output
⊕ Σ final^2 + cache

↹ news•feed•google
⊕ sentiment>0 => pos
⊕ sentiment<0 => neg
Σ trend + factors

BAD EXAMPLES (TOO VERBOSE):
↹ data:"source" -> Parse input
⊕ process:"condition" -> Check value

Convert input to concise SynthLang format using minimal symbols."""

    translator = FrameworkTranslator(lm=lm)
    try:
        result = translator.translate(source, instructions)
        
        # Calculate metrics if requested
        if show_metrics:
            # Simple token estimation (can be improved)
            def calculate_tokens(text: str) -> int:
                return len(text.split())
            
            original_tokens = calculate_tokens(source)
            translated_tokens = calculate_tokens(result["target"])
            
            # Estimate cost using standard rate
            cost_per_1k = 0.0025  # $2.50 per million tokens
            original_cost = (original_tokens / 1000) * cost_per_1k
            translated_cost = (translated_tokens / 1000) * cost_per_1k
            savings = max(0, original_cost - translated_cost)
            reduction = ((original_tokens - translated_tokens) / original_tokens * 100)
            
            click.echo("\nMetrics:")
            click.echo(f"Original Tokens: {original_tokens}")
            click.echo(f"Translated Tokens: {translated_tokens}")
            click.echo(f"Cost Savings: ${savings:.4f}")
            click.echo(f"Token Reduction: {reduction:.0f}%")
            click.echo("")
        
        click.echo("Translation complete")
        click.echo("\nSource prompt:")
        click.echo(source)
        click.echo("\nTranslated prompt:")
        click.echo(result["target"])
        click.echo("\nExplanation:")
        click.echo(result["explanation"])
        
    except Exception as e:
        raise click.ClickException(f"Translation failed: {str(e)}")


@main.command()
@click.option("--task", required=True, help="Task description")
def generate(task: str):
    """Generate system prompts."""
    config_data = load_config()
    api_key = get_api_key()
    
    # Create language model
    lm = dspy.LM(model=config_data.model, api_key=api_key)
    dspy.configure(lm=lm)
    
    # Initialize generator with language model
    generator = SystemPromptGenerator(lm=lm)
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
@click.option("--prompt", required=True, help="Prompt to optimize")
@click.option("--use-proxy", is_flag=True, help="Use proxy service if available")
def optimize(prompt: str, use_proxy: bool):
    """Optimize prompts using DSPy techniques."""
    # Try to use proxy if requested
    if use_proxy:
        try:
            from synthlang.proxy.api import ProxyClient
            from synthlang.proxy.auth import get_credentials
            
            creds = get_credentials()
            if "api_key" in creds:
                endpoint = creds.get("endpoint", "https://api.synthlang.org")
                client = ProxyClient(endpoint, creds["api_key"])
                
                click.echo("Using proxy service for optimization...")
                response = client.optimize(prompt)
                
                click.echo("Prompt optimized")
                click.echo("\nOriginal prompt:")
                click.echo(response.get("original", prompt))
                click.echo("\nOptimized prompt:")
                click.echo(response.get("optimized", "No optimization available"))
                
                if "improvements" in response:
                    click.echo("\nImprovements made:")
                    for improvement in response["improvements"]:
                        click.echo(f"- {improvement}")
                
                return
            else:
                click.echo("No API key found for proxy service. Falling back to local optimization.")
        except Exception as e:
            click.echo(f"Error using proxy service: {str(e)}. Falling back to local optimization.")
    
    # Local implementation
    config_data = load_config()
    api_key = get_api_key()
    
    # Create language model
    lm = dspy.LM(model=config_data.model, api_key=api_key)
    dspy.configure(lm=lm)
    
    # Initialize optimizer with language model
    optimizer = PromptOptimizer(lm=lm)
    try:
        result = optimizer.optimize(prompt)
        click.echo("Prompt optimized")
        click.echo("\nOriginal prompt:")
        click.echo(result["original"])
        click.echo("\nOptimized prompt:")
        click.echo(result["optimized"])
        click.echo("\nImprovements made:")
        for improvement in result["improvements"]:
            click.echo(f"- {improvement}")
        click.echo("\nMetrics:")
        click.echo(f"- Clarity: {float(result['metrics']['clarity_score']):.2f}")
        click.echo(f"- Specificity: {float(result['metrics']['specificity_score']):.2f}")
        click.echo(f"- Consistency: {float(result['metrics']['consistency_score']):.2f}")
    except Exception as e:
        raise click.ClickException(f"Optimization failed: {str(e)}")


@main.group()
def prompt():
    """Manage evolved prompts."""
    pass


@prompt.command()
@click.option("--name", required=True, help="Name to save prompt under")
@click.option("--prompt", required=True, help="Prompt content")
@click.option("--metadata", help="Optional JSON metadata")
def save(name: str, prompt: str, metadata: Optional[str] = None):
    """Save a prompt with metadata."""
    try:
        manager = PromptManager()
        meta_dict = json.loads(metadata) if metadata else None
        manager.save(name, prompt, meta_dict)
        click.echo(f"Prompt saved as: {name}")
    except Exception as e:
        raise click.ClickException(f"Failed to save prompt: {str(e)}")


@main.group()
def config():
    """Manage configuration."""
    pass


@config.command()
def show():
    """Show current configuration."""
    try:
        config_data = load_config()
        click.echo("\nCurrent configuration:")
        for key, value in config_data.dict().items():
            # Mask API key
            if key == "openai_api_key" and value:
                value = value[:4] + "..." + value[-4:]
            click.echo(f"{key}: {value}")
    except Exception as e:
        raise click.ClickException(f"Failed to show configuration: {str(e)}")


@config.command()
@click.argument("key")
@click.argument("value")
def set(key: str, value: str):
    """Set a configuration value."""
    try:
        config_manager = ConfigManager()
        config_manager.update({key: value})
        click.echo(f"Updated {key} = {value}")
    except Exception as e:
        raise click.ClickException(f"Failed to update configuration: {str(e)}")


# Register proxy commands
proxy = register_proxy_commands(main)


if __name__ == "__main__":
    main()
