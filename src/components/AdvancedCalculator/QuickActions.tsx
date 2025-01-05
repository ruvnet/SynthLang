import { useState } from "react";
import { Download, Upload, Search, Tag, Star, Clock, Settings2, Plus, Edit } from "lucide-react";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "../ui/dialog";
import { Button } from "../ui/button";
import { ScrollArea } from "../ui/scroll-area";
import { usePresetManager } from "../../hooks/usePresetManager";
import { PresetConfiguration } from "./presetTypes";
import { Textarea } from "../ui/textarea";
import { Input } from "../ui/input";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../ui/tabs";
import { Badge } from "../ui/badge";
import { CustomPresetForm } from "./CustomPresetForm";
import { DEFAULT_FRAMEWORKS_CONFIG } from "./constants";
import type { SynthLangConfig } from "./types";
import { optimizedPresets } from "./optimizedPresets";

export const QuickActions = () => {
  const {
    presets,
    isLoading,
    error,
    loadPreset,
    importPreset,
    exportPreset,
    savePreset,
  } = usePresetManager();

  const [isLoadOpen, setIsLoadOpen] = useState(false);
  const [isExportOpen, setIsExportOpen] = useState(false);
  const [exportData, setExportData] = useState("");
  const [importData, setImportData] = useState("");
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedPreset, setSelectedPreset] = useState<PresetConfiguration | null>(null);
  const [activeTab, setActiveTab] = useState("optimized");
  const [isCreatingPreset, setIsCreatingPreset] = useState(false);

  const filteredPresets = (presetList: PresetConfiguration[]) => {
    if (!searchQuery) return presetList;
    const query = searchQuery.toLowerCase();
    return presetList.filter(
      preset => 
        preset.name.toLowerCase().includes(query) ||
        preset.description.toLowerCase().includes(query) ||
        preset.metadata.tags?.some(tag => tag.toLowerCase().includes(query))
    );
  };

  const renderPresetCard = (preset: PresetConfiguration, onClick: () => void, onEdit?: () => void) => (
    <div
      key={preset.id}
      className="w-full glass-panel p-4 hover:bg-accent/50 transition-colors text-left space-y-2"
    >
      <div 
        className="cursor-pointer" 
        onClick={onClick}
      >
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-2">
            <Settings2 className="w-4 h-4 text-purple-400" />
            <h4 className="font-semibold">{preset.name}</h4>
          </div>
          <div className="flex items-center gap-2">
            {onEdit && (
              <Button
                variant="ghost"
                size="icon"
                className="h-8 w-8"
                onClick={(e) => {
                  e.stopPropagation();
                  onEdit();
                }}
              >
                <Edit className="h-4 w-4" />
              </Button>
            )}
            <Clock className="w-4 h-4 text-muted-foreground" />
            <span className="text-xs text-muted-foreground">
              {new Date(preset.metadata.updatedAt).toLocaleDateString()}
            </span>
          </div>
        </div>
        <p className="text-sm text-muted-foreground">{preset.description}</p>
        <div className="flex flex-wrap gap-2 mt-2">
          {preset.settings.customSettings?.streamingEnabled && (
            <Badge variant="outline" className="text-xs">
              Streaming
            </Badge>
          )}
          {preset.settings.customSettings?.cacheEnabled && (
            <Badge variant="outline" className="text-xs">
              Caching
            </Badge>
          )}
          {preset.settings.customSettings?.parallelProcessing && (
            <Badge variant="outline" className="text-xs">
              Parallel
            </Badge>
          )}
          {preset.settings.customSettings?.batchProcessing && (
            <Badge variant="outline" className="text-xs">
              Batch
            </Badge>
          )}
          {preset.metadata.tags?.map(tag => (
            <Badge key={tag} variant="secondary" className="text-xs">
              {tag}
            </Badge>
          ))}
        </div>
        <div className="flex items-center gap-4 text-xs text-muted-foreground mt-2">
          <div>
            <span className="font-medium">Model:</span> {preset.settings.model}
          </div>
          <div>
            <span className="font-medium">Temperature:</span> {preset.settings.temperature}
          </div>
          <div>
            <span className="font-medium">Context:</span> {(preset.settings.maxTokens / 1024).toFixed(1)}K
          </div>
        </div>
      </div>
    </div>
  );

  const handleLoadPreset = async (preset: PresetConfiguration, isOptimized: boolean = false) => {
    try {
      // Only try to load from storage if it's not an optimized preset
      if (!isOptimized) {
        await loadPreset(preset.id);
      }
      
      // Map preset settings to calculator configuration directly
      const config: SynthLangConfig = {
        model: preset.settings.model,
        contextSize: preset.settings.maxTokens,
        features: {
          contextWindow: preset.settings.maxTokens,
          temperature: preset.settings.temperature,
          streamingMode: preset.settings.customSettings?.streamingEnabled ?? true,
          customPrompt: preset.settings.customSettings?.customPrompt || "",
          responseFormat: "json"
        },
        optimizations: {
          caching: preset.settings.customSettings?.cacheEnabled ?? true,
          batchProcessing: preset.settings.customSettings?.batchProcessing ?? false,
          compression: true
        },
        frameworks: DEFAULT_FRAMEWORKS_CONFIG,
        customFrameworks: []
      };

      localStorage.setItem('synthLang.calculatorConfig', JSON.stringify(config));
      
      // Dispatch storage event to trigger config update
      window.dispatchEvent(new StorageEvent('storage', {
        key: 'synthLang.calculatorConfig',
        newValue: JSON.stringify(config)
      }));

      setIsLoadOpen(false);
    } catch (err) {
      console.error('Failed to load preset:', err);
    }
  };

  const handleExportPreset = (preset: PresetConfiguration) => {
    const exportedData = exportPreset(preset);
    if (exportedData) {
      setExportData(exportedData);
      setIsExportOpen(true);
    }
  };

  const handleImportPreset = () => {
    try {
      importPreset(importData);
      setImportData("");
      setIsLoadOpen(false);
    } catch (err) {
      console.error("Failed to import preset:", err);
    }
  };

  const handleEditPreset = (preset: PresetConfiguration) => {
    setActiveTab("custom");
    // Use setTimeout to ensure the tab switch happens before setting the form state
    setTimeout(() => {
      setSelectedPreset(preset);
      setIsCreatingPreset(true);
    }, 0);
  };

  return (
    <div className="grid md:grid-cols-2 gap-4">
      {/* Load Preset Dialog */}
      <Dialog open={isLoadOpen} onOpenChange={setIsLoadOpen}>
        <DialogTrigger asChild>
          <button className="glass-panel p-4 hover:bg-accent/50 transition-colors text-left">
            <div className="flex items-center gap-2 mb-2">
              <Download className="w-5 h-5 text-purple-400" />
              <h3 className="font-semibold">Load Preset Configuration</h3>
            </div>
            <p className="text-sm text-muted-foreground">Use optimized settings for common scenarios</p>
          </button>
        </DialogTrigger>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>Load Preset Configuration</DialogTitle>
            <DialogDescription>
              Choose from optimized presets or load your custom configurations
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4 py-4">
            {error && <p className="text-red-500">{error}</p>}
            
            <div className="flex items-center space-x-2 mb-4">
              <Search className="w-4 h-4 text-muted-foreground" />
              <Input
                placeholder="Search presets..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="flex-1"
              />
            </div>

            <Tabs value={activeTab} onValueChange={setActiveTab}>
              <TabsList className="w-full">
                <TabsTrigger value="optimized" className="flex-1">
                  <Star className="w-4 h-4 mr-2" />
                  Optimized
                </TabsTrigger>
                <TabsTrigger value="custom" className="flex-1">
                  <Tag className="w-4 h-4 mr-2" />
                  Custom
                </TabsTrigger>
                <TabsTrigger value="import" className="flex-1">
                  <Download className="w-4 h-4 mr-2" />
                  Import
                </TabsTrigger>
              </TabsList>

              <TabsContent value="optimized" className="mt-4">
                <ScrollArea className="h-[400px] pr-4">
                  <div className="space-y-3">
                    {filteredPresets(optimizedPresets as unknown as PresetConfiguration[]).map((preset) => 
                      renderPresetCard(
                        preset,
                        () => handleLoadPreset(preset, true),
                        () => handleEditPreset(preset)
                      )
                    )}
                  </div>
                </ScrollArea>
              </TabsContent>

              <TabsContent value="custom" className="mt-4">
                {(isCreatingPreset || selectedPreset) && activeTab === "custom" ? (
                  <div className="space-y-4">
                    <div className="flex justify-between items-center">
                      <h3 className="text-lg font-semibold">
                        {selectedPreset ? 'Edit Preset' : 'Create New Preset'}
                      </h3>
                      <Button
                        variant="ghost"
                        onClick={() => {
                          setIsCreatingPreset(false);
                          setSelectedPreset(null);
                        }}
                      >
                        Cancel
                      </Button>
                    </div>
                    <CustomPresetForm
                      onSave={(preset) => {
                        if (selectedPreset) {
                          // When editing an optimized preset, create a new custom preset
                          const newPreset = {
                            ...preset,
                            metadata: {
                              ...preset.metadata,
                              tags: [...(preset.metadata.tags || []), "custom", "optimized-based"]
                            }
                          };
                          savePreset(newPreset);
                        } else {
                          savePreset(preset);
                        }
                        setIsCreatingPreset(false);
                        setSelectedPreset(null);
                      }}
                      onCancel={() => {
                        setIsCreatingPreset(false);
                        setSelectedPreset(null);
                      }}
                      initialPreset={selectedPreset}
                    />
                  </div>
                ) : (
                  <div className="space-y-4">
                    <div className="flex justify-between items-center">
                      <h3 className="text-lg font-semibold">Custom Presets</h3>
                      <Button
                        onClick={() => setIsCreatingPreset(true)}
                        className="flex items-center gap-2"
                      >
                        <Plus className="w-4 h-4" />
                        New Preset
                      </Button>
                    </div>
                    <ScrollArea className="h-[400px] pr-4">
                      <div className="space-y-3">
                        {filteredPresets(presets).length > 0 ? (
                          filteredPresets(presets).map((preset) => 
                            renderPresetCard(preset, () => handleLoadPreset(preset))
                          )
                        ) : (
                          <div className="text-center text-muted-foreground py-8">
                            <p>No custom presets yet.</p>
                            <p className="text-sm">Create one to get started!</p>
                          </div>
                        )}
                      </div>
                    </ScrollArea>
                  </div>
                )}
              </TabsContent>

              <TabsContent value="import" className="mt-4">
                <div className="space-y-4">
                  <div className="glass-panel p-4">
                    <h4 className="font-semibold mb-2">Import from JSON</h4>
                    <p className="text-sm text-muted-foreground mb-4">
                      Paste a previously exported preset configuration to import it.
                    </p>
                    <Textarea
                      value={importData}
                      onChange={(e) => setImportData(e.target.value)}
                      placeholder="Paste preset JSON here..."
                      className="h-[200px] font-mono text-sm"
                    />
                    <Button 
                      onClick={handleImportPreset}
                      disabled={!importData.trim()}
                      className="w-full mt-4"
                    >
                      Import Configuration
                    </Button>
                  </div>
                </div>
              </TabsContent>
            </Tabs>
          </div>
        </DialogContent>
      </Dialog>

      {/* Export Settings Dialog */}
      <Dialog open={isExportOpen} onOpenChange={setIsExportOpen}>
        <DialogTrigger asChild>
          <button className="glass-panel p-4 hover:bg-accent/50 transition-colors text-left">
            <div className="flex items-center gap-2 mb-2">
              <Upload className="w-5 h-5 text-blue-400" />
              <h3 className="font-semibold">Export Settings</h3>
            </div>
            <p className="text-sm text-muted-foreground">Save your configuration for later use</p>
          </button>
        </DialogTrigger>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>Export Settings</DialogTitle>
            <DialogDescription>
              Export your preset configurations to share or backup
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <ScrollArea className="h-[300px] pr-4">
              <div className="space-y-2">
                {presets.map((preset) => (
                  <button
                    key={preset.id}
                    onClick={() => handleExportPreset(preset)}
                    className="w-full glass-panel p-3 hover:bg-accent/50 transition-colors text-left"
                  >
                    <h4 className="font-semibold">{preset.name}</h4>
                    <p className="text-sm text-muted-foreground">{preset.description}</p>
                  </button>
                ))}
              </div>
            </ScrollArea>
            {exportData && (
              <div className="space-y-2">
                <h4 className="font-semibold">Exported Configuration</h4>
                <Textarea
                  value={exportData}
                  readOnly
                  className="h-[200px] font-mono text-sm"
                />
                <Button
                  onClick={() => {
                    navigator.clipboard.writeText(exportData);
                  }}
                  className="w-full"
                >
                  Copy to Clipboard
                </Button>
              </div>
            )}
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
};
