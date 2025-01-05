import { useState, useEffect } from 'react';
import { Calculator as CalcIcon, FileText, Zap, ArrowDownUp } from 'lucide-react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../ui/tabs";
import { Slider } from "../ui/slider";
import { ModelSelector } from './ModelSelector';
import { TokenInput } from './TokenInput';
import { SpeedMetrics } from './SpeedMetrics';
import { OutputMetrics } from './OutputMetrics';
import { MetricsDisplay } from './MetricsDisplay';
import { TokenMetrics } from './types';
import { modelSearch, ModelSpec } from '../../config/modelSearch';
import {
  DEFAULT_TOKEN_COUNT,
  DEFAULT_PROCESSING_TIME,
  DEFAULT_BASE_LATENCY,
  DEFAULT_OUTPUT_RATIO,
  DEFAULT_OUTPUT_COST,
  calculateTokens,
  calculateTokensFromWords,
  calculateTokensFromPages,
} from './constants';

// Get all available chat models
const AVAILABLE_MODELS = Object.entries(modelSearch.getModelsByMode('chat'))
  .filter(([_, model]) => model.input_cost_per_token)
  .sort(([nameA], [nameB]) => {
    if (nameA === 'o1') return -1;
    if (nameB === 'o1') return 1;
    return nameA.localeCompare(nameB);
  })
  .reduce((acc, [name, model]) => {
    acc[name] = model;
    return acc;
  }, {} as Record<string, ModelSpec>);

const DEFAULT_MODEL = 'o1' in AVAILABLE_MODELS ? 'o1' : Object.keys(AVAILABLE_MODELS)[0];

const Calculator = () => {
  const [promptText, setPromptText] = useState("");
  const [tokenCount, setTokenCount] = useState(DEFAULT_TOKEN_COUNT);
  const [tokenMetrics, setTokenMetrics] = useState<TokenMetrics | null>(null);
  const [selectedModel, setSelectedModel] = useState(DEFAULT_MODEL);
  const [processingTime, setProcessingTime] = useState(DEFAULT_PROCESSING_TIME);
  const [baseLatency, setBaseLatency] = useState(DEFAULT_BASE_LATENCY);
  const [outputRatio, setOutputRatio] = useState(DEFAULT_OUTPUT_RATIO);
  const [outputCost, setOutputCost] = useState(DEFAULT_OUTPUT_COST);
  const [reductionPercent, setReductionPercent] = useState(70); // Default 70% reduction

  const calculateMetrics = (tokens: number) => {
    const optimizedTokens = Math.ceil(tokens * (1 - reductionPercent / 100)); // Convert percent to decimal
    const modelSpec = AVAILABLE_MODELS[selectedModel];
    const originalCost = tokens * (modelSpec.input_cost_per_token || 0);
    const optimizedCost = optimizedTokens * (modelSpec.input_cost_per_token || 0);
    const savings = originalCost - optimizedCost;
    
    const improvementFactor = tokens / optimizedTokens; // e.g., 3.33×
    const percentageIncrease = ((improvementFactor - 1) * 100); // e.g., 233%
    
    setTokenMetrics({
      originalTokens: tokens,
      optimizedTokens,
      improvementFactor,
      percentageIncrease,
      modelCosts: {
        [selectedModel]: {
          original: originalCost,
          optimized: optimizedCost,
          savings,
          savingsPercent: (savings / originalCost) * 100
        }
      }
    });
  };

  // Initialize with default token count
  useEffect(() => {
    calculateMetrics(DEFAULT_TOKEN_COUNT);
  }, []);

  // Recalculate when model changes
  useEffect(() => {
    if (tokenCount) {
      calculateMetrics(tokenCount);
    }
  }, [selectedModel]);

  const handleTokenCountChange = (count: number) => {
    setTokenCount(count);
    calculateMetrics(count);
  };

  const handleWordsChange = (words: number) => {
    const tokens = calculateTokensFromWords(words);
    setTokenCount(tokens);
    calculateMetrics(tokens);
  };

  const handlePagesChange = (pages: number) => {
    const tokens = calculateTokensFromPages(pages);
    setTokenCount(tokens);
    calculateMetrics(tokens);
  };

  const handlePromptChange = (text: string) => {
    setPromptText(text);
    if (text.trim()) {
      const tokens = calculateTokens(text);
      setTokenCount(tokens);
      calculateMetrics(tokens);
    } else {
      // If prompt is empty, keep current token count
      calculateMetrics(tokenCount);
    }
  };

  return (
    <div className="space-y-4">
      <div className="space-y-4">
        <div className="flex gap-4">
          <ModelSelector
            selectedModel={selectedModel}
            onModelSelect={setSelectedModel}
            availableModels={AVAILABLE_MODELS}
          />
        </div>
        
        <div className="space-y-2">
          <div className="flex justify-between">
            <label className="text-sm font-medium">Reduction Percentage</label>
            <span className="text-sm text-muted-foreground">{reductionPercent}%</span>
          </div>
          <Slider
            min={0}
            max={100}
            step={1}
            value={[reductionPercent]}
            onValueChange={([value]) => {
              setReductionPercent(value);
              if (tokenCount) {
                calculateMetrics(tokenCount);
              }
            }}
            className="w-full"
          />
        </div>
      </div>

      <Tabs defaultValue="tokens" className="w-full">
        <TabsList className="grid grid-cols-4 gap-4 bg-transparent h-auto p-1">
          <TabsTrigger 
            value="tokens"
            className="data-[state=active]:bg-purple-500/20 h-10 px-4"
          >
            <CalcIcon className="w-4 h-4 mr-2" />
            Tokens
          </TabsTrigger>
          <TabsTrigger 
            value="prompt"
            className="data-[state=active]:bg-purple-500/20 h-10 px-4"
          >
            <FileText className="w-4 h-4 mr-2" />
            Prompt
          </TabsTrigger>
          <TabsTrigger 
            value="speed"
            className="data-[state=active]:bg-purple-500/20 h-10 px-4"
          >
            <Zap className="w-4 h-4 mr-2" />
            Speed
          </TabsTrigger>
          <TabsTrigger 
            value="output"
            className="data-[state=active]:bg-purple-500/20 h-10 px-4"
          >
            <ArrowDownUp className="w-4 h-4 mr-2" />
            Output
          </TabsTrigger>
        </TabsList>

        <TabsContent value="tokens">
          <TokenInput
            tokenCount={tokenCount}
            onTokenCountChange={handleTokenCountChange}
            onWordsChange={handleWordsChange}
            onPagesChange={handlePagesChange}
          />
        </TabsContent>

        <TabsContent value="prompt">
          <textarea
            className="console-input w-full h-24"
            placeholder="Enter your prompt here (optional) to override token count..."
            value={promptText}
            onChange={(e) => handlePromptChange(e.target.value)}
          />
        </TabsContent>

        <TabsContent value="speed">
          <SpeedMetrics
            tokenMetrics={tokenMetrics}
            processingTime={processingTime}
            baseLatency={baseLatency}
            onProcessingTimeChange={setProcessingTime}
            onBaseLatencyChange={setBaseLatency}
          />
        </TabsContent>

        <TabsContent value="output">
          <OutputMetrics
            tokenMetrics={tokenMetrics}
            selectedModel={selectedModel}
            availableModels={AVAILABLE_MODELS}
            outputRatio={outputRatio}
            outputCost={outputCost}
            onOutputRatioChange={setOutputRatio}
            onOutputCostChange={setOutputCost}
          />
        </TabsContent>
      </Tabs>

      {tokenMetrics && (
        <MetricsDisplay
          tokenMetrics={tokenMetrics}
          selectedModel={selectedModel}
          availableModels={AVAILABLE_MODELS}
        />
      )}
    </div>
  );
};

export default Calculator;
