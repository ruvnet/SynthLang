import { Copy, Play, Check, AlertTriangle, Loader2 } from "lucide-react";
import { useState, useCallback } from "react";
import { usePlaygroundContext } from "./PlaygroundContext";
import { useSynthLang } from "./useSynthLang";
import { PlaygroundOutput } from "./PlaygroundContext";
import { useSettingsContext } from "../../services/settingsService";
import { callOpenRouter } from "../../services/openRouterService";

interface CodeExampleProps {
  code: string;
  title?: string;
  description?: string;
  language?: string;
}

export const CodeExample = ({ 
  code, 
  title, 
  description, 
  language = "synthlang" 
}: CodeExampleProps) => {
  const [copied, setCopied] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [exampleOutput, setExampleOutput] = useState<string | null>(null);
  const { loadExample, isLoading } = usePlaygroundContext();
  const { highlightSyntax, validateSynthLang } = useSynthLang();
  const { settings } = useSettingsContext();

  const handleCopy = useCallback(async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      setError("Failed to copy code to clipboard");
      setTimeout(() => setError(null), 3000);
    }
  }, [code]);

  const handleTryIt = useCallback(async () => {
    try {
      setError(null);
      setIsRunning(true);
      setExampleOutput("");

      // Only validate if it's SynthLang code
      if (language === "synthlang") {
        // Skip validation for comment-only code
        const nonCommentLines = code.split('\n')
          .map(line => line.trim())
          .filter(line => line && !line.startsWith('#'));

        if (nonCommentLines.length > 0) {
          const errors = validateSynthLang(code);
          if (errors.length > 0) {
            throw new Error(errors[0]); // Show first error
          }
        }
      }

      // Call OpenRouter if API key is available
      if (!settings.openRouterApiKey) {
        throw new Error("OpenRouter API key not found. Please add your API key in Settings.");
      }

      setExampleOutput("");
      await callOpenRouter(
        code, 
        {
          model: settings.defaultModel,
          temperature: 0.7,
          maxTokens: 1000
        }, 
        settings.openRouterApiKey,
        'interpreter',
        undefined,
        undefined,
        (chunk) => {
          setExampleOutput(prev => (prev || "") + chunk);
        }
      );

      // Also load into playground for reference
      await loadExample(code);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load example");
      setTimeout(() => setError(null), 5000);
    } finally {
      setIsRunning(false);
    }
  }, [code, language, loadExample, validateSynthLang, settings]);

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        {title && (
          <h4 className="text-sm font-medium">{title}</h4>
        )}
        {error && (
          <div className="flex items-center gap-2 text-red-400 text-xs animate-in fade-in slide-in-from-top-1">
            <AlertTriangle className="w-3 h-3" />
            <span>{error}</span>
          </div>
        )}
      </div>
      {description && (
        <p className="text-sm text-muted-foreground">{description}</p>
      )}
      <div className="relative group pt-8">
        <div className="absolute top-2 right-2 flex items-center gap-2 opacity-0 
                      group-hover:opacity-100 transition-opacity">
          <button
            onClick={handleTryIt}
            className={`p-1.5 rounded-md transition-colors flex items-center gap-1.5
                     ${isRunning || isLoading ? 'bg-purple-500/30 cursor-not-allowed' : 'bg-black/20 hover:bg-black/30'}`}
            title="Try in playground"
            disabled={isRunning || isLoading}
          >
            {isRunning ? (
              <Loader2 className="w-3.5 h-3.5 text-purple-400 animate-spin" />
            ) : (
              <Play className={`w-3.5 h-3.5 ${isLoading ? 'text-muted-foreground' : 'text-purple-400'}`} />
            )}
            <span className={`text-xs ${isLoading ? 'text-muted-foreground' : 'text-purple-400'}`}>
              {isRunning ? 'Running...' : isLoading ? 'Loading...' : 'Try it'}
            </span>
          </button>
          <button
            onClick={handleCopy}
            className="p-1.5 bg-black/20 hover:bg-black/30 rounded-md transition-colors"
            title="Copy code"
            disabled={isRunning || isLoading}
          >
            {copied ? (
              <Check className="w-3.5 h-3.5 text-green-400" />
            ) : (
              <Copy className={`w-3.5 h-3.5 ${isRunning || isLoading ? 'text-muted-foreground' : 'text-muted-foreground hover:text-purple-400'}`} />
            )}
          </button>
        </div>
        <div className="rounded-lg border border-border/40 bg-black/20">
          {language === "synthlang" ? (
            <pre
              className="p-4 font-mono text-sm whitespace-pre-wrap break-words"
              dangerouslySetInnerHTML={{ 
                __html: highlightSyntax(code)
              }}
            />
          ) : (
            <pre className="p-4 font-mono text-sm whitespace-pre-wrap break-words">
              <code>{code}</code>
            </pre>
          )}
        </div>
        {exampleOutput && (
          <div className="mt-4">
            <PlaygroundOutput>{exampleOutput}</PlaygroundOutput>
          </div>
        )}
      </div>
    </div>
  );
};

// Utility component for displaying multiple examples in a grid
export const CodeExampleGrid = ({ 
  examples 
}: { 
  examples: Array<CodeExampleProps>
}) => (
  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
    {examples.map((example, index) => (
      <CodeExample key={index} {...example} />
    ))}
  </div>
);

// Utility component for displaying a list of examples
export const CodeExampleList = ({ 
  examples 
}: { 
  examples: Array<CodeExampleProps>
}) => (
  <div className="space-y-6">
    {examples.map((example, index) => (
      <CodeExample key={index} {...example} />
    ))}
  </div>
);
