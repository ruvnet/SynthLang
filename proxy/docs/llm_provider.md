# LLM Provider Module

The LLM Provider module provides a modular and extensible interface for interacting with various Large Language Model (LLM) providers, such as OpenAI.

## Architecture

The module is designed with a clean, modular architecture:

```
src/app/llm_providers/
├── __init__.py           # Main entry point and API
├── base.py               # Abstract base class for providers
├── exceptions.py         # Custom exceptions
├── factory.py            # Factory for creating provider instances
└── providers/            # Provider implementations
    ├── __init__.py
    └── openai_provider.py  # OpenAI implementation
```

The main `llm_provider.py` file in `src/app/` serves as a compatibility layer that re-exports the functions from the `llm_providers` package to maintain backward compatibility with existing code.

## Usage

### Basic Usage

```python
from src.app import llm_provider

# Get a chat completion
response = await llm_provider.complete_chat(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how are you?"}
    ],
    temperature=0.7
)

# Get a streaming chat completion
async for chunk in await llm_provider.stream_chat(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how are you?"}
    ],
    temperature=0.7
):
    print(chunk)

# Get embeddings for text
embedding = llm_provider.get_embedding("Hello, world!")

# Get embeddings for multiple texts
embeddings = await llm_provider.get_embeddings(["Hello, world!", "How are you?"])

# List available models
models = await llm_provider.list_models()
```

### Error Handling

The module provides custom exceptions for different types of errors:

```python
from src.app import llm_provider

try:
    response = await llm_provider.complete_chat(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello"}]
    )
except llm_provider.LLMAuthenticationError:
    # Handle authentication errors
    print("Authentication failed. Check your API key.")
except llm_provider.LLMRateLimitError:
    # Handle rate limit errors
    print("Rate limit exceeded. Try again later.")
except llm_provider.LLMConnectionError:
    # Handle connection errors
    print("Connection error. Check your internet connection.")
except llm_provider.LLMTimeoutError:
    # Handle timeout errors
    print("Request timed out. Try again later.")
except llm_provider.LLMProviderError as e:
    # Handle other provider errors
    print(f"LLM provider error: {e}")
```

## Extending with New Providers

To add a new LLM provider:

1. Create a new file in the `providers` directory (e.g., `anthropic_provider.py`)
2. Implement the `BaseLLMProvider` interface
3. Register the provider in the factory

Example:

```python
# providers/anthropic_provider.py
from ..base import BaseLLMProvider

class AnthropicProvider(BaseLLMProvider):
    # Implement all required methods
    ...

# In __init__.py
from .providers.anthropic_provider import AnthropicProvider
LLMProviderFactory.register_provider("anthropic", AnthropicProvider)
```

## Configuration

The module uses environment variables for configuration:

- `OPENAI_API_KEY`: API key for OpenAI
- Other provider-specific environment variables

## Error Handling

The module provides custom exceptions for different types of errors:

- `LLMProviderError`: Base exception for all LLM provider errors
- `LLMAuthenticationError`: Authentication errors
- `LLMRateLimitError`: Rate limit errors
- `LLMConnectionError`: Connection errors
- `LLMTimeoutError`: Timeout errors
- `LLMModelNotFoundError`: Model not found errors
- `LLMInvalidRequestError`: Invalid request errors