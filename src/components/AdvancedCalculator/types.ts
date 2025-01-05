export interface SynthLangConfig {
  model: string;
  contextSize: number;
  features: SynthLangFeatures;
  optimizations: OptimizationConfig;
  frameworks: FrameworksConfig;
  customFrameworks: Framework[];
}

export interface SynthLangFeatures {
  responseFormat: ResponseFormat;
  temperature: number;
  streamingMode: boolean;
  contextWindow: number;
  customPrompt: string;
  [key: string]: string | number | boolean;
}

export interface OptimizationConfig {
  compression: boolean;
  caching: boolean;
  batchProcessing: boolean;
  contextPruning: boolean;
  streamOptimization: boolean;
  [key: string]: boolean;
}

export interface FrameworksConfig {
  [key: string]: FrameworkState;
}

export interface FrameworkState {
  enabled: boolean;
  selectedGlyphs: string[];
  customGlyphs: string[];
}

export type ResponseFormat = 'json' | 'markdown' | 'text' | 'custom';

export interface Framework {
  id: string;
  name: string;
  description: string;
  details: string;
  applications: string[];
  glyphs: Glyph[];
  examples: string[];
  group: FrameworkGroup;
}

export interface Glyph {
  symbol: string;
  name: string;
  description: string;
  usage: string;
}

export interface GlyphInfo extends Glyph {
  id: string;
  category?: string;
}

export type FrameworkGroup = 
  | 'mathematical'
  | 'logographic'
  | 'semitic'
  | 'classical'
  | 'constructed'
  | 'optimization';

export interface MetricsData {
  tokenUsage: number;
  processingSpeed: number;
  costEfficiency: number;
  optimizationScore: number;
  timestamp: number;
}

export interface TabData {
  id: string;
  label: string;
  description?: string;
}

export interface FeatureOption {
  id: string;
  name: string;
  description: string;
  type: 'boolean' | 'number' | 'string';
  defaultValue: string | number | boolean;
}
