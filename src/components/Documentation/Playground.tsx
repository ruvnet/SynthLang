import { Play, Copy, Check, RotateCcw, AlertTriangle, Command, Loader2 } from "lucide-react";
import { usePlaygroundContext, PlaygroundError, PlaygroundOutput, PlaygroundLoading } from "./PlaygroundContext";
import { PlaygroundSettings, type PlaygroundSettings as PlaygroundSettingsType } from "./PlaygroundSettings";
import { useSettingsContext } from "../../services/settingsService";

export const Playground = () => {
  const {
    code,
    copied,
    output,
    errors,
    isLoading,
    highlightedCode,
    setCode,
    handleCopy,
    handleRun,
    handleReset,
    handleKeyDown,
    settings,
    updateSettings
  } = usePlaygroundContext();

  const { settings: globalSettings } = useSettingsContext();
  const hasOpenRouterKey = !!globalSettings?.openRouterApiKey;

  const handleSettingsChange = (newSettings: PlaygroundSettingsType) => {
    updateSettings(newSettings);
  };

  return (
    <div className="rounded-lg border border-border/40 bg-card/30 backdrop-blur overflow-hidden">
      <div className="flex items-center justify-between p-2 border-b border-border/40 bg-black/20">
        <span className="text-sm font-medium">SynthLang Editor</span>
        <div className="flex items-center gap-4">
          <div className="hidden md:flex items-center gap-4 text-xs text-muted-foreground">
            <div className="flex items-center gap-1">
              <Command className="w-3 h-3" />
              <span>+</span>
              <span>↵</span>
              <span className="ml-1">to run</span>
            </div>
            <div className="flex items-center gap-1">
              <Command className="w-3 h-3" />
              <span>+</span>
              <span>⇧</span>
              <span>+</span>
              <span>R</span>
              <span className="ml-1">to reset</span>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <PlaygroundSettings onSettingsChange={handleSettingsChange} />
            <button
              onClick={handleReset}
              className="p-1 hover:bg-white/5 rounded transition-colors"
              title="Reset code (⌘⇧R)"
              disabled={isLoading}
            >
              <RotateCcw className={`w-4 h-4 ${isLoading ? 'text-muted-foreground/50' : 'text-muted-foreground'}`} />
            </button>
            <button
              onClick={handleCopy}
              className="p-1 hover:bg-white/5 rounded transition-colors"
              title="Copy code"
              disabled={isLoading}
            >
              {copied ? (
                <Check className="w-4 h-4 text-green-400" />
              ) : (
                <Copy className={`w-4 h-4 ${isLoading ? 'text-muted-foreground/50' : 'text-muted-foreground'}`} />
              )}
            </button>
            <button
              onClick={handleRun}
              className={`flex items-center gap-1 px-2 py-1 rounded text-sm font-medium 
                       transition-colors ${
                         isLoading 
                           ? 'bg-purple-500/30 cursor-not-allowed' 
                           : 'bg-purple-500/20 hover:bg-purple-500/30'
                       } disabled:opacity-50`}
              title="Run code (⌘↵)"
              disabled={isLoading || !hasOpenRouterKey}
            >
              {isLoading ? (
                <Loader2 className="w-3 h-3 animate-spin" />
              ) : (
                <Play className="w-3 h-3" />
              )}
              {isLoading ? 'Running...' : 'Run'}
            </button>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 divide-y md:divide-y-0 md:divide-x divide-border/40">
        <div className="relative p-4 min-h-[800px]">
          <div
            className="absolute inset-0 pointer-events-none p-4 font-mono text-sm"
            dangerouslySetInnerHTML={{ __html: highlightedCode }}
            style={{ whiteSpace: 'pre-wrap' }}
          />
          <textarea
            value={code}
            onChange={(e) => setCode(e.target.value)}
            onKeyDown={handleKeyDown}
            className="w-full h-full min-h-[800px] bg-transparent border-none 
                     outline-none resize-none font-mono text-sm text-transparent 
                     caret-white disabled:cursor-not-allowed"
            spellCheck={false}
            style={{ caretColor: 'white' }}
            placeholder="Enter your SynthLang code here..."
            disabled={isLoading}
          />
        </div>

        <div className="relative p-4 bg-black/10 min-h-[800px]">
          <div className="absolute inset-0 p-4 overflow-y-auto">
            {isLoading ? (
              <PlaygroundLoading />
            ) : errors.length > 0 ? (
              <div className="space-y-2">
                <div className="flex items-center gap-2 text-red-400">
                  <AlertTriangle className="w-4 h-4" />
                  <span className="font-medium">Validation Errors</span>
                </div>
                <div className="space-y-1">
                  {errors.map((error, index) => (
                    <PlaygroundError key={index} error={error} />
                  ))}
                </div>
              </div>
            ) : output ? (
              <PlaygroundOutput>{output}</PlaygroundOutput>
            ) : !hasOpenRouterKey ? (
              <div className="flex items-center gap-2 text-yellow-500 text-sm">
                <AlertTriangle className="w-4 h-4" />
                <span>Configure OpenRouter API key in settings to run code</span>
              </div>
            ) : (
              <div className="text-sm text-muted-foreground italic">
                Click "Run" or press ⌘↵ to see the output
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
