export const SYSTEM_PROMPT = {
  interpreter: `You are a helpful AI assistant that interprets and executes SynthLang commands.
You understand the SynthLang syntax and can process commands with mathematical precision.
You provide clear explanations of your interpretations and actions.`,
  base: `You are a helpful AI assistant.`
};

export interface CompletionOptions {
  model: string;
  messages: Array<{
    role: string;
    content: string;
  }>;
  stream?: boolean;
  temperature?: number;
  max_tokens?: number;
  onChunk?: (chunk: string) => void;
}

export interface OpenRouterModel {
  id: string;
  name: string;
  description: string;
  context_length: number;
  pricing: {
    prompt: string | number;
    completion: string | number;
  };
}

class OpenRouterService {
  private readonly API_URL = 'https://openrouter.ai/api/v1';

  async streamCompletion(options: CompletionOptions, apiKey: string): Promise<any> {
    const response = await fetch(`${this.API_URL}/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`,
        'HTTP-Referer': window.location.origin,
      },
      body: JSON.stringify({
        model: options.model,
        messages: options.messages,
        stream: options.stream,
        temperature: options.temperature,
        max_tokens: options.max_tokens,
      }),
    });

    if (!response.ok) {
      throw new Error(`OpenRouter API error: ${response.statusText}`);
    }

    if (options.stream && response.body) {
      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n').filter(line => line.trim() !== '');
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const jsonStr = line.slice(6);
            if (jsonStr === '[DONE]') continue;
            
            try {
              const json = JSON.parse(jsonStr);
              const content = json.choices[0]?.delta?.content;
              if (content) {
                options.onChunk?.(content);
              }
            } catch (err) {
              console.error('Failed to parse chunk:', err);
            }
          }
        }
      }
    } else {
      const data = await response.json();
      return data;
    }
  }

  async getAvailableModels(apiKey: string): Promise<OpenRouterModel[]> {
    const response = await fetch(`${this.API_URL}/models`, {
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'HTTP-Referer': window.location.origin,
      },
    });

    if (!response.ok) {
      throw new Error(`OpenRouter API error: ${response.statusText}`);
    }

    const data = await response.json();
    return data.data.map((model: any) => ({
      id: model.id,
      name: model.name,
      description: model.description,
      context_length: model.context_length,
      pricing: {
        prompt: parseFloat(model.pricing.prompt.toString()),
        completion: parseFloat(model.pricing.completion.toString())
      }
    }));
  }

  async checkOpenRouterAvailability(apiKey: string): Promise<boolean> {
    try {
      const response = await fetch(`${this.API_URL}/status`, {
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'HTTP-Referer': window.location.origin,
        },
      });
      return response.ok;
    } catch (err) {
      return false;
    }
  }

  async callOpenRouter(options: CompletionOptions, apiKey: string): Promise<any> {
    const response = await fetch(`${this.API_URL}/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`,
        'HTTP-Referer': window.location.origin,
      },
      body: JSON.stringify({
        model: options.model,
        messages: options.messages,
        temperature: options.temperature,
        max_tokens: options.max_tokens,
      }),
    });

    if (!response.ok) {
      throw new Error(`OpenRouter API error: ${response.statusText}`);
    }

    return response.json();
  }
}

const service = new OpenRouterService();
export const openRouterService = service;

export const checkOpenRouterAvailability = (apiKey: string) => service.checkOpenRouterAvailability(apiKey);
export const getAvailableModels = (apiKey: string) => service.getAvailableModels(apiKey);
export const streamCompletion = (options: CompletionOptions, apiKey: string) => service.streamCompletion(options, apiKey);

export const callOpenRouter = async (
  code: string,
  settings: { model: string; temperature: number; maxTokens: number },
  apiKey: string,
  mode: 'interpreter' | 'base' | 'translator' = 'interpreter',
  instructions?: string,
  signal?: AbortSignal,
  onChunk?: (chunk: string) => void
) => {
  const messages = [
    {
      role: 'system',
      content: instructions || SYSTEM_PROMPT[mode]
    },
    {
      role: 'user',
      content: code
    }
  ];

  return openRouterService.streamCompletion({
    model: settings.model,
    messages,
    temperature: settings.temperature,
    max_tokens: settings.maxTokens,
    stream: true,
    onChunk
  }, apiKey);
};
