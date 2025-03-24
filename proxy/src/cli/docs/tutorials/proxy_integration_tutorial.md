# SynthLang Proxy Integration Tutorial

This tutorial will guide you through using the SynthLang Proxy capabilities in the CLI.

## Overview

SynthLang Proxy provides several advanced features:

1. **Local Proxy Server**: Run your own proxy server for development and testing
2. **Remote Proxy Connection**: Connect to remote proxy services
3. **Advanced Compression**: Compress prompts for efficiency
4. **Semantic Caching**: Cache responses to avoid redundant API calls
5. **Agent Tools**: Use built-in tools for common tasks

## Prerequisites

- SynthLang CLI installed (`pip install synthlang`)
- Python 3.8 or higher
- API key for remote proxy services (optional)

## Getting Started

### 1. Starting a Local Proxy Server

You can start a local proxy server for development and testing:

```bash
synthlang proxy serve --port 8000
```

This will start a FastAPI server on `http://localhost:8000` that provides all the proxy capabilities.

### 2. Connecting to a Remote Proxy

To use a remote proxy service, you need to save your credentials:

```bash
synthlang proxy login --api-key "your-api-key" --endpoint "https://api.example.com"
```

This saves your credentials securely for future use.

### 3. Using Chat Completion

Once you've set up your credentials, you can use the chat completion feature:

```bash
synthlang proxy chat "What is the capital of France?"
```

You can also specify a model and system message:

```bash
synthlang proxy chat --model "gpt-4o" --system "You are a helpful assistant" "What is the capital of France?"
```

### 4. Compressing Prompts

SynthLang provides advanced prompt compression:

```bash
synthlang proxy compress "This is a long prompt that will be compressed using SynthLang compression techniques"
```

For even more compression, you can use gzip:

```bash
synthlang proxy compress --use-gzip "This is a long prompt that will be compressed using SynthLang compression techniques"
```

To decompress:

```bash
synthlang proxy decompress "↹ compressed•text"
```

### 5. Managing the Cache

SynthLang uses semantic caching to avoid redundant API calls. You can manage the cache:

```bash
# View cache statistics
synthlang proxy cache-stats

# Clear the cache
synthlang proxy clear-cache
```

### 6. Using Agent Tools

SynthLang includes a set of built-in tools that can be used by agents:

```bash
# List available tools
synthlang proxy tools

# Call a tool
synthlang proxy call-tool --tool "calculate" --args '{"expression": "2+2"}'
```

## Advanced Usage

### Using Proxy with Existing Commands

You can use the proxy service with existing commands by adding the `--use-proxy` flag:

```bash
synthlang translate --source "Analyze customer feedback" --framework synthlang --use-proxy
```

```bash
synthlang optimize --prompt "Generate a report on sales data" --use-proxy
```

### Health Check

You can check the health of the proxy service:

```bash
synthlang proxy health
```

### Logging Out

To clear your saved credentials:

```bash
synthlang proxy logout
```

## API Reference

### Proxy Commands

| Command | Description |
|---------|-------------|
| `proxy serve` | Start a local proxy server |
| `proxy login` | Save credentials for proxy service |
| `proxy logout` | Clear saved credentials |
| `proxy chat` | Send a chat request to the proxy |
| `proxy compress` | Compress a prompt |
| `proxy decompress` | Decompress a prompt |
| `proxy clear-cache` | Clear the semantic cache |
| `proxy cache-stats` | Show cache statistics |
| `proxy tools` | List available agent tools |
| `proxy call-tool` | Call an agent tool |
| `proxy health` | Check proxy service health |

## Troubleshooting

### Connection Issues

If you're having trouble connecting to a remote proxy:

1. Check your API key with `synthlang proxy login`
2. Verify the endpoint URL
3. Check your network connection
4. Try the health check: `synthlang proxy health`

### Cache Issues

If you're getting unexpected results:

1. Try clearing the cache: `synthlang proxy clear-cache`
2. Check cache statistics: `synthlang proxy cache-stats`

### Server Issues

If the local server won't start:

1. Check if the port is already in use
2. Try a different port: `synthlang proxy serve --port 8001`
3. Check for error messages in the console

## Next Steps

- Explore the [SynthLang API documentation](https://synthlang.org/docs/api)
- Learn about [agent development](https://synthlang.org/docs/agents)
- Contribute to the [SynthLang project](https://github.com/ruvnet/SynthLang)