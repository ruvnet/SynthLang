import { PresetConfiguration } from "./presetTypes";

export const optimizedPresets: PresetConfiguration[] = [
  {
    id: "gpt4o-performance",
    name: "GPT-4o Performance",
    description: "High-performance configuration optimized for complex tasks",
    settings: {
      model: "gpt-4o",
      temperature: 0.7,
      maxTokens: 8192,
      topP: 0.9,
      frequencyPenalty: 0.3,
      presencePenalty: 0.3,
      customSettings: {
        streamingEnabled: true,
        cacheEnabled: true,
        parallelProcessing: true,
        customPrompt: `↹ model.gpt-4o @openrouter
⊕ context(8192) ^format(json)

# Optimizations
⊕ optimize [
  temperature: 0.7,
  streaming: true,
  cache: true,
  parallel: true
]

# Features
⊕ features [
  contextWindow: 8192,
  topP: 0.9,
  frequencyPenalty: 0.3,
  presencePenalty: 0.3
]`
      }
    },
    metadata: {
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      tags: ["gpt-4o", "performance", "high-throughput"]
    }
  },
  {
    id: "gpt4o-creative",
    name: "GPT-4O Creative",
    description: "Optimized for creative writing and content generation",
    settings: {
      model: "gpt-4o",
      temperature: 0.9,
      maxTokens: 8192,
      topP: 0.95,
      frequencyPenalty: 0.5,
      presencePenalty: 0.5,
      customSettings: {
        streamingEnabled: true,
        cacheEnabled: false,
        parallelProcessing: false,
        customPrompt: `↹ model.gpt-4o @openrouter
⊕ context(8192) ^format(markdown)

# Optimizations
⊕ optimize [
  temperature: 0.9,
  streaming: true,
  creative: true
]

# Features
⊕ features [
  contextWindow: 8192,
  topP: 0.95,
  frequencyPenalty: 0.5,
  presencePenalty: 0.5
]`
      }
    },
    metadata: {
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      tags: ["gpt-4o", "creative", "content"]
    }
  },
  {
    id: "o1-mini-fast",
    name: "O1-Mini Fast",
    description: "Ultra-fast responses optimized for quick interactions",
    settings: {
      model: "o1-mini",
      temperature: 0.5,
      maxTokens: 4096,
      topP: 0.8,
      frequencyPenalty: 0.2,
      presencePenalty: 0.2,
      customSettings: {
        streamingEnabled: true,
        cacheEnabled: true,
        batchProcessing: true,
        customPrompt: `↹ model.o1-mini @openrouter
⊕ context(4096) ^format(json)

# Optimizations
⊕ optimize [
  temperature: 0.5,
  streaming: true,
  cache: true,
  batch: true
]

# Features
⊕ features [
  contextWindow: 4096,
  topP: 0.8,
  frequencyPenalty: 0.2,
  presencePenalty: 0.2
]

# Efficiency
⊕ config [
  mode: "fast",
  priority: "speed",
  compression: true
]`
      }
    },
    metadata: {
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      tags: ["o1", "efficient", "fast"]
    }
  },
  {
    id: "o1-mini-balanced",
    name: "O1-Mini Balanced",
    description: "Balanced configuration for general-purpose use",
    settings: {
      model: "o1-mini",
      temperature: 0.7,
      maxTokens: 4096,
      topP: 0.9,
      frequencyPenalty: 0.3,
      presencePenalty: 0.3,
      customSettings: {
        streamingEnabled: true,
        cacheEnabled: true,
        batchProcessing: false,
        customPrompt: `↹ model.o1-mini @openrouter
⊕ context(4096) ^format(json)

# Optimizations
⊕ optimize [
  temperature: 0.7,
  streaming: true,
  cache: true
]

# Features
⊕ features [
  contextWindow: 4096,
  topP: 0.9,
  frequencyPenalty: 0.3,
  presencePenalty: 0.3
]

# Balance
⊕ config [
  mode: "balanced",
  priority: "quality"
]`
      }
    },
    metadata: {
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      tags: ["o1", "balanced", "general"]
    }
  },
  {
    id: "gpt4o-analytical",
    name: "GPT-4O Analytical",
    description: "Optimized for data analysis and logical reasoning",
    settings: {
      model: "gpt-4o",
      temperature: 0.3,
      maxTokens: 8192,
      topP: 0.8,
      frequencyPenalty: 0.2,
      presencePenalty: 0.2,
      customSettings: {
        streamingEnabled: false,
        cacheEnabled: true,
        parallelProcessing: true,
        customPrompt: `↹ model.gpt-4o @openrouter
⊕ context(8192) ^format(json)

# Optimizations
⊕ optimize [
  temperature: 0.3,
  precision: true,
  cache: true,
  parallel: true
]

# Features
⊕ features [
  contextWindow: 8192,
  topP: 0.8,
  frequencyPenalty: 0.2,
  presencePenalty: 0.2
]

# Analysis
⊕ config [
  mode: "analytical",
  priority: "precision"
]`
      }
    },
    metadata: {
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      tags: ["gpt-4o", "analytical", "precise"]
    }
  },
  {
    id: "o1-mini-interactive",
    name: "O1-Mini Interactive",
    description: "Optimized for real-time chat and interactive sessions",
    settings: {
      model: "o1-mini",
      temperature: 0.8,
      maxTokens: 2048,
      topP: 0.95,
      frequencyPenalty: 0.4,
      presencePenalty: 0.4,
      customSettings: {
        streamingEnabled: true,
        cacheEnabled: true,
        batchProcessing: false,
        customPrompt: `↹ model.o1-mini @openrouter
⊕ context(2048) ^format(markdown)

# Optimizations
⊕ optimize [
  temperature: 0.8,
  streaming: true,
  interactive: true
]

# Features
⊕ features [
  contextWindow: 2048,
  topP: 0.95,
  frequencyPenalty: 0.4,
  presencePenalty: 0.4
]

# Interactive
⊕ config [
  mode: "chat",
  priority: "responsiveness"
]`
      }
    },
    metadata: {
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      tags: ["o1", "interactive", "chat"]
    }
  }
];
