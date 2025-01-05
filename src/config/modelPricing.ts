export interface ModelPricing {
  input: number;
  output: number;
  contextWindow: number;
}

export const MODEL_PRICING: Record<string, ModelPricing> = {
  "gpt-4": {
    input: 0.03,
    output: 0.06,
    contextWindow: 8192
  },
  "gpt-4-32k": {
    input: 0.06,
    output: 0.12,
    contextWindow: 32768
  },
  "gpt-3.5-turbo": {
    input: 0.0015,
    output: 0.002,
    contextWindow: 4096
  },
  "gpt-3.5-turbo-16k": {
    input: 0.003,
    output: 0.004,
    contextWindow: 16384
  },
  "claude-2": {
    input: 0.008,
    output: 0.024,
    contextWindow: 100000
  },
  "claude-instant-1": {
    input: 0.0008,
    output: 0.0024,
    contextWindow: 100000
  },
  "palm-2": {
    input: 0.0005,
    output: 0.0005,
    contextWindow: 8192
  }
};
