# Migration Guide: From OpenAI API to SynthLang Proxy

This guide helps you migrate your applications from direct OpenAI API usage to SynthLang Proxy, providing a smooth transition path with minimal code changes.

## Overview

SynthLang Proxy is designed as a drop-in replacement for the OpenAI API, making migration straightforward in most cases. By changing just the API endpoint URL, you can immediately benefit from features like token compression, semantic caching, and agentic capabilities.

## Migration Steps

### Step 1: Install SynthLang Proxy

First, install and configure SynthLang Proxy. You have several options:

- **Docker**: Use the provided Docker image
- **Self-hosted**: Install on your own server
- **Serverless**: Deploy to a serverless platform

See the [Installation Guide](installation.md) for detailed instructions.

### Step 2: Update API Endpoint URL

The primary change needed is to update your API endpoint URL from OpenAI's to your SynthLang Proxy instance:

#### JavaScript Example

**Before:**
```javascript
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

const response = await openai.chat.completions.create({
  model: 'gpt-4o',
  messages: [
    { role: 'user', content: 'Hello, how are you?' }
  ]
});
```

**After:**
```javascript
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
  baseURL: 'http://your-synthlang-proxy-url:8000/v1', // Only this line changes
});

const response = await openai.chat.completions.create({
  model: 'gpt-4o',
  messages: [
    { role: 'user', content: 'Hello, how are you?' }
  ]
});
```

#### Python Example

**Before:**
```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

response = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {"role": "user", "content": "Hello, how are you?"}
  ]
)
```

**After:**
```python
from openai import OpenAI

client = OpenAI(
  api_key="your-api-key",
  base_url="http://your-synthlang-proxy-url:8000/v1"  # Only this line changes
)

response = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {"role": "user", "content": "Hello, how are you?"}
  ]
)
```

#### Curl Example

**Before:**
```bash
curl https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key" \
  -d '{
    "model": "gpt-4o",
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ]
  }'
```

**After:**
```bash
curl http://your-synthlang-proxy-url:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key" \
  -d '{
    "model": "gpt-4o",
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ]
  }'
```

### Step 3: Configure Authentication

You have several options for authentication:

1. **Pass-Through Authentication**: SynthLang Proxy can pass your original OpenAI API key to OpenAI
2. **Custom Authentication**: Use a SynthLang Proxy API key for authentication to the proxy, which then uses its own OpenAI API key

For the simplest migration, start with pass-through authentication, then consider custom authentication for more control.

### Step 4: Test the Integration

Before fully migrating, test the integration to ensure everything works as expected:

1. Make a simple API call and verify the response
2. Check logs for any errors or warnings
3. Monitor performance and token usage

### Step 5: Enable SynthLang Features

Once the basic integration is working, you can enable SynthLang-specific features:

#### Compression

Compression is enabled by default. You can control it per request:

```javascript
const response = await openai.chat.completions.create({
  model: 'gpt-4o',
  messages: [
    { role: 'user', content: 'Hello, how are you?' }
  ],
  use_synthlang: true,  // Enable SynthLang compression (default)
  use_gzip: true        // Enable additional gzip compression
});
```

#### Semantic Caching

Semantic caching is enabled by default. You can control it per request:

```javascript
const response = await openai.chat.completions.create({
  model: 'gpt-4o',
  messages: [
    { role: 'user', content: 'Hello, how are you?' }
  ],
  cache: true  // Enable semantic caching (default)
});
```

#### Agent Tools

You can use agent tools without any code changes, through natural language or hashtag directives:

```javascript
const response = await openai.chat.completions.create({
  model: 'gpt-4o',
  messages: [
    { role: 'user', content: "What's the weather in London?" }  // Automatically triggers weather tool
  ]
});
```

Or with explicit hashtags:

```javascript
const response = await openai.chat.completions.create({
  model: 'gpt-4o',
  messages: [
    { role: 'user', content: "#tool_weather London" }  // Explicitly triggers weather tool
  ]
});
```

## Framework-Specific Migration Guides

### React Applications

For React applications using the OpenAI API:

1. Update the API client configuration to point to SynthLang Proxy
2. Ensure environment variables are correctly set
3. Test functionality with simple requests before full migration

Example React component:

```jsx
import React, { useState } from 'react';
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: process.env.REACT_APP_OPENAI_API_KEY,
  baseURL: process.env.REACT_APP_SYNTHLANG_PROXY_URL || 'http://localhost:8000/v1',
});

function ChatComponent() {
  const [input, setInput] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const completion = await openai.chat.completions.create({
        model: 'gpt-4o',
        messages: [{ role: 'user', content: input }],
      });
      
      setResponse(completion.choices[0].message.content);
    } catch (error) {
      console.error('Error:', error);
      setResponse('Error: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input 
          value={input} 
          onChange={(e) => setInput(e.target.value)} 
          placeholder="Ask something..." 
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Thinking...' : 'Send'}
        </button>
      </form>
      <div>{response}</div>
    </div>
  );
}

export default ChatComponent;
```

### Node.js Applications

For Node.js applications:

1. Update the OpenAI client configuration
2. Configure environment variables
3. Consider adding error handling specific to SynthLang Proxy

Example Express middleware:

```javascript
const OpenAI = require('openai');

// Configure OpenAI client
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
  baseURL: process.env.SYNTHLANG_PROXY_URL || 'http://localhost:8000/v1',
});

// Middleware for handling AI requests
const aiMiddleware = async (req, res, next) => {
  try {
    const { prompt } = req.body;
    
    if (!prompt) {
      return res.status(400).json({ error: 'Prompt is required' });
    }
    
    const completion = await openai.chat.completions.create({
      model: 'gpt-4o',
      messages: [{ role: 'user', content: prompt }],
    });
    
    req.aiResponse = completion.choices[0].message.content;
    next();
  } catch (error) {
    console.error('AI service error:', error);
    
    // Handle specific SynthLang Proxy errors
    if (error.response && error.response.status === 429) {
      return res.status(429).json({ error: 'Rate limit exceeded' });
    }
    
    res.status(500).json({ error: 'AI service error' });
  }
};

module.exports = aiMiddleware;
```

### Python Applications

For Python applications:

1. Update the OpenAI client configuration
2. Set environment variables
3. Implement proper error handling

Example FastAPI integration:

```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

# Initialize OpenAI client
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("SYNTHLANG_PROXY_URL", "http://localhost:8000/v1")
)

class PromptRequest(BaseModel):
    prompt: str
    model: str = "gpt-4o"

class AIResponse(BaseModel):
    text: str

@app.post("/generate", response_model=AIResponse)
async def generate_text(request: PromptRequest):
    try:
        response = client.chat.completions.create(
            model=request.model,
            messages=[
                {"role": "user", "content": request.prompt}
            ]
        )
        return AIResponse(text=response.choices[0].message.content)
    except Exception as e:
        # Handle errors
        if "429" in str(e):
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        raise HTTPException(status_code=500, detail=str(e))
```

## Migrating Streaming Responses

If your application uses streaming responses, the migration is similar:

### JavaScript Example

```javascript
const stream = await openai.chat.completions.create({
  model: 'gpt-4o',
  messages: [{ role: 'user', content: 'Write a story about a robot.' }],
  stream: true,
});

for await (const chunk of stream) {
  process.stdout.write(chunk.choices[0]?.delta?.content || '');
}
```

No changes are needed except for the `baseURL` in the client configuration.

### Python Example

```python
stream = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Write a story about a robot."}],
    stream=True
)

for chunk in stream:
    content = chunk.choices[0].delta.content
    if content:
        print(content, end="")
```

Again, only the `base_url` in the client configuration needs to change.

## Common Migration Issues

### Error Handling

SynthLang Proxy tries to match OpenAI's error format, but there might be slight differences. Make sure your error handling is flexible enough to accommodate these differences.

### Rate Limiting

SynthLang Proxy implements its own rate limiting, which might be different from OpenAI's. Adjust your backoff strategy accordingly.

### Token Counting

SynthLang Proxy's compression means token counts in responses might be different from direct OpenAI API calls. If your application relies on specific token counts, be aware of this difference.

### API Key Management

If you're using custom authentication, you'll need to manage both OpenAI API keys and SynthLang Proxy API keys.

## Advanced Migration

### Migrating to Agent Tools

To fully leverage SynthLang Proxy's capabilities, consider modifying your application to use agent tools:

1. Identify operations that could benefit from tools (e.g., data analysis, web search)
2. Update prompts to use hashtag directives or natural language patterns
3. Implement UI for tool-specific interactions if needed

### Optimizing for Compression

To maximize compression benefits:

1. Structure prompts consistently
2. Use clear, concise language
3. Organize multi-part prompts logically
4. Consider domain-specific compression for specialized applications

### Implementing Caching Strategy

To make the most of semantic caching:

1. Identify common query patterns
2. Pre-warm the cache with frequently asked questions
3. Monitor cache hit rates and adjust the similarity threshold
4. Consider purging the cache for time-sensitive information

## Gradual Migration Strategy

For complex applications, consider a phased migration:

1. **Phase 1**: Direct replacement for high-volume, non-critical endpoints
2. **Phase 2**: Add agent capabilities to key user interactions
3. **Phase 3**: Optimize prompts for compression
4. **Phase 4**: Implement custom tools for application-specific functionality

## Monitoring the Migration

During and after migration, monitor:

1. **Performance**: Response times, latency, and throughput
2. **Costs**: Token usage and API costs
3. **Errors**: Error rates and types
4. **Cache Performance**: Hit rates and efficiency
5. **User Experience**: Any changes in response quality or user satisfaction

## Rollback Plan

In case of issues, have a rollback plan:

1. Switch back to direct OpenAI API usage
2. Keep the previous configuration available
3. Document any changes needed for rollback
4. Test the rollback procedure in advance

## Conclusion

Migrating to SynthLang Proxy can significantly reduce costs and enhance capabilities with minimal code changes. By following this guide, you can smoothly transition your applications while minimizing disruption to users.

For additional assistance, refer to the [FAQ](faq.md) or [contact support](support@example.com).