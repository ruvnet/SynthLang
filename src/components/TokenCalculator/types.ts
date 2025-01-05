import { ModelSpec } from "../../config/modelSearch";

export interface TokenMetrics {
  originalTokens: number;
  optimizedTokens: number;
  improvementFactor: number;  // e.g., 3.33×
  percentageIncrease: number; // e.g., 233%
  modelCosts: {
    [key: string]: {
      original: number;
      optimized: number;
      savings: number;
      savingsPercent: number;
    };
  };
}

export interface CalculatorProps {
  tokenCount: number;
  promptText: string;
  tokenMetrics: TokenMetrics | null;
  selectedModel: string;
  onTokenCountChange: (count: number) => void;
  onPromptChange: (text: string) => void;
}

export interface ModelSelectorProps {
  selectedModel: string;
  onModelSelect: (model: string) => void;
  availableModels: Record<string, ModelSpec>;
}

export interface TokenInputProps {
  tokenCount: number;
  onTokenCountChange: (count: number) => void;
  onWordsChange: (words: number) => void;
  onPagesChange: (pages: number) => void;
}

export interface SpeedMetricsProps {
  tokenMetrics: TokenMetrics | null;
  processingTime: number;
  baseLatency: number;
  onProcessingTimeChange: (time: number) => void;
  onBaseLatencyChange: (latency: number) => void;
}

export interface OutputMetricsProps {
  tokenMetrics: TokenMetrics | null;
  selectedModel: string;
  availableModels: Record<string, ModelSpec>;
  outputRatio: number;
  outputCost: number;
  onOutputRatioChange: (ratio: number) => void;
  onOutputCostChange: (cost: number) => void;
}

export interface MetricsDisplayProps {
  tokenMetrics: TokenMetrics;
  selectedModel: string;
  availableModels: Record<string, ModelSpec>;
}
