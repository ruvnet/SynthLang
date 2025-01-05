import { useLocation } from "react-router-dom";
import MainNav from "../components/MainNav";
import { Calculator, ArrowRight } from "lucide-react";

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

const Translate = () => {
  const location = useLocation();
  const state = location.state as LocationState;

  return (
    <div className="min-h-screen bg-background">
      <MainNav title="SynthLang Translator" />
      <main className="container mx-auto p-4">
        {/* Metrics Overview */}
        {state?.metrics && (
          <div className="grid md:grid-cols-4 gap-4 mb-6">
            <div className="glass-panel p-4">
              <div className="text-sm text-muted-foreground mb-1">Original Tokens</div>
              <div className="text-2xl font-bold">{state.metrics.originalTokens}</div>
            </div>
            <div className="glass-panel p-4">
              <div className="text-sm text-muted-foreground mb-1">Optimized Tokens</div>
              <div className="text-2xl font-bold">{state.metrics.optimizedTokens}</div>
            </div>
            <div className="glass-panel p-4">
              <div className="text-sm text-muted-foreground mb-1">Cost Savings</div>
              <div className="text-2xl font-bold text-green-400">
                ${state.metrics.savings.toFixed(4)}
              </div>
            </div>
            <div className="glass-panel p-4">
              <div className="text-sm text-muted-foreground mb-1">Reduction</div>
              <div className="text-2xl font-bold text-purple-400">70%</div>
            </div>
          </div>
        )}

        {/* Translation Interface */}
        <div className="grid md:grid-cols-2 gap-6">
          {/* Original Text */}
          <div className="glass-panel p-6">
            <h2 className="text-xl font-semibold mb-4">Original Prompt</h2>
            <textarea
              className="console-input w-full h-64 mb-4"
              value={state?.originalText || ""}
              readOnly
            />
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Calculator className="w-4 h-4" />
              <span>Tokens: {state?.metrics?.originalTokens || 0}</span>
              <span className="mx-2">•</span>
              <span>Cost: ${state?.metrics?.originalCost.toFixed(4) || "0.0000"}</span>
            </div>
          </div>

          {/* SynthLang Translation */}
          <div className="glass-panel p-6">
            <h2 className="text-xl font-semibold mb-4">SynthLang Translation</h2>
            <textarea
              className="console-input w-full h-64 mb-4"
              placeholder="Optimized translation will appear here..."
            />
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <Calculator className="w-4 h-4" />
                <span>Tokens: {state?.metrics?.optimizedTokens || 0}</span>
                <span className="mx-2">•</span>
                <span>Cost: ${state?.metrics?.optimizedCost.toFixed(4) || "0.0000"}</span>
              </div>
              <button className="console-button flex items-center gap-2">
                Test Translation
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>

        {/* Translation Details */}
        <div className="glass-panel p-6 mt-6">
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
    </div>
  );
};

export default Translate;
