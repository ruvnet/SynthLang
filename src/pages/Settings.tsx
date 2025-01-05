import { useState, useEffect } from "react";
import { Save, Loader2, Info, Lock, Trash2, Key, Database, Github, AlertCircle } from "lucide-react";
import MainNav from "../components/MainNav";
import { useToast } from "../components/ui/use-toast";
import { 
  Settings as SettingsType,
  OpenRouterModel,
  loadSettings,
  saveSettings,
  clearSettings,
  fetchAvailableModels,
  testApiKey
} from "../services/settingsService";

const DEFAULT_API_KEY = import.meta.env.VITE_OPENROUTER_KEY;
const SETTINGS_KEY = 'symbolic-scribe-settings';

// Helper to dispatch settings change event
const notifySettingsChange = () => {
  window.dispatchEvent(new CustomEvent('settingsChanged'));
};

const Settings = () => {
  const [apiKey, setApiKey] = useState<string>(DEFAULT_API_KEY || "");
  const [selectedModel, setSelectedModel] = useState("");
  const [models, setModels] = useState<OpenRouterModel[]>([]);
  const [enabledModels, setEnabledModels] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isTestingKey, setIsTestingKey] = useState(false);
  const [isUsingDefaultKey, setIsUsingDefaultKey] = useState(Boolean(DEFAULT_API_KEY));
  const [hasStoredKey, setHasStoredKey] = useState(Boolean(localStorage.getItem(SETTINGS_KEY)));
  const { toast } = useToast();

  // Load saved settings
  useEffect(() => {
    const settings = loadSettings();
    if (settings) {
      const isDefault = settings.apiKey === DEFAULT_API_KEY;
      setIsUsingDefaultKey(isDefault);
      setApiKey(settings.apiKey);
      setSelectedModel(settings.defaultModel);
      setEnabledModels(settings.enabledModels);
      setHasStoredKey(Boolean(localStorage.getItem(SETTINGS_KEY)));
      
      // If we have an API key, fetch models
      if (settings.apiKey) {
        loadModels(settings.apiKey);
      }
    }
  }, []);

  const loadModels = async (key: string) => {
    setIsLoading(true);
    try {
      const fetchedModels = await fetchAvailableModels(key);
      setModels(fetchedModels);
      
      // If no models are enabled yet, enable all by default
      if (enabledModels.length === 0) {
        setEnabledModels(fetchedModels.map(model => model.id));
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to fetch available models. Please check your API key.",
        duration: 3000
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleApiKeyChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const newKey = e.target.value;
    setApiKey(newKey);
    setIsUsingDefaultKey(newKey === DEFAULT_API_KEY);
    
    // Clear validation timeout if it exists
    if (window.apiKeyTimeout) {
      clearTimeout(window.apiKeyTimeout);
    }

    // Set new validation timeout
    if (newKey) {
      window.apiKeyTimeout = setTimeout(async () => {
        setIsTestingKey(true);
        const isValid = await testApiKey(newKey);
        setIsTestingKey(false);
        
        if (isValid) {
          loadModels(newKey);
          toast({
            title: "Success",
            description: "API key is valid",
            duration: 3000
          });
        } else {
          toast({
            title: "Error",
            description: "Invalid API key",
            duration: 3000
          });
        }
      }, 1000);
    }
  };

  const handleModelToggle = (modelId: string) => {
    setEnabledModels(prev => {
      if (prev.includes(modelId)) {
        return prev.filter(id => id !== modelId);
      } else {
        return [...prev, modelId];
      }
    });
  };

  const handleSave = () => {
    const settings: SettingsType = {
      apiKey,
      defaultModel: selectedModel,
      enabledModels
    };

    try {
      saveSettings(settings);
      setHasStoredKey(true);
      setIsUsingDefaultKey(apiKey === DEFAULT_API_KEY);
      notifySettingsChange();
      toast({
        title: "Success",
        description: "Settings saved successfully",
        duration: 3000
      });
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to save settings",
        duration: 3000
      });
    }
  };

  const handleClear = () => {
    const defaultSettings = clearSettings();
    setHasStoredKey(false);
    
    if (defaultSettings) {
      // If we have default settings (from .env), use them
      setApiKey(defaultSettings.apiKey);
      setSelectedModel(defaultSettings.defaultModel);
      setEnabledModels(defaultSettings.enabledModels);
      setIsUsingDefaultKey(true);
      loadModels(defaultSettings.apiKey);
    } else {
      // If no default settings, clear everything
      setApiKey("");
      setSelectedModel("");
      setEnabledModels([]);
      setModels([]);
      setIsUsingDefaultKey(false);
    }

    notifySettingsChange();
    toast({
      title: "Success",
      description: "Stored settings cleared successfully",
      duration: 3000
    });
  };

  return (
    <div className="min-h-screen flex flex-col">
      <MainNav title="Settings" />

      {/* Main Content */}
      <main className="flex-1 p-4">
        <div className="glass-panel p-6 max-w-2xl mx-auto space-y-8">
          {/* GitHub Link */}
          <div className="flex justify-end">
            <a 
              href="https://github.com/ruvnet/symbolic-scribe"
              target="_blank"
              rel="noopener noreferrer"
              className="console-button flex items-center gap-2"
            >
              <Github className="w-4 h-4" />
              View Source
            </a>
          </div>
          <div className="space-y-6">
            <div>
              <h2 className="text-xl text-console-cyan font-code mb-4 flex items-center gap-2">
                <Key className="w-5 h-5" />
                OpenRouter Configuration
              </h2>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-console-cyan mb-2">API Key</label>
                  <div className="relative">
                    <input
                      type="password"
                      className="console-input w-full pr-10"
                      placeholder={DEFAULT_API_KEY ? "Using default API key from environment" : "Enter your OpenRouter API key"}
                      value={apiKey}
                      onChange={handleApiKeyChange}
                    />
                    {isTestingKey && (
                      <Loader2 className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 animate-spin text-gray-400" />
                    )}
                  </div>
                  {isUsingDefaultKey && DEFAULT_API_KEY && (
                    <div className="flex items-center gap-2 mt-2 text-console-green">
                      <Info className="w-4 h-4" />
                      <span className="text-sm">Using default API key from environment</span>
                    </div>
                  )}
                  <div className="flex items-center gap-2 mt-2 text-gray-400">
                    <Lock className="w-4 h-4" />
                    <span className="text-sm">Keys entered here are encrypted and stored only in your browser's local storage. View the <a href="https://github.com/ruvnet/symbolic-scribe" className="text-console-cyan hover:underline" target="_blank" rel="noopener noreferrer">source code</a> for details.</span>
                  </div>
                  <p className="text-sm text-gray-400 mt-1">
                    <span className="flex items-center gap-1">
                      <Key className="w-3 h-3" /> Get your API key from <a href="https://openrouter.ai/keys" className="text-console-cyan hover:underline" target="_blank" rel="noopener noreferrer">OpenRouter</a>
                    </span>
                  </p>
                  <p className="text-sm text-gray-400 mt-1">
                    {DEFAULT_API_KEY 
                      ? "You can override the default API key by entering your own key above"
                      : <span className="flex items-center gap-1"><AlertCircle className="w-4 h-4 text-yellow-500" /> No default API key found. Please enter your OpenRouter API key to get started.</span>}
                  </p>
                </div>

                <div>
                  <label className="block text-console-cyan mb-2 flex items-center gap-2">
                    <Database className="w-4 h-4" />
                    Default Model
                  </label>
                  <select
                    className="console-input w-full"
                    value={selectedModel}
                    onChange={(e) => setSelectedModel(e.target.value)}
                  >
                    <option value="">Select a model</option>
                    {models.map((model) => (
                      <option key={model.id} value={model.id}>
                        {model.name}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-console-cyan mb-2">Available Models</label>
                  <div className="bg-gray-800 rounded-lg p-4">
                    <div className="max-h-[400px] overflow-y-auto pr-2 space-y-2 custom-scrollbar">
                      {isLoading ? (
                        <div className="flex items-center justify-center py-4">
                          <Loader2 className="w-6 h-6 animate-spin text-console-cyan" />
                        </div>
                      ) : models.length > 0 ? (
                        models.map((model) => (
                          <div key={model.id} className="flex items-start space-x-2 p-2 hover:bg-gray-700/50 rounded-lg transition-colors">
                            <input
                              type="checkbox"
                              id={model.id}
                              className="console-checkbox mt-1"
                              checked={enabledModels.includes(model.id)}
                              onChange={() => handleModelToggle(model.id)}
                            />
                            <label htmlFor={model.id} className="text-gray-300 flex-1">
                              <div className="font-medium">{model.name}</div>
                              <div className="text-sm text-gray-400 mt-1">
                                Context: {model.context_length.toLocaleString()} tokens
                              </div>
                              <div className="text-sm text-gray-400">
                                Pricing: ${model.pricing.prompt}/1K prompt, ${model.pricing.completion}/1K completion
                              </div>
                              <div className="text-sm text-gray-400 mt-1">
                                {model.description}
                              </div>
                            </label>
                          </div>
                        ))
                      ) : (
                        <p className="text-gray-400 text-center py-4">
                          {apiKey ? "No models available" : "Enter API key to view available models"}
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div className="flex justify-between items-center gap-4">
              <button
                className="console-button flex items-center space-x-2 bg-red-900/30 hover:bg-red-900/50"
                onClick={handleClear}
                disabled={isLoading || isTestingKey || !hasStoredKey}
              >
                <Trash2 className="w-4 h-4" />
                <span>Clear Stored Key</span>
              </button>
              <button
                className="console-button flex items-center space-x-2"
                onClick={handleSave}
                disabled={isLoading || isTestingKey}
              >
                {(isLoading || isTestingKey) ? (
                  <Loader2 className="w-4 h-4 animate-spin" />
                ) : (
                  <Save className="w-4 h-4" />
                )}
                <span>Save Settings</span>
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

// Add type declaration for the timeout
declare global {
  interface Window {
    apiKeyTimeout: ReturnType<typeof setTimeout>;
  }
}

export default Settings;
