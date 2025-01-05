export interface PresetConfiguration {
  id: string;
  name: string;
  description: string;
  settings: {
    model: string;
    temperature: number;
    maxTokens: number;
    topP: number;
    frequencyPenalty: number;
    presencePenalty: number;
    customSettings?: Record<string, any>;
  };
  metadata: {
    createdAt: string;
    updatedAt: string;
    tags?: string[];
  };
}

export type PresetList = PresetConfiguration[];

export interface PresetStorageState {
  presets: PresetList;
  selectedPresetId: string | null;
}
