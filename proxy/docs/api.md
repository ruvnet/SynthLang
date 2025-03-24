# SynthLang Proxy API Reference

This document provides a comprehensive reference for all API endpoints available in SynthLang Proxy.

## API Overview

SynthLang Proxy provides a REST API that is compatible with the OpenAI API, making it easy to integrate with existing applications that use OpenAI's API. Additionally, it offers SynthLang-specific endpoints for advanced functionality.

## Base URL

The base URL for all API endpoints is:

```
http://<host>:<port>/
```

For example, if you're running SynthLang Proxy locally on port 8000, the base URL would be:

```
http://localhost:8000/
```

## Authentication

All API endpoints require authentication using an API key. The API key can be provided in the following ways:

1. **HTTP Header**: `Authorization: Bearer <api_key>`
2. **Query Parameter**: `?api_key=<api_key>`

Example:

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_api_key" \
  -d '{
    "model": "gpt-4o",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Hello, how are you?"}
    ]
  }'
```

## Rate Limiting

SynthLang Proxy implements rate limiting to protect the service from abuse. Rate limits are based on the user's role:

- **Basic Users**: 60 requests per minute (default)
- **Premium Users**: 120 requests per minute (default)

Rate limit information is included in the response headers:

- `X-RateLimit-Limit`: Maximum number of requests per minute
- `X-RateLimit-Remaining`: Number of requests remaining in the current window
- `X-RateLimit-Reset`: Time when the rate limit window resets (Unix timestamp)

## Error Handling

SynthLang Proxy returns standard HTTP status codes to indicate the success or failure of an API request.

Common status codes:

- `200 OK`: Success
- `400 Bad Request`: Invalid request
- `401 Unauthorized`: Missing or invalid API key
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Endpoint not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

Error responses include a JSON object with details about the error:

```json
{
  "error": {
    "message": "Detailed error message",
    "type": "error_type",
    "code": "error_code",
    "param": "parameter_name",
    "status": 400
  }
}
```

## Common Headers

SynthLang Proxy supports several custom headers that can be used to control behavior across endpoints:

| Header | Description | Values |
|--------|-------------|--------|
| `X-Mask-PII-Before-LLM` | Mask PII before sending to LLM | `0` (disabled) or `1` (enabled) |
| `X-Mask-PII-In-Logs` | Mask PII in logs | `0` (disabled) or `1` (enabled) |
| `X-Use-SynthLang` | Enable SynthLang compression | `0` (disabled) or `1` (enabled) |
| `X-Use-Gzip` | Enable additional gzip compression | `0` (disabled) or `1` (enabled) |
| `X-Disable-Keyword-Detection` | Disable keyword detection | `0` (disabled) or `1` (enabled) |

These headers override the default configuration for the specific request.

## OpenAI-Compatible Endpoints

### Chat Completions

Create a chat completion similar to OpenAI's chat completion endpoint.

**Endpoint**: `POST /v1/chat/completions`

**Request Body**:

```json
{
  "model": "gpt-4o",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello, how are you?"}
  ],
  "temperature": 0.7,
  "top_p": 1.0,
  "n": 1,
  "stream": false,
  "max_tokens": 100,
  "presence_penalty": 0.0,
  "frequency_penalty": 0.0,
  "use_synthlang": true,
  "use_gzip": false,
  "disable_keyword_detection": false
}
```

**Parameters**:

| Name | Type | Description | Default |
|------|------|-------------|---------|
| model | string | The model to use (gpt-4o, gpt-4o-mini, etc.) | gpt-4o |
| messages | array | Array of message objects | Required |
| temperature | number | Controls randomness (0-2) | 0.7 |
| top_p | number | Controls diversity via nucleus sampling (0-1) | 1.0 |
| n | integer | Number of completions to generate | 1 |
| stream | boolean | Whether to stream responses | false |
| max_tokens | integer | Maximum number of tokens to generate | Varies by model |
| presence_penalty | number | Penalty for new token presence (0-2) | 0.0 |
| frequency_penalty | number | Penalty for token frequency (0-2) | 0.0 |
| use_synthlang | boolean | Enable SynthLang compression | true |
| use_gzip | boolean | Enable additional gzip compression | false |
| disable_keyword_detection | boolean | Disable keyword detection | false |

**Headers**:

| Header | Description | Values |
|--------|-------------|--------|
| `X-Mask-PII-Before-LLM` | Mask PII before sending to LLM | `0` (disabled) or `1` (enabled) |
| `X-Mask-PII-In-Logs` | Mask PII in logs | `0` (disabled) or `1` (enabled) |

**Response**:

```json
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion",
  "created": 1677858242,
  "model": "gpt-4o",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "I'm doing well, thank you for asking! How can I help you today?"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 18,
    "completion_tokens": 16,
    "total_tokens": 34
  }
}
```

**Streaming Response**:

When `stream` is set to `true`, the response is a stream of server-sent events:

```
data: {"id":"chatcmpl-abc123","object":"chat.completion.chunk","created":1677858242,"model":"gpt-4o","choices":[{"index":0,"delta":{"role":"assistant"},"finish_reason":null}]}

data: {"id":"chatcmpl-abc123","object":"chat.completion.chunk","created":1677858242,"model":"gpt-4o","choices":[{"index":0,"delta":{"content":"I'm"},"finish_reason":null}]}

data: {"id":"chatcmpl-abc123","object":"chat.completion.chunk","created":1677858242,"model":"gpt-4o","choices":[{"index":0,"delta":{"content":" doing"},"finish_reason":null}]}

data: {"id":"chatcmpl-abc123","object":"chat.completion.chunk","created":1677858242,"model":"gpt-4o","choices":[{"index":0,"delta":{"content":" well"},"finish_reason":null}]}

...

data: {"id":"chatcmpl-abc123","object":"chat.completion.chunk","created":1677858242,"model":"gpt-4o","choices":[{"index":0,"delta":{},"finish_reason":"stop"}]}

data: [DONE]
```

### Completions (Legacy)

Create a completion similar to OpenAI's completion endpoint.

**Endpoint**: `POST /v1/completions`

**Request Body**:

```json
{
  "model": "gpt-4o",
  "prompt": "Once upon a time",
  "temperature": 0.7,
  "max_tokens": 50,
  "top_p": 1.0,
  "n": 1,
  "stream": false,
  "use_synthlang": true,
  "use_gzip": false
}
```

**Parameters**: Similar to chat completions, but with `prompt` instead of `messages`.

**Headers**: Same as chat completions, including PII masking headers.

**Response**: Similar structure to chat completions.

### Models

List available models.

**Endpoint**: `GET /v1/models`

**Response**:

```json
{
  "object": "list",
  "data": [
    {
      "id": "gpt-4o",
      "object": "model",
      "created": 1677610602,
      "owned_by": "openai"
    },
    {
      "id": "gpt-4o-mini",
      "object": "model",
      "created": 1677610602,
      "owned_by": "openai"
    },
    {
      "id": "gpt-4-turbo",
      "object": "model",
      "created": 1677610602,
      "owned_by": "openai"
    }
  ]
}
```

## SynthLang-Specific Endpoints

### Health Check

Check the health of the SynthLang Proxy service.

**Endpoint**: `GET /health`

**Response**:

```json
{
  "status": "ok",
  "version": "1.0.0",
  "timestamp": "2025-03-23T05:28:46Z",
  "uptime": 3600,
  "components": {
    "database": "ok",
    "cache": "ok",
    "llm_provider": "ok"
  }
}
```

### SynthLang Translation

Translate natural language to SynthLang format.

**Endpoint**: `POST /v1/synthlang/translate`

**Request Body**:

```json
{
  "text": "Create a chatbot that helps users with programming questions",
  "instructions": null
}
```

**Response**:

```json
{
  "source": "Create a chatbot that helps users with programming questions",
  "target": "↹ chatbot•programming ⊕ help•users => response",
  "explanation": "The translation uses SynthLang symbolic notation to represent a chatbot focused on programming that helps users by providing responses."
}
```

### System Prompt Generation

Generate a system prompt from a task description.

**Endpoint**: `POST /v1/synthlang/generate`

**Request Body**:

```json
{
  "task_description": "Create a system prompt for a chatbot that helps with programming"
}
```

**Response**:

```json
{
  "prompt": "You are an expert programming assistant with deep knowledge of multiple programming languages, frameworks, libraries, and best practices. Your goal is to help users solve programming problems, debug code, explain concepts, and provide guidance on software development tasks. When responding to queries:\n\n1. If the user provides code, analyze it carefully before responding\n2. Offer clear, concise explanations with practical examples\n3. Suggest best practices and potential improvements\n4. When appropriate, provide code snippets that demonstrate solutions\n5. If a question is ambiguous, ask clarifying questions to better understand the user's needs\n\nYour responses should be technically accurate, helpful, and tailored to the user's level of expertise.",
  "rationale": "This prompt establishes the assistant as a programming expert, sets clear expectations for behavior, and provides specific guidelines for how to respond to different types of programming questions.",
  "metadata": {
    "tokens": 178,
    "model": "gpt-4o-mini",
    "version": "1.0.0"
  }
}
```

### Prompt Optimization

Optimize a prompt for clarity, specificity, and efficiency.

**Endpoint**: `POST /v1/synthlang/optimize`

**Request Body**:

```json
{
  "prompt": "Tell me about databases",
  "max_iterations": 3
}
```

**Response**:

```json
{
  "original": "Tell me about databases",
  "optimized": "Provide a comprehensive overview of database management systems, including their types (relational, NoSQL, graph, etc.), key features, common use cases, and popular implementations. Include brief explanations of fundamental concepts like ACID properties, indexing, transactions, and normalization. Conclude with recent trends in database technology.",
  "improvements": [
    "Added specificity about database types",
    "Requested explanations of key concepts",
    "Included request for recent trends",
    "Structured the prompt with clear sections"
  ],
  "metrics": {
    "original_tokens": 4,
    "optimized_tokens": 62,
    "clarity_score": 0.92,
    "specificity_score": 0.85,
    "iterations": 2
  }
}
```

### Prompt Evolution

Evolve a prompt using genetic algorithms.

**Endpoint**: `POST /v1/synthlang/evolve`

**Request Body**:

```json
{
  "seed_prompt": "Write code to sort an array",
  "n_generations": 10,
  "population_size": 8,
  "mutation_rate": 0.1
}
```

**Response**:

```json
{
  "seed_prompt": "Write code to sort an array",
  "best_prompt": "Implement a sorting algorithm for an array of integers. Compare at least two different sorting methods (e.g., quick sort, merge sort, heap sort), analyzing their time and space complexity. Include well-commented code examples in a programming language of your choice, with test cases demonstrating correctness and explaining the performance characteristics of each approach.",
  "generations": 10,
  "population_size": 8,
  "mutation_rate": 0.1,
  "fitness": {
    "clarity": 0.94,
    "specificity": 0.91,
    "completeness": 0.89,
    "overall": 0.92
  },
  "evolution_path": [
    {
      "generation": 1,
      "best_fitness": 0.72,
      "average_fitness": 0.61
    },
    {
      "generation": 5,
      "best_fitness": 0.85,
      "average_fitness": 0.76
    },
    {
      "generation": 10,
      "best_fitness": 0.92,
      "average_fitness": 0.84
    }
  ]
}
```

### Prompt Classification

Classify a prompt into categories.

**Endpoint**: `POST /v1/synthlang/classify`

**Request Body**:

```json
{
  "text": "Write a function that calculates prime numbers",
  "labels": ["code", "math", "algorithm", "data science"]
}
```

**Response**:

```json
{
  "text": "Write a function that calculates prime numbers",
  "label": "algorithm",
  "confidence": 0.87,
  "all_labels": [
    {"label": "algorithm", "score": 0.87},
    {"label": "code", "score": 0.85},
    {"label": "math", "score": 0.72},
    {"label": "data science", "score": 0.31}
  ],
  "explanation": "This prompt is primarily asking for an algorithm to calculate prime numbers. While it involves coding and mathematics, the core task is algorithmic in nature."
}
```

### Prompt Management

Save, load, list, delete, and compare prompts.

#### Save Prompt

**Endpoint**: `POST /v1/synthlang/prompts/save`

**Request Body**:

```json
{
  "name": "database-overview",
  "prompt": "Provide a comprehensive overview of database management systems...",
  "metadata": {
    "category": "technology",
    "author": "user1",
    "tags": ["database", "technology", "overview"]
  }
}
```

**Response**:

```json
{
  "success": true,
  "name": "database-overview",
  "id": "prompt_123456",
  "timestamp": "2025-03-23T05:28:46Z"
}
```

#### Load Prompt

**Endpoint**: `POST /v1/synthlang/prompts/load`

**Request Body**:

```json
{
  "name": "database-overview"
}
```

**Response**:

```json
{
  "name": "database-overview",
  "prompt": "Provide a comprehensive overview of database management systems...",
  "metadata": {
    "category": "technology",
    "author": "user1",
    "tags": ["database", "technology", "overview"]
  },
  "created_at": "2025-03-23T05:00:00Z",
  "updated_at": "2025-03-23T05:28:46Z"
}
```

#### List Prompts

**Endpoint**: `GET /v1/synthlang/prompts/list`

**Response**:

```json
{
  "prompts": [
    {
      "name": "database-overview",
      "metadata": {
        "category": "technology",
        "author": "user1",
        "tags": ["database", "technology", "overview"]
      },
      "created_at": "2025-03-23T05:00:00Z"
    },
    {
      "name": "sorting-algorithm",
      "metadata": {
        "category": "code",
        "author": "user1",
        "tags": ["algorithm", "sorting", "code"]
      },
      "created_at": "2025-03-23T04:30:00Z"
    }
  ],
  "count": 2
}
```

#### Delete Prompt

**Endpoint**: `POST /v1/synthlang/prompts/delete`

**Request Body**:

```json
{
  "name": "database-overview"
}
```

**Response**:

```json
{
  "success": true,
  "name": "database-overview",
  "timestamp": "2025-03-23T05:40:00Z"
}
```

#### Compare Prompts

**Endpoint**: `POST /v1/synthlang/prompts/compare`

**Request Body**:

```json
{
  "name1": "sorting-algorithm-v1",
  "name2": "sorting-algorithm-v2"
}
```

**Response**:

```json
{
  "prompts": {
    "sorting-algorithm-v1": "Implement a sorting algorithm...",
    "sorting-algorithm-v2": "Implement and compare sorting algorithms..."
  },
  "differences": {
    "added": ["compare sorting algorithms"],
    "removed": [],
    "modified": ["Implement a sorting algorithm" -> "Implement and compare sorting algorithms"]
  },
  "metrics": {
    "similarity_score": 0.78,
    "token_difference": 12,
    "clarity_comparison": {
      "sorting-algorithm-v1": 0.82,
      "sorting-algorithm-v2": 0.89
    },
    "specificity_comparison": {
      "sorting-algorithm-v1": 0.75,
      "sorting-algorithm-v2": 0.88
    }
  }
}
```

### Semantic Cache Management

#### Clear Cache

Clear the semantic cache.

**Endpoint**: `POST /v1/cache/clear`

**Response**:

```json
{
  "success": true,
  "cleared_entries": 156,
  "timestamp": "2025-03-23T05:45:00Z"
}
```

#### Cache Statistics

Get statistics about the semantic cache.

**Endpoint**: `GET /v1/cache/stats`

**Response**:

```json
{
  "entries": 156,
  "hits": 1024,
  "misses": 512,
  "hit_rate": 0.67,
  "size_bytes": 2456789,
  "memory_usage": "2.4 MB",
  "oldest_entry": "2025-03-22T00:00:00Z",
  "newest_entry": "2025-03-23T05:45:00Z",
  "model_stats": {
    "gpt-4o": {
      "entries": 100,
      "hits": 800,
      "hit_rate": 0.75
    },
    "gpt-4o-mini": {
      "entries": 56,
      "hits": 224,
      "hit_rate": 0.55
    }
  }
}
```

### Agent Tools

#### List Tools

List available agent tools.

**Endpoint**: `GET /v1/tools`

**Response**:

```json
{
  "tools": [
    {
      "name": "weather",
      "description": "Get weather information for a location",
      "parameters": {
        "location": {
          "type": "string",
          "description": "Location to get weather for"
        }
      },
      "required_role": "basic"
    },
    {
      "name": "calculator",
      "description": "Perform mathematical calculations",
      "parameters": {
        "expression": {
          "type": "string",
          "description": "Mathematical expression to evaluate"
        }
      },
      "required_role": "basic"
    },
    {
      "name": "web_search",
      "description": "Search the web for information",
      "parameters": {
        "query": {
          "type": "string",
          "description": "Search query"
        }
      },
      "required_role": "premium"
    }
  ],
  "count": 3
}
```

#### Call Tool

Call an agent tool directly.

**Endpoint**: `POST /v1/tools/call`

**Request Body**:

```json
{
  "tool": "calculator",
  "parameters": {
    "expression": "2+2*5"
  }
}
```

**Response**:

```json
{
  "tool": "calculator",
  "result": {
    "value": 12,
    "steps": [
      "Evaluate 2*5 = 10",
      "Add 2 + 10 = 12"
    ]
  },
  "execution_time": 15
}
```

### Keyword Pattern Management

#### List Patterns

List all keyword patterns.

**Endpoint**: `GET /v1/keywords/patterns`

**Response**:

```json
{
  "patterns": [
    {
      "name": "weather_query",
      "pattern": "(?:what's|what is|how's|how is)\\s+(?:the)?\\s*(?:weather|temperature)\\s+(?:like)?\\s*(?:in|at|near)?\\s+(?P<location>[\\w\\s]+)",
      "tool": "weather",
      "description": "Detects weather queries",
      "priority": 100,
      "required_role": "basic",
      "enabled": true
    },
    {
      "name": "calculate_query",
      "pattern": "(?:calculate|compute|evaluate|what is)\\s+(?P<expression>[\\d\\s\\+\\-\\*\\/\\(\\)\\^\\%]+)",
      "tool": "calculator",
      "description": "Detects calculation requests",
      "priority": 90,
      "required_role": "basic",
      "enabled": true
    }
  ],
  "count": 2,
  "settings": {
    "enable_detection": true,
    "detection_threshold": 0.7,
    "default_role": "basic"
  }
}
```

#### Add Pattern

Add a new keyword pattern.

**Endpoint**: `POST /v1/keywords/patterns`

**Request Body**:

```json
{
  "name": "stock_price_query",
  "pattern": "(?:what's|what is|get|check)\\s+(?:the)?\\s*(?:stock price|share price|stock value)\\s+(?:of|for)?\\s+(?P<ticker>[A-Z]+)",
  "tool": "stock_price",
  "description": "Detects requests for stock price information",
  "priority": 95,
  "required_role": "premium",
  "enabled": true
}
```

**Response**:

```json
{
  "success": true,
  "name": "stock_price_query",
  "timestamp": "2025-03-23T05:50:00Z"
}
```

#### Update Pattern

Update an existing keyword pattern.

**Endpoint**: `PUT /v1/keywords/patterns/{pattern_name}`

**Request Body**:

```json
{
  "priority": 97,
  "enabled": false
}
```

**Response**:

```json
{
  "success": true,
  "name": "stock_price_query",
  "timestamp": "2025-03-23T05:51:00Z",
  "updated_fields": ["priority", "enabled"]
}
```

#### Delete Pattern

Delete a keyword pattern.

**Endpoint**: `DELETE /v1/keywords/patterns/{pattern_name}`

**Response**:

```json
{
  "success": true,
  "name": "stock_price_query",
  "timestamp": "2025-03-23T05:52:00Z"
}
```

#### Update Settings

Update keyword detection settings.

**Endpoint**: `PUT /v1/keywords/settings`

**Request Body**:

```json
{
  "enable_detection": true,
  "detection_threshold": 0.8,
  "default_role": "basic"
}
```

**Response**:

```json
{
  "success": true,
  "settings": {
    "enable_detection": true,
    "detection_threshold": 0.8,
    "default_role": "basic"
  },
  "timestamp": "2025-03-23T05:53:00Z"
}
```

## Using with API Clients

### JavaScript/Node.js

```javascript
const axios = require('axios');

const apiClient = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${API_KEY}`,
    'X-Mask-PII-Before-LLM': '1',  // Enable PII masking before sending to LLM
    'X-Mask-PII-In-Logs': '1'      // Enable PII masking in logs
  }
});

async function chatCompletion() {
  try {
    const response = await apiClient.post('/v1/chat/completions', {
      model: 'gpt-4o',
      messages: [
        { role: 'system', content: 'You are a helpful assistant.' },
        { role: 'user', content: 'Hello, how are you?' }
      ]
    });
    return response.data;
  } catch (error) {
    console.error('Error:', error.response?.data || error.message);
    throw error;
  }
}
```

### Python

```python
import requests

API_KEY = 'your_api_key'
BASE_URL = 'http://localhost:8000'

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {API_KEY}',
    'X-Mask-PII-Before-LLM': '1',  # Enable PII masking before sending to LLM
    'X-Mask-PII-In-Logs': '1'      # Enable PII masking in logs
}

def chat_completion():
    try:
        response = requests.post(
            f'{BASE_URL}/v1/chat/completions',
            headers=headers,
            json={
                'model': 'gpt-4o',
                'messages': [
                    {'role': 'system', 'content': 'You are a helpful assistant.'},
                    {'role': 'user', 'content': 'Hello, how are you?'}
                ]
            }
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')
        raise
```

### cURL

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_api_key" \
  -H "X-Mask-PII-Before-LLM: 1" \
  -H "X-Mask-PII-In-Logs: 1" \
  -d '{
    "model": "gpt-4o",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Hello, how are you?"}
    ]
  }'
```

## API Versioning

SynthLang Proxy uses versioned API endpoints (`/v1/`) to ensure backwards compatibility as the API evolves. Future versions of the API will be made available under new version prefixes (e.g., `/v2/`).

## API Stability

API endpoints are classified into three stability levels:

- **Stable**: Fully supported and backwards compatible
- **Beta**: Functional but may change in future releases
- **Experimental**: May change significantly or be removed

All endpoints under `/v1/` are considered stable unless otherwise noted in the documentation.

## Webhooks

SynthLang Proxy supports webhooks for asynchronous notifications about events:

- **Completion Finished**: Notifies when a long-running completion is finished
- **Tool Execution Completed**: Notifies when a tool execution is completed
- **System Events**: Notifies about system events (cache cleared, settings updated, etc.)

Webhook configuration is managed through the administration API endpoints (not covered in this document).