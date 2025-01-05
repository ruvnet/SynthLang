export interface GlyphInfo {
  symbol: string;
  name: string;
  description: string;
  usage: string;
}

export interface Framework {
  id: string;
  name: string;
  description: string;
  details: string;
  applications: string[];
  glyphs: GlyphInfo[];
  examples: string[];
  group: 'mathematical' | 'logographic' | 'semitic' | 'classical' | 'constructed' | 'optimization';
}

export interface FrameworkState {
  enabled: boolean;
  selectedGlyphs: string[];
  customGlyphs: GlyphInfo[];
}

export interface FrameworksConfig {
  [key: string]: FrameworkState;
}

export interface MetricData {
  value: number;
  label: string;
  description: string;
}

export interface FeatureOption {
  id: string;
  name: string;
  description: string;
  defaultValue: boolean | string | number;
  type: 'boolean' | 'string' | 'number';
}

export type ResponseFormat = 'json' | 'markdown' | 'text' | 'custom';

export interface SynthLangFeatures {
  temperature: number;
  streamingMode: boolean;
  contextWindow: number;
  customPrompt: string;
  responseFormat: ResponseFormat;
  [key: string]: string | number | boolean | ResponseFormat;
}

export interface SynthLangConfig {
  model: string;
  contextSize: number;
  features: SynthLangFeatures;
  optimizations: Record<string, boolean>;
  frameworks: FrameworksConfig;
  customFrameworks: Framework[];
}

export interface TabData {
  id: string;
  label: string;
  description: string;
}
