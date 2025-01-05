import React from 'react';
import { Button } from '../ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { SynthLangConfig } from './types';

export interface PresetManagerProps {
  config: SynthLangConfig;
  onConfigChange: (config: SynthLangConfig) => void;
}

export const PresetManager: React.FC<PresetManagerProps> = ({ config, onConfigChange }) => {
  const [presets, setPresets] = React.useState<{ name: string; config: SynthLangConfig }[]>(() => {
    const savedPresets = localStorage.getItem('synthLangPresets');
    return savedPresets ? JSON.parse(savedPresets) : [];
  });

  const savePreset = React.useCallback(() => {
    const name = prompt('Enter a name for this preset:');
    if (!name) return;

    const newPreset = { name, config };
    const updatedPresets = [...presets, newPreset];
    setPresets(updatedPresets);
    localStorage.setItem('synthLangPresets', JSON.stringify(updatedPresets));
  }, [config, presets]);

  const loadPreset = React.useCallback((preset: { name: string; config: SynthLangConfig }) => {
    onConfigChange(preset.config);
  }, [onConfigChange]);

  const deletePreset = React.useCallback((index: number) => {
    const updatedPresets = presets.filter((_, i) => i !== index);
    setPresets(updatedPresets);
    localStorage.setItem('synthLangPresets', JSON.stringify(updatedPresets));
  }, [presets]);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-semibold">Configuration Presets</h3>
        <Button onClick={savePreset}>Save Current Config</Button>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {presets.map((preset, index) => (
          <Card key={index}>
            <CardHeader>
              <CardTitle>{preset.name}</CardTitle>
              <CardDescription>Saved configuration preset</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex justify-between">
                <Button variant="outline" onClick={() => loadPreset(preset)}>
                  Load
                </Button>
                <Button variant="destructive" onClick={() => deletePreset(index)}>
                  Delete
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {presets.length === 0 && (
        <div className="text-center text-muted-foreground py-8">
          No saved presets. Save your current configuration to create a preset.
        </div>
      )}
    </div>
  );
};
