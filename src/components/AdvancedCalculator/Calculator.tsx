import React from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { CALCULATOR_TABS } from './constants';
import { PresetManager } from './PresetManager';
import { PreviewDisplay } from './PreviewDisplay';
import { ComparisonDisplay } from './ComparisonDisplay';
import { MetricsDisplay } from './MetricsDisplay';
import { SynthLangConfig } from './types';

export const AdvancedCalculator: React.FC = () => {
  const [config, setConfig] = React.useState<SynthLangConfig>({
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
    frameworks: {},
    customFrameworks: []
  });

  const getPreviewContent = React.useCallback(() => {
    return `# Configuration Preview
↹ Model: ${config.model}
↹ Context Size: ${config.contextSize}

# Features
⊕ Response Format: ${config.features.responseFormat}
⊕ Temperature: ${config.features.temperature}
⊕ Streaming Mode: ${config.features.streamingMode}
⊕ Context Window: ${config.features.contextWindow}

# Optimizations
⊕ Compression: ${config.optimizations.compression}
⊕ Caching: ${config.optimizations.caching}
⊕ Batch Processing: ${config.optimizations.batchProcessing}
⊕ Context Pruning: ${config.optimizations.contextPruning}
⊕ Stream Optimization: ${config.optimizations.streamOptimization}`;
  }, [config]);

  return (
    <div className="space-y-8">
      <Tabs defaultValue="presets">
        <TabsList>
          {CALCULATOR_TABS.map((tab) => (
            <TabsTrigger key={tab.id} value={tab.id}>
              {tab.label}
            </TabsTrigger>
          ))}
        </TabsList>

        <TabsContent value="presets" className="space-y-4">
          <PresetManager config={config} onConfigChange={setConfig} />
        </TabsContent>

        <TabsContent value="basic" className="space-y-4">
          <PreviewDisplay config={config} getPreviewContent={getPreviewContent} />
        </TabsContent>

        <TabsContent value="frameworks" className="space-y-4">
          <ComparisonDisplay config={config} />
        </TabsContent>

        <TabsContent value="metrics" className="space-y-4">
          <MetricsDisplay config={config} />
        </TabsContent>
      </Tabs>
    </div>
  );
};
