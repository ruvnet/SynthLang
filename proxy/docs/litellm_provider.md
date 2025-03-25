# LiteLLM Provider

The SynthLang proxy includes a modular LiteLLM provider that allows for easy integration with multiple LLM providers and extension of capabilities.

## Overview

The LiteLLM provider is implemented as a class-based module that encapsulates all LiteLLM functionality and provides extension points for adding new capabilities. It maintains backward compatibility with the existing API while allowing for more advanced usage.

## Basic Usage

For basic usage, you can continue to use the existing functions:

```python
from src.app.litellm_provider import complete_chat, stream_chat

# Non-streaming completion
response = await complete_chat(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello"}],
    temperature=0.7
)

# Streaming completion
async for chunk in stream_chat(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello"}],
    temperature=0.7
):
    print(chunk)
```

## Advanced Usage

For more advanced usage, you can access the provider instance directly:

```python
from src.app.litellm_provider import provider

# Add a custom model mapping
provider.add_model_mapping("my-custom-model", "openai/gpt-4o")

# Add a custom model fallback
provider.add_model_fallback("my-custom-model", ["openai/gpt-4o", "openai/gpt-3.5-turbo"])

# Use the provider directly
response = await provider.complete_chat(
    model="my-custom-model",
    messages=[{"role": "user", "content": "Hello"}],
    temperature=0.7
)
```

## Complex JSON Support

The LiteLLM provider supports complex JSON data in message content, which is compatible with the OpenAI API standard. This allows you to send structured data in your messages:

```python
# Example with complex JSON content
response = await provider.complete_chat(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": {
            "main_text": "This is a complex message with nested structure",
            "metadata": {
                "source": "user interface",
                "timestamp": 1677652288,
                "client_info": {"browser": "Chrome", "version": "98.0.4758.102"}
            },
            "attachments": [
                {"title": "Document 1", "content": "Some content here"},
                {"title": "Document 2", "content": "More content here"}
            ]
        }}
    ],
    temperature=0.7
)
```

The provider automatically handles the conversion of complex JSON data to string format for internal processing, ensuring compatibility with the LLM provider.

## Extension Points

The LiteLLM provider includes several extension points for customizing behavior:

### Pre-processing Hooks

Pre-processing hooks are called before each request and can modify the request parameters:

```python
def add_system_message(params):
    """Add a system message to the beginning of the messages list."""
    messages = params.get("messages", [])
    
    # Check if there's already a system message
    has_system = any(msg.get("role") == "system" for msg in messages)
    
    if not has_system:
        messages.insert(0, {
            "role": "system",
            "content": "You are a helpful assistant that provides concise responses."
        })
        params["messages"] = messages
    
    return params

provider.add_pre_process_hook(add_system_message)
```

### Post-processing Hooks

Post-processing hooks are called after each response and can modify the response:

```python
def add_metadata(response):
    """Add metadata to the response."""
    response["metadata"] = {
        "enhanced_by": "SynthLang",
        "version": "1.0.0"
    }
    return response

provider.add_post_process_hook(add_metadata)
```

### Custom Capabilities

You can register custom capabilities with the provider:

```python
class CachedEmbedding:
    """A simple embedding service with caching."""
    
    def __init__(self):
        self.cache = {}
    
    async def get_embedding(self, text, model="text-embedding-ada-002"):
        """Get an embedding for the given text, with caching."""
        if text in self.cache:
            return self.cache[text]
        
        # In a real implementation, this would call litellm.embedding()
        embedding = [0.1, 0.2, 0.3, 0.4, 0.5]
        self.cache[text] = embedding
        return embedding

# Register the new capability
provider.register_capability("cached_embedding", CachedEmbedding())

# Use the new capability
embedding = await provider.cached_embedding.get_embedding("This is a test")
```

## Configuration

The LiteLLM provider can be configured through environment variables:

- `LITELLM_TIMEOUT`: The timeout for LiteLLM requests (default: 30 seconds)
- `LITELLM_MAX_RETRIES`: The maximum number of retries for LiteLLM requests (default: 3)
- `OPENAI_API_KEY`: The API key for OpenAI
- `ANTHROPIC_API_KEY`: The API key for Anthropic

## Model Mapping

The provider includes a default model mapping that maps internal model names to provider-specific model names:

```python
{
    "gpt-4o-mini": "openai/gpt-4o-mini",
    "gpt-4o": "openai/gpt-4o",
    "gpt-4": "openai/gpt-4-turbo",
    "gpt-3.5-turbo": "openai/gpt-3.5-turbo",
    "claude-3-opus": "anthropic/claude-3-opus",
    "claude-3-sonnet": "anthropic/claude-3-sonnet",
    "claude-3-haiku": "anthropic/claude-3-haiku"
}
```

You can add custom model mappings using the `add_model_mapping` method.

## Model Fallbacks

The provider includes a default model fallback configuration:

```python
{
    "gpt-4o-mini": ["openai/gpt-4o-mini", "openai/gpt-3.5-turbo"]
}
```

You can add custom model fallbacks using the `add_model_fallback` method.

## Error Handling

The provider includes error handling and logging for LiteLLM errors. It also includes a patch for a known issue with LiteLLM and Python 3.12 related to the `__annotations__` attribute.

## Examples

See the `proxy/examples/litellm_extensions.py` file for examples of using the modular LiteLLM provider.