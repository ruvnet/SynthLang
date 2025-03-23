# SynthLang CLI Documentation

The SynthLang CLI provides a powerful command-line interface for interacting with the SynthLang Proxy and performing various prompt engineering tasks. This document covers the installation, configuration, and usage of the CLI tool.

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Install from PyPI

```bash
pip install synthlang
```

### Install from Source

```bash
git clone https://github.com/yourusername/synthlang-proxy.git
cd synthlang-proxy/proxy/src/cli
pip install -e .
```

## Configuration

The CLI can be configured using environment variables, configuration files, or command-line arguments.

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key
- `SYNTHLANG_PROXY_URL`: URL of the SynthLang Proxy service
- `SYNTHLANG_API_KEY`: API key for the SynthLang Proxy service

### Configuration File

Create a `.env` file in your working directory or home directory:

```
OPENAI_API_KEY=your_openai_api_key
SYNTHLANG_PROXY_URL=http://localhost:8000
SYNTHLANG_API_KEY=your_synthlang_api_key
```

## Core Commands

### Translate

Convert natural language to SynthLang format or translate between programming frameworks.

```bash
synthlang translate --source "Create a function to calculate Fibonacci numbers" --framework synthlang
```

Options:
- `--source`, `-s`: Source text to translate
- `--framework`, `-f`: Target framework (synthlang, python, javascript, etc.)
- `--use-proxy`: Use the SynthLang Proxy service for translation
- `--output`, `-o`: Output file (default: stdout)

### Evolve

Improve prompts using genetic algorithms and evolutionary techniques.

```bash
synthlang evolve --seed "Error handling pattern" --generations 5 --population 6
```

Options:
- `--seed`, `-s`: Seed prompt to evolve
- `--generations`, `-g`: Number of generations to evolve (default: 3)
- `--population`, `-p`: Population size per generation (default: 4)
- `--mutation-rate`, `-m`: Mutation rate (default: 0.1)
- `--output`, `-o`: Output file for evolved prompt (default: stdout)

### Optimize

Optimize prompts for efficiency, clarity, and effectiveness.

```bash
synthlang optimize --prompt "Optimize database queries for high throughput"
```

Options:
- `--prompt`, `-p`: Prompt to optimize
- `--iterations`, `-i`: Number of optimization iterations (default: 3)
- `--metric`, `-m`: Optimization metric (tokens, clarity, specificity)
- `--use-proxy`: Use the SynthLang Proxy service for optimization
- `--output`, `-o`: Output file for optimized prompt (default: stdout)

### Classify

Analyze and categorize prompts based on their content and structure.

```bash
synthlang classify predict --text "Create a function to calculate prime numbers" --labels "code,math,algorithm"
```

Subcommands:
- `predict`: Predict the category of a prompt
- `analyze`: Analyze the structure and components of a prompt

Options:
- `--text`, `-t`: Text to classify
- `--labels`, `-l`: Comma-separated list of possible labels
- `--model`, `-m`: Model to use for classification (default: gpt-4o-mini)

## Proxy Commands

### Proxy Serve

Start a local proxy server that provides SynthLang functionality.

```bash
synthlang proxy serve --port 8000 --host 0.0.0.0
```

Options:
- `--port`, `-p`: Port to listen on (default: 8000)
- `--host`, `-h`: Host to bind to (default: 127.0.0.1)
- `--config`, `-c`: Path to configuration file
- `--log-level`, `-l`: Logging level (debug, info, warning, error)

### Proxy Login

Save credentials for the SynthLang Proxy service.

```bash
synthlang proxy login --api-key "your-api-key" --url "http://localhost:8000"
```

Options:
- `--api-key`, `-k`: API key for authentication
- `--url`, `-u`: URL of the proxy service (default: http://localhost:8000)

### Proxy Logout

Remove saved credentials for the SynthLang Proxy service.

```bash
synthlang proxy logout
```

### Proxy Chat

Send a chat request to the proxy service.

```bash
synthlang proxy chat "What is the capital of France?"
```

Options:
- `--model`, `-m`: Model to use (default: gpt-4o-mini)
- `--system`, `-s`: System message
- `--temperature`, `-t`: Temperature for response generation (default: 0.7)
- `--stream`: Enable streaming response
- `--max-tokens`: Maximum tokens in the response

### Proxy Compress

Compress a prompt using SynthLang compression techniques.

```bash
synthlang proxy compress "This is a long prompt that will be compressed using SynthLang compression techniques"
```

Options:
- `--use-gzip`, `-g`: Apply additional gzip compression
- `--input-file`, `-i`: Input file containing the prompt
- `--output-file`, `-o`: Output file for compressed prompt

### Proxy Decompress

Decompress a SynthLang-compressed prompt.

```bash
synthlang proxy decompress "↹ prompt•compressed"
```

Options:
- `--input-file`, `-i`: Input file containing the compressed prompt
- `--output-file`, `-o`: Output file for decompressed prompt

### Proxy Clear Cache

Clear the semantic cache on the proxy server.

```bash
synthlang proxy clear-cache
```

### Proxy Cache Stats

Show statistics about the semantic cache.

```bash
synthlang proxy cache-stats
```

### Proxy Tools

List available agent tools on the proxy server.

```bash
synthlang proxy tools
```

Options:
- `--verbose`, `-v`: Show detailed information about each tool

### Proxy Call Tool

Call an agent tool directly.

```bash
synthlang proxy call-tool --tool "calculate" --args '{"expression": "2+2"}'
```

Options:
- `--tool`, `-t`: Name of the tool to call
- `--args`, `-a`: JSON string of arguments for the tool
- `--input`, `-i`: Input file containing tool arguments (JSON)

### Proxy Health

Check the health of the proxy service.

```bash
synthlang proxy health
```

## Keyword Management

The CLI includes a tool for managing keyword detection configurations. This allows you to define patterns that trigger specific tools when detected in user messages.

### List Patterns

List all patterns in the configuration.

```bash
python keywords.py list
```

### Show Pattern

Show details for a specific pattern.

```bash
python keywords.py show weather_query
```

### Add Pattern

Add a new pattern to the configuration.

```bash
python keywords.py add weather_query \
  --pattern "(?:what's|what is|how's|how is)\\s+(?:the)?\\s*(?:weather|temperature)\\s+(?:like)?\\s*(?:in|at|near)?\\s+(?P<location>[\\w\\s]+)" \
  --tool "weather" \
  --description "Detects weather queries" \
  --priority 100
```

Options:
- `--pattern`, `-p`: Regex pattern with named capture groups
- `--tool`, `-t`: Tool to invoke when pattern matches
- `--description`, `-d`: Description of the pattern
- `--priority`, `-r`: Priority (higher numbers are checked first)
- `--required-role`, `-o`: Role required to use this pattern
- `--disabled`: Disable the pattern

### Edit Pattern

Edit an existing pattern in the configuration.

```bash
python keywords.py edit weather_query --priority 90 --enable
```

Options:
- `--pattern`, `-p`: New regex pattern
- `--tool`, `-t`: New tool to invoke
- `--description`, `-d`: New description
- `--priority`, `-r`: New priority
- `--required-role`, `-o`: New required role
- `--enable`: Enable the pattern
- `--disable`: Disable the pattern

### Delete Pattern

Delete a pattern from the configuration.

```bash
python keywords.py delete weather_query
```

### Import Configuration

Import patterns from another configuration file.

```bash
python keywords.py import /path/to/other/config.toml --overwrite
```

Options:
- `--overwrite`, `-o`: Overwrite existing patterns

### Export Configuration

Export patterns to another configuration file.

```bash
python keywords.py export /path/to/export/config.toml
```

### Create Default Configuration

Create a default configuration with predefined patterns.

```bash
python keywords.py create-default
```

### Show Settings

Show current keyword detection settings.

```bash
python keywords.py settings
```

### Update Settings

Update keyword detection settings.

```bash
python keywords.py update-settings --enable-detection true --detection-threshold 0.8 --default-role "basic"
```

Options:
- `--enable-detection`, `-e`: Enable or disable keyword detection
- `--detection-threshold`, `-t`: Detection threshold (0.0 to 1.0)
- `--default-role`, `-r`: Default role for users

## Mathematical Frameworks

The SynthLang CLI supports various mathematical frameworks for prompt engineering:

### Set Theory

Component combination and analysis.

Example pattern:
```
↹ components•sets
⊕ combine => union
Σ result + validation
```

### Category Theory

Structure-preserving transformations.

Example pattern:
```
↹ source•target•mapping
⊕ preserve => properties
Σ transformed + verified
```

### Topology

Continuous transformations and boundaries.

Example pattern:
```
↹ system•changes•boundaries
⊕ maintain => continuity
Σ robust + stable
```

### Abstract Algebra

Operation composition and invariants.

Example pattern:
```
↹ operations•elements
⊕ compose => structure
Σ result + properties
```

## Example Scripts

The CLI includes several example scripts to demonstrate its capabilities:

- `basic_translation.sh`: Basic prompt translation examples
- `advanced_translation.sh`: Advanced translation with metrics
- `optimization_examples.sh`: Prompt optimization scenarios
- `evolution_examples.sh`: Prompt evolution with parameters
- `classification_examples.sh`: Pattern classification examples
- `pipeline_example.sh`: Multi-step processing pipeline
- `mathematical_pattern_examples.sh`: Mathematical framework examples
- `agentic_reasoning_pipeline.sh`: Agentic reasoning demonstration

## Performance Metrics

SynthLang provides significant improvements over traditional prompt engineering:

| Metric | Traditional | SynthLang | Improvement |
|--------|-------------|-----------|-------------|
| Token Usage | ~150 tokens/step | ~25 tokens/step | 83% reduction |
| Processing Speed | Baseline | 40% faster | 40% improvement |
| Structure Consistency | Variable | 90% consistent | 90% improvement |
| Pattern Recognition | 70% accuracy | 95% accuracy | 25% improvement |

## Best Practices

### Pattern Design

| Aspect | Recommendation | Example |
|--------|----------------|---------|
| Input | Clear context definition | `↹ domain•constraints•requirements` |
| Process | Step-by-step transformation | `⊕ analyze => result` |
| Output | Explicit deliverables | `Σ solution + validation` |

### Pattern Application

| Phase | Action | Tool |
|-------|--------|------|
| Analysis | Understand requirements | `translate` command |
| Evolution | Improve patterns | `evolve` command |
| Validation | Verify properties | `classify` command |
| Optimization | Enhance efficiency | `optimize` command |
| Integration | Connect to services | `proxy` commands |

## Troubleshooting

### Common Issues

1. **API Key Issues**
   - Ensure your OpenAI API key is set correctly
   - Check that your SynthLang Proxy API key is valid

2. **Connection Problems**
   - Verify the proxy URL is correct
   - Check that the proxy server is running
   - Ensure your network allows connections to the proxy

3. **Permission Errors**
   - Verify you have the required role for the operation
   - Check file permissions if writing to output files

### Logging

Enable debug logging for more detailed information:

```bash
synthlang --log-level debug [command]
```

## Development

### Project Structure

```
cli/
├── docs/                    # Documentation
│   ├── mathematical_patterns.md
│   └── tutorials/          # Detailed tutorials
├── scripts/                # Example scripts
│   ├── basic_translation.sh
│   ├── advanced_translation.sh
│   └── ...
├── examples/               # Example outputs
├── synthlang/              # Main package
│   ├── __init__.py
│   ├── cli.py              # CLI entry point
│   ├── config.py           # Configuration handling
│   └── core/               # Core functionality
└── tests/                  # Test cases
```

### Adding New Commands

To add a new command to the CLI:

1. Create a new module in the appropriate package
2. Implement the command functionality
3. Register the command in the CLI entry point

Example:

```python
import click

@click.command()
@click.argument("input_text")
@click.option("--output", "-o", help="Output file")
def my_command(input_text, output):
    """My custom command description."""
    result = process_input(input_text)
    if output:
        with open(output, "w") as f:
            f.write(result)
    else:
        click.echo(result)

# In cli.py
cli.add_command(my_command)
```

### Testing

Run the test suite:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=synthlang
```

## Version History

- **0.2.0** (2025-03-23)
  - Added proxy integration and advanced features
  - Implemented agent SDK and tool registry
  - Added advanced prompt compression
  - Added semantic caching
  - Improved CLI structure with command groups

- **0.1.0** (2024-01-01)
  - Initial release of SynthLang CLI
  - Core DSPy module implementation
  - Framework translation functionality
  - System prompt generation
  - Configuration management
  - Logging system
  - Command-line interface

## License

MIT License - see [LICENSE](LICENSE) file for details