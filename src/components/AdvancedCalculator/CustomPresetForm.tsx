import { useState, useEffect } from "react";
import { Input } from "../ui/input";
import { Slider } from "../ui/slider";
import { Button } from "../ui/button";
import { Label } from "../ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../ui/select";
import { Switch } from "../ui/switch";
import { PresetConfiguration } from "./presetTypes";
import { v4 as uuidv4 } from "uuid";

interface CustomPresetFormProps {
  onSave: (preset: PresetConfiguration) => void;
  onCancel: () => void;
  initialPreset?: PresetConfiguration;
}

export const CustomPresetForm = ({ onSave, onCancel, initialPreset }: CustomPresetFormProps) => {
  const [name, setName] = useState(initialPreset?.name || "");
  const [description, setDescription] = useState(initialPreset?.description || "");
  const [model, setModel] = useState(initialPreset?.settings.model || "");
  const [temperature, setTemperature] = useState(initialPreset?.settings.temperature || 0.7);
  const [maxTokens, setMaxTokens] = useState(initialPreset?.settings.maxTokens || 2048);
  const [topP, setTopP] = useState(initialPreset?.settings.topP || 0.9);
  const [frequencyPenalty, setFrequencyPenalty] = useState(initialPreset?.settings.frequencyPenalty || 0.3);
  const [presencePenalty, setPresencePenalty] = useState(initialPreset?.settings.presencePenalty || 0.3);
  const [streamingEnabled, setStreamingEnabled] = useState(initialPreset?.settings.customSettings?.streamingEnabled ?? true);
  const [cacheEnabled, setCacheEnabled] = useState(initialPreset?.settings.customSettings?.cacheEnabled ?? true);

  const models = [
    { id: "gpt-4o", name: "GPT-4O" },
    { id: "o1-mini", name: "O1-Mini" },
    { id: "o1-preview", name: "O1-Preview" },
    { id: "gpt-4", name: "GPT-4" }
  ];

  const handleSave = () => {
    const preset: PresetConfiguration = {
      id: uuidv4(),
      name,
      description,
      settings: {
        model,
        temperature,
        maxTokens,
        topP,
        frequencyPenalty,
        presencePenalty,
        customSettings: {
          streamingEnabled,
          cacheEnabled,
        }
      },
      metadata: {
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
        tags: ["custom"]
      }
    };
    onSave(preset);
  };

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <Label>Name</Label>
        <Input
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="My Custom Preset"
        />
      </div>

      <div className="space-y-2">
        <Label>Description</Label>
        <Input
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Description of your preset configuration"
        />
      </div>

      <div className="space-y-2">
        <Label>Model</Label>
        <Select value={model} onValueChange={setModel}>
          <SelectTrigger>
            <SelectValue placeholder="Select model" />
          </SelectTrigger>
          <SelectContent>
            {models.map((m) => (
              <SelectItem key={m.id} value={m.id}>
                {m.name}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <div className="space-y-2">
        <Label>Temperature ({temperature})</Label>
        <Slider
          value={[temperature]}
          onValueChange={([value]) => setTemperature(value)}
          min={0}
          max={1}
          step={0.1}
        />
      </div>

      <div className="space-y-2">
        <Label>Max Tokens ({maxTokens})</Label>
        <Slider
          value={[maxTokens]}
          onValueChange={([value]) => setMaxTokens(value)}
          min={256}
          max={4096}
          step={256}
        />
      </div>

      <div className="space-y-2">
        <Label>Top P ({topP})</Label>
        <Slider
          value={[topP]}
          onValueChange={([value]) => setTopP(value)}
          min={0}
          max={1}
          step={0.1}
        />
      </div>

      <div className="space-y-2">
        <Label>Frequency Penalty ({frequencyPenalty})</Label>
        <Slider
          value={[frequencyPenalty]}
          onValueChange={([value]) => setFrequencyPenalty(value)}
          min={0}
          max={2}
          step={0.1}
        />
      </div>

      <div className="space-y-2">
        <Label>Presence Penalty ({presencePenalty})</Label>
        <Slider
          value={[presencePenalty]}
          onValueChange={([value]) => setPresencePenalty(value)}
          min={0}
          max={2}
          step={0.1}
        />
      </div>

      <div className="flex items-center justify-between">
        <div className="space-y-0.5">
          <Label>Streaming</Label>
          <div className="text-sm text-muted-foreground">
            Enable real-time response streaming
          </div>
        </div>
        <Switch
          checked={streamingEnabled}
          onCheckedChange={setStreamingEnabled}
        />
      </div>

      <div className="flex items-center justify-between">
        <div className="space-y-0.5">
          <Label>Response Caching</Label>
          <div className="text-sm text-muted-foreground">
            Cache responses for improved performance
          </div>
        </div>
        <Switch
          checked={cacheEnabled}
          onCheckedChange={setCacheEnabled}
        />
      </div>

      <div className="flex justify-end space-x-2 pt-4">
        <Button variant="outline" onClick={onCancel}>
          Cancel
        </Button>
        <Button onClick={handleSave} disabled={!name || !description || !model}>
          {initialPreset ? 'Save Changes' : 'Create Preset'}
        </Button>
      </div>
    </div>
  );
};
