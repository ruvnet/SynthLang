import { ArrowDownUp, DollarSign } from "lucide-react";
import { OutputMetricsProps } from "./types";
import { formatPercentage, DEFAULT_OUTPUT_COST } from "./constants";

export const OutputMetrics = ({
  tokenMetrics,
  selectedModel,
  availableModels,
  outputRatio,
  outputCost,
  onOutputRatioChange,
  onOutputCostChange
}: OutputMetricsProps) => {
  const calculateOutputCost = (tokens: number) => {
    if (!availableModels[selectedModel].output_cost_per_token) return 0;
    return (tokens * outputRatio) * (availableModels[selectedModel].output_cost_per_token || outputCost);
  };

  return (
    <div className="font-mono text-xs bg-black/20 p-4 rounded space-y-2">
      <div className="text-muted-foreground mb-4">
        Output costs based on estimated response length
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="space-y-2">
          <label className="text-sm text-muted-foreground flex items-center gap-2">
            <ArrowDownUp className="w-3 h-3" />
            Response Ratio (x input length)
          </label>
          <select 
            className="console-input w-full font-mono"
            value={outputRatio}
            onChange={(e) => onOutputRatioChange(parseFloat(e.target.value))}
          >
            <option value="0.25">0.25x</option>
            <option value="0.5">0.50x</option>
            <option value="0.75">0.75x</option>
            <option value="1">1.00x</option>
            <option value="1.5">1.50x</option>
            <option value="2">2.00x</option>
          </select>
        </div>
        <div className="space-y-2">
          <label className="text-sm text-muted-foreground flex items-center gap-2">
            <DollarSign className="w-3 h-3" />
            Output Cost/Token ($)
          </label>
          <input
            type="number"
            min="0"
            step="0.000001"
            className="console-input w-full font-mono"
            placeholder="Enter cost per token..."
            value={outputCost}
            onChange={(e) => {
              const value = Math.max(0, parseFloat(e.target.value) || DEFAULT_OUTPUT_COST);
              onOutputCostChange(value);
            }}
            onWheel={(e) => e.currentTarget.blur()}
          />
        </div>
      </div>
      {tokenMetrics && (
        <>
          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <DollarSign className="w-3 h-3" />
              <span className="text-purple-400">Output Cost/Token:</span>
              <span className="font-mono">
                ${availableModels[selectedModel].output_cost_per_token?.toFixed(6) || '0.00'}
              </span>
            </div>
            <div className="flex items-center gap-2">
              <ArrowDownUp className="w-3 h-3" />
              <span className="text-purple-400">Original Output Cost:</span>
              <span className="font-mono">
                ${calculateOutputCost(tokenMetrics.originalTokens).toFixed(4)}
              </span>
            </div>
            <div className="flex items-center gap-2">
              <ArrowDownUp className="w-3 h-3" />
              <span className="text-purple-400">Optimized Output Cost:</span>
              <span className="font-mono">
                ${calculateOutputCost(tokenMetrics.optimizedTokens).toFixed(4)}
              </span>
            </div>
          </div>
          <div className="flex items-center gap-2 text-green-400">
            <DollarSign className="w-3 h-3" />
            <span>Output Savings:</span>
            <span>
              <span className="font-mono">
                ${(calculateOutputCost(tokenMetrics.originalTokens) - 
                   calculateOutputCost(tokenMetrics.optimizedTokens)).toFixed(4)}
              </span>
              <span className="text-xs ml-1">
                ({formatPercentage(
                  calculateOutputCost(tokenMetrics.originalTokens) - 
                  calculateOutputCost(tokenMetrics.optimizedTokens),
                  calculateOutputCost(tokenMetrics.originalTokens)
                )})
              </span>
            </span>
          </div>
        </>
      )}
    </div>
  );
};

export default OutputMetrics;
