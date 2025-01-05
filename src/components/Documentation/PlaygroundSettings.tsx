import React from "react";
import { Settings2, AlertCircle } from "lucide-react";
import { useState } from "react";
import { useSettingsContext } from "../../services/settingsService";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../ui/select";
import { Switch } from "../ui/switch";
import { Button } from "../ui/button";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "../ui/tooltip";
import { Slider } from "../ui/slider";
import { Input } from "../ui/input";
import { Label } from "../ui/label";

interface PlaygroundSettingsProps {
  onSettingsChange: (settings: PlaygroundSettings) => void;
}

export interface PlaygroundSettings {
  model: string;
  temperature: number;
  maxTokens: number;
  autoFormat: boolean;
  syntaxHighlighting: boolean;
  showLineNumbers: boolean;
}

export const PlaygroundSettings: React.FC<PlaygroundSettingsProps> = ({ onSettingsChange }) => {
  const { settings: globalSettings } = useSettingsContext();
  const [isOpen, setIsOpen] = useState(false);
  const [settings, setSettings] = useState<PlaygroundSettings>({
    model: "openai/gpt-3.5-turbo",
    temperature: 0.7,
    maxTokens: 1000,
    autoFormat: true,
    syntaxHighlighting: true,
    showLineNumbers: true
  });

  const hasOpenRouterKey = !!globalSettings?.openRouterApiKey;

  const models = hasOpenRouterKey ? [
    { value: "openai/gpt-4", label: "GPT-4" },
    { value: "openai/gpt-3.5-turbo", label: "GPT-3.5 Turbo" },
    { value: "anthropic/claude-2", label: "Claude 2" },
    { value: "anthropic/claude-instant-v1", label: "Claude Instant" }
  ] : [
    { value: "openai/gpt-3.5-turbo", label: "GPT-3.5 Turbo (OpenRouter API key required)" }
  ];


  const handleSettingChange = (key: keyof PlaygroundSettings, value: any) => {
    const newSettings = { ...settings, [key]: value };
    setSettings(newSettings);
    onSettingsChange(newSettings);
  };

  return (
    <div className="relative">
      <TooltipProvider>
        <Tooltip>
          <TooltipTrigger asChild>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setIsOpen(!isOpen)}
              className="relative"
            >
              <Settings2 className="w-4 h-4" />
              {!hasOpenRouterKey && (
                <AlertCircle className="w-3 h-3 text-yellow-500 absolute -top-1 -right-1" />
              )}
            </Button>
          </TooltipTrigger>
          {!hasOpenRouterKey && (
            <TooltipContent>
              <p>OpenRouter API key not configured. Some features may be limited.</p>
            </TooltipContent>
          )}
        </Tooltip>
      </TooltipProvider>

      {isOpen && (
        <div className="absolute right-0 top-10 w-80 p-4 rounded-lg border border-border/40 
                       bg-card/95 backdrop-blur-sm shadow-xl z-50">
          <h3 className="text-sm font-medium mb-4">Playground Settings</h3>
          
          <div className="space-y-4">
            <div className="space-y-2">
              <Label>Model</Label>
              <Select
                value={settings.model}
                onValueChange={(value) => handleSettingChange("model", value)}
                disabled={!hasOpenRouterKey}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select a model" />
                </SelectTrigger>
                <SelectContent>
                  {models.map((model) => (
                    <SelectItem key={model.value} value={model.value}>
                      {model.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              {!hasOpenRouterKey && (
                <p className="text-xs text-yellow-500">
                  Configure OpenRouter API key in settings to access more models
                </p>
              )}
            </div>

            <div className="space-y-2">
              <Label>Temperature</Label>
              <div className="pt-2">
                <Slider
                  min={0}
                  max={1}
                  step={0.1}
                  value={[settings.temperature]}
                  onValueChange={([value]) => handleSettingChange("temperature", value)}
                />
              </div>
              <div className="flex justify-between text-xs text-muted-foreground">
                <span>Precise</span>
                <span>{settings.temperature}</span>
                <span>Creative</span>
              </div>
            </div>

            <div className="space-y-2">
              <Label>Max Tokens</Label>
              <Input
                type="number"
                value={settings.maxTokens}
                onChange={(e) => handleSettingChange("maxTokens", parseInt(e.target.value))}
                min={1}
                max={4000}
              />
            </div>

            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <Label>Auto Format</Label>
                <Switch
                  checked={settings.autoFormat}
                  onCheckedChange={(checked) => handleSettingChange("autoFormat", checked)}
                />
              </div>

              <div className="flex items-center justify-between">
                <Label>Syntax Highlighting</Label>
                <Switch
                  checked={settings.syntaxHighlighting}
                  onCheckedChange={(checked) => handleSettingChange("syntaxHighlighting", checked)}
                />
              </div>

              <div className="flex items-center justify-between">
                <Label>Show Line Numbers</Label>
                <Switch
                  checked={settings.showLineNumbers}
                  onCheckedChange={(checked) => handleSettingChange("showLineNumbers", checked)}
                />
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
