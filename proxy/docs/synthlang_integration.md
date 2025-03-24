# SynthLang Integration

This document describes the integration of SynthLang core functionality into the proxy service.

## Overview

SynthLang is a powerful prompt engineering framework that provides advanced capabilities for working with LLM prompts. The integration brings these capabilities directly into the proxy service, allowing for more sophisticated prompt manipulation, optimization, and management.

The integration is designed to:

1. Use the existing SynthLang core modules from the CLI
2. Provide a clean API interface for the core functionality
3. Expose the functionality through FastAPI endpoints
4. Maintain backward compatibility with the existing compression/decompression functionality

## Architecture

The SynthLang integration follows a modular architecture:

```
proxy/src/app/synthlang/
  ├── __init__.py           # Exports main functionality
  ├── compression.py        # Original compression/decompression functionality
  ├── api.py                # API interface for SynthLang core
  ├── endpoints.py          # FastAPI endpoints
  ├── models.py             # Pydantic models for API
  ├── utils.py              # Utility functions
  └── core/                 # Core modules from CLI
      └── __init__.py       # Imports core modules from CLI
```

## Features

The SynthLang integration provides the following features:

### 1. Prompt Compression and Decompression

The original functionality for compressing and decompressing prompts using the SynthLang CLI is maintained and enhanced.

```python
from app.synthlang.api import synthlang_api

# Compress a prompt
compressed = synthlang_api.compress("This is a prompt to compress")

# Decompress a prompt
decompressed = synthlang_api.decompress(compressed)
```

### 2. Prompt Translation

Translate natural language prompts to SynthLang format.

```python
from app.synthlang.api import synthlang_api

# Translate a prompt
result = synthlang_api.translate("Create a chatbot that helps users with programming questions")
# Result: {"source": "...", "target": "↹ chatbot•programming ⊕ help•users => response", "explanation": "..."}
```

### 3. System Prompt Generation

Generate system prompts from task descriptions.

```python
from app.synthlang.api import synthlang_api

# Generate a system prompt
result = synthlang_api.generate("Create a system prompt for a chatbot that helps with programming")
# Result: {"prompt": "...", "rationale": "...", "metadata": {...}}
```

### 4. Prompt Optimization

Optimize prompts using DSPy techniques.

```python
from app.synthlang.api import synthlang_api

# Optimize a prompt
result = synthlang_api.optimize("This is a prompt to optimize")
# Result: {"optimized": "...", "improvements": [...], "metrics": {...}, "original": "..."}
```

### 5. Prompt Evolution

Evolve prompts using genetic algorithms.

```python
from app.synthlang.api import synthlang_api

# Evolve a prompt
result = synthlang_api.evolve("This is a seed prompt", n_generations=10)
# Result: {"best_prompt": "...", "fitness": {...}, "generations": 10, ...}
```

### 6. Prompt Classification

Classify prompts using DSPy.

```python
from app.synthlang.api import synthlang_api

# Classify a prompt
result = synthlang_api.classify("This is a prompt to classify", labels=["category1", "category2"])
# Result: {"input": "...", "label": "category1", "explanation": "..."}
```

### 7. Prompt Management

Manage prompts (save, load, list, delete, compare).

```python
from app.synthlang.api import synthlang_api

# Save a prompt
synthlang_api.save_prompt("my-prompt", "This is a prompt to save", {"key": "value"})

# Load a prompt
result = synthlang_api.load_prompt("my-prompt")
# Result: {"name": "my-prompt", "prompt": "...", "metadata": {...}}

# List prompts
prompts = synthlang_api.list_prompts()
# Result: [{"name": "prompt1", ...}, {"name": "prompt2", ...}, ...]

# Delete a prompt
success = synthlang_api.delete_prompt("my-prompt")
# Result: True

# Compare prompts
result = synthlang_api.compare_prompts("prompt1", "prompt2")
# Result: {"prompts": {...}, "metrics": {...}, "differences": {...}}
```

## API Endpoints

The SynthLang integration exposes the following API endpoints:

### Translation

```
POST /v1/synthlang/translate
{
  "text": "Create a chatbot that helps users with programming questions",
  "instructions": null
}
```

### Generation

```
POST /v1/synthlang/generate
{
  "task_description": "Create a system prompt for a chatbot that helps with programming"
}
```

### Optimization

```
POST /v1/synthlang/optimize
{
  "prompt": "This is a prompt to optimize",
  "max_iterations": 5
}
```

### Evolution

```
POST /v1/synthlang/evolve
{
  "seed_prompt": "This is a seed prompt",
  "n_generations": 10
}
```

### Classification

```
POST /v1/synthlang/classify
{
  "text": "This is a prompt to classify",
  "labels": ["category1", "category2"]
}
```

### Prompt Management

```
POST /v1/synthlang/prompts/save
{
  "name": "my-prompt",
  "prompt": "This is a prompt to save",
  "metadata": {"key": "value"}
}

POST /v1/synthlang/prompts/load
{
  "name": "my-prompt"
}

GET /v1/synthlang/prompts/list

POST /v1/synthlang/prompts/delete
{
  "name": "my-prompt"
}

POST /v1/synthlang/prompts/compare
{
  "name1": "prompt1",
  "name2": "prompt2"
}
```

## Configuration

The SynthLang integration can be configured using environment variables:

- `SYNTHLANG_FEATURES_ENABLED`: Enable/disable SynthLang features (default: `true`)
- `SYNTHLANG_DEFAULT_MODEL`: Default model to use for SynthLang operations (default: `gpt-4o-mini`)
- `SYNTHLANG_STORAGE_DIR`: Directory for storing prompts (default: `/tmp/synthlang`)
- `OPENAI_API_KEY`: API key for OpenAI (required for DSPy operations)

## Usage Examples

### Translating a Prompt

```python
import requests

response = requests.post(
    "http://localhost:8000/v1/synthlang/translate",
    json={
        "text": "Create a chatbot that helps users with programming questions"
    },
    headers={"Authorization": "Bearer your-api-key"}
)

result = response.json()
print(result["target"])  # SynthLang format
```

### Optimizing a Prompt

```python
import requests

response = requests.post(
    "http://localhost:8000/v1/synthlang/optimize",
    json={
        "prompt": "This is a prompt to optimize",
        "max_iterations": 5
    },
    headers={"Authorization": "Bearer your-api-key"}
)

result = response.json()
print(result["optimized"])  # Optimized prompt
print(result["improvements"])  # List of improvements
```

### Evolving a Prompt

```python
import requests

response = requests.post(
    "http://localhost:8000/v1/synthlang/evolve",
    json={
        "seed_prompt": "This is a seed prompt",
        "n_generations": 10
    },
    headers={"Authorization": "Bearer your-api-key"}
)

result = response.json()
print(result["best_prompt"])  # Best evolved prompt
print(result["fitness"])  # Fitness scores
```

## Testing

The SynthLang integration includes comprehensive tests:

```bash
# Run all tests
pytest proxy/tests/test_synthlang_integration.py

# Run specific test
pytest proxy/tests/test_synthlang_integration.py::test_synthlang_api_initialization
```

## Troubleshooting

### SynthLang API is disabled

If you receive an error that the SynthLang API is disabled, check the `SYNTHLANG_FEATURES_ENABLED` environment variable.

### Failed to initialize language model

If you receive an error that the language model failed to initialize:

1. Check that the `OPENAI_API_KEY` environment variable is set
2. Check that DSPy is installed (`pip install dspy-ai`)
3. Check the logs for more detailed error messages

### No prompt found with name

If you receive an error that no prompt was found with a given name:

1. Check that the prompt exists using the `/v1/synthlang/prompts/list` endpoint
2. Check that the `SYNTHLANG_STORAGE_DIR` environment variable is set correctly
3. Check that the directory exists and is writable

## Future Enhancements

1. Add support for more language models (Claude, Llama, etc.)
2. Add support for fine-tuning SynthLang models
3. Add a web UI for SynthLang functionality
4. Add support for prompt templates and variables
5. Add support for prompt versioning and history