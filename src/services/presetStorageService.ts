import { CalculatorPreset, PresetMetadata, DEFAULT_PRESETS } from '../components/AdvancedCalculator/presetTypes';

const STORAGE_KEY = 'calculator_presets';
const PRESET_IDS_KEY = 'calculator_preset_ids';

export class LocalPresetStorageService {
  private async getStoredPresets(): Promise<Record<string, CalculatorPreset>> {
    const storedData = localStorage.getItem(STORAGE_KEY);
    let presets: Record<string, CalculatorPreset>;
    
    if (!storedData) {
      // Initialize with default presets
      presets = DEFAULT_PRESETS.reduce((acc, preset) => {
        acc[preset.id] = preset;
        return acc;
      }, {} as Record<string, CalculatorPreset>);
    } else {
      presets = JSON.parse(storedData);
      // Ensure default presets are always available
      DEFAULT_PRESETS.forEach(preset => {
        if (!presets[preset.id]) {
          presets[preset.id] = preset;
        }
      });
    }
    
    await this.setStoredPresets(presets);
    return presets;
  }

  private async setStoredPresets(presets: Record<string, CalculatorPreset>): Promise<void> {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(presets));
  }

  async savePreset(preset: CalculatorPreset): Promise<void> {
    const presets = await this.getStoredPresets();
    preset.updatedAt = new Date().toISOString();
    if (!preset.createdAt) {
      preset.createdAt = preset.updatedAt;
    }
    presets[preset.id] = preset;
    await this.setStoredPresets(presets);
  }

  async loadPreset(id: string): Promise<CalculatorPreset | null> {
    const presets = await this.getStoredPresets();
    return presets[id] || null;
  }

  async listPresets(): Promise<PresetMetadata[]> {
    const presets = await this.getStoredPresets();
    return Object.values(presets).map(preset => ({
      id: preset.id,
      name: preset.name,
      description: preset.description,
      createdAt: preset.createdAt,
      updatedAt: preset.updatedAt
    }));
  }

  async deletePreset(id: string): Promise<void> {
    const presets = await this.getStoredPresets();
    // Don't allow deletion of default presets
    if (DEFAULT_PRESETS.some(p => p.id === id)) {
      throw new Error('Cannot delete default preset');
    }
    delete presets[id];
    await this.setStoredPresets(presets);
  }

  async exportPreset(id: string): Promise<string> {
    const preset = await this.loadPreset(id);
    if (!preset) {
      throw new Error('Preset not found');
    }
    return JSON.stringify(preset, null, 2);
  }

  async importPreset(data: string): Promise<CalculatorPreset> {
    try {
      const preset = JSON.parse(data) as CalculatorPreset;
      
      // Validate required fields
      if (!preset.id || !preset.name || !preset.features) {
        throw new Error('Invalid preset format');
      }

      // Generate new ID if it already exists
      const presets = await this.getStoredPresets();
      if (presets[preset.id]) {
        preset.id = `${preset.id}_${Date.now()}`;
      }

      // Update timestamps
      preset.createdAt = new Date().toISOString();
      preset.updatedAt = preset.createdAt;

      await this.savePreset(preset);
      return preset;
    } catch (error) {
      throw new Error('Failed to import preset: Invalid format');
    }
  }
}

// Export singleton instance
export const presetStorageService = new LocalPresetStorageService();
