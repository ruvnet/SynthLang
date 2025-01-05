import { useState, useCallback, useEffect } from "react";
import { PresetConfiguration, PresetList } from "../components/AdvancedCalculator/presetTypes";
import { presetStorageService } from "../services/presetStorageService";

export const usePresetManager = () => {
  const [presets, setPresets] = useState<PresetList>([]);
  const [selectedPresetId, setSelectedPresetId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Load presets on mount
  useEffect(() => {
    try {
      const loadedPresets = presetStorageService.listPresets();
      setPresets(loadedPresets);
    } catch (err) {
      setError("Failed to load presets");
      console.error(err);
    }
  }, []);

  // Load a specific preset
  const loadPreset = useCallback(async (presetId: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const preset = presetStorageService.loadPreset(presetId);
      if (preset) {
        setSelectedPresetId(presetId);
        return preset;
      } else {
        throw new Error("Preset not found");
      }
    } catch (err) {
      setError("Failed to load preset");
      console.error(err);
      return null;
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Save a preset
  const savePreset = useCallback(async (preset: PresetConfiguration) => {
    setIsLoading(true);
    setError(null);
    try {
      presetStorageService.savePreset(preset);
      setPresets(presetStorageService.listPresets());
      setSelectedPresetId(preset.id);
    } catch (err) {
      setError("Failed to save preset");
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Delete a preset
  const deletePreset = useCallback(async (presetId: string) => {
    setIsLoading(true);
    setError(null);
    try {
      presetStorageService.deletePreset(presetId);
      setPresets(presetStorageService.listPresets());
      if (selectedPresetId === presetId) {
        setSelectedPresetId(null);
      }
    } catch (err) {
      setError("Failed to delete preset");
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  }, [selectedPresetId]);

  // Import a preset from JSON
  const importPreset = useCallback((presetJson: string) => {
    try {
      const preset = presetStorageService.importPreset(presetJson);
      savePreset(preset);
      return preset;
    } catch (err) {
      setError("Failed to import preset");
      console.error(err);
      return null;
    }
  }, [savePreset]);

  // Export a preset to JSON
  const exportPreset = useCallback((preset: PresetConfiguration) => {
    try {
      return presetStorageService.exportPreset(preset);
    } catch (err) {
      setError("Failed to export preset");
      console.error(err);
      return null;
    }
  }, []);

  return {
    presets,
    selectedPresetId,
    isLoading,
    error,
    loadPreset,
    savePreset,
    deletePreset,
    importPreset,
    exportPreset
  };
};
