import { SynthLangConfig } from './types';

export interface PresetMetadata {
  id: string;
  name: string;
  description: string;
  createdAt: string;
  updatedAt: string;
}

export interface CalculatorPreset extends PresetMetadata {
  features: SynthLangConfig;
}

export interface PresetManagerState {
  presets: CalculatorPreset[];
  currentPreset: string | null;
  loading: boolean;
  error: string | null;
}

export interface PresetStorageData {
  presets: CalculatorPreset[];
  lastUpdated: string;
}

export const DEFAULT_PRESETS: CalculatorPreset[] = [
  {
    id: 'performance',
    name: 'Performance Mode',
    description: 'Optimized for maximum processing speed and efficiency',
    features: {
      model: 'gpt-4',
      contextSize: 8192,
      features: {
        contextWindow: 8192,
        temperature: 0.5,
        streamingMode: true,
        customPrompt: '',
        responseFormat: 'json'
      },
      optimizations: {
        caching: true,
        batchProcessing: true,
        compression: true,
        streamOptimization: true,
        contextPruning: true
      },
      frameworks: {},
      customFrameworks: []
    },
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  },
  {
    id: 'accuracy',
    name: 'High Accuracy Mode',
    description: 'Optimized for maximum precision and reliability',
    features: {
      model: 'gpt-4',
      contextSize: 32768,
      features: {
        contextWindow: 32768,
        temperature: 0.2,
        streamingMode: false,
        customPrompt: '',
        responseFormat: 'json'
      },
      optimizations: {
        caching: false,
        batchProcessing: false,
        compression: false,
        streamOptimization: false,
        contextPruning: false
      },
      frameworks: {},
      customFrameworks: []
    },
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  }
];
