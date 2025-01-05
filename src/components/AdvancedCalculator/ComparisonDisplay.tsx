import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Progress } from '../ui/progress';
import { SynthLangConfig } from './types';

interface ComparisonDisplayProps {
  config: SynthLangConfig;
}

interface OptimizationMetric {
  name: string;
  score: number;
  recommendation?: string;
}

export const ComparisonDisplay: React.FC<ComparisonDisplayProps> = ({ config }) => {
  const getOptimizationMetrics = React.useCallback((): OptimizationMetric[] => {
    const metrics: OptimizationMetric[] = [];

    // Context window utilization
    const contextScore = (config.features.contextWindow / config.contextSize) * 100;
    metrics.push({
      name: 'Context Utilization',
      score: contextScore,
      recommendation: contextScore > 80 
        ? 'Consider increasing context size for better performance'
        : contextScore < 30
        ? 'Context window could be reduced to save tokens'
        : undefined
    });

    // Temperature optimization
    const tempScore = config.features.temperature <= 0.7 ? 100 : (1 - config.features.temperature) * 100;
    metrics.push({
      name: 'Temperature Balance',
      score: tempScore,
      recommendation: tempScore < 70
        ? 'Lower temperature for more consistent outputs'
        : undefined
    });

    // Optimization features
    const optCount = Object.values(config.optimizations).filter(Boolean).length;
    const optScore = (optCount / Object.keys(config.optimizations).length) * 100;
    metrics.push({
      name: 'Optimization Coverage',
      score: optScore,
      recommendation: optScore < 60
        ? 'Enable more optimization features for better performance'
        : undefined
    });

    return metrics;
  }, [config]);

  const metrics = getOptimizationMetrics();
  const overallScore = metrics.reduce((acc, m) => acc + m.score, 0) / metrics.length;

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Overall Optimization Score</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            <Progress value={overallScore} className="h-4" />
            <p className="text-sm text-muted-foreground text-right">
              {Math.round(overallScore)}%
            </p>
          </div>
        </CardContent>
      </Card>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {metrics.map((metric) => (
          <Card key={metric.name}>
            <CardHeader>
              <CardTitle className="text-lg">{metric.name}</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <Progress value={metric.score} className="h-2" />
                <p className="text-sm text-muted-foreground">
                  Score: {Math.round(metric.score)}%
                </p>
                {metric.recommendation && (
                  <p className="text-sm text-yellow-500 mt-2">
                    Tip: {metric.recommendation}
                  </p>
                )}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};
