import type { PlaygroundSettings } from '../components/Documentation/PlaygroundSettings';

interface OpenRouterResponse {
  choices: Array<{
    message: {
      content: string;
    };
  }>;
}

const SYSTEM_PROMPT = `You are a SynthLang interpreter. Process the following SynthLang code according to these rules:

[Grammar and Syntax]
1. Task Glyphs (T)
   - Σ (Summarize)
   - ↹ (Focus/Filter)
   - ⊕ (Combine/Merge)
   - ? (Query/Clarify)
   - IF (Conditional)

2. Subject Glyphs (S)
   Examples: •dataset, •salesData, 花 (flower), 山 (mountain)

3. Modifiers (M)
   Examples: ^4, ^eng, ^urgent, ^7d, ^brief, etc.

4. Flow Glyphs (F)
   Examples: [p=5], ⊕, →

5. Microparticles
   - : (Link labels to objects)
   - => (Implication/Result)
   - | (Logical OR)
   - + (Concatenate outputs)
   - -> (Action direction)

Process the input and provide output according to these rules.`;

export const callOpenRouter = async (
  code: string, 
  settings: PlaygroundSettings, 
  apiKey: string
): Promise<string> => {
  try {
    const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`,
        'HTTP-Referer': window.location.origin,
        'X-Title': 'SynthLang Playground'
      },
      body: JSON.stringify({
        model: settings.model,
        messages: [
          {
            role: 'system',
            content: SYSTEM_PROMPT
          },
          {
            role: 'user',
            content: code
          }
        ],
        temperature: settings.temperature,
        max_tokens: settings.maxTokens,
        top_p: 0.9,
        frequency_penalty: 0.0,
        presence_penalty: 0.0,
        stream: false
      })
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || 'Failed to process SynthLang code');
    }

    const data: OpenRouterResponse = await response.json();
    return data.choices[0]?.message?.content || '';
  } catch (error) {
    console.error('OpenRouter API error:', error);
    throw new Error('Failed to process SynthLang code. Please check your API key and try again.');
  }
};

// Helper function to check if OpenRouter is available
export const checkOpenRouterAvailability = async (apiKey: string): Promise<boolean> => {
  try {
    const response = await fetch('https://openrouter.ai/api/v1/auth/key', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'HTTP-Referer': window.location.origin,
        'X-Title': 'SynthLang Playground'
      }
    });

    return response.ok;
  } catch (error) {
    console.error('Failed to check OpenRouter availability:', error);
    return false;
  }
};

// Helper function to get available models
export const getAvailableModels = async (apiKey: string) => {
  try {
    const response = await fetch('https://openrouter.ai/api/v1/models', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'HTTP-Referer': window.location.origin,
        'X-Title': 'SynthLang Playground'
      }
    });

    if (!response.ok) {
      throw new Error('Failed to fetch models');
    }

    const data = await response.json();
    return data.data || [];
  } catch (error) {
    console.error('Failed to fetch OpenRouter models:', error);
    return [];
  }
};
