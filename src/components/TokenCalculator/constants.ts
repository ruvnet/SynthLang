// Default values for calculations
export const DEFAULT_TOKEN_COUNT = 100000;
export const DEFAULT_WORDS_PER_TOKEN = 0.75;
export const DEFAULT_CHARS_PER_TOKEN = 4;
export const DEFAULT_WORDS_PER_PAGE = 250;
export const DEFAULT_PROCESSING_TIME = 0.5; // ms/token
export const DEFAULT_BASE_LATENCY = 500; // ms
export const DEFAULT_OUTPUT_RATIO = 0.5; // 50% of input length
export const DEFAULT_OUTPUT_COST = 0.000060; // $ per token

// Features for the landing page
export const FEATURES = [
  {
    title: "Prompt Translation",
    description: "Convert standard prompts into optimized SynthLang format",
    icon: "Sparkles",
    link: "/translate",
    color: "text-purple-400"
  },
  {
    title: "Multi-Model Testing",
    description: "Test prompts across different models via OpenRouter",
    icon: "Gauge",
    link: "/test",
    color: "text-blue-400"
  },
  {
    title: "Cost Analytics",
    description: "Track token usage and cost savings across translations",
    icon: "DollarSign",
    link: "/analytics",
    color: "text-green-400"
  }
];

// Utility functions
export const formatTime = (ms: number): string => {
  return ms >= 1000 ? `${(ms/1000).toFixed(2)}s` : `${ms.toFixed(0)}ms`;
};

export const formatPercentage = (value: number, total: number): string => {
  return `${Math.round((value / total) * 100)}%`;
};

export const calculateTokens = (text: string): number => {
  return Math.ceil(text.length / DEFAULT_CHARS_PER_TOKEN);
};

export const calculateTokensFromWords = (words: number): number => {
  return Math.ceil(words / DEFAULT_WORDS_PER_TOKEN);
};

export const calculateTokensFromPages = (pages: number): number => {
  return calculateTokensFromWords(pages * DEFAULT_WORDS_PER_PAGE);
};

export const calculateLatency = (tokens: number): number => {
  return DEFAULT_BASE_LATENCY + (tokens * DEFAULT_PROCESSING_TIME);
};
