import { useState, useCallback } from 'react';
import { SynthLangConfig } from '../components/AdvancedCalculator/types';

interface ComparisonMetrics {
  tokenEfficiency: number;  // Ratio of output tokens to input tokens
  processingSpeed: number;  // Tokens per second
  memoryUsage: number;     // MB per request
  costEfficiency: number;  // Cost per 1k tokens
  optimizationScore: number; // 0-100 score based on enabled optimizations
  frameworkUtilization: number; // % of framework features utilized
}

interface ComparisonResult {
  metrics: ComparisonMetrics;
  recommendations: string[];
  potentialImprovements: {
    category: string;
    current: number;
    potential: number;
    suggestion: string;
  }[];
}

export function useConfigComparison(baseConfig: SynthLangConfig, compareConfig?: SynthLangConfig) {
  const [results, setResults] = useState<ComparisonResult | null>(null);

  const analyzeConfig = useCallback((config: SynthLangConfig): ComparisonMetrics => {
    // Calculate optimization score based on enabled features
    const optimizations = Object.values(config.optimizations).filter(Boolean).length;
    const maxOptimizations = Object.keys(config.optimizations).length;
    const optimizationScore = (optimizations / maxOptimizations) * 100;

    // Calculate framework utilization
    const enabledFrameworks = Object.entries(config.frameworks)
      .filter(([_, state]) => state.enabled).length;
    const totalFrameworks = Object.keys(config.frameworks).length;
    const frameworkUtilization = (enabledFrameworks / totalFrameworks) * 100;

    // Calculate token efficiency based on model and settings
    const baseEfficiency = config.model.includes('gpt-4') ? 1.4 : 1.2;
    const compressionBonus = config.optimizations.compression ? 0.3 : 0;
    const tokenEfficiency = baseEfficiency + compressionBonus;

    // Calculate processing speed based on model and optimizations
    const baseSpeed = config.model.includes('gpt-4') ? 15 : 30;
    const batchBonus = config.optimizations.batchProcessing ? 10 : 0;
    const cacheBonus = config.optimizations.caching ? 5 : 0;
    const processingSpeed = baseSpeed + batchBonus + cacheBonus;

    // Calculate memory usage based on context size and optimizations
    const baseMemory = (config.contextSize / 1024) * 2; // 2MB per 1K tokens base
    const memoryOptimization = config.optimizations.compression ? 0.7 : 1;
    const memoryUsage = baseMemory * memoryOptimization;

    // Calculate cost efficiency
    const baseCost = 0.0045; // Base cost per 1k tokens
    const optimizationDiscount = optimizationScore / 100 * 0.3; // Up to 30% discount
    const costEfficiency = baseCost * (1 - optimizationDiscount);

    return {
      tokenEfficiency,
      processingSpeed,
      memoryUsage,
      costEfficiency,
      optimizationScore,
      frameworkUtilization
    };
  }, []);

  const generateRecommendations = useCallback((metrics: ComparisonMetrics, config: SynthLangConfig): string[] => {
    const recommendations: string[] = [];

    if (metrics.optimizationScore < 70) {
      recommendations.push('Enable more optimizations to improve performance');
    }
    if (metrics.frameworkUtilization < 50) {
      recommendations.push('Consider utilizing more SynthLang frameworks for better expressiveness');
    }
    if (!config.optimizations.compression) {
      recommendations.push('Enable token compression to reduce costs');
    }
    if (!config.optimizations.batchProcessing && metrics.processingSpeed < 25) {
      recommendations.push('Enable batch processing to improve throughput');
    }
    if (config.contextSize > 8192 && !config.optimizations.compression) {
      recommendations.push('Large context size detected: enable compression to reduce memory usage');
    }

    return recommendations;
  }, []);

  const calculateImprovements = useCallback((metrics: ComparisonMetrics, config: SynthLangConfig) => {
    const improvements = [];

    // Token efficiency improvements
    improvements.push({
      category: 'Token Efficiency',
      current: metrics.tokenEfficiency,
      potential: metrics.tokenEfficiency * 1.5,
      suggestion: 'Enable compression and optimize framework usage'
    });

    // Processing speed improvements
    improvements.push({
      category: 'Processing Speed',
      current: metrics.processingSpeed,
      potential: metrics.processingSpeed * 1.8,
      suggestion: 'Enable batch processing and caching'
    });

    // Cost efficiency improvements
    improvements.push({
      category: 'Cost Efficiency',
      current: metrics.costEfficiency,
      potential: metrics.costEfficiency * 0.6,
      suggestion: 'Optimize context size and enable all cost-saving features'
    });

    return improvements;
  }, []);

  const compareConfigs = useCallback(() => {
    const baseMetrics = analyzeConfig(baseConfig);
    const recommendations = generateRecommendations(baseMetrics, baseConfig);
    const improvements = calculateImprovements(baseMetrics, baseConfig);

    setResults({
      metrics: baseMetrics,
      recommendations,
      potentialImprovements: improvements
    });
  }, [baseConfig, analyzeConfig, generateRecommendations, calculateImprovements]);

  return {
    results,
    compareConfigs
  };
}
