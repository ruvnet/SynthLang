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
from synthlang.core import (
    FrameworkTranslator, 
    SystemPromptGenerator, 
    PromptOptimizer,
    PromptEvolver,
    PromptManager,
    PromptClassifier
)

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
@click.option("--seed", required=True, help="Initial prompt to evolve")
@click.option("--generations", default=10, help="Number of evolutionary generations")
@click.option("--population", default=5, help="Population size per generation")
@click.option("--mutation-rate", default=0.3, help="Rate of mutation between generations (0-1)")
@click.option("--tournament-size", default=3, help="Number of prompts competing in each tournament")
@click.option("--fitness", type=click.Choice(['clarity', 'specificity', 'task', 'hybrid']), default='hybrid', 
              help="Fitness function for evolution (clarity, specificity, task completion, or hybrid)")
@click.option("--save-lineage", is_flag=True, help="Save the evolutionary history of prompts")
@click.option("--test-cases", type=click.Path(exists=True), help="JSON file with test cases for task-based fitness")
@click.option("--save-prompt", help="Save the best prompt under this name")
def evolve(seed: str, generations: int, population: int, mutation_rate: float, 
           tournament_size: int, fitness: str, save_lineage: bool, test_cases: Optional[str],
           save_prompt: Optional[str]):
    """Evolve prompts using genetic algorithms and self-play tournaments.
    
    Example:
        synthlang evolve \\
            --seed "analyze data and generate insights" \\
            --generations 20 \\
            --population 8 \\
            --mutation-rate 0.4 \\
            --tournament-size 4 \\
            --fitness hybrid \\
            --save-lineage
    """
    config_data = load_config()
    api_key = get_api_key()
    
    # Create language model
    lm = dspy.LM(model=config_data.model, api_key=api_key)
    dspy.configure(lm=lm)
    
    # Load test cases if provided
    test_suite = None
    if test_cases:
        with open(test_cases) as f:
            data = json.load(f)
            test_suite = data.get('test_cases', [])
    
    # Initialize evolutionary optimizer
    optimizer = PromptEvolver(
        lm=lm,
        population_size=population,
        mutation_rate=mutation_rate,
        tournament_size=tournament_size,
        fitness_type=fitness,
        test_cases=test_suite
    )
    
    try:
        # Run evolution
        click.echo(f"\nStarting prompt evolution:")
        click.echo(f"- Initial prompt: {seed}")
        click.echo(f"- Generations: {generations}")
        click.echo(f"- Population: {population}")
        click.echo(f"- Mutation rate: {mutation_rate}")
        click.echo(f"- Tournament size: {tournament_size}")
        click.echo(f"- Fitness function: {fitness}")
        
        result = optimizer.evolve(
            seed_prompt=seed,
            n_generations=generations
        )
        
        # Display results
        click.echo("\nEvolution complete!")
        click.echo("\nBest prompt:")
        click.echo(result["best_prompt"])
        click.echo("\nFitness scores:")
        click.echo(f"- Clarity: {float(result['fitness']['clarity']):.2f}")
        click.echo(f"- Specificity: {float(result['fitness']['specificity']):.2f}")
        click.echo(f"- Task completion: {float(result['fitness']['task_score']):.2f}")
        click.echo(f"- Overall fitness: {float(result['fitness']['overall']):.2f}")
        
        click.echo("\nEvolution metrics:")
        click.echo(f"- Generations completed: {result['generations']}")
        click.echo(f"- Total variants created: {result['total_variants']}")
        click.echo(f"- Successful mutations: {result['successful_mutations']}")
        click.echo(f"- Tournament winners: {result['tournament_winners']}")
        
        # Save evolutionary history if requested
        if save_lineage:
            lineage_file = f"prompt_evolution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(lineage_file, 'w') as f:
                json.dump(result['lineage'], f, indent=2)
            click.echo(f"\nEvolutionary history saved to: {lineage_file}")
            
        # Save best prompt if requested
        if save_prompt:
            manager = PromptManager()
            manager.save(
                save_prompt,
                result["best_prompt"],
                {
                    'fitness': result['fitness'],
                    'generations': generations,
                    'evolution_metrics': {
                        'total_variants': result['total_variants'],
                        'successful_mutations': result['successful_mutations'],
                        'tournament_winners': result['tournament_winners']
                    }
                }
            )
            click.echo(f"\nBest prompt saved as: {save_prompt}")
            
    except Exception as e:
        raise click.ClickException(f"Evolution failed: {str(e)}")

@main.command()
@click.option("--prompt", required=True, help="Prompt to optimize")
def optimize(prompt: str):
    """Optimize prompts using DSPy techniques."""
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

@prompt.command()
@click.option("--name", required=True, help="Name of prompt to load")
def load(name: str):
    """Load a saved prompt."""
    try:
        manager = PromptManager()
        data = manager.load(name)
        click.echo("\nPrompt details:")
        click.echo(f"Name: {data['name']}")
        click.echo("\nContent:")
        click.echo(data['prompt'])
        click.echo("\nMetadata:")
        click.echo(json.dumps(data['metadata'], indent=2))
    except Exception as e:
        raise click.ClickException(f"Failed to load prompt: {str(e)}")

@prompt.command()
def list():
    """List all saved prompts."""
    try:
        manager = PromptManager()
        prompts = manager.list()
        if not prompts:
            click.echo("No saved prompts found")
            return
            
        click.echo("\nSaved prompts:")
        for p in prompts:
            click.echo(f"\nName: {p['name']}")
            click.echo(f"Created: {p['metadata'].get('created', 'unknown')}")
            if 'fitness' in p['metadata']:
                click.echo(f"Fitness: {p['metadata']['fitness']:.2f}")
    except Exception as e:
        raise click.ClickException(f"Failed to list prompts: {str(e)}")

@prompt.command()
@click.option("--name", required=True, help="Name of prompt to delete")
def delete(name: str):
    """Delete a saved prompt."""
    try:
        manager = PromptManager()
        manager.delete(name)
        click.echo(f"Deleted prompt: {name}")
    except Exception as e:
        raise click.ClickException(f"Failed to delete prompt: {str(e)}")

@prompt.command()
@click.option("--prompt1", required=True, help="First prompt name")
@click.option("--prompt2", required=True, help="Second prompt name")
def compare(prompt1: str, prompt2: str):
    """Compare two saved prompts."""
    try:
        manager = PromptManager()
        result = manager.compare(prompt1, prompt2)
        
        click.echo("\nPrompt Comparison:")
        click.echo(f"\n{prompt1}:")
        click.echo(result['prompts'][prompt1])
        click.echo(f"\n{prompt2}:")
        click.echo(result['prompts'][prompt2])
        
        click.echo("\nMetrics:")
        for name in [prompt1, prompt2]:
            metrics = result['metrics'][name]
            fitness = metrics['fitness']
            click.echo(f"\n{name}:")
            click.echo("- Fitness scores:")
            click.echo(f"  Clarity: {float(fitness['clarity']):.2f}")
            click.echo(f"  Specificity: {float(fitness['specificity']):.2f}")
            click.echo(f"  Task completion: {float(fitness['task_score']):.2f}")
            click.echo(f"  Overall: {float(fitness['overall']):.2f}")
            click.echo(f"- Generations: {metrics['generations']}")
            click.echo(f"- Created: {metrics['created']}")
            if 'evolution_metrics' in metrics:
                evo = metrics['evolution_metrics']
                click.echo("- Evolution metrics:")
                click.echo(f"  Total variants: {evo.get('total_variants', 0)}")
                click.echo(f"  Successful mutations: {evo.get('successful_mutations', 0)}")
                click.echo(f"  Tournament winners: {evo.get('tournament_winners', 0)}")
            
        click.echo("\nDifferences:")
        diffs = result['differences']
        click.echo(f"- Overall fitness delta: {diffs['fitness']:.2f}")
        click.echo(f"- Generation delta: {diffs['generations']}")
    except Exception as e:
        raise click.ClickException(f"Failed to compare prompts: {str(e)}")

@main.group()
def classify():
    """Classify and finetune prompts."""
    pass

@classify.command()
@click.option("--text", required=True, help="Text to classify")
@click.option("--labels", required=True, help="Comma-separated list of possible labels")
@click.option("--model", type=click.Path(exists=True), help="Path to saved classifier model")
def predict(text: str, labels: str, model: Optional[str] = None):
    """Classify a piece of text."""
    config_data = load_config()
    api_key = get_api_key()
    
    # Create language model
    lm = dspy.LM(model=config_data.model, api_key=api_key)
    dspy.configure(lm=lm)
    
    # Initialize classifier
    label_list = [l.strip() for l in labels.split(",")]
    classifier = PromptClassifier(lm=lm, labels=label_list)
    
    # Load saved model if provided
    if model:
        classifier.load(model)
        
    try:
        result = classifier.classify(text)
        click.echo("\nClassification result:")
        click.echo(f"Input: {result['input']}")
        click.echo(f"Label: {result['label']}")
        click.echo(f"Explanation: {result['explanation']}")
    except Exception as e:
        raise click.ClickException(f"Classification failed: {str(e)}")

@classify.command()
@click.option("--train-data", required=True, type=click.Path(exists=True), help="JSON file with training data")
@click.option("--labels", required=True, help="Comma-separated list of possible labels")
@click.option("--save-model", help="Path to save trained model")
def train(train_data: str, labels: str, save_model: Optional[str] = None):
    """Train a classifier on examples."""
    config_data = load_config()
    api_key = get_api_key()
    
    # Create language model
    lm = dspy.LM(model=config_data.model, api_key=api_key)
    dspy.configure(lm=lm)
    
    # Load training data
    with open(train_data) as f:
        data = json.load(f)
        examples = data.get("examples", [])
        
    # Initialize classifier
    label_list = [l.strip() for l in labels.split(",")]
    classifier = PromptClassifier(lm=lm, labels=label_list)
    
    try:
        # Train classifier
        result = classifier.train(examples)
        
        click.echo("\nTraining complete!")
        click.echo(f"Examples used: {result['examples_used']}")
        click.echo(f"Final accuracy: {result['final_accuracy']:.2f}")
        
        # Save model if requested
        if save_model:
            classifier.save(save_model)
            click.echo(f"\nModel saved to: {save_model}")
    except Exception as e:
        raise click.ClickException(f"Training failed: {str(e)}")

@classify.command()
@click.option("--test-data", required=True, type=click.Path(exists=True), help="JSON file with test data")
@click.option("--model", required=True, type=click.Path(exists=True), help="Path to saved classifier model")
def evaluate(test_data: str, model: str):
    """Evaluate a trained classifier."""
    config_data = load_config()
    api_key = get_api_key()
    
    # Create language model
    lm = dspy.LM(model=config_data.model, api_key=api_key)
    dspy.configure(lm=lm)
    
    # Load test data
    with open(test_data) as f:
        data = json.load(f)
        examples = data.get("examples", [])
        
    # Load classifier
    classifier = PromptClassifier(lm=lm, labels=[])  # Labels will be loaded from model
    classifier.load(model)
    
    try:
        # Run evaluation
        result = classifier.evaluate(examples)
        
        click.echo("\nEvaluation complete!")
        click.echo(f"Test examples: {result['examples']}")
        click.echo(f"Accuracy: {result['accuracy']:.2f}")
    except Exception as e:
        raise click.ClickException(f"Evaluation failed: {str(e)}")

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
