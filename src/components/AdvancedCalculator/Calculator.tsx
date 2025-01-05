import React from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Switch } from '../ui/switch';
import { Slider } from '../ui/slider';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { CALCULATOR_TABS, FEATURE_OPTIONS, OPTIMIZATION_OPTIONS, DEFAULT_CONFIG } from './constants';
import { SynthLangConfig } from './types';

export function AdvancedCalculator() {
  const [config, setConfig] = React.useState<SynthLangConfig>(DEFAULT_CONFIG);

  const handleFeatureChange = (id: string, value: boolean | string | number) => {
    setConfig(prev => ({
      ...prev,
      features: {
        ...prev.features,
        [id]: value
      }
    }));
  };

  const handleOptimizationChange = (id: string, value: boolean) => {
    setConfig(prev => ({
      ...prev,
      optimizations: {
        ...prev.optimizations,
        [id]: value
      }
    }));
  };

  return (
    <div className="w-full max-w-4xl mx-auto p-4 space-y-4">
      <Card>
        <CardHeader>
          <CardTitle>Advanced SynthLang Calculator</CardTitle>
          <CardDescription>
            Configure and optimize your SynthLang implementation with advanced settings and features
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="basic" className="w-full">
            <TabsList className="grid w-full grid-cols-4">
              {CALCULATOR_TABS.map((tab) => (
                <TabsTrigger key={tab.id} value={tab.id}>
                  {tab.label}
                </TabsTrigger>
              ))}
            </TabsList>

            <TabsContent value="basic" className="space-y-4">
              <div className="grid gap-4">
                <div className="space-y-2">
                  <Label>Model Selection</Label>
                  <Input
                    value={config.model}
                    onChange={(e) => setConfig(prev => ({ ...prev, model: e.target.value }))}
                    placeholder="Select model..."
                  />
                </div>
                <div className="space-y-2">
                  <Label>Context Size</Label>
                  <Input
                    type="number"
                    value={config.contextSize}
                    onChange={(e) => setConfig(prev => ({ ...prev, contextSize: parseInt(e.target.value) }))}
                  />
                </div>
              </div>
            </TabsContent>

            <TabsContent value="advanced" className="space-y-4">
              {FEATURE_OPTIONS.map((feature) => (
                <div key={feature.id} className="flex items-center justify-between space-x-4">
                  <div>
                    <Label>{feature.name}</Label>
                    <p className="text-sm text-gray-500">{feature.description}</p>
                  </div>
                  {feature.type === 'boolean' ? (
                    <Switch
                      checked={config.features[feature.id] as boolean}
                      onCheckedChange={(checked) => handleFeatureChange(feature.id, checked)}
                    />
                  ) : feature.type === 'number' ? (
                    <Slider
                      value={[config.features[feature.id] as number]}
                      onValueChange={([value]) => handleFeatureChange(feature.id, value)}
                      max={feature.id === 'temperature' ? 1 : 8192}
                      step={feature.id === 'temperature' ? 0.1 : 1}
                      className="w-[200px]"
                    />
                  ) : (
                    <Input
                      value={config.features[feature.id] as string}
                      onChange={(e) => handleFeatureChange(feature.id, e.target.value)}
                      className="w-[200px]"
                    />
                  )}
                </div>
              ))}
            </TabsContent>

            <TabsContent value="optimization" className="space-y-4">
              {OPTIMIZATION_OPTIONS.map((opt) => (
                <div key={opt.id} className="flex items-center justify-between space-x-4">
                  <div>
                    <Label>{opt.name}</Label>
                    <p className="text-sm text-gray-500">{opt.description}</p>
                  </div>
                  <Switch
                    checked={config.optimizations[opt.id]}
                    onCheckedChange={(checked) => handleOptimizationChange(opt.id, checked)}
                  />
                </div>
              ))}
            </TabsContent>

            <TabsContent value="metrics" className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <Card>
                  <CardHeader>
                    <CardTitle>Performance Metrics</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-gray-500">Placeholder for performance metrics</p>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader>
                    <CardTitle>Cost Analysis</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-gray-500">Placeholder for cost analysis</p>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  );
}
