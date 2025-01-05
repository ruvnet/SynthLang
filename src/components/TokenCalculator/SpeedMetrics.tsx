import { Clock, Zap } from "lucide-react";
import { SpeedMetricsProps } from "./types";
import { formatTime, formatPercentage, calculateLatency, DEFAULT_PROCESSING_TIME, DEFAULT_BASE_LATENCY } from "./constants";

export const SpeedMetrics = ({
  tokenMetrics,
  processingTime,
  baseLatency,
  onProcessingTimeChange,
  onBaseLatencyChange
}: SpeedMetricsProps) => {
  return (
    <div className="font-mono text-xs bg-black/20 p-4 rounded space-y-2">
      <div className="text-muted-foreground mb-4">
        Processing time estimates based on token count and network latency
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="space-y-2">
          <label className="text-sm text-muted-foreground flex items-center gap-2">
            <Zap className="w-3 h-3" />
            Processing Rate (ms/token)
          </label>
          <input
            type="number"
            min="0.1"
            step="0.1"
            className="console-input w-full font-mono"
            placeholder="Enter processing rate..."
            value={processingTime}
            onChange={(e) => {
              const value = Math.max(0.1, parseFloat(e.target.value) || DEFAULT_PROCESSING_TIME);
              onProcessingTimeChange(value);
            }}
            onWheel={(e) => e.currentTarget.blur()}
          />
        </div>
        <div className="space-y-2">
          <label className="text-sm text-muted-foreground flex items-center gap-2">
            <Clock className="w-3 h-3" />
            Base Latency (ms)
          </label>
          <input
            type="number"
            min="0"
            step="50"
            className="console-input w-full font-mono"
            placeholder="Enter base latency..."
            value={baseLatency}
            onChange={(e) => {
              const value = Math.max(0, parseInt(e.target.value) || DEFAULT_BASE_LATENCY);
              onBaseLatencyChange(value);
            }}
            onWheel={(e) => e.currentTarget.blur()}
          />
        </div>
      </div>
      {tokenMetrics && (
        <>
          <div className="flex items-center gap-2">
            <Zap className="w-3 h-3" />
            <span className="text-purple-400">Original Processing:</span>
            <span className="font-mono">
              {formatTime(calculateLatency(tokenMetrics.originalTokens))}
            </span>
          </div>
          <div className="flex items-center gap-2">
            <Zap className="w-3 h-3" />
            <span className="text-purple-400">Optimized Processing:</span>
            <span className="font-mono">
              {formatTime(calculateLatency(tokenMetrics.optimizedTokens))}
            </span>
          </div>
          <div className="flex items-center gap-2 text-green-400">
            <Clock className="w-3 h-3" />
            <span>Time Saved:</span>
            <span className="font-mono">
              {formatTime(
                calculateLatency(tokenMetrics.originalTokens) - 
                calculateLatency(tokenMetrics.optimizedTokens)
              )}
              <span className="text-xs ml-1">
                ({formatPercentage(
                  calculateLatency(tokenMetrics.originalTokens) - calculateLatency(tokenMetrics.optimizedTokens),
                  calculateLatency(tokenMetrics.originalTokens)
                )})
              </span>
            </span>
          </div>
        </>
      )}
    </div>
  );
};

export default SpeedMetrics;
