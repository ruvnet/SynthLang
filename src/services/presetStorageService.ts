import { PresetConfiguration, PresetList } from "../components/AdvancedCalculator/presetTypes";

const STORAGE_KEY = "synthLang.presets";

export const presetStorageService = {
  listPresets: (): PresetList => {
    return presetStorageService.getPresets();
  },

  loadPreset: (presetId: string): PresetConfiguration | null => {
    const presets = presetStorageService.getPresets();
    return presets.find(p => p.id === presetId) || null;
  },

  savePreset: (preset: PresetConfiguration): void => {
    const presets = presetStorageService.getPresets();
    const existingIndex = presets.findIndex(p => p.id === preset.id);
    
    if (existingIndex >= 0) {
      presets[existingIndex] = preset;
    } else {
      presets.push(preset);
    }
    
    localStorage.setItem(STORAGE_KEY, JSON.stringify(presets));
  },

  getPresets: (): PresetList => {
    const storedPresets = localStorage.getItem(STORAGE_KEY);
    return storedPresets ? JSON.parse(storedPresets) : [];
  },

  deletePreset: (presetId: string): void => {
    const presets = presetStorageService.getPresets();
    const filteredPresets = presets.filter(p => p.id !== presetId);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(filteredPresets));
  },

  exportPreset: (preset: PresetConfiguration): string => {
    return JSON.stringify(preset, null, 2);
  },

  importPreset: (presetJson: string): PresetConfiguration => {
    try {
      const preset = JSON.parse(presetJson) as PresetConfiguration;
      
      // Validate required fields
      if (!preset.id || !preset.name || !preset.settings) {
        throw new Error("Invalid preset format");
      }
      
      return preset;
    } catch (error) {
      throw new Error("Failed to parse preset JSON");
    }
  }
};
