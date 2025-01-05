import React, { useEffect, useState } from "react";
import Layout from "../components/Layout";
import { useSettingsContext, type Settings } from "../services/settingsService";
import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";
import { Button } from "../components/ui/button";
import { Switch } from "../components/ui/switch";
import { useToast } from "../components/ui/use-toast";
import { checkOpenRouterAvailability, getAvailableModels } from "../services/openRouterService";
import { Loader2 } from "lucide-react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../components/ui/select";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "../components/ui/table";

interface OpenRouterModel {
  id: string;
  name: string;
  context_length: number;
  pricing: {
    prompt: string | number;
    completion: string | number;
  };
}

const Settings = () => {
  const { settings, updateSettings } = useSettingsContext();
  const { toast } = useToast();
  const [isValidating, setIsValidating] = useState(false);
  const [models, setModels] = useState<OpenRouterModel[]>([]);
  const [isLoadingModels, setIsLoadingModels] = useState(false);

  useEffect(() => {
    const loadModels = async () => {
      if (settings.openRouterApiKey) {
        setIsLoadingModels(true);
        try {
          const availableModels = await getAvailableModels(settings.openRouterApiKey);
          setModels(availableModels);
        } catch (error) {
          console.error('Failed to load models:', error);
        }
        setIsLoadingModels(false);
      }
    };

    loadModels();
  }, [settings.openRouterApiKey]);

  const handleApiKeyChange = async (apiKey: string) => {
    updateSettings({ openRouterApiKey: apiKey });
    
    if (apiKey) {
      setIsValidating(true);
      const isValid = await checkOpenRouterAvailability(apiKey);
      setIsValidating(false);

      toast({
        title: isValid ? "API Key Valid" : "API Key Invalid",
        description: isValid 
          ? "Successfully connected to OpenRouter" 
          : "Please check your API key and try again",
        variant: isValid ? "default" : "destructive",
      });
    }
  };

  const handleModelToggle = (modelId: string, enabled: boolean) => {
    const model = models.find(m => m.id === modelId);
    const promptPrice = typeof model?.pricing.prompt === 'string' 
      ? parseFloat(model.pricing.prompt) 
      : model?.pricing.prompt || 0;

    const updatedSettings: Partial<Settings> = {
      models: {
        ...settings.models,
        [modelId]: {
          enabled,
          contextWindow: model?.context_length || 4096,
          costPer1kTokens: promptPrice,
        }
      }
    };
    updateSettings(updatedSettings);
  };

  const enabledModels = Object.entries(settings.models || {})
    .filter(([_, model]) => model.enabled)
    .map(([id]) => id);

  const formatPrice = (price: string | number) => {
    const numPrice = typeof price === 'string' ? parseFloat(price) : price;
    return `$${numPrice.toFixed(4)}`;
  };

  return (
    <Layout title="Settings">
      <div className="container mx-auto p-4">
        <div className="max-w-4xl mx-auto space-y-8">
          <div className="glass-panel p-6 rounded-lg border border-border/40 bg-card/30 backdrop-blur">
            <h2 className="text-xl font-bold mb-6">OpenRouter Integration</h2>
            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="apiKey">API Key</Label>
                <div className="flex gap-2">
                  <Input
                    id="apiKey"
                    type="password"
                    value={settings.openRouterApiKey || ""}
                    onChange={(e) => handleApiKeyChange(e.target.value)}
                    placeholder="Enter your OpenRouter API key"
                    className="font-mono"
                  />
                  <Button 
                    onClick={() => handleApiKeyChange(settings.openRouterApiKey || '')}
                    disabled={isValidating || !settings.openRouterApiKey}
                  >
                    {isValidating ? (
                      <Loader2 className="h-4 w-4 animate-spin" />
                    ) : (
                      "Validate"
                    )}
                  </Button>
                </div>
                <p className="text-sm text-muted-foreground">
                  Get your API key from{" "}
                  <a
                    href="https://openrouter.ai/keys"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-primary hover:underline"
                  >
                    OpenRouter
                  </a>
                </p>
              </div>

              {settings.openRouterApiKey && (
                <div className="space-y-4 mt-6">
                  <div className="space-y-2">
                    <Label>Default Model</Label>
                    <Select
                      value={settings.defaultModel || 'deepseek-coder-33b'}
                      onValueChange={(value) => updateSettings({ defaultModel: value } as Partial<Settings>)}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Select default model" />
                      </SelectTrigger>
                      <SelectContent>
                        {enabledModels.map((modelId) => (
                          <SelectItem key={modelId} value={modelId}>
                            {modelId}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <p className="text-sm text-muted-foreground">
                      Select the default model for new playground sessions
                    </p>
                  </div>

                  <h3 className="text-lg font-semibold pt-4">Available Models</h3>
                  {isLoadingModels ? (
                    <div className="flex justify-center p-4">
                      <Loader2 className="h-6 w-6 animate-spin" />
                    </div>
                  ) : (
                    <Table>
                      <TableHeader>
                        <TableRow>
                          <TableHead>Model</TableHead>
                          <TableHead>Context Length</TableHead>
                          <TableHead>Price (per 1k tokens)</TableHead>
                          <TableHead>Enabled</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {models.map((model) => (
                          <TableRow key={model.id}>
                            <TableCell className="font-medium">
                              {model.name}
                              {model.id === settings.defaultModel && (
                                <span className="ml-2 text-xs text-muted-foreground">(Default)</span>
                              )}
                            </TableCell>
                            <TableCell>{model.context_length.toLocaleString()}</TableCell>
                            <TableCell>{formatPrice(model.pricing.prompt)}</TableCell>
                            <TableCell>
                              <Switch
                                checked={settings.models?.[model.id]?.enabled ?? false}
                                onCheckedChange={(checked) => handleModelToggle(model.id, checked)}
                              />
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  )}
                </div>
              )}
            </div>
          </div>

          <div className="glass-panel p-6 rounded-lg border border-border/40 bg-card/30 backdrop-blur">
            <h2 className="text-xl font-bold mb-6">Interface Settings</h2>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="space-y-1">
                  <Label>Dark Mode</Label>
                  <p className="text-sm text-muted-foreground">
                    Toggle dark/light theme
                  </p>
                </div>
                <Switch
                  checked={settings.theme === 'dark'}
                  onCheckedChange={(checked) => 
                    updateSettings({ theme: checked ? 'dark' : 'light' })
                  }
                />
              </div>

              <div className="space-y-2">
                <Label>Font Size</Label>
                <Input
                  type="number"
                  value={settings.fontSize || 14}
                  onChange={(e) => 
                    updateSettings({ fontSize: parseInt(e.target.value) || 14 })
                  }
                  min={12}
                  max={24}
                />
                <p className="text-sm text-muted-foreground">
                  Adjust the editor font size (12-24px)
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default Settings;
