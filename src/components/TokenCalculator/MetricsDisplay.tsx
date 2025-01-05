import { Terminal, Cpu, DollarSign, Check, X, FunctionSquare, Image, Music, Bot, MessageSquare } from "lucide-react";
import { MetricsDisplayProps } from "./types";
import { formatPercentage } from "./constants";

export const MetricsDisplay = ({
  tokenMetrics,
  selectedModel,
  availableModels
}: MetricsDisplayProps) => {
  const modelFeatures = [
    {
      icon: FunctionSquare,
      title: "Function Calling",
      key: "supports_function_calling"
    },
    {
      icon: Image,
      title: "Vision",
      key: "supports_vision"
    },
    {
      icon: Music,
      title: "Audio Input/Output",
      key: "supports_audio_input",
      extraKey: "supports_audio_output"
    },
    {
      icon: Bot,
      title: "System Messages",
      key: "supports_system_messages"
    },
    {
      icon: MessageSquare,
      title: "Response Schema",
      key: "supports_response_schema"
    },
    {
      icon: FunctionSquare,
      title: "Parallel Functions",
      key: "supports_parallel_function_calling"
    }
  ];

  return (
    <div className="grid grid-cols-2 gap-4 p-4 bg-accent/20 rounded-lg">
      <div>
        <div className="text-sm text-muted-foreground mb-2">Selected Model ({selectedModel})</div>
        <div className="space-y-1">
          {/* Model Specs */}
          <div className="font-mono text-xs bg-black/20 p-2 rounded mb-2 space-y-1">
            <div className="flex items-center gap-2">
              <Terminal className="w-3 h-3" />
              <span className="text-purple-400">Provider:</span>
              <span>{availableModels[selectedModel].litellm_provider}</span>
            </div>
            <div className="flex items-center gap-2">
              <Cpu className="w-3 h-3" />
              <span className="text-purple-400">Tokens:</span>
              <span>
                i:{availableModels[selectedModel].max_input_tokens || '?'} /
                o:{availableModels[selectedModel].max_output_tokens || '?'}
              </span>
            </div>
            <div className="flex items-center gap-2">
              <DollarSign className="w-3 h-3" />
              <span className="text-purple-400">Cost/Token:</span>
              <span>
                i:${availableModels[selectedModel].input_cost_per_token?.toFixed(6)} /
                o:${availableModels[selectedModel].output_cost_per_token?.toFixed(6)}
              </span>
            </div>
            <div className="flex flex-wrap gap-2 mt-1 border-t border-white/10 pt-1">
              {modelFeatures.map(({ icon: Icon, title, key, extraKey }) => (
                <div 
                  key={key}
                  className="flex items-center gap-1 bg-black/10 px-1 rounded" 
                  title={`Supports ${title}`}
                >
                  <Icon className="w-3 h-3" />
                  {availableModels[selectedModel][key as keyof typeof availableModels[typeof selectedModel]] || 
                   (extraKey && availableModels[selectedModel][extraKey as keyof typeof availableModels[typeof selectedModel]]) ? 
                    <Check className="w-3 h-3 text-green-400" /> : 
                    <X className="w-3 h-3 text-red-400" />
                  }
                </div>
              ))}
            </div>
          </div>
          <div className="flex justify-between">
            <span>Original Cost:</span>
            <span className="font-mono">${tokenMetrics.modelCosts[selectedModel].original.toFixed(4)}</span>
          </div>
          <div className="flex justify-between">
            <span>Optimized Cost:</span>
            <span className="font-mono">${tokenMetrics.modelCosts[selectedModel].optimized.toFixed(4)}</span>
          </div>
          <div className="flex justify-between text-green-400 font-bold">
            <span>Savings:</span>
            <span>
              <span className="font-mono">${tokenMetrics.modelCosts[selectedModel].savings.toFixed(4)}</span>
              <span className="text-xs ml-1">
                ({formatPercentage(
                  tokenMetrics.modelCosts[selectedModel].savings,
                  tokenMetrics.modelCosts[selectedModel].original
                )})
              </span>
            </span>
          </div>
        </div>
      </div>
      <div>
        <div className="text-sm text-muted-foreground mb-2">
          Token Usage ({formatPercentage(tokenMetrics.optimizedTokens, tokenMetrics.originalTokens)} of original)
        </div>
        <div className="space-y-1">
          <div className="flex justify-between">
            <span>Original:</span>
            <span className="font-mono">{tokenMetrics.originalTokens}</span>
          </div>
          <div className="flex justify-between">
            <span>Optimized:</span>
            <span className="font-mono">{tokenMetrics.optimizedTokens}</span>
          </div>
          <div className="flex justify-between text-purple-400 font-bold">
            <span>Reduction:</span>
            <span className="font-mono">
              {formatPercentage(
                tokenMetrics.originalTokens - tokenMetrics.optimizedTokens,
                tokenMetrics.originalTokens
              )}
            </span>
          </div>
          <div className="flex justify-between text-blue-400 font-bold">
            <span>Improvement:</span>
            <span className="font-mono">
              {tokenMetrics.improvementFactor.toFixed(2)}×
            </span>
          </div>
          <div className="flex justify-between text-green-400 font-bold">
            <span>Speed Increase:</span>
            <span className="font-mono">
              {tokenMetrics.percentageIncrease.toFixed(0)}%
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MetricsDisplay;
