import CryptoJS from 'crypto-js';
import OpenAI from 'openai';

const ENCRYPTION_KEY = import.meta.env.VITE_ENCRYPTION_KEY || 'symbolic-scribe-key';
const DEFAULT_API_KEY = import.meta.env.VITE_OPENROUTER_KEY;
const SETTINGS_KEY = 'symbolic-scribe-settings';

export interface Settings {
  apiKey: string;
  defaultModel: string;
  enabledModels: string[];
}

export interface OpenRouterModel {
  id: string;
  name: string;
  description: string;
  context_length: number;
  pricing: {
    prompt: string;
    completion: string;
  };
}

// Initialize OpenAI client with OpenRouter base URL
export const createOpenRouterClient = (apiKey: string) => {
  return new OpenAI({
    baseURL: "https://openrouter.ai/api/v1",
    apiKey,
    defaultHeaders: {
      "HTTP-Referer": window.location.origin,
      "X-Title": "Symbolic Scribe"
    },
    dangerouslyAllowBrowser: true
  });
};

// Encrypt the API key before storing
const encryptApiKey = (apiKey: string): string => {
  return CryptoJS.AES.encrypt(apiKey, ENCRYPTION_KEY).toString();
};

// Decrypt the stored API key
const decryptApiKey = (encryptedApiKey: string): string => {
  const bytes = CryptoJS.AES.decrypt(encryptedApiKey, ENCRYPTION_KEY);
  return bytes.toString(CryptoJS.enc.Utf8);
};

// Save settings to local storage
export const saveSettings = (settings: Settings): void => {
  const encryptedSettings = {
    ...settings,
    apiKey: encryptApiKey(settings.apiKey)
  };
  localStorage.setItem(SETTINGS_KEY, JSON.stringify(encryptedSettings));
};

// Clear settings from local storage and return default settings if available
export const clearSettings = (): Settings | null => {
  localStorage.removeItem(SETTINGS_KEY);
  
  if (DEFAULT_API_KEY) {
    return {
      apiKey: DEFAULT_API_KEY,
      defaultModel: '',
      enabledModels: []
    };
  }
  
  return null;
};

// Load settings from local storage or use default API key
export const loadSettings = (): Settings | null => {
  const settingsJson = localStorage.getItem(SETTINGS_KEY);
  
  // If no settings in storage but we have a default key
  if (!settingsJson && DEFAULT_API_KEY) {
    return {
      apiKey: DEFAULT_API_KEY,
      defaultModel: '',
      enabledModels: []
    };
  }

  if (!settingsJson) return null;

  const settings = JSON.parse(settingsJson);
  return {
    ...settings,
    apiKey: settings.apiKey ? decryptApiKey(settings.apiKey) : DEFAULT_API_KEY || ''
  };
};

// Fetch available models from OpenRouter
export const fetchAvailableModels = async (apiKey: string): Promise<OpenRouterModel[]> => {
  try {
    const client = createOpenRouterClient(apiKey);
    const response = await client.models.list();

    return response.data.map((model: any) => ({
      id: model.id,
      name: model.name || model.id.split('/').pop() || model.id,
      description: model.description || 'No description available',
      context_length: model.context_length || 4096,
      pricing: {
        prompt: model.pricing?.prompt || '0',
        completion: model.pricing?.completion || '0'
      }
    }));
  } catch (error) {
    console.error('Error fetching models:', error);
    throw error;
  }
};

// Test API key validity
export const testApiKey = async (apiKey: string): Promise<boolean> => {
  try {
    const client = createOpenRouterClient(apiKey);
    const response = await client.models.list();
    return Boolean(response.data && Array.isArray(response.data));
  } catch (error) {
    console.error('Error testing API key:', error);
    return false;
  }
};

// Test prompt with selected model
export const testPrompt = async (apiKey: string, modelId: string, prompt: string, onChunk: (chunk: string) => void): Promise<void> => {
  try {
    const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'HTTP-Referer': window.location.origin,
        'X-Title': 'Symbolic Scribe',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model: modelId,
        messages: [
          {
            role: "user",
            content: prompt
          }
        ],
        stream: true
      })
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error?.message || `Failed to test prompt: ${response.status}`);
    }

    if (!response.body) {
      throw new Error('No response body');
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value);
      const lines = chunk.split('\n');

      for (const line of lines) {
        if (line.trim() === '') continue;
        if (line.trim() === 'data: [DONE]') continue;
        if (!line.startsWith('data: ')) continue;

        try {
          const json = JSON.parse(line.slice(6));
          const content = json.choices?.[0]?.delta?.content;
          if (content) {
            onChunk(content);
          }
        } catch (e) {
          console.error('Error parsing chunk:', e);
        }
      }
    }
  } catch (error: any) {
    console.error('Error testing prompt:', error);
    if (error.message.includes('401')) {
      throw new Error('Invalid API key. Please check your settings.');
    }
    throw new Error(error.message || 'Failed to test prompt. Please try again.');
  }
};
