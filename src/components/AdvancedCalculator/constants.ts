import { TabData, FeatureOption, SynthLangConfig } from './types';

export const CALCULATOR_TABS: TabData[] = [
  {
    id: 'basic',
    label: 'Basic Settings',
    description: 'Configure core SynthLang parameters and model selection'
  },
  {
    id: 'advanced',
    label: 'Advanced Features',
    description: 'Fine-tune language processing and optimization settings'
  },
  {
    id: 'optimization',
    label: 'Optimizations',
    description: 'Performance and efficiency settings'
  },
  {
    id: 'metrics',
    label: 'Metrics',
    description: 'View detailed performance and cost metrics'
  }
];

export const FEATURE_OPTIONS: FeatureOption[] = [
  {
    id: 'contextWindow',
    name: 'Context Window',
    description: 'Maximum number of tokens for context',
    defaultValue: 4096,
    type: 'number'
  },
  {
    id: 'temperature',
    name: 'Temperature',
    description: 'Controls randomness in output (0.0-1.0)',
    defaultValue: 0.7,
    type: 'number'
  },
  {
    id: 'streamingMode',
    name: 'Streaming Mode',
    description: 'Enable token streaming for real-time output',
    defaultValue: true,
    type: 'boolean'
  },
  {
    id: 'customPrompt',
    name: 'Custom Prompt',
    description: 'Custom system prompt override',
    defaultValue: '',
    type: 'string'
  }
];

export const OPTIMIZATION_OPTIONS: FeatureOption[] = [
  {
    id: 'caching',
    name: 'Response Caching',
    description: 'Cache responses for improved performance',
    defaultValue: true,
    type: 'boolean'
  },
  {
    id: 'batchProcessing',
    name: 'Batch Processing',
    description: 'Process multiple requests in batches',
    defaultValue: false,
    type: 'boolean'
  },
  {
    id: 'compression',
    name: 'Token Compression',
    description: 'Compress tokens for reduced API costs',
    defaultValue: true,
    type: 'boolean'
  }
];

export const DEFAULT_CONFIG: SynthLangConfig = {
  model: 'gpt-4',
  contextSize: 4096,
  features: {
    contextWindow: 4096,
    temperature: 0.7,
    streamingMode: true,
    customPrompt: ''
  },
  optimizations: {
    caching: true,
    batchProcessing: false,
    compression: true
  }
};
