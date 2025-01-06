import { useState, useEffect, useMemo, useCallback } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Calculator, ArrowRight, Loader2, AlertCircle } from "lucide-react";
import Layout from "../components/Layout";
import { calculateTokens } from "../components/TokenCalculator/constants";
import { modelSearch } from "../config/modelSearch";
import { useSettingsContext } from "../services/settingsService";
import { callOpenRouter, checkOpenRouterAvailability } from "../services/openRouterService";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "../components/ui/accordion";
import { Switch } from "../components/ui/switch";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "../components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../components/ui/tabs";
import { FRAMEWORK_OPTIONS, DEFAULT_FRAMEWORKS_CONFIG } from "../components/AdvancedCalculator/constants";
import { FrameworksConfig, FrameworkState } from "../components/AdvancedCalculator/types";
import { SystemPromptDisplay } from "../components/Translate/SystemPromptDisplay";
import { FrameworkWizard } from "../components/Translate/FrameworkWizard";
import { getCustomFrameworks } from "../services/frameworkStorage";

interface LocationState {
  originalText: string;
  metrics: {
    originalTokens: number;
    optimizedTokens: number;
    originalCost: number;
    optimizedCost: number;
    savings: number;
  };
}

interface TranslationConfig {
  frameworks: FrameworksConfig;
}

interface TranslationMetrics {
  originalTokens: number;
  optimizedTokens: number;
  originalCost: number;
  optimizedCost: number;
  savings: number;
}

const Translate = () => {
  const customFrameworks = useMemo(() => getCustomFrameworks(), []);
  const allFrameworkOptions = useMemo(() => [...FRAMEWORK_OPTIONS, ...customFrameworks], [customFrameworks]);

  const [config, setConfig] = useState<TranslationConfig>(() => {
    const customConfig = customFrameworks.reduce((acc, framework) => ({
      ...acc,
      [framework.id]: { enabled: false, selectedGlyphs: [], customGlyphs: [] }
    }), {});

    return {
      frameworks: {
        ...DEFAULT_FRAMEWORKS_CONFIG,
        ...customConfig
      }
    };
  });

  const location = useLocation();
  const navigate = useNavigate();
  const { settings } = useSettingsContext();
  const initialState = location.state as LocationState;

  const [originalText, setOriginalText] = useState(initialState?.originalText || "");
  const [translatedText, setTranslatedText] = useState("");
  const [metrics, setMetrics] = useState<TranslationMetrics | null>(initialState?.metrics || null);
  const [isTranslating, setIsTranslating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);

  // Get the selected model and its cost
  const defaultModel = Object.entries(settings.models)
    .find(([_, settings]) => settings.enabled)?.[0] || "openai/gpt-3.5-turbo";
  const selectedModel = settings.models[defaultModel];
  const [modelCost, setModelCost] = useState(selectedModel?.costPer1kTokens || 0);
  const modelContext = selectedModel?.contextWindow || 4096;

  // Initialize model cost and trigger initial calculation
  useEffect(() => {
    const initialCost = 0.0025; // $2.50 per million tokens
    setModelCost(initialCost);
    
    // Trigger initial metrics calculation with the default cost
    if (metrics) {
      const originalCost = (metrics.originalTokens / 1000) * initialCost;
      const optimizedCost = (metrics.optimizedTokens / 1000) * initialCost;
      setMetrics({
        ...metrics,
        originalCost,
        optimizedCost,
        savings: Math.max(0, originalCost - optimizedCost)
      });
    }
  }, [selectedModel]);

  const handleFrameworkToggle = useCallback((id: string, enabled: boolean) => {
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
  }, []);

  const handleGlyphToggle = useCallback((frameworkId: string, glyph: { symbol: string }) => {
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
  }, []);

  const translateToSynthLang = useCallback(async (text: string) => {
    if (!text.trim()) {
      setError("Please enter a prompt to translate");
      return;
    }

    setIsTranslating(true);
    setError(null);
    setTranslatedText(""); // Clear previous translation

    try {
      // Calculate original metrics
      const originalTokens = calculateTokens(text);
      const originalCost = (originalTokens / 1000) * modelCost;

      // Call OpenRouter API
      const apiKey = settings.openRouterApiKey?.trim();
      if (!apiKey) {
        throw new Error("OpenRouter API key not found. Please add it in Settings.");
      }

      // Validate API key before use
      const isValid = await checkOpenRouterAvailability(apiKey);
      if (!isValid) {
        throw new Error("Invalid OpenRouter API key. Please check your API key in Settings and ensure it's correctly copied.");
      }

      // Call OpenRouter with error handling
      try {
        const frameworkInstructions = Object.entries(config.frameworks)
          .filter(([_, state]) => state.enabled)
          .map(([id]) => {
            const framework = allFrameworkOptions.find(f => f.id === id)!;
            const selectedGlyphs = framework.glyphs
              .filter(g => config.frameworks[id].selectedGlyphs.includes(g.symbol))
              .map(g => `${g.symbol} (${g.name}): ${g.description}\nUsage: ${g.usage}`);
            
            return `${framework.name}:\n${framework.description}\nAvailable Glyphs:\n${selectedGlyphs.join('\n')}`;
          })
          .join('\n\n');

        const instructions = `${frameworkInstructions}\n\nSYNTHLANG TRANSLATION FORMAT:

RULES:
1. Use ONLY these symbols: ↹ (input), ⊕ (process), Σ (output)
2. NO quotes, arrows, or descriptions
3. Use • to join related items
4. Use => for transformations
5. Maximum 30 characters per line
6. Use mathematical operators (+, >, <, ^)
7. Break complex tasks into steps

IMPORTANT: Keep translations extremely concise!

GOOD EXAMPLES:
↹ data•source
⊕ condition>5 => action
Σ result + log

↹ input•stream, params
⊕ transform => output
⊕ Σ final^2 + cache

↹ news•feed•google
⊕ sentiment>0 => pos
⊕ sentiment<0 => neg
Σ trend + factors

BAD EXAMPLES (TOO VERBOSE):
↹ data:"source" -> Parse input
⊕ process:"condition" -> Check value

Convert input to concise SynthLang format using minimal symbols:
${text}`;

        await callOpenRouter(
          text.trim(),
          {
            model: defaultModel,
            temperature: 0.1,
            maxTokens: 2000
          },
          apiKey,
          'translator',
          instructions,
          undefined,
          (chunk) => {
            setTranslatedText(prev => {
              const newText = (prev || "") + chunk;
              
              // Calculate metrics with current text
              const optimizedTokens = calculateTokens(newText);
              
              // Calculate costs using actual model pricing
              const originalCost = Number(((originalTokens / 1000) * modelCost).toFixed(6));
              const optimizedCost = Number(((optimizedTokens / 1000) * modelCost).toFixed(6));
              const savings = Number((originalCost - optimizedCost).toFixed(6));

              // Update metrics with precise values
              setMetrics({
                originalTokens,
                optimizedTokens,
                originalCost,
                optimizedCost,
                savings: Math.max(0, savings) // Ensure non-negative savings
              });

              return newText;
            });
          }
        );

      } catch (err) {
        if (err instanceof Error && err.message.includes('Failed to process')) {
          throw new Error("Translation failed. Please check your API key in Settings and ensure you have sufficient credits.");
        }
        throw err;
      }

    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to translate prompt. Please try again.");
      console.error("Translation error:", err);
    } finally {
      setIsTranslating(false);
    }
  }, [config.frameworks, allFrameworkOptions, modelCost, defaultModel, settings.openRouterApiKey]);

  // Update config when custom frameworks change
  useEffect(() => {
    const customConfig = customFrameworks.reduce((acc, framework) => ({
      ...acc,
      [framework.id]: { enabled: false, selectedGlyphs: [], customGlyphs: [] }
    }), {});

    setConfig(prev => ({
      ...prev,
      frameworks: {
        ...prev.frameworks,
        ...customConfig
      }
    }));
  }, [customFrameworks]);

  // Initialize metrics for initial text
  useEffect(() => {
    if (initialState?.originalText) {
      // Calculate initial metrics
      const text = initialState.originalText;
      const tokens = calculateTokens(text);
      const cost = Number(((tokens / 1000) * modelCost).toFixed(6));
      
      setMetrics(prev => ({
        ...prev,
        originalTokens: tokens,
        originalCost: cost,
        optimizedTokens: prev?.optimizedTokens || 0,
        optimizedCost: prev?.optimizedCost || 0,
        savings: prev ? Math.max(0, cost - prev.optimizedCost) : 0
      }));

      // Start translation if needed
      translateToSynthLang(text);
    }
  }, [initialState, modelCost]);

  const handleTestTranslation = useCallback(() => {
    navigate("/playground", { 
      state: { 
        prompt: translatedText
      } 
    });
  }, [navigate, translatedText]);

  return (
    <Layout title="Translate">
      <main className="container mx-auto px-4 py-6 max-w-[1200px]">
        {/* Metrics Overview */}
        {metrics && (
          <div className="grid grid-cols-2 md:grid-cols-5 lg:grid-cols-5 gap-4 mb-6">
            <div className="glass-panel p-4 rounded-lg border border-border/40 bg-card/30 backdrop-blur">
              <div className="text-sm text-muted-foreground mb-1">Original Tokens</div>
              <div className="text-xl md:text-2xl font-bold">{metrics.originalTokens}</div>
            </div>
            <div className="glass-panel p-4 rounded-lg border border-border/40 bg-card/30 backdrop-blur">
              <div className="text-sm text-muted-foreground mb-1">Optimized Tokens</div>
              <div className="text-xl md:text-2xl font-bold">{metrics.optimizedTokens}</div>
            </div>
            <div className="glass-panel p-4 rounded-lg border border-border/40 bg-card/30 backdrop-blur">
              <div className="text-sm text-muted-foreground mb-1">Model Cost (per 1M)</div>
              <div className="flex items-center gap-2">
                <span>$</span>
                <input
                  type="number"
                  defaultValue="2.50"
                  onChange={(e) => {
                    const newCost = Number(e.target.value) / 1000;
                    setModelCost(newCost);
                    
                    // Recalculate metrics with new cost
                    if (metrics) {
                      const originalCost = (metrics.originalTokens / 1000) * newCost;
                      const optimizedCost = (metrics.optimizedTokens / 1000) * newCost;
                      setMetrics({
                        ...metrics,
                        originalCost,
                        optimizedCost,
                        savings: Math.max(0, originalCost - optimizedCost)
                      });
                    }
                  }}
                  className="w-24 px-2 py-1 text-lg font-bold bg-background border rounded"
                  step="0.01"
                  min="0"
                />
              </div>
            </div>
            <div className="glass-panel p-4 rounded-lg border border-border/40 bg-card/30 backdrop-blur">
              <div className="text-sm text-muted-foreground mb-1">Cost Savings</div>
              <div className="text-xl md:text-2xl font-bold text-green-400">
                ${metrics.savings.toFixed(4)}
              </div>
            </div>
            <div className="glass-panel p-4 rounded-lg border border-border/40 bg-card/30 backdrop-blur">
              <div className="text-sm text-muted-foreground mb-1">Reduction</div>
              <div className="text-xl md:text-2xl font-bold text-purple-400">
                {((metrics.originalTokens - metrics.optimizedTokens) / metrics.originalTokens * 100).toFixed(0)}%
              </div>
            </div>
          </div>
        )}

        {/* Translation Interface */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Original Text */}
          <div className="glass-panel p-4 md:p-6 rounded-lg border border-border/40 bg-card/30 backdrop-blur">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg md:text-xl font-semibold">Original Prompt</h2>
              <button
                className="console-button flex items-center gap-2 text-sm"
                onClick={async () => {
                  try {
                    const apiKey = settings.openRouterApiKey?.trim();
                    if (!apiKey) {
                      throw new Error("OpenRouter API key not found. Please add it in Settings.");
                    }

                    setIsGenerating(true);
                    setOriginalText(""); // Clear existing text
                    
                    const samplePrompt = "Generate a detailed technical instruction prompt about 1000 tokens in length. The prompt should be well-structured, comprehensive, and follow a similar format to documentation or technical specifications. Include numbered sections, bullet points, and clear implementation steps.";

                    const systemPrompt = "You are a helpful AI assistant that generates detailed technical instruction prompts.";

                    await callOpenRouter(
                      samplePrompt,
                      {
                        model: defaultModel,
                        temperature: 0.7,
                        maxTokens: 2000
                      },
                      apiKey,
                      'base',
                      systemPrompt,
                      undefined,
                      (chunk) => {
                        setOriginalText(prev => {
                          const newText = prev + chunk;
                          // Calculate metrics for the new text
                          const tokens = calculateTokens(newText);
                          const cost = Number(((tokens / 1000) * modelCost).toFixed(6));
                          
                          setMetrics(prev => ({
                            ...prev,
                            originalTokens: tokens,
                            originalCost: cost,
                            optimizedTokens: prev?.optimizedTokens || 0,
                            optimizedCost: prev?.optimizedCost || 0,
                            savings: prev ? Math.max(0, cost - prev.optimizedCost) : 0
                          }));
                          
                          return newText;
                        });
                      }
                    );
                  } catch (err) {
                    setError(err instanceof Error ? err.message : "Failed to generate sample prompt");
                  } finally {
                    setIsGenerating(false);
                  }
                }}
                disabled={isGenerating || isTranslating}
              >
                {isGenerating ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    Generating...
                  </>
                ) : (
                  <>
                    Generate Sample
                  </>
                )}
              </button>
            </div>
            <textarea
              className="console-input w-full h-48 md:h-64 mb-4 text-sm md:text-base"
              value={originalText}
              onChange={(e) => {
                const text = e.target.value;
                setOriginalText(text);
                setError(null);

                // Calculate initial metrics
                const tokens = calculateTokens(text);
                const cost = Number(((tokens / 1000) * modelCost).toFixed(6));
                
                setMetrics(prev => ({
                  ...prev,
                  originalTokens: tokens,
                  originalCost: cost,
                  optimizedTokens: prev?.optimizedTokens || 0,
                  optimizedCost: prev?.optimizedCost || 0,
                  savings: prev ? Math.max(0, cost - prev.optimizedCost) : 0
                }));
              }}
              placeholder="Enter your prompt here..."
            />
            <div className="flex flex-wrap items-center gap-2 text-sm text-muted-foreground">
              <Calculator className="w-4 h-4" />
              <span>Tokens: {metrics?.originalTokens || 0}</span>
              <span className="mx-2">•</span>
              <span>Cost: ${metrics?.originalCost.toFixed(4) || "0.0000"}</span>
            </div>
          </div>

          {/* SynthLang Translation */}
          <div className="glass-panel p-4 md:p-6 rounded-lg border border-border/40 bg-card/30 backdrop-blur">
            <h2 className="text-lg md:text-xl font-semibold mb-4">SynthLang Translation</h2>
            <textarea
              className="console-input w-full h-48 md:h-64 mb-4 text-sm md:text-base"
              value={translatedText}
              placeholder="Optimized translation will appear here..."
              readOnly
            />
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
              <div className="flex flex-wrap items-center gap-2 text-sm text-muted-foreground">
                <Calculator className="w-4 h-4" />
                <span>Tokens: {metrics?.optimizedTokens || 0}</span>
                <span className="mx-2">•</span>
                <span>Cost: ${metrics?.optimizedCost.toFixed(4) || "0.0000"}</span>
              </div>
              <div className="flex flex-wrap items-center gap-2">
                <button 
                  className="console-button flex items-center gap-2 text-sm"
                  onClick={() => translateToSynthLang(originalText)}
                  disabled={isTranslating || !originalText.trim()}
                >
                  {isTranslating ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      Translating...
                    </>
                  ) : (
                    <>
                      Translate
                      <ArrowRight className="w-4 h-4" />
                    </>
                  )}
                </button>
                <button 
                  className="console-button flex items-center gap-2 text-sm"
                  onClick={handleTestTranslation}
                  disabled={!translatedText || isTranslating}
                >
                  Test Translation
                  <ArrowRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Translation Details */}
        {error && (
          <div className="glass-panel p-4 mt-6 rounded-lg border border-red-500/40 bg-red-500/10 text-red-400 flex items-center gap-2">
            <AlertCircle className="w-4 h-4" />
            <span className="text-sm">{error}</span>
          </div>
        )}

        {!settings.openRouterApiKey && (
          <div className="glass-panel p-4 mt-6 rounded-lg border border-yellow-500/40 bg-yellow-500/10 text-yellow-400 flex items-center gap-2">
            <AlertCircle className="w-4 h-4" />
            <span className="text-sm">OpenRouter API key not found. Please add it in Settings to use the translation feature.</span>
          </div>
        )}

        {/* Framework Selection and System Prompt */}
        <Tabs defaultValue="frameworks" className="mt-6">
          <div className="mb-4">
            <FrameworkWizard
              onFrameworkCreated={(framework) => {
                setConfig(prev => ({
                  ...prev,
                  frameworks: {
                    ...prev.frameworks,
                    [framework.id]: {
                      enabled: true,
                      selectedGlyphs: [],
                      customGlyphs: []
                    }
                  }
                }));
              }}
            />
          </div>

          <TabsList className="grid w-full grid-cols-2 mb-4">
            <TabsTrigger value="frameworks">Frameworks</TabsTrigger>
            <TabsTrigger value="system-prompt">System Prompt</TabsTrigger>
          </TabsList>

          <TabsContent value="frameworks">
            <Card>
              <CardHeader>
                <CardTitle>Translation Frameworks</CardTitle>
                <CardDescription>Select mathematical frameworks and glyphs to enhance translation</CardDescription>
              </CardHeader>
              <CardContent className="overflow-hidden">
                <Accordion type="multiple" className="w-full space-y-2">
                  {allFrameworkOptions.map((framework) => (
                    <AccordionItem key={framework.id} value={framework.id} className="border rounded-lg">
                      <div className="flex items-center justify-between pr-4">
                        <AccordionTrigger className="hover:no-underline flex-1 px-2">
                          <div className="flex flex-col sm:flex-row items-start sm:items-center gap-2">
                            <div className="font-semibold">{framework.name}</div>
                            <div className="text-xs sm:text-sm text-muted-foreground">
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
                              <div className="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 gap-2">
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
                                    <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 w-[calc(100vw-2rem)] sm:w-64 p-3 bg-popover text-popover-foreground text-sm rounded shadow-lg opacity-0 group-hover:opacity-100 transition-opacity z-50 pointer-events-none">
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
                            <div className="grid grid-cols-1 gap-2 overflow-x-auto">
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
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="system-prompt">
            <SystemPromptDisplay frameworks={config.frameworks} />
          </TabsContent>
        </Tabs>

        <div className="glass-panel p-4 md:p-6 mt-6 rounded-lg border border-border/40 bg-card/30 backdrop-blur">
          <h2 className="text-lg md:text-xl font-semibold mb-4">Optimization Details</h2>
          <div className="space-y-4 overflow-x-auto">
            <div>
              <h3 className="text-base md:text-lg font-medium mb-2">Token Reduction Strategy</h3>
              <ul className="list-disc list-inside text-sm text-muted-foreground">
                <li>Removed redundant context</li>
                <li>Optimized instruction format</li>
                <li>Compressed similar patterns</li>
                <li>Enhanced semantic density</li>
              </ul>
            </div>
            <div>
              <h3 className="text-base md:text-lg font-medium mb-2">Preservation Guarantees</h3>
              <ul className="list-disc list-inside text-sm text-muted-foreground">
                <li>Core instruction integrity</li>
                <li>Critical context retention</li>
                <li>Semantic equivalence</li>
                <li>Output quality maintenance</li>
              </ul>
            </div>
          </div>
        </div>
      </main>
    </Layout>
  );
};

export default Translate;
