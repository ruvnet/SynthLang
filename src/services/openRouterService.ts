import type { PlaygroundSettings } from '../components/Documentation/PlaygroundSettings';

interface OpenRouterResponse {
  choices: Array<{
    message: {
      content: string;
    };
  }>;
}

interface OpenRouterStreamChunk {
  choices: Array<{
    delta: {
      content?: string;
    };
  }>;
}

export const SYSTEM_PROMPT = {
  interpreter: `You are a SynthLang interpreter. Process the following SynthLang code according to these rules:

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

Process the input and provide output according to these rules.`,

  translator: `You are a SynthLang translator that converts standard prompts into SynthLang's hyper-efficient format. Follow these rules precisely:

[Framework Integration]
1. Mathematical Frameworks:
   - Use provided framework glyphs appropriately in the translation
   - Apply framework-specific notation where relevant
   - Maintain mathematical rigor according to each framework's rules
   - Preserve semantic relationships using framework symbols
   - Combine multiple frameworks coherently when specified

2. Optimization Frameworks:
   - Apply compression and optimization techniques to maximize efficiency
   - Use machine-level patterns for low-level optimization
   - Maintain semantic clarity while achieving maximum density
   - Combine optimization techniques coherently

3. Framework Combinations:
   - Integrate mathematical and optimization frameworks seamlessly
   - Use optimization techniques to enhance mathematical expressions
   - Preserve mathematical precision while maximizing efficiency
   - Apply framework-specific optimizations where appropriate

[Grammar Rules]
1. Task Glyphs:
   - ↹ (Focus/Filter) for main tasks and instructions
   - Σ (Summarize) for condensing information
   - ⊕ (Combine/Merge) for context and data integration
   - ? (Query/Clarify) for validation checks
   - IF for conditional operations

2. Subject Markers:
   - Use • before datasets (e.g., •customerData)
   - Use 花 for abstract concepts
   - Use 山 for hierarchical structures

3. Modifiers:
   - ^format(type) for output format
   - ^n for importance level
   - ^lang for language specification
   - ^t{n} for time constraints

4. Flow Control:
   - [p=n] for priority (1-5)
   - -> for sequential operations
   - + for parallel tasks
   - | for alternatives

[Translation Process]
1. Structure:
   - Start with model selection: ↹ model.{name}
   - Add format specification: ⊕ format(json)
   - Group related operations with []
   - Separate major sections with blank lines

2. Data Sources:
   - Convert datasets to •name format
   - Link related data with :
   - Use ⊕ to merge multiple sources
   - Add ^t{timeframe} for temporal data

3. Tasks:
   - Convert objectives to task glyphs
   - Add priority levels based on impact
   - Chain dependent operations with ->
   - Group parallel tasks with +
   - Use ? for validation steps

4. Optimization:
   - Remove articles (a, an, the)
   - Convert verbose phrases to symbols
   - Use abbreviations (e.g., cfg, eval, impl)
   - Maintain semantic relationships
   - Group similar operations
   - Chain related analyses

Convert the input to SynthLang format, focusing on maximum efficiency while preserving critical information.`
};

export const callOpenRouter = async (
  code: string, 
  settings: PlaygroundSettings, 
  apiKey: string,
  mode: 'interpreter' | 'translator' = 'interpreter',
  frameworkInstructions?: string,
  onStream?: (chunk: string) => void
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
            content: frameworkInstructions || settings.systemPrompt || SYSTEM_PROMPT[mode]
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
        stream: !!onStream
      })
    });

    if (!response.ok) {
      const error = await response.json();
      if (error.error?.message?.includes('insufficient_quota')) {
        throw new Error('Insufficient credits. Please check your OpenRouter account.');
      } else if (error.error?.message?.includes('invalid_api_key')) {
        throw new Error('Invalid API key. Please check your API key in Settings.');
      } else if (error.error?.message?.includes('model_not_available')) {
        throw new Error('Selected model is not available. Please choose a different model.');
      }
      throw new Error(error.error?.message || 'Failed to process SynthLang code');
    }

    if (onStream) {
      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      let fullContent = '';

      if (!reader) {
        throw new Error('Stream not available');
      }

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ') && line !== 'data: [DONE]') {
            try {
              const data: OpenRouterStreamChunk = JSON.parse(line.slice(6));
              const content = data.choices[0]?.delta?.content;
              if (content) {
                fullContent += content;
                onStream(content);
              }
            } catch (e) {
              console.error('Failed to parse stream chunk:', e);
            }
          }
        }
      }

      return fullContent;
    } else {
      const data: OpenRouterResponse = await response.json();
      const content = data.choices[0]?.message?.content;
      
      if (!content) {
        throw new Error('No response received from the model. Please try again.');
      }

      return content;
    }
  } catch (error) {
    console.error('OpenRouter API error:', error);
    if (error instanceof Error) {
      throw error; // Re-throw specific errors
    }
    throw new Error('Failed to process SynthLang code. Please check your connection and try again.');
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

    if (!response.ok) {
      const error = await response.json();
      if (error.error?.message?.includes('invalid_api_key')) {
        throw new Error('Invalid API key');
      }
    }

    return response.ok;
  } catch (error) {
    console.error('Failed to check OpenRouter availability:', error);
    if (error instanceof Error && error.message === 'Invalid API key') {
      throw error;
    }
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
