import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { SynthLangConfig } from './types';
import { useOpenRouterModels } from '../../hooks/useOpenRouterModels';

interface PreviewDisplayProps {
  config?: SynthLangConfig;
}

export const PreviewDisplay: React.FC<PreviewDisplayProps> = ({ config }) => {
  const { models, isLoading, error } = useOpenRouterModels();

  if (!config) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Preview</CardTitle>
          <CardDescription>No configuration loaded. Configure settings in the Calculator tab.</CardDescription>
        </CardHeader>
      </Card>
    );
  }

  const model = models?.find(m => m.id === config.model);

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader>
          <CardTitle>Model Configuration</CardTitle>
          <CardDescription>Current settings and optimizations</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <h3 className="font-semibold mb-2">Model Details</h3>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span>Model:</span>
                    <span className="font-mono">{model?.name || config.model}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Context Size:</span>
                    <span className="font-mono">{config.contextSize} tokens</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Temperature:</span>
                    <span className="font-mono">{config.features.temperature}</span>
                  </div>
                </div>
              </div>
              <div>
                <h3 className="font-semibold mb-2">Optimizations</h3>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span>Caching:</span>
                    <span className="font-mono">{config.optimizations.caching ? 'Enabled' : 'Disabled'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Batch Processing:</span>
                    <span className="font-mono">{config.optimizations.batchProcessing ? 'Enabled' : 'Disabled'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Compression:</span>
                    <span className="font-mono">{config.optimizations.compression ? 'Enabled' : 'Disabled'}</span>
                  </div>
                </div>
              </div>
            </div>

            <div>
              <h3 className="font-semibold mb-2">Generated SynthLang Prompt</h3>
              <pre className="text-sm bg-black/20 p-4 rounded overflow-x-auto">
                {`↹ model.${config.model} @openrouter
⊕ context(${config.contextSize}) ^format(${config.features.responseFormat})

# Settings
⊕ optimize [
  temperature: ${config.features.temperature},
  streaming: ${config.features.streamingMode},
  cache: ${config.optimizations.caching}
]

# Advanced
⊕ features [
  contextWindow: ${config.features.contextWindow},
  customPrompt: "${config.features.customPrompt}"
]

# Optimizations
⊕ config [
  batchProcessing: ${config.optimizations.batchProcessing},
  compression: ${config.optimizations.compression}
]`}
              </pre>
            </div>
          </div>
        </CardContent>
      </Card>

      {error && (
        <Card className="border-red-500">
          <CardHeader>
            <CardTitle className="text-red-500">Error</CardTitle>
            <CardDescription>{error}</CardDescription>
          </CardHeader>
        </Card>
      )}
    </div>
  );
};
