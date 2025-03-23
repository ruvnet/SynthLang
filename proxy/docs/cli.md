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

### Proxy API Key Management

Manage API keys for the proxy server.

#### List API Keys

List all API keys registered with the proxy server.

```bash
synthlang proxy apikey list
```

#### Create API Key

Create a new API key for the proxy server.

```bash
synthlang proxy apikey create --user-id "test_user" --rate-limit 100 --save-env
```

Options:
- `--user-id`, `-u`: User ID associated with the API key (required)
- `--rate-limit`, `-r`: Rate limit in requests per minute
- `--prefix`, `-p`: API key prefix (default: "sk_")
- `--save-env`, `-s`: Save API key to .env file

#### Delete API Key

Delete an API key from the proxy server.

```bash
synthlang proxy apikey delete "sk_1234567890abcdef"
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
python keywords.py import /path/to/config.toml
```

### Export Configuration

Export patterns to another configuration file.

```bash
python keywords.py export /path/to/config.toml
```

## Examples

### Basic Translation

```bash
synthlang translate --source "Create a function to calculate the factorial of a number" --framework synthlang
```

### Using the Proxy Service

```bash
# Login to the proxy service
synthlang proxy login --api-key "your-api-key"

# Send a chat request
synthlang proxy chat "What is the capital of France?"

# Call a tool
synthlang proxy call-tool --tool "calculate" --args '{"expression": "2+2"}'
```

### Managing API Keys

```bash
# Create a new API key
synthlang proxy apikey create --user-id "test_user" --rate-limit 100 --save-env

# List all API keys
synthlang proxy apikey list

# Delete an API key
synthlang proxy apikey delete "sk_1234567890abcdef"
```

### Working with Compression

```bash
# Compress a prompt
synthlang proxy compress "This is a long prompt that will be compressed"

# Decompress a prompt
synthlang proxy decompress "↹ prompt•compressed"
```

## Troubleshooting

### Common Issues

1. **API Key Not Found**: Make sure you've set your API key using the `login` command or environment variables.
2. **Connection Refused**: Check that the proxy server is running and accessible at the specified URL.
3. **Permission Denied**: Ensure your API key has the necessary permissions for the operation.

### Getting Help

For more information about a specific command, use the `--help` flag:

```bash
synthlang --help
synthlang proxy --help
synthlang proxy apikey --help
```

## Advanced Usage

### Scripting

The CLI can be used in scripts for automation:

```bash
#!/bin/bash
# Example script to process multiple prompts

PROMPTS=("prompt1.txt" "prompt2.txt" "prompt3.txt")

for prompt in "${PROMPTS[@]}"; do
  echo "Processing $prompt..."
  synthlang optimize --prompt "$(cat $prompt)" --output "${prompt%.txt}_optimized.txt"
done
```

### Integration with Other Tools

The CLI can be integrated with other tools in your workflow:

```bash
# Example: Pipe output to jq for JSON processing
synthlang proxy call-tool --tool "weather" --args '{"location": "New York"}' | jq '.temperature'