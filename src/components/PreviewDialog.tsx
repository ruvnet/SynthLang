import { useState, useRef, useEffect } from "react";
import { X, Loader2, ArrowLeft } from "lucide-react";
import { OpenRouterModel } from "../services/settingsService";

interface PreviewDialogProps {
  isOpen: boolean;
  onClose: () => void;
  models: OpenRouterModel[];
  prompt: string;
  onTest: (modelId: string, prompt: string, onChunk: (chunk: string) => void) => Promise<void>;
}

type ViewTab = 'preview' | 'response';

const PreviewDialog = ({ isOpen, onClose, models, prompt, onTest }: PreviewDialogProps) => {
  const [selectedModel, setSelectedModel] = useState("");
  const [response, setResponse] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [step, setStep] = useState<'select' | 'response'>('select');
  const [activeTab, setActiveTab] = useState<ViewTab>('preview');
  const responseEndRef = useRef<HTMLDivElement>(null);
  const [startTime, setStartTime] = useState<Date | null>(null);

  const scrollToBottom = () => {
    responseEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [response]);

  if (!isOpen) return null;

  const handleTest = async () => {
    if (!selectedModel) {
      setError("Please select a model");
      return;
    }

    setIsLoading(true);
    setError("");
    setResponse("");
    setStartTime(new Date());
    setStep('response');
    setActiveTab('response');

    try {
      await onTest(selectedModel, prompt, (chunk) => {
        setResponse(prev => prev + chunk);
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setIsLoading(false);
    }
  };

  const handleBack = () => {
    setStep('select');
    setResponse("");
    setError("");
    setActiveTab('preview');
    setStartTime(null);
  };

  const handleClose = () => {
    onClose();
    setStep('select');
    setSelectedModel("");
    setResponse("");
    setError("");
    setActiveTab('preview');
    setStartTime(null);
  };

  const selectedModelName = models.find(m => m.id === selectedModel)?.name || selectedModel;

  const formatTimestamp = (date: Date) => {
    return date.toLocaleTimeString('en-US', { 
      hour12: false,
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="glass-panel w-full max-w-3xl max-h-[80vh] overflow-hidden flex flex-col m-4">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-700">
          <div className="flex items-center gap-2">
            {step === 'response' && (
              <button 
                onClick={handleBack}
                className="console-button p-1"
                title="Back to model selection"
              >
                <ArrowLeft className="w-5 h-5" />
              </button>
            )}
            <h2 className="text-xl text-console-cyan font-code">
              {step === 'select' ? 'Preview Prompt' : `Response from ${selectedModelName}`}
            </h2>
          </div>
          <button 
            onClick={handleClose}
            className="console-button p-1"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Tabs - Only show in response step */}
        {step === 'response' && (
          <div className="flex border-b border-gray-700">
            <button
              className={`px-4 py-2 font-code ${
                activeTab === 'preview' 
                  ? 'text-console-cyan border-b-2 border-console-cyan' 
                  : 'text-gray-400 hover:text-gray-300'
              }`}
              onClick={() => setActiveTab('preview')}
            >
              Preview
            </button>
            <button
              className={`px-4 py-2 font-code ${
                activeTab === 'response' 
                  ? 'text-console-cyan border-b-2 border-console-cyan' 
                  : 'text-gray-400 hover:text-gray-300'
              }`}
              onClick={() => setActiveTab('response')}
            >
              Response
            </button>
          </div>
        )}

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {step === 'select' ? (
            <>
              {/* Model Selection */}
              <div>
                <label className="block text-console-cyan mb-2">Select Model</label>
                <select
                  className="console-input w-full"
                  value={selectedModel}
                  onChange={(e) => setSelectedModel(e.target.value)}
                >
                  <option value="">Choose a model...</option>
                  {models.map((model) => (
                    <option key={model.id} value={model.id}>
                      {model.name}
                    </option>
                  ))}
                </select>
              </div>

              {/* Prompt Display */}
              <div>
                <label className="block text-console-cyan mb-2">Prompt</label>
                <div className="console-input w-full min-h-[100px] p-3 whitespace-pre-wrap">
                  {prompt}
                </div>
              </div>

              {error && (
                <div className="text-red-400 p-3 bg-red-900/20 rounded-lg">
                  {error}
                </div>
              )}
            </>
          ) : (
            activeTab === 'preview' ? (
              // Preview Tab Content
              <div className="space-y-4">
                <div>
                  <label className="block text-console-cyan mb-2">Original Prompt</label>
                  <div className="console-input w-full p-3 whitespace-pre-wrap">
                    {prompt}
                  </div>
                </div>
              </div>
            ) : (
              // Response Tab Content
              <div className="console-input w-full min-h-[400px] p-3 font-mono text-sm">
                <div className="text-gray-400">
                  {startTime && `[${formatTimestamp(startTime)}] `}$ Generating response with {selectedModelName}...
                </div>
                {error ? (
                  <div className="text-red-400 mt-2">{error}</div>
                ) : (
                  <>
                    <div className="whitespace-pre-wrap mt-2">
                      <span className="text-gray-400">
                        {response ? `[${formatTimestamp(new Date())}] ` : ''}
                      </span>
                      <span className="text-gray-300">{response}</span>
                      {isLoading && (
                        <span className="inline-block w-2 h-4 ml-1 bg-console-cyan animate-pulse" />
                      )}
                    </div>
                  </>
                )}
                <div ref={responseEndRef} />
              </div>
            )
          )}
        </div>

        {/* Footer */}
        <div className="border-t border-gray-700 p-4 flex justify-end gap-3">
          {step === 'select' ? (
            <>
              <button 
                className="console-button"
                onClick={handleClose}
              >
                Close
              </button>
              <button
                className="console-button"
                onClick={handleTest}
                disabled={isLoading || !selectedModel}
              >
                {isLoading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin mr-2" />
                    Testing...
                  </>
                ) : (
                  'Test Prompt'
                )}
              </button>
            </>
          ) : (
            <button 
              className="console-button"
              onClick={handleClose}
            >
              Close
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default PreviewDialog;
