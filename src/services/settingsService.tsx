import React, { createContext, useContext, useState, ReactNode } from 'react';

export interface ModelSettings {
  enabled: boolean;
  contextWindow: number;
  costPer1kTokens: number;
}

export interface Settings {
  openRouterApiKey?: string;
  theme?: 'light' | 'dark';
  fontSize?: number;
  defaultModel: string;
  models: {
    [key: string]: ModelSettings;
  };
}

interface SettingsContextType {
  settings: Settings;
  updateSettings: (settings: Partial<Settings>) => void;
}

const defaultSettings: Settings = {
  theme: 'dark',
  fontSize: 14,
  defaultModel: 'openai/gpt-3.5-turbo',
  models: {
    'openai/gpt-4': {
      enabled: true,
      contextWindow: 8192,
      costPer1kTokens: 0.03
    },
    'openai/gpt-3.5-turbo': {
      enabled: true,
      contextWindow: 4096,
      costPer1kTokens: 0.002
    },
    'anthropic/claude-2': {
      enabled: true,
      contextWindow: 100000,
      costPer1kTokens: 0.011
    },
    'anthropic/claude-instant-v1': {
      enabled: true,
      contextWindow: 100000,
      costPer1kTokens: 0.0015
    }
  }
};

const SettingsContext = createContext<SettingsContextType>({
  settings: defaultSettings,
  updateSettings: () => undefined
});

export const useSettingsContext = () => {
  const context = useContext(SettingsContext);
  if (!context) {
    throw new Error('useSettingsContext must be used within a SettingsProvider');
  }
  return context;
};

interface SettingsProviderProps {
  children: ReactNode;
  initialSettings?: Partial<Settings>;
}

export const SettingsProvider: React.FC<SettingsProviderProps> = ({ 
  children, 
  initialSettings = {} 
}) => {
  const [settings, setSettings] = useState<Settings>(() => {
    try {
      const savedSettings = localStorage.getItem('synthlang-settings');
      const parsed = savedSettings ? JSON.parse(savedSettings) : {};
      return {
        ...defaultSettings,
        ...initialSettings,
        ...parsed,
        // Ensure defaultModel is set to DeepSeek if not already set
        defaultModel: parsed.defaultModel || defaultSettings.defaultModel,
        // Ensure models object exists
        models: {
          ...defaultSettings.models,
          ...(parsed.models || {}),
        }
      };
    } catch (error) {
      console.error('Failed to load settings:', error);
      return { 
        ...defaultSettings, 
        ...initialSettings,
        defaultModel: defaultSettings.defaultModel,
        models: { ...defaultSettings.models }
      };
    }
  });

  const updateSettings = (newSettings: Partial<Settings>) => {
    setSettings(prev => {
      const updated = { ...prev, ...newSettings };
      try {
        localStorage.setItem('synthlang-settings', JSON.stringify(updated));
      } catch (error) {
        console.error('Failed to save settings:', error);
      }
      return updated;
    });
  };

  return (
    <SettingsContext.Provider value={{ settings, updateSettings }}>
      {children}
    </SettingsContext.Provider>
  );
};
