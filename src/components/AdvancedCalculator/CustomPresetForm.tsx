import { useState } from "react";
import { Input } from "../ui/input";
import { Slider } from "../ui/slider";
import { Button } from "../ui/button";
import { Label } from "../ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../ui/select";
import { Switch } from "../ui/switch";
import { PresetConfiguration } from "./presetTypes";
import { v4 as uuidv4 } from "uuid";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "../ui/accordion";
import { Textarea } from "../ui/textarea";

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
  const [batchProcessing, setBatchProcessing] = useState(initialPreset?.settings.customSettings?.batchProcessing ?? false);
  const [compression, setCompression] = useState(initialPreset?.settings.customSettings?.compression ?? true);
  const [customPrompt, setCustomPrompt] = useState(initialPreset?.settings.customSettings?.customPrompt || "");
  const [responseFormat, setResponseFormat] = useState(initialPreset?.settings.customSettings?.responseFormat || "json");

  const models = [
    { id: "gpt-4o", name: "GPT-4O" },
    { id: "o1-mini", name: "O1-Mini" },
    { id: "o1-preview", name: "O1-Preview" },
    { id: "gpt-4", name: "GPT-4" }
  ];

  const generateSynthLangPrompt = (settings: any) => {
    return `↹ model.${settings.model} @openrouter
⊕ context(${settings.maxTokens}) ^format(${settings.customSettings?.responseFormat || 'json'})

# Optimizations
⊕ optimize [
  temperature: ${settings.temperature},
  streaming: ${settings.customSettings?.streamingEnabled},
  cache: ${settings.customSettings?.cacheEnabled},
  batch: ${settings.customSettings?.batchProcessing}
]

# Features
⊕ features [
  contextWindow: ${settings.maxTokens},
  topP: ${settings.topP},
  frequencyPenalty: ${settings.frequencyPenalty},
  presencePenalty: ${settings.presencePenalty}
]

# Configuration
⊕ config [
  compression: ${settings.customSettings?.compression},
  mode: "optimized"
]`;
  };

  const handleSave = () => {
    const settings = {
      model,
      temperature,
      maxTokens,
      topP,
      frequencyPenalty,
      presencePenalty,
      customSettings: {
        streamingEnabled,
        cacheEnabled,
        batchProcessing,
        compression,
        responseFormat,
        customPrompt: customPrompt || generateSynthLangPrompt({
          model,
          temperature,
          maxTokens,
          topP,
          frequencyPenalty,
          presencePenalty,
          customSettings: {
            streamingEnabled,
            cacheEnabled,
            batchProcessing,
            compression,
            responseFormat
          }
        })
      }
    };

    const preset: PresetConfiguration = {
      id: initialPreset?.id || uuidv4(),
      name,
      description,
      settings,
      metadata: {
        createdAt: initialPreset?.metadata.createdAt || new Date().toISOString(),
        updatedAt: new Date().toISOString(),
        tags: initialPreset?.metadata.tags || ["custom"]
      }
    };
    onSave(preset);
  };

  return (
    <div className="space-y-6">
      <div className="space-y-4">
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
      </div>

      <Accordion type="multiple" className="w-full">
        <AccordionItem value="basic-settings">
          <AccordionTrigger>Basic Settings</AccordionTrigger>
          <AccordionContent>
            <div className="space-y-4 pt-4">
              <div className="space-y-2">
                <Label>Temperature ({temperature})</Label>
                <Slider
                  value={[temperature]}
                  onValueChange={([value]) => setTemperature(value)}
                  min={0}
                  max={1}
                  step={0.1}
                />
                <p className="text-sm text-muted-foreground">Controls randomness in output generation</p>
              </div>

              <div className="space-y-2">
                <Label>Max Tokens ({maxTokens})</Label>
                <Slider
                  value={[maxTokens]}
                  onValueChange={([value]) => setMaxTokens(value)}
                  min={256}
                  max={8192}
                  step={256}
                />
                <p className="text-sm text-muted-foreground">Maximum length of generated responses</p>
              </div>

              <div className="space-y-2">
                <Label>Response Format</Label>
                <Select value={responseFormat} onValueChange={setResponseFormat}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select format" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="json">JSON</SelectItem>
                    <SelectItem value="markdown">Markdown</SelectItem>
                    <SelectItem value="text">Plain Text</SelectItem>
                    <SelectItem value="custom">Custom Schema</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </AccordionContent>
        </AccordionItem>

        <AccordionItem value="advanced-settings">
          <AccordionTrigger>Advanced Settings</AccordionTrigger>
          <AccordionContent>
            <div className="space-y-4 pt-4">
              <div className="space-y-2">
                <Label>Top P ({topP})</Label>
                <Slider
                  value={[topP]}
                  onValueChange={([value]) => setTopP(value)}
                  min={0}
                  max={1}
                  step={0.1}
                />
                <p className="text-sm text-muted-foreground">Nucleus sampling threshold</p>
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
                <p className="text-sm text-muted-foreground">Reduces repetition of token sequences</p>
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
                <p className="text-sm text-muted-foreground">Encourages discussing new topics</p>
              </div>
            </div>
          </AccordionContent>
        </AccordionItem>

        <AccordionItem value="optimizations">
          <AccordionTrigger>Optimizations</AccordionTrigger>
          <AccordionContent>
            <div className="space-y-4 pt-4">
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

              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label>Batch Processing</Label>
                  <div className="text-sm text-muted-foreground">
                    Process multiple requests in batches
                  </div>
                </div>
                <Switch
                  checked={batchProcessing}
                  onCheckedChange={setBatchProcessing}
                />
              </div>

              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label>Token Compression</Label>
                  <div className="text-sm text-muted-foreground">
                    Compress tokens for reduced API costs
                  </div>
                </div>
                <Switch
                  checked={compression}
                  onCheckedChange={setCompression}
                />
              </div>
            </div>
          </AccordionContent>
        </AccordionItem>

        <AccordionItem value="custom-prompt">
          <AccordionTrigger>Custom System Prompt</AccordionTrigger>
          <AccordionContent>
            <div className="space-y-4 pt-4">
              <div className="space-y-2">
                <Label>Custom Prompt</Label>
                <Textarea
                  value={customPrompt}
                  onChange={(e) => setCustomPrompt(e.target.value)}
                  placeholder="Enter custom system prompt..."
                  className="min-h-[200px] font-mono text-sm"
                />
              </div>

              <div className="space-y-2">
                <Label>Generated SynthLang Prompt</Label>
                <pre className="p-2 bg-black/20 rounded text-xs font-mono overflow-x-auto">
                  {generateSynthLangPrompt({
                    model,
                    temperature,
                    maxTokens,
                    topP,
                    frequencyPenalty,
                    presencePenalty,
                    customSettings: {
                      streamingEnabled,
                      cacheEnabled,
                      batchProcessing,
                      compression,
                      responseFormat
                    }
                  })}
                </pre>
                <p className="text-sm text-muted-foreground">
                  This is the default SynthLang prompt that will be used if no custom prompt is provided.
                </p>
              </div>

              <div className="text-sm text-muted-foreground mt-4">
                <p>Tips for Custom Prompts:</p>
                <ul className="list-disc list-inside space-y-1 mt-2">
                  <li>Use SynthLang syntax for optimal performance</li>
                  <li>Include framework-specific glyphs when needed</li>
                  <li>Define clear optimization parameters</li>
                  <li>Specify response format requirements</li>
                </ul>
              </div>
            </div>
          </AccordionContent>
        </AccordionItem>
      </Accordion>

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
