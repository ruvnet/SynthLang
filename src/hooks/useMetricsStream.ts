import { useState, useCallback, useEffect } from 'react';
import { SynthLangConfig } from '../components/AdvancedCalculator/types';

interface MetricsData {
  tokenUsage: number;
  processingSpeed: number;
  costEfficiency: number;
  optimizationScore: number;
  timestamp: number;
}

export function useMetricsStream(config: SynthLangConfig) {
  const [isStreaming, setIsStreaming] = useState(false);
  const [metrics, setMetrics] = useState<MetricsData>({
    tokenUsage: 0,
    processingSpeed: 0,
    costEfficiency: 0,
    optimizationScore: 0,
    timestamp: Date.now()
  });

  const calculateMetrics = useCallback(() => {
    // Calculate token usage based on context size and optimizations
    const baseTokens = config.contextSize;
    const compressionFactor = config.optimizations.compression ? 0.7 : 1;
    const tokenUsage = Math.round(baseTokens * compressionFactor);

    // Calculate processing speed based on optimizations
    const baseSpeed = 30; // tokens per second
    const batchBonus = config.optimizations.batchProcessing ? 15 : 0;
    const cacheBonus = config.optimizations.caching ? 10 : 0;
    const streamBonus = config.optimizations.streamOptimization ? 5 : 0;
    const processingSpeed = baseSpeed + batchBonus + cacheBonus + streamBonus;

    // Calculate cost efficiency (cost per 1k tokens)
    const baseCost = 0.002; // $0.002 per 1k tokens
    const optimizationDiscount = 
      (config.optimizations.compression ? 0.1 : 0) +
      (config.optimizations.caching ? 0.05 : 0) +
      (config.optimizations.contextPruning ? 0.05 : 0);
    const costEfficiency = baseCost * (1 - optimizationDiscount);

    // Calculate overall optimization score (0-100)
    const enabledOptimizations = Object.values(config.optimizations).filter(Boolean).length;
    const totalOptimizations = Object.keys(config.optimizations).length;
    const optimizationScore = Math.round((enabledOptimizations / totalOptimizations) * 100);

    return {
      tokenUsage,
      processingSpeed,
      costEfficiency,
      optimizationScore,
      timestamp: Date.now()
    };
  }, [config]);

  useEffect(() => {
    let interval: NodeJS.Timeout;

    if (isStreaming) {
      // Initial calculation
      setMetrics(calculateMetrics());

      // Update metrics every second
      interval = setInterval(() => {
        setMetrics(prev => ({
          ...calculateMetrics(),
          // Add some random variation to make it look more realistic
          tokenUsage: prev.tokenUsage + Math.floor(Math.random() * 100 - 50),
          processingSpeed: prev.processingSpeed + Math.floor(Math.random() * 4 - 2),
          costEfficiency: prev.costEfficiency * (1 + (Math.random() * 0.02 - 0.01))
        }));
      }, 1000);
    }

    return () => {
      if (interval) {
        clearInterval(interval);
      }
    };
  }, [isStreaming, calculateMetrics]);

  const startStreaming = useCallback(() => {
    setIsStreaming(true);
  }, []);

  const stopStreaming = useCallback(() => {
    setIsStreaming(false);
  }, []);

  return {
    metrics,
    isStreaming,
    startStreaming,
    stopStreaming
  };
}
