# OpenRouter Integration Guide

## Overview

This guide details the integration of OpenRouter's API into the SynthLang system for prompt testing and model comparison. OpenRouter provides access to multiple language models through a unified API, enabling comprehensive prompt testing and performance analysis.

## API Configuration

### Authentication

```typescript
const OPENROUTER_API_KEY = process.env.OPENROUTER_API_KEY;
const OPENROUTER_BASE_URL = 'https://openrouter.ai/api/v1';

interface OpenRouterConfig {
  apiKey: string;
  baseUrl: string;
  defaultModel: string;
  timeout: number;
  retryAttempts: number;
}
```

### Available Models

```typescript
enum OpenRouterModel {
  GPT35Turbo = 'gpt-3.5-turbo',
  GPT4 = 'gpt-4',
  Claude2 = 'claude-2',
  PaLM2 = 'palm-2',
  LLaMA2 = 'llama-2',
}

interface ModelConfig {
  id: OpenRouterModel;
  contextWindow: number;
  costPer1kTokens: number;
  maxTokens: number;
  capabilities: string[];
}
```

## API Endpoints

### Chat Completions

```typescript
interface ChatCompletionRequest {
  model: OpenRouterModel;
  messages: Array<{
    role: 'system' | 'user' | 'assistant';
    content: string;
  }>;
  temperature?: number;
  max_tokens?: number;
  top_p?: number;
  frequency_penalty?: number;
  presence_penalty?: number;
}

interface ChatCompletionResponse {
  id: string;
  object: string;
  created: number;
  model: string;
  choices: Array<{
    index: number;
    message: {
      role: string;
      content: string;
    };
    finish_reason: string;
  }>;
  usage: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
}
```

## Implementation

### API Client

```typescript
export class OpenRouterClient {
  private config: OpenRouterConfig;
  private axios: AxiosInstance;

  constructor(config: Partial<OpenRouterConfig>) {
    this.config = {
      apiKey: config.apiKey || process.env.OPENROUTER_API_KEY,
      baseUrl: config.baseUrl || OPENROUTER_BASE_URL,
      defaultModel: config.defaultModel || OpenRouterModel.GPT35Turbo,
      timeout: config.timeout || 30000,
      retryAttempts: config.retryAttempts || 3,
    };

    this.axios = axios.create({
      baseURL: this.config.baseUrl,
      timeout: this.config.timeout,
      headers: {
        'Authorization': `Bearer ${this.config.apiKey}`,
        'Content-Type': 'application/json',
      },
    });
  }

  async testPrompt(prompt: string, model: OpenRouterModel): Promise<TestResponse> {
    try {
      const startTime = Date.now();
      const response = await this.axios.post('/chat/completions', {
        model,
        messages: [{ role: 'user', content: prompt }],
      });
      const endTime = Date.now();

      return {
        model,
        response: response.data.choices[0].message.content,
        metrics: {
          latency: endTime - startTime,
          tokens: response.data.usage.total_tokens,
          cost: this.calculateCost(response.data.usage, model),
        },
      };
    } catch (error) {
      throw this.handleError(error);
    }
  }

  async batchTest(prompt: string, models: OpenRouterModel[]): Promise<BatchTestResult> {
    const results = await Promise.all(
      models.map(model => this.testPrompt(prompt, model))
    );

    return {
      results,
      summary: this.calculateSummary(results),
    };
  }

  private calculateCost(usage: any, model: OpenRouterModel): number {
    const modelConfig = this.getModelConfig(model);
    return (usage.total_tokens / 1000) * modelConfig.costPer1kTokens;
  }

  private calculateSummary(results: TestResponse[]): TestSummary {
    return {
      averageLatency: results.reduce((acc, r) => acc + r.metrics.latency, 0) / results.length,
      totalCost: results.reduce((acc, r) => acc + r.metrics.cost, 0),
      successRate: results.filter(r => r.response).length / results.length,
    };
  }
}
```

### Error Handling

```typescript
class OpenRouterError extends Error {
  constructor(
    message: string,
    public statusCode?: number,
    public response?: any
  ) {
    super(message);
    this.name = 'OpenRouterError';
  }
}

function handleOpenRouterError(error: any): never {
  if (axios.isAxiosError(error)) {
    throw new OpenRouterError(
      error.response?.data?.message || error.message,
      error.response?.status,
      error.response?.data
    );
  }
  throw error;
}
```

## Usage Examples

### Basic Usage

```typescript
const client = new OpenRouterClient({
  apiKey: 'your-api-key',
});

// Test with a single model
const result = await client.testPrompt(
  'Translate this prompt to SynthLang format',
  OpenRouterModel.GPT35Turbo
);

// Test with multiple models
const batchResult = await client.batchTest(
  'Translate this prompt to SynthLang format',
  [OpenRouterModel.GPT35Turbo, OpenRouterModel.Claude2]
);
```

### Advanced Usage

```typescript
// Custom configuration
const client = new OpenRouterClient({
  apiKey: 'your-api-key',
  timeout: 60000,
  retryAttempts: 5,
  defaultModel: OpenRouterModel.GPT4,
});

// Advanced prompt testing
const result = await client.testPrompt(
  {
    messages: [
      {
        role: 'system',
        content: 'You are a SynthLang translation expert',
      },
      {
        role: 'user',
        content: 'Translate this prompt to SynthLang format',
      },
    ],
    temperature: 0.7,
    max_tokens: 2000,
  },
  OpenRouterModel.GPT4
);
```

## Best Practices

1. **Error Handling**
   - Implement proper error handling
   - Use retry mechanisms for transient failures
   - Log errors appropriately
   - Provide meaningful error messages

2. **Rate Limiting**
   - Implement rate limiting
   - Use exponential backoff
   - Queue requests when necessary
   - Monitor usage limits

3. **Performance**
   - Cache responses when appropriate
   - Use batch requests when possible
   - Monitor response times
   - Optimize request payload size

4. **Security**
   - Secure API key storage
   - Validate input data
   - Sanitize responses
   - Use HTTPS only
   - Implement request signing

5. **Monitoring**
   - Track API usage
   - Monitor error rates
   - Track response times
   - Set up alerts

## Troubleshooting

Common issues and solutions:

1. **Authentication Errors**
   - Verify API key
   - Check key permissions
   - Ensure proper header format

2. **Rate Limiting**
   - Implement backoff strategy
   - Monitor usage limits
   - Queue requests
   - Use batch endpoints

3. **Timeout Issues**
   - Adjust timeout settings
   - Implement retry logic
   - Monitor network conditions
   - Use appropriate timeouts

4. **Response Parsing**
   - Validate response format
   - Handle edge cases
   - Implement error handling
   - Log parsing errors

## Testing

```typescript
describe('OpenRouterClient', () => {
  let client: OpenRouterClient;

  beforeEach(() => {
    client = new OpenRouterClient({
      apiKey: 'test-key',
    });
  });

  it('should handle successful requests', async () => {
    const result = await client.testPrompt(
      'Test prompt',
      OpenRouterModel.GPT35Turbo
    );
    expect(result.response).toBeDefined();
    expect(result.metrics).toBeDefined();
  });

  it('should handle errors appropriately', async () => {
    // Test error scenarios
  });

  it('should calculate costs correctly', async () => {
    // Test cost calculations
  });
});
