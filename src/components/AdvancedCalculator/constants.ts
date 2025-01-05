import { TabData, FeatureOption, SynthLangConfig, OptimizationConfig, FrameworksConfig, SynthLangFeatures, Framework } from './types';

export const CALCULATOR_TABS: TabData[] = [
  { id: 'presets', label: 'Presets' },
  { id: 'basic', label: 'Basic' },
  { id: 'frameworks', label: 'Frameworks' },
  { id: 'advanced', label: 'Advanced' },
  { id: 'optimization', label: 'Optimization' },
  { id: 'metrics', label: 'Metrics' }
];

export const DEFAULT_FRAMEWORKS_CONFIG: FrameworksConfig = {
  mathematical: {
    enabled: false,
    selectedGlyphs: [],
    customGlyphs: []
  },
  logographic: {
    enabled: false,
    selectedGlyphs: [],
    customGlyphs: []
  },
  semitic: {
    enabled: false,
    selectedGlyphs: [],
    customGlyphs: []
  },
  classical: {
    enabled: false,
    selectedGlyphs: [],
    customGlyphs: []
  },
  constructed: {
    enabled: false,
    selectedGlyphs: [],
    customGlyphs: []
  },
  optimization: {
    enabled: false,
    selectedGlyphs: [],
    customGlyphs: []
  }
};

export const DEFAULT_CONFIG: SynthLangConfig = {
  model: 'gpt-4',
  contextSize: 8192,
  features: {
    responseFormat: 'json',
    temperature: 0.7,
    streamingMode: true,
    contextWindow: 4096,
    customPrompt: ''
  },
  optimizations: {
    compression: false,
    caching: false,
    batchProcessing: false,
    contextPruning: false,
    streamOptimization: false
  },
  frameworks: DEFAULT_FRAMEWORKS_CONFIG,
  customFrameworks: []
};

export const FEATURE_OPTIONS: FeatureOption[] = [
  {
    id: 'temperature',
    name: 'Temperature',
    description: 'Controls randomness in the output. Higher values make the output more diverse.',
    type: 'number',
    defaultValue: 0.7
  },
  {
    id: 'streamingMode',
    name: 'Streaming Mode',
    description: 'Enable token-by-token streaming for real-time output.',
    type: 'boolean',
    defaultValue: true
  },
  {
    id: 'contextWindow',
    name: 'Context Window',
    description: 'Maximum number of tokens to consider for context.',
    type: 'number',
    defaultValue: 4096
  },
  {
    id: 'customPrompt',
    name: 'Custom Prompt',
    description: 'Custom system prompt to override defaults.',
    type: 'string',
    defaultValue: ''
  }
];

export const OPTIMIZATION_OPTIONS = [
  {
    id: 'compression',
    name: 'Token Compression',
    description: 'Compress tokens to reduce API costs and improve performance'
  },
  {
    id: 'caching',
    name: 'Response Caching',
    description: 'Cache responses to improve performance and reduce costs'
  },
  {
    id: 'batchProcessing',
    name: 'Batch Processing',
    description: 'Process multiple requests in batches for better efficiency'
  },
  {
    id: 'contextPruning',
    name: 'Context Pruning',
    description: 'Automatically prune context to optimize token usage'
  },
  {
    id: 'streamOptimization',
    name: 'Stream Optimization',
    description: 'Optimize streaming performance and reliability'
  }
];
