import React, { useEffect, useState } from 'react';
import { Play } from 'lucide-react';
import { useSettingsContext } from '../../services/settingsService';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from '../ui/card';
import { Button } from '../ui/button';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '../ui/dialog';
import { Switch } from '../ui/switch';
import { Slider } from '../ui/slider';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '../ui/accordion';
import { Textarea } from '../ui/textarea';
import { CALCULATOR_TABS, FEATURE_OPTIONS, OPTIMIZATION_OPTIONS, DEFAULT_CONFIG, FRAMEWORK_OPTIONS } from './constants';
import { SynthLangConfig, ResponseFormat } from './types';

interface AdvancedCalculatorProps {
  onTabChange?: (tab: string) => void;
}

export const AdvancedCalculator: React.FC<AdvancedCalculatorProps> = ({ onTabChange }) => {
  const [activeTab, setActiveTab] = useState('basic');
  const { settings } = useSettingsContext();
  const [config, setConfig] = React.useState<SynthLangConfig>(() => {
    // Try to load saved config from localStorage
    const savedConfig = localStorage.getItem('synthLang.calculatorConfig');
    if (savedConfig) {
      try {
        return JSON.parse(savedConfig);
      } catch (err) {
        console.error('Failed to parse saved config:', err);
      }
    }
    
    // Fall back to default config
    const defaultModel = Object.entries(settings.models)
      .find(([_, settings]) => settings.enabled)?.[0] || DEFAULT_CONFIG.model;
    
    return {
      ...DEFAULT_CONFIG,
      model: defaultModel,
      contextSize: settings.models[defaultModel]?.contextWindow || DEFAULT_CONFIG.contextSize
    };
  });

  // Load config when it changes in localStorage
  useEffect(() => {
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === 'synthLang.calculatorConfig' && e.newValue) {
        try {
          const newConfig = JSON.parse(e.newValue);
          setConfig(newConfig);
        } catch (err) {
          console.error('Failed to parse updated config:', err);
        }
      }
    };

    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, []);

  // Update context size when model changes
  useEffect(() => {
    const modelSettings = settings.models[config.model];
    if (modelSettings) {
      setConfig(prev => ({
        ...prev,
        contextSize: modelSettings.contextWindow
      }));
    }
  }, [config.model, settings.models]);

  const handleFeatureChange = (id: string, value: string | number | boolean) => {
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

  const handleFrameworkToggle = (id: string, enabled: boolean) => {
    setConfig(prev => ({
      ...prev,
      frameworks: {
        ...prev.frameworks,
        [id]: {
          ...prev.frameworks[id],
          enabled,
          selectedGlyphs: enabled ? prev.frameworks[id].selectedGlyphs : []
        }
      }
    }));
  };

  const handleGlyphToggle = (frameworkId: string, glyph: { symbol: string }) => {
    setConfig(prev => {
      const currentGlyphs = prev.frameworks[frameworkId].selectedGlyphs;
      const newGlyphs = currentGlyphs.includes(glyph.symbol)
        ? currentGlyphs.filter(g => g !== glyph.symbol)
        : [...currentGlyphs, glyph.symbol];
      
      return {
        ...prev,
        frameworks: {
          ...prev.frameworks,
          [frameworkId]: {
            ...prev.frameworks[frameworkId],
            selectedGlyphs: newGlyphs
          }
        }
      };
    });
  };

  const getPreviewContent = () => {
    const enabledFrameworks = Object.entries(config.frameworks)
      .filter(([_, state]) => state.enabled)
      .map(([id, state]) => {
        const framework = FRAMEWORK_OPTIONS.find(f => f.id === id)!;
        return `⊕ use ${framework.name} [
  glyphs: ${state.selectedGlyphs.join(' ')}
]`;
      })
      .join('\n');

    return `↹ model.${config.model} @openrouter
⊕ context(${config.contextSize}) ^format(${config.features.responseFormat})

# Frameworks
${enabledFrameworks}

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
]`;
  };

  const renderFrameworkSection = (title: string, group: string) => (
    <div>
      <h3 className="text-lg font-semibold mb-2">{title}</h3>
      <Accordion type="multiple" className="w-full space-y-2">
        {FRAMEWORK_OPTIONS.filter(f => f.group === group).map((framework) => (
          <AccordionItem key={framework.id} value={framework.id} className="border rounded-lg">
            <div className="flex items-center justify-between pr-4">
              <AccordionTrigger className="hover:no-underline flex-1">
                <div className="flex items-center gap-2">
                  <div className="font-semibold">{framework.name}</div>
                  <div className="text-sm text-muted-foreground">
                    ({framework.glyphs.map(g => g.symbol).join(' ')})
                  </div>
                </div>
              </AccordionTrigger>
              <Switch
                checked={config.frameworks[framework.id]?.enabled || false}
                onCheckedChange={(checked) => handleFrameworkToggle(framework.id, checked)}
              />
            </div>
            <AccordionContent>
              <div className="pt-2 pb-4 space-y-6">
                <div>
                  <p className="text-sm text-muted-foreground mb-2">
                    {framework.description}
                  </p>
                  <div className="space-y-4">
                    <div className="grid grid-cols-5 gap-2">
                      {framework.glyphs.map((glyph, i) => (
                        <div key={i} className="relative group">
                          <button
                            className={`w-full p-2 text-lg rounded transition-colors ${
                              config.frameworks[framework.id]?.selectedGlyphs.includes(glyph.symbol)
                                ? 'bg-primary text-primary-foreground'
                                : 'bg-accent/20 hover:bg-accent/40'
                            }`}
                            onClick={() => handleGlyphToggle(framework.id, glyph)}
                            disabled={!config.frameworks[framework.id]?.enabled}
                          >
                            {glyph.symbol}
                          </button>
                          <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 w-64 p-3 bg-popover text-popover-foreground text-sm rounded shadow-lg opacity-0 group-hover:opacity-100 transition-opacity z-50 pointer-events-none">
                            <div className="font-semibold">{glyph.name}</div>
                            <div className="text-xs mt-1">{glyph.description}</div>
                            <div className="text-xs mt-1 font-mono">{glyph.usage}</div>
                          </div>
                        </div>
                      ))}
                    </div>
                    <div className="text-sm text-muted-foreground">
                      Click glyphs to select/deselect them for use in your prompts. 
                      Hover over glyphs to see their descriptions and usage examples.
                    </div>
                  </div>
                </div>
                <div>
                  <h4 className="text-sm font-medium mb-2">Examples:</h4>
                  <div className="grid grid-cols-1 gap-2">
                    {framework.examples.map((example, i) => (
                      <div key={i} className="text-sm font-mono bg-accent/10 p-2 rounded">
                        {example}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </AccordionContent>
          </AccordionItem>
        ))}
      </Accordion>
    </div>
  );

  return (
    <div className="w-full space-y-4">
      <Card>
        <CardHeader>
          <CardTitle>Advanced SynthLang Calculator</CardTitle>
          <CardDescription>
            Configure and optimize your SynthLang implementation with advanced settings and features
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Tabs value={activeTab} onValueChange={(value) => {
            setActiveTab(value);
            onTabChange?.(value);
          }} className="w-full">
            <TabsList className="grid w-full grid-cols-6">
              {CALCULATOR_TABS.map((tab) => (
                <TabsTrigger key={tab.id} value={tab.id}>
                  {tab.label}
                </TabsTrigger>
              ))}
            </TabsList>

            <TabsContent value="basic" className="space-y-4">
              <div className="grid grid-cols-2 gap-8">
                <div className="space-y-4">
                  <div className="space-y-2">
                    <Label>Model Selection</Label>
                    <div className="space-y-1">
                      <select
                        className="w-full p-2 rounded-md border border-input bg-background"
                        value={config.model}
                        onChange={(e) => setConfig(prev => ({ ...prev, model: e.target.value }))}
                      >
                        {Object.entries(settings.models)
                          .filter(([_, modelSettings]) => modelSettings.enabled)
                          .map(([modelId, modelSettings]) => (
                            <option key={modelId} value={modelId}>
                              {modelId} ({(modelSettings.costPer1kTokens * 1000).toFixed(2)}¢/1k tokens)
                            </option>
                          ))}
                      </select>
                      <p className="text-xs text-muted-foreground">
                        Context Window: {settings.models[config.model]?.contextWindow.toLocaleString()} tokens
                      </p>
                    </div>
                  </div>
                  <div className="space-y-2">
                    <Label>Context Size</Label>
                    <div className="space-y-1">
                      <select
                        className="w-full p-2 rounded-md border border-input bg-background"
                        value={config.contextSize}
                        onChange={(e) => setConfig(prev => ({ ...prev, contextSize: parseInt(e.target.value) }))}
                      >
                        {[4096, 8192, 16384, 32768, 100000]
                          .filter(size => size <= (settings.models[config.model]?.contextWindow || 0))
                          .map(size => (
                            <option key={size} value={size}>
                              {(size / 1024).toFixed(0)}K tokens
                            </option>
                          ))}
                      </select>
                      <p className="text-xs text-muted-foreground">
                        Cost: ${((config.contextSize / 1000) * (settings.models[config.model]?.costPer1kTokens || 0)).toFixed(4)}/request
                      </p>
                    </div>
                  </div>
                  <div className="space-y-2">
                    <Label>Response Format</Label>
                    <select
                      className="w-full p-2 rounded-md border border-input bg-background"
                      value={config.features.responseFormat}
                      onChange={(e) => handleFeatureChange('responseFormat', e.target.value as ResponseFormat)}
                    >
                      <option value="json">JSON</option>
                      <option value="markdown">Markdown</option>
                      <option value="text">Plain Text</option>
                      <option value="custom">Custom Schema</option>
                    </select>
                  </div>
                </div>
                <div className="space-y-4">
                  <div className="bg-accent/20 p-4 rounded-lg">
                    <h4 className="text-sm font-medium mb-2">Real-time Metrics</h4>
                    <div className="grid grid-cols-2 gap-2 text-sm">
                      <div>Context Size:</div>
                      <div className="text-blue-400">{config.contextSize} tokens</div>
                      <div>Response Format:</div>
                      <div className="text-purple-400">{config.features.responseFormat}</div>
                      <div>Temperature:</div>
                      <div className="text-green-400">{config.features.temperature}</div>
                    </div>
                  </div>
                </div>
              </div>
            </TabsContent>

            <TabsContent value="frameworks" className="space-y-6">
              <div className="grid grid-cols-2 gap-6">
                <div className="space-y-4">
                  <Card>
                    <CardHeader>
                      <CardTitle>Mathematical Frameworks</CardTitle>
                      <CardDescription>Select frameworks and specialized glyphs for your prompts</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <Dialog>
                        <DialogTrigger asChild>
                          <button className="w-full p-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90">
                            Add New Framework
                          </button>
                        </DialogTrigger>
                        <DialogContent>
                          <DialogHeader>
                            <DialogTitle>Create New Framework</DialogTitle>
                            <DialogDescription>
                              Add a new mathematical framework to your SynthLang configuration.
                            </DialogDescription>
                          </DialogHeader>
                          <div className="space-y-4 py-4">
                            <div className="space-y-2">
                              <Label>Framework Name</Label>
                              <Input id="name" placeholder="Enter framework name" />
                            </div>
                            <div className="space-y-2">
                              <Label>Description</Label>
                              <Textarea
                                id="description"
                                placeholder="Describe your framework's purpose and use cases"
                                className="min-h-[100px]"
                              />
                            </div>
                          </div>
                          <DialogFooter>
                            <button
                              className="px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90"
                              onClick={() => {
                                const id = `custom_${Date.now()}`;
                                const name = (document.getElementById('name') as HTMLInputElement).value;
                                const description = (document.getElementById('description') as HTMLTextAreaElement).value;
                                
                                setConfig(prev => ({
                                  ...prev,
                                  customFrameworks: [
                                    ...prev.customFrameworks,
                                    {
                                      id,
                                      name: name || 'New Framework',
                                      description: description || 'Description of your framework',
                                      details: 'Detailed explanation of your framework',
                                      applications: [],
                                      glyphs: [],
                                      examples: [],
                                      group: 'mathematical'
                                    }
                                  ],
                                  frameworks: {
                                    ...prev.frameworks,
                                    [id]: {
                                      enabled: true,
                                      selectedGlyphs: [],
                                      customGlyphs: []
                                    }
                                  }
                                }));
                              }}
                            >
                              Create Framework
                            </button>
                          </DialogFooter>
                        </DialogContent>
                      </Dialog>
                      <div className="space-y-6">
                        {renderFrameworkSection('Mathematical Frameworks', 'mathematical')}
                        {renderFrameworkSection('Logographic Systems', 'logographic')}
                        {renderFrameworkSection('Semitic Scripts', 'semitic')}
                        {renderFrameworkSection('Classical Languages', 'classical')}
                        {renderFrameworkSection('Constructed Languages', 'constructed')}
                      </div>
                    </CardContent>
        <CardFooter>
          <Button 
            className="w-full flex items-center gap-2"
            onClick={() => {
              // Save current config
              localStorage.setItem('synthLang.calculatorConfig', JSON.stringify(config));
              
              // Switch to preview tab
              setActiveTab('preview');
              onTabChange?.('preview');
            }}
          >
            <Play className="w-4 h-4" />
            Generate Preview
          </Button>
        </CardFooter>
                  </Card>
                </div>
                <div className="space-y-4">
                  <Card>
                    <CardHeader>
                      <CardTitle>Preview</CardTitle>
                      <CardDescription>Generated SynthLang syntax with selected frameworks</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <pre className="text-sm bg-black/20 p-4 rounded overflow-x-auto">
                        {getPreviewContent()}
                      </pre>
                    </CardContent>
                  </Card>
                </div>
              </div>
            </TabsContent>

            <TabsContent value="advanced" className="space-y-4">
              <div className="space-y-6">
                {/* Regular Features */}
                <div className="space-y-4">
                  {FEATURE_OPTIONS.filter(f => f.id !== 'customPrompt').map((feature) => (
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
                </div>

                {/* Custom Prompt Accordion */}
                <Accordion type="single" collapsible className="w-full">
                  <AccordionItem value="custom-prompt">
                    <AccordionTrigger className="text-left">
                      <div>
                        <div className="font-semibold">Custom System Prompt</div>
                        <p className="text-sm text-muted-foreground">Override the default system prompt with custom instructions</p>
                      </div>
                    </AccordionTrigger>
                    <AccordionContent>
                      <div className="pt-4 space-y-4">
                        <Textarea
                          value={config.features.customPrompt as string}
                          onChange={(e) => handleFeatureChange('customPrompt', e.target.value)}
                          placeholder="Enter your custom system prompt..."
                          className="min-h-[200px] font-mono text-sm"
                        />
                        <div className="text-sm text-muted-foreground">
                          <p>Tips:</p>
                          <ul className="list-disc list-inside space-y-1 mt-2">
                            <li>Use clear, specific instructions</li>
                            <li>Include examples where helpful</li>
                            <li>Define expected output format</li>
                            <li>Specify any constraints or requirements</li>
                          </ul>
                        </div>
                      </div>
                    </AccordionContent>
                  </AccordionItem>
                </Accordion>
              </div>
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
              <div className="grid grid-cols-3 gap-4">
                <Card>
                  <CardHeader>
                    <CardTitle>Performance Metrics</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span>Response Time:</span>
                        <span className="font-mono">35ms</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Throughput:</span>
                        <span className="font-mono">23.2 req/s</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Memory Usage:</span>
                        <span className="font-mono">27KB/req</span>
                      </div>
                    </div>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader>
                    <CardTitle>Cost Analysis</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span>Base Cost:</span>
                        <span className="font-mono">$0.0045/req</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Optimized:</span>
                        <span className="font-mono">$0.0015/req</span>
                      </div>
                      <div className="flex justify-between text-green-400">
                        <span>Savings:</span>
                        <span className="font-mono">70%</span>
                      </div>
                    </div>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader>
                    <CardTitle>Token Usage</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span>Original:</span>
                        <span className="font-mono">150 tokens</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Optimized:</span>
                        <span className="font-mono">45 tokens</span>
                      </div>
                      <div className="flex justify-between text-blue-400">
                        <span>Improvement:</span>
                        <span className="font-mono">3.33×</span>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  );
};
