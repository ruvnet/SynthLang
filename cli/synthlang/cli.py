"""Command-line interface for SynthLang."""
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import click
import dspy

from synthlang import __version__
from synthlang.config import Config, ConfigManager
from synthlang.core import FrameworkTranslator, SystemPromptGenerator, PromptOptimizer

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
    """SynthLang CLI - Framework translation and prompt engineering tool."""
    pass

@main.command()
@click.option("--source", required=True, help="Natural language prompt to translate")
@click.option("--framework", required=True, help="Target framework for translation (use 'synthlang' for SynthLang format)")
@click.option("--show-metrics", is_flag=True, help="Show token and cost metrics")
def translate(source: str, framework: str, show_metrics: bool):
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
    
    config_data = load_config()
    api_key = get_api_key()
    
    # Create language model
    lm = dspy.LM(model=config_data.model, api_key=api_key)

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
def optimize(prompt: str):
    """Optimize prompts using DSPy techniques."""
    config_data = load_config()
    api_key = get_api_key()
    
    # Create language model
    lm = dspy.LM(model=config_data.model, api_key=api_key)
    
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

@main.command()
@click.option("--path", required=True, help="Path to save the program state")
@click.option("--format", type=click.Choice(['json', 'pkl']), default='json', help="Save format (json or pkl)")
def save(path: str, format: str):
    """Save the current program state.
    
    Example:
        synthlang save --path ./my_program.json --format json
        synthlang save --path ./my_program.pkl --format pkl
    """
    try:
        # Get current configuration
        config_data = load_config()
        
        # Create state dictionary
        state = {
            'config': config_data.model_dump(),
            'version': __version__,
            'timestamp': datetime.now().isoformat(),
            'model': config_data.model
        }
        
        # Save state based on format
        if format == 'json':
            with open(path, 'w') as f:
                json.dump(state, f, indent=2)
        else:  # pkl
            import pickle
            with open(path, 'wb') as f:
                pickle.dump(state, f)
                
        click.echo(f"Program state saved to: {path}")
            
    except Exception as e:
        raise click.ClickException(f"Failed to save program state: {str(e)}")

@main.command()
@click.option("--path", required=True, help="Path to load the program state from")
@click.option("--format", type=click.Choice(['json', 'pkl']), default='json', help="Load format (json or pkl)")
def load(path: str, format: str):
    """Load a saved program state.
    
    Example:
        synthlang load --path ./my_program.json --format json
        synthlang load --path ./my_program.pkl --format pkl
    """
    try:
        # Load state based on format
        if format == 'json':
            with open(path, 'r') as f:
                state = json.load(f)
        else:  # pkl
            import pickle
            with open(path, 'rb') as f:
                state = pickle.load(f)
        
        # Update configuration
        config_manager = ConfigManager()
        config_manager.update({
            'model': state['model'],
            'environment': state.get('environment', 'production'),
            'log_level': state.get('log_level', 'INFO')
        })
        
        # Show loaded state
        click.echo(f"Program state loaded from: {path}")
        click.echo("\nLoaded state details:")
        click.echo(f"- Version: {state['version']}")
        click.echo(f"- Model: {state['model']}")
        click.echo(f"- Timestamp: {state['timestamp']}")
            
    except Exception as e:
        raise click.ClickException(f"Failed to load program state: {str(e)}")

@main.group()
def config():
    """Manage configuration."""
    pass

@config.command()
def show():
    """Show current configuration."""
    config_data = load_config()
    click.echo("Current configuration:")
    click.echo(json.dumps(config_data.model_dump(), indent=2))

@config.command()
@click.option("--key", required=True, help="Configuration key to update")
@click.option("--value", required=True, help="New value")
def set(key: str, value: str):
    """Update configuration value."""
    config_manager = ConfigManager()
    try:
        updated_config = config_manager.update({key: value})
        click.echo("Configuration updated")
        click.echo(f"Set {key} = {value}")
    except Exception as e:
        raise click.ClickException(f"Failed to update configuration: {str(e)}")

if __name__ == "__main__":
    main()
