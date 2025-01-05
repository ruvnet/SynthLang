import React from 'react';
import { Card, CardContent } from '../ui/card';
import { Progress } from '../ui/progress';
import { SynthLangConfig } from './types';

interface MetricsDisplayProps {
  config: SynthLangConfig;
  metrics?: {
    tokenUsage: number;
    processingSpeed: number;
    costEfficiency: number;
    optimizationScore: number;
    timestamp: number;
  };
}

export const MetricsDisplay: React.FC<MetricsDisplayProps> = ({ config, metrics = {
  tokenUsage: 0,
  processingSpeed: 0,
  costEfficiency: 0,
  optimizationScore: 0,
  timestamp: Date.now()
} }) => {
  const formatMetric = (value: number, type: string) => {
    switch (type) {
      case 'tokens':
        return `${value.toLocaleString()} tokens`;
      case 'speed':
        return `${value.toFixed(1)} tok/s`;
      case 'cost':
        return `$${value.toFixed(4)}/1k tokens`;
      case 'score':
        return `${value}%`;
      default:
        return value.toString();
    }
  };

  const renderMetricCard = (title: string, value: number, type: string, colorClass: string) => (
    <div className="bg-accent/10 p-4 rounded-lg">
      <h3 className="text-sm font-medium mb-2">{title}</h3>
      <div className={`text-2xl font-mono ${colorClass}`}>
        {formatMetric(value, type)}
      </div>
    </div>
  );

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 gap-4">
        {renderMetricCard('Token Usage', metrics.tokenUsage, 'tokens', 'text-blue-500')}
        {renderMetricCard('Processing Speed', metrics.processingSpeed, 'speed', 'text-green-500')}
        {renderMetricCard('Cost Efficiency', metrics.costEfficiency, 'cost', 'text-yellow-500')}
        {renderMetricCard('Optimization Score', metrics.optimizationScore, 'score', 'text-purple-500')}
      </div>

      <Card>
        <CardContent className="pt-6">
          <div className="space-y-4">
            <div>
              <div className="flex justify-between mb-2">
                <span className="text-sm font-medium">Token Usage</span>
                <span className="text-sm text-muted-foreground">
                  {formatMetric(metrics.tokenUsage, 'tokens')}
                </span>
              </div>
              <Progress value={Math.min((metrics.tokenUsage / config.contextSize) * 100, 100)} />
            </div>

            <div>
              <div className="flex justify-between mb-2">
                <span className="text-sm font-medium">Processing Speed</span>
                <span className="text-sm text-muted-foreground">
                  {formatMetric(metrics.processingSpeed, 'speed')}
                </span>
              </div>
              <Progress value={(metrics.processingSpeed / 60) * 100} />
            </div>

            <div>
              <div className="flex justify-between mb-2">
                <span className="text-sm font-medium">Cost Efficiency</span>
                <span className="text-sm text-muted-foreground">
                  {formatMetric(metrics.costEfficiency, 'cost')}
                </span>
              </div>
              <Progress value={(1 - metrics.costEfficiency / 0.002) * 100} />
            </div>

            <div>
              <div className="flex justify-between mb-2">
                <span className="text-sm font-medium">Optimization Score</span>
                <span className="text-sm text-muted-foreground">
                  {formatMetric(metrics.optimizationScore, 'score')}
                </span>
              </div>
              <Progress value={metrics.optimizationScore} />
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
