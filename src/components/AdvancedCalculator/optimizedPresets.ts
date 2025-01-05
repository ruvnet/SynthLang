import { PresetConfiguration } from "./presetTypes";
import { v4 as uuidv4 } from "uuid";

export const optimizedPresets: PresetConfiguration[] = [
  {
    id: uuidv4(),
    name: "GPT-4O",
    description: "High-performance configuration using GPT-4O",
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
        contextWindow: 8192,
        responseFormat: "json"
      }
    },
    metadata: {
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      tags: ["gpt-4o", "performance", "optimized"]
    }
  },
  {
    id: uuidv4(),
    name: "O1-Mini",
    description: "Fast and efficient using O1-Mini",
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
        contextWindow: 4096,
        responseFormat: "json"
      }
    },
    metadata: {
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      tags: ["o1", "efficient", "fast"]
    }
  },
  {
    id: uuidv4(),
    name: "O1-Preview",
    description: "Advanced performance using O1-Preview",
    settings: {
      model: "o1-preview",
      temperature: 0.6,
      maxTokens: 8192,
      topP: 0.85,
      frequencyPenalty: 0.25,
      presencePenalty: 0.25,
      customSettings: {
        streamingEnabled: true,
        cacheEnabled: true,
        adaptiveProcessing: true,
        contextWindow: 8192,
        responseFormat: "json"
      }
    },
    metadata: {
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      tags: ["o1", "preview", "performance"]
    }
  },
  {
    id: uuidv4(),
    name: "Balanced GPT-4",
    description: "Balanced configuration for general use",
    settings: {
      model: "gpt-4",
      temperature: 0.6,
      maxTokens: 4096,
      topP: 0.85,
      frequencyPenalty: 0.25,
      presencePenalty: 0.25,
      customSettings: {
        streamingEnabled: true,
        cacheEnabled: true,
        adaptiveProcessing: true,
        contextWindow: 4096,
        responseFormat: "json"
      }
    },
    metadata: {
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      tags: ["gpt-4", "balanced", "recommended"]
    }
  }
];

// Function to create a new preset from an existing one
export const createPresetFromExisting = (
  preset: PresetConfiguration,
  newName: string,
  newDescription: string
): PresetConfiguration => {
  return {
    ...preset,
    id: uuidv4(),
    name: newName,
    description: newDescription,
    metadata: {
      ...preset.metadata,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      tags: [...(preset.metadata.tags || []), "custom"]
    }
  };
};
