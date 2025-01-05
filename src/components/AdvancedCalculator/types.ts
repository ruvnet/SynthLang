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

export interface SynthLangConfig {
  model: string;
  contextSize: number;
  features: Record<string, boolean | string | number>;
  optimizations: Record<string, boolean>;
}

export interface TabData {
  id: string;
  label: string;
  description: string;
}
