import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { AlertCircle } from 'lucide-react';

interface ModelSettings {
  enabled: boolean;
  models: string[];
}

interface Settings {
  openRouterApiKey?: string;
  defaultModel: string;
  theme: string;
  models: ModelSettings;
}

interface SettingsContextType {
  settings: Settings;
  updateSettings: (newSettings: Partial<Settings>) => void;
  clearApiKey: () => void;
}

const SettingsContext = createContext<SettingsContextType | null>(null);

const STORAGE_KEY = 'synthLangSettings';

const DEFAULT_SETTINGS: Settings = {
  defaultModel: "openai/gpt-3.5-turbo",
  theme: "dark",
  models: {
    enabled: true,
    models: ["openai/gpt-3.5-turbo", "openai/gpt-4", "anthropic/claude-2"]
  }
};

export const SettingsProvider = ({ children }: { children: ReactNode }) => {
  const [settings, setSettings] = useState<Settings>(DEFAULT_SETTINGS);

  useEffect(() => {
    const loadSettings = () => {
      const savedSettings = localStorage.getItem(STORAGE_KEY);
      if (savedSettings) {
        try {
          const parsed = JSON.parse(savedSettings);
          setSettings({
            ...DEFAULT_SETTINGS,
            ...parsed,
            models: {
              ...DEFAULT_SETTINGS.models,
              ...parsed.models
            }
          });
        } catch (error) {
          console.error('Failed to parse settings:', error);
          setSettings(DEFAULT_SETTINGS);
        }
      }
    };

    loadSettings();
  }, []);

  const updateSettings = (newSettings: Partial<Settings>) => {
    setSettings(prev => {
      const updated = {
        ...prev,
        ...newSettings,
        models: {
          ...prev.models,
          ...(newSettings.models || {})
        }
      };
      localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));
      return updated;
    });
  };

  const clearApiKey = () => {
    setSettings(prev => {
      const { openRouterApiKey, ...rest } = prev;
      localStorage.setItem(STORAGE_KEY, JSON.stringify(rest));
      return {
        ...DEFAULT_SETTINGS,
        ...rest
      };
    });
  };

  return (
    <SettingsContext.Provider value={{ settings, updateSettings, clearApiKey }}>
      {children}
    </SettingsContext.Provider>
  );
};

export const useSettingsContext = () => {
  const context = useContext(SettingsContext);
  if (!context) {
    throw new Error('useSettingsContext must be used within a SettingsProvider');
  }
  return context;
};

export const ApiKeyMessage = () => {
  const { settings } = useSettingsContext();
  const hasApiKey = !!settings.openRouterApiKey;

  if (hasApiKey) return null;

  return (
    <div className="rounded-lg border border-yellow-500/20 bg-yellow-500/10 p-4 mb-4">
      <div className="flex items-center gap-2 text-yellow-500 mb-2">
        <AlertCircle className="w-4 h-4" />
        <h3 className="font-medium">API Key Required</h3>
      </div>
      <p className="text-sm text-yellow-500/80">
        Some features require an OpenRouter API key. Please add your API key in the{' '}
        <a href="/settings" className="underline hover:text-yellow-400">
          Settings
        </a>{' '}
        page to access all functionality.
      </p>
    </div>
  );
};
