import { useState, useCallback, useEffect } from 'react';
import { CalculatorPreset, PresetMetadata } from '../components/AdvancedCalculator/presetTypes';
import { presetStorageService } from '../services/presetStorageService';

export function usePresetManager() {
  const [presets, setPresets] = useState<PresetMetadata[]>([]);
  const [currentPreset, setCurrentPreset] = useState<CalculatorPreset | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Load all presets on mount
  useEffect(() => {
    loadPresets();
  }, []);

  const loadPresets = async () => {
    try {
      setLoading(true);
      const presetList = await presetStorageService.listPresets();
      setPresets(presetList);
      setError(null);
    } catch (err) {
      setError('Failed to load presets');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const loadPreset = useCallback(async (id: string) => {
    try {
      setLoading(true);
      const preset = await presetStorageService.loadPreset(id);
      if (preset) {
        setCurrentPreset(preset);
        setError(null);
        return preset;
      }
      throw new Error('Preset not found');
    } catch (err) {
      setError('Failed to load preset');
      console.error(err);
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  const savePreset = useCallback(async (preset: CalculatorPreset) => {
    try {
      setLoading(true);
      await presetStorageService.savePreset(preset);
      await loadPresets(); // Refresh list
      setError(null);
    } catch (err) {
      setError('Failed to save preset');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, []);

  const deletePreset = useCallback(async (id: string) => {
    try {
      setLoading(true);
      await presetStorageService.deletePreset(id);
      await loadPresets(); // Refresh list
      if (currentPreset?.id === id) {
        setCurrentPreset(null);
      }
      setError(null);
    } catch (err) {
      setError('Failed to delete preset');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [currentPreset?.id]);

  const exportPreset = useCallback(async (id: string) => {
    try {
      setLoading(true);
      const exportData = await presetStorageService.exportPreset(id);
      setError(null);
      return exportData;
    } catch (err) {
      setError('Failed to export preset');
      console.error(err);
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  const importPreset = useCallback(async (data: string) => {
    try {
      setLoading(true);
      const imported = await presetStorageService.importPreset(data);
      await loadPresets(); // Refresh list
      setError(null);
      return imported;
    } catch (err) {
      setError('Failed to import preset');
      console.error(err);
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    presets,
    currentPreset,
    loading,
    error,
    loadPreset,
    savePreset,
    deletePreset,
    exportPreset,
    importPreset
  };
}
