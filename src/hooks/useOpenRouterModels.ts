import { useState, useEffect } from 'react';
import { getAvailableModels } from '../services/openRouterService';
import { useSettingsContext } from '../services/settingsService';

interface OpenRouterModel {
  id: string;
  name: string;
  description?: string;
  context_length?: number;
  pricing?: {
    prompt: string;
    completion: string;
  };
}

export const useOpenRouterModels = () => {
  const [models, setModels] = useState<OpenRouterModel[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const { settings } = useSettingsContext();

  useEffect(() => {
    const loadModels = async () => {
      try {
        if (!settings.openRouterApiKey) {
          setError('OpenRouter API key not found');
          return;
        }

        const availableModels = await getAvailableModels(settings.openRouterApiKey);
        setModels(availableModels);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load models');
      } finally {
        setIsLoading(false);
      }
    };

    loadModels();
  }, [settings.openRouterApiKey]);

  return {
    models,
    isLoading,
    error,
    getModelById: (id: string) => models.find(m => m.id === id),
  };
};
