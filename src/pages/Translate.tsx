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

  // Get the default model (first enabled model)
  const defaultModel = Object.entries(settings.models)
    .find(([_, settings]) => settings.enabled)?.[0] || "openai/gpt-3.5-turbo";
  const modelCost = settings.models[defaultModel]?.costPer1kTokens || 0;

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
      let translatedContent;
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

LINE STRUCTURE (EXACT SYNTAX REQUIRED):
↹ label:"content" -> description   # Input (MUST START HERE)
⊕ label:"content" -> description   # Process (MIDDLE STEPS)
Σ label:"content" -> description   # Output (MUST END HERE)

COMPONENT REQUIREMENTS (EACH LINE MUST FOLLOW):
1. Task Glyph (FIRST CHARACTER):
   ↹ = Input/Parse (REQUIRED START)
   ⊕ = Process/Transform (MIDDLE)
   Σ = Output/Generate (REQUIRED END)

2. Label (AFTER GLYPH):
   - Single word only
   - Ends with colon
   - No spaces/hyphens
   VALID: header: content: data:
   INVALID: my-label: two words: data-field:

3. Content (IN QUOTES):
   - Double quotes required
   - Exact text inside
   - No escaped quotes
   VALID: "[Title]" "text here"
   INVALID: [Title] 'text' "escaped \\"quotes\\""

4. Arrow (EXACT SPACING):
   - Space before ->
   - Space after ->
   VALID: " -> "
   INVALID: "->" "-> " " ->"

5. Description (VERB FIRST):
   - Starts with verb
   - Clear purpose
   - Brief phrase
   VALID: Parse section, Extract data
   INVALID: Section parsed, The data is extracted

SEQUENCE RULES (STRICT ORDER):
1. START with ↹ operations (REQUIRED):
   - Must begin with input
   - Extract raw content
   - Parse sections

2. CONTINUE with ⊕ operations:
   - Process content
   - Transform data
   - Apply formatting

3. END with Σ operations (REQUIRED):
   - Must end with output
   - Format results
   - Generate final form

EXAMPLE WITH EXACT FORMAT:
Input:
[Overview]
1. Main Points
   * First point
   * Second point

Valid SynthLang Format:
↹ header:"[Overview]" -> Parse section title
↹ title:"Main Points" -> Extract section name
↹ list:"First point, Second point" -> Parse list items
⊕ analyze:"content structure" -> Process structure
⊕ validate:"syntax rules" -> Check formatting
⊕ format:"documentation" -> Apply structure
Σ output:"formatted content" -> Generate final output

Convert input to SynthLang format using EXACT syntax:
${text}`;

        translatedContent = await callOpenRouter(
          text.trim(),
          {
            model: defaultModel,
            temperature: 0.2,
            maxTokens: 2000,
            autoFormat: true,
            syntaxHighlighting: true,
            showLineNumbers: true
          },
          apiKey,
          'translator',
          instructions
        );
      } catch (err) {
        if (err instanceof Error && err.message.includes('Failed to process')) {
          throw new Error("Translation failed. Please check your API key in Settings and ensure you have sufficient credits.");
        }
        throw err;
      }

      if (!translatedContent) {
        throw new Error("No translation received. Please try again.");
      }

      // Calculate optimized metrics
      const optimizedTokens = calculateTokens(translatedContent);
      const optimizedCost = (optimizedTokens / 1000) * modelCost;
      const savings = originalCost - optimizedCost;

      // Update state
      setTranslatedText(translatedContent);
      setMetrics({
        originalTokens,
        optimizedTokens,
        originalCost,
        optimizedCost,
        savings
      });

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

  // Translate initial text if provided
  useEffect(() => {
    if (initialState?.originalText) {
      translateToSynthLang(initialState.originalText);
    }
  }, [initialState, translateToSynthLang]);

  const handleTestTranslation = useCallback(() => {
    navigate("/playground", { 
      state: { 
        prompt: translatedText
      } 
    });
  }, [navigate, translatedText]);

  return (
    <Layout title="Translate">
      <main className="container mx-auto p-4">
        {/* Metrics Overview */}
        {metrics && (
          <div className="grid md:grid-cols-4 gap-4 mb-6">
            <div className="glass-panel p-4 rounded-lg border border-border/40 bg-card/30 backdrop-blur">
              <div className="text-sm text-muted-foreground mb-1">Original Tokens</div>
              <div className="text-2xl font-bold">{metrics.originalTokens}</div>
            </div>
            <div className="glass-panel p-4 rounded-lg border border-border/40 bg-card/30 backdrop-blur">
              <div className="text-sm text-muted-foreground mb-1">Optimized Tokens</div>
              <div className="text-2xl font-bold">{metrics.optimizedTokens}</div>
            </div>
            <div className="glass-panel p-4 rounded-lg border border-border/40 bg-card/30 backdrop-blur">
              <div className="text-sm text-muted-foreground mb-1">Cost Savings</div>
              <div className="text-2xl font-bold text-green-400">
                ${metrics.savings.toFixed(4)}
              </div>
            </div>
            <div className="glass-panel p-4 rounded-lg border border-border/40 bg-card/30 backdrop-blur">
              <div className="text-sm text-muted-foreground mb-1">Reduction</div>
              <div className="text-2xl font-bold text-purple-400">
                {((metrics.originalTokens - metrics.optimizedTokens) / metrics.originalTokens * 100).toFixed(0)}%
              </div>
            </div>
          </div>
        )}

        {/* Translation Interface */}
        <div className="grid md:grid-cols-2 gap-6">
          {/* Original Text */}
          <div className="glass-panel p-6 rounded-lg border border-border/40 bg-card/30 backdrop-blur">
            <h2 className="text-xl font-semibold mb-4">Original Prompt</h2>
            <textarea
              className="console-input w-full h-64 mb-4"
              value={originalText}
              onChange={(e) => {
                setOriginalText(e.target.value);
                setError(null);
              }}
              placeholder="Enter your prompt here..."
            />
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Calculator className="w-4 h-4" />
              <span>Tokens: {metrics?.originalTokens || 0}</span>
              <span className="mx-2">•</span>
              <span>Cost: ${metrics?.originalCost.toFixed(4) || "0.0000"}</span>
            </div>
          </div>

          {/* SynthLang Translation */}
          <div className="glass-panel p-6 rounded-lg border border-border/40 bg-card/30 backdrop-blur">
            <h2 className="text-xl font-semibold mb-4">SynthLang Translation</h2>
            <textarea
              className="console-input w-full h-64 mb-4"
              value={translatedText}
              placeholder="Optimized translation will appear here..."
              readOnly
            />
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <Calculator className="w-4 h-4" />
                <span>Tokens: {metrics?.optimizedTokens || 0}</span>
                <span className="mx-2">•</span>
                <span>Cost: ${metrics?.optimizedCost.toFixed(4) || "0.0000"}</span>
              </div>
              <div className="flex items-center gap-4">
                <button 
                  className="console-button flex items-center gap-2"
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
                  className="console-button flex items-center gap-2"
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
            <span>{error}</span>
          </div>
        )}

        {!settings.openRouterApiKey && (
          <div className="glass-panel p-4 mt-6 rounded-lg border border-yellow-500/40 bg-yellow-500/10 text-yellow-400 flex items-center gap-2">
            <AlertCircle className="w-4 h-4" />
            <span>OpenRouter API key not found. Please add it in Settings to use the translation feature.</span>
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

          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="frameworks">Frameworks</TabsTrigger>
            <TabsTrigger value="system-prompt">System Prompt</TabsTrigger>
          </TabsList>

          <TabsContent value="frameworks">
            <Card>
              <CardHeader>
                <CardTitle>Translation Frameworks</CardTitle>
                <CardDescription>Select mathematical frameworks and glyphs to enhance translation</CardDescription>
              </CardHeader>
              <CardContent>
                <Accordion type="multiple" className="w-full space-y-2">
                  {allFrameworkOptions.map((framework) => (
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
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="system-prompt">
            <SystemPromptDisplay frameworks={config.frameworks} />
          </TabsContent>
        </Tabs>

        <div className="glass-panel p-6 mt-6 rounded-lg border border-border/40 bg-card/30 backdrop-blur">
          <h2 className="text-xl font-semibold mb-4">Optimization Details</h2>
          <div className="space-y-4">
            <div>
              <h3 className="text-lg font-medium mb-2">Token Reduction Strategy</h3>
              <ul className="list-disc list-inside text-muted-foreground">
                <li>Removed redundant context</li>
                <li>Optimized instruction format</li>
                <li>Compressed similar patterns</li>
                <li>Enhanced semantic density</li>
              </ul>
            </div>
            <div>
              <h3 className="text-lg font-medium mb-2">Preservation Guarantees</h3>
              <ul className="list-disc list-inside text-muted-foreground">
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
