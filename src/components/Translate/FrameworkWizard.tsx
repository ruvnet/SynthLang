import { useState } from "react";
import { Plus, X, ArrowRight, ArrowLeft, Save, Trash } from "lucide-react";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "../ui/dialog";
import { Input } from "../ui/input";
import { Textarea } from "../ui/textarea";
import { Button } from "../ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../ui/select";
import { CustomFramework, generateFrameworkId, saveCustomFramework } from "../../services/frameworkStorage";
import { GlyphInfo } from "../AdvancedCalculator/types";

interface FrameworkWizardProps {
  onFrameworkCreated: (framework: CustomFramework) => void;
}

interface WizardStep {
  title: string;
  description: string;
}

const STEPS: WizardStep[] = [
  {
    title: "Basic Information",
    description: "Enter the basic details of your framework"
  },
  {
    title: "Framework Details",
    description: "Provide detailed information about your framework"
  },
  {
    title: "Glyphs",
    description: "Add glyphs and their meanings"
  },
  {
    title: "Examples",
    description: "Add usage examples"
  }
];

const FRAMEWORK_GROUPS = [
  'mathematical',
  'logographic',
  'semitic',
  'classical',
  'constructed',
  'optimization'
] as const;

export const FrameworkWizard = ({ onFrameworkCreated }: FrameworkWizardProps) => {
  const [open, setOpen] = useState(false);
  const [step, setStep] = useState(0);
  const [framework, setFramework] = useState<Partial<CustomFramework>>({
    id: '',
    name: '',
    description: '',
    details: '',
    group: 'mathematical',
    applications: [],
    glyphs: [],
    examples: []
  });
  const [newGlyph, setNewGlyph] = useState<Partial<GlyphInfo>>({
    symbol: '',
    name: '',
    description: '',
    usage: ''
  });
  const [newExample, setNewExample] = useState('');
  const [newApplication, setNewApplication] = useState('');

  const resetForm = () => {
    setStep(0);
    setFramework({
      id: '',
      name: '',
      description: '',
      details: '',
      group: 'mathematical',
      applications: [],
      glyphs: [],
      examples: []
    });
    setNewGlyph({
      symbol: '',
      name: '',
      description: '',
      usage: ''
    });
    setNewExample('');
    setNewApplication('');
  };

  const handleClose = () => {
    setOpen(false);
    resetForm();
  };

  const handleNext = () => {
    if (step < STEPS.length - 1) {
      setStep(step + 1);
    }
  };

  const handleBack = () => {
    if (step > 0) {
      setStep(step - 1);
    }
  };

  const handleSave = () => {
    const newFramework: CustomFramework = {
      ...framework as CustomFramework,
      id: generateFrameworkId(),
      createdAt: Date.now(),
      updatedAt: Date.now()
    };
    saveCustomFramework(newFramework);
    onFrameworkCreated(newFramework);
    handleClose();
  };

  const addGlyph = () => {
    if (newGlyph.symbol && newGlyph.name && newGlyph.description && newGlyph.usage) {
      setFramework(prev => ({
        ...prev,
        glyphs: [...(prev.glyphs || []), newGlyph as GlyphInfo]
      }));
      setNewGlyph({
        symbol: '',
        name: '',
        description: '',
        usage: ''
      });
    }
  };

  const removeGlyph = (index: number) => {
    setFramework(prev => ({
      ...prev,
      glyphs: prev.glyphs?.filter((_, i) => i !== index)
    }));
  };

  const addExample = () => {
    if (newExample.trim()) {
      setFramework(prev => ({
        ...prev,
        examples: [...(prev.examples || []), newExample.trim()]
      }));
      setNewExample('');
    }
  };

  const removeExample = (index: number) => {
    setFramework(prev => ({
      ...prev,
      examples: prev.examples?.filter((_, i) => i !== index)
    }));
  };

  const addApplication = () => {
    if (newApplication.trim()) {
      setFramework(prev => ({
        ...prev,
        applications: [...(prev.applications || []), newApplication.trim()]
      }));
      setNewApplication('');
    }
  };

  const removeApplication = (index: number) => {
    setFramework(prev => ({
      ...prev,
      applications: prev.applications?.filter((_, i) => i !== index)
    }));
  };

  const renderStep = () => {
    switch (step) {
      case 0:
        return (
          <div className="space-y-4">
            <div>
              <label className="text-sm font-medium mb-1.5 block">Framework Name</label>
              <Input
                value={framework.name}
                onChange={e => setFramework(prev => ({ ...prev, name: e.target.value }))}
                placeholder="Enter framework name"
                className="text-base sm:text-sm"
              />
            </div>
            <div>
              <label className="text-sm font-medium mb-1.5 block">Framework Group</label>
              <Select
                value={framework.group}
                onValueChange={value => setFramework(prev => ({ ...prev, group: value as typeof FRAMEWORK_GROUPS[number] }))}
              >
                <SelectTrigger className="text-base sm:text-sm">
                  <SelectValue placeholder="Select a group" />
                </SelectTrigger>
                <SelectContent>
                  {FRAMEWORK_GROUPS.map(group => (
                    <SelectItem key={group} value={group} className="text-base sm:text-sm">
                      {group.charAt(0).toUpperCase() + group.slice(1)}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div>
              <label className="text-sm font-medium mb-1.5 block">Short Description</label>
              <Input
                value={framework.description}
                onChange={e => setFramework(prev => ({ ...prev, description: e.target.value }))}
                placeholder="Brief description of the framework"
                className="text-base sm:text-sm"
              />
            </div>
          </div>
        );

      case 1:
        return (
          <div className="space-y-4">
            <div>
              <label className="text-sm font-medium mb-1.5 block">Detailed Description</label>
              <Textarea
                value={framework.details}
                onChange={e => setFramework(prev => ({ ...prev, details: e.target.value }))}
                placeholder="Detailed explanation of your framework"
                className="min-h-[100px] text-base sm:text-sm"
              />
            </div>
            <div>
              <label className="text-sm font-medium mb-1.5 block">Applications</label>
              <div className="space-y-3">
                <div className="flex flex-col sm:flex-row gap-2">
                  <Input
                    value={newApplication}
                    onChange={e => setNewApplication(e.target.value)}
                    placeholder="Add an application"
                    className="text-base sm:text-sm flex-1"
                  />
                  <Button onClick={addApplication} type="button" className="text-base sm:text-sm w-full sm:w-auto">
                    Add
                  </Button>
                </div>
                <div className="space-y-2 max-h-[200px] overflow-y-auto">
                  {framework.applications?.map((app, index) => (
                    <div key={index} className="flex items-center justify-between bg-accent/20 p-2 rounded text-sm">
                      <span className="flex-1 mr-2">{app}</span>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => removeApplication(index)}
                        className="shrink-0"
                      >
                        <Trash className="h-4 w-4" />
                      </Button>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        );

      case 2:
        return (
          <div className="space-y-4">
            <div className="space-y-3">
              <div>
                <label className="text-sm font-medium mb-1.5 block">Symbol</label>
                <Input
                  value={newGlyph.symbol}
                  onChange={e => setNewGlyph(prev => ({ ...prev, symbol: e.target.value }))}
                  placeholder="Glyph symbol"
                  className="text-base sm:text-sm"
                />
              </div>
              <div>
                <label className="text-sm font-medium mb-1.5 block">Name</label>
                <Input
                  value={newGlyph.name}
                  onChange={e => setNewGlyph(prev => ({ ...prev, name: e.target.value }))}
                  placeholder="Glyph name"
                  className="text-base sm:text-sm"
                />
              </div>
              <div>
                <label className="text-sm font-medium mb-1.5 block">Description</label>
                <Input
                  value={newGlyph.description}
                  onChange={e => setNewGlyph(prev => ({ ...prev, description: e.target.value }))}
                  placeholder="Glyph description"
                  className="text-base sm:text-sm"
                />
              </div>
              <div>
                <label className="text-sm font-medium mb-1.5 block">Usage</label>
                <Input
                  value={newGlyph.usage}
                  onChange={e => setNewGlyph(prev => ({ ...prev, usage: e.target.value }))}
                  placeholder="Usage example"
                  className="text-base sm:text-sm"
                />
              </div>
              <Button onClick={addGlyph} type="button" className="w-full text-base sm:text-sm">
                Add Glyph
              </Button>
            </div>
            <div className="space-y-2 max-h-[200px] overflow-y-auto">
              {framework.glyphs?.map((glyph, index) => (
                <div key={index} className="flex items-start justify-between bg-accent/20 p-3 rounded">
                  <div className="flex-1 mr-2">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-lg">{glyph.symbol}</span>
                      <span className="font-medium text-sm">{glyph.name}</span>
                    </div>
                    <p className="text-xs text-muted-foreground">{glyph.description}</p>
                    <p className="text-xs font-mono mt-1">{glyph.usage}</p>
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => removeGlyph(index)}
                    className="shrink-0"
                  >
                    <Trash className="h-4 w-4" />
                  </Button>
                </div>
              ))}
            </div>
          </div>
        );

      case 3:
        return (
          <div className="space-y-4">
            <div>
              <label className="text-sm font-medium mb-1.5 block">Examples</label>
              <div className="space-y-3">
                <div className="flex flex-col sm:flex-row gap-2">
                  <Input
                    value={newExample}
                    onChange={e => setNewExample(e.target.value)}
                    placeholder="Add an example"
                    className="text-base sm:text-sm flex-1"
                  />
                  <Button onClick={addExample} type="button" className="text-base sm:text-sm w-full sm:w-auto">
                    Add
                  </Button>
                </div>
                <div className="space-y-2 max-h-[300px] overflow-y-auto">
                  {framework.examples?.map((example, index) => (
                    <div key={index} className="flex items-center justify-between bg-accent/20 p-2 rounded">
                      <span className="font-mono text-sm flex-1 mr-2 break-all">{example}</span>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => removeExample(index)}
                        className="shrink-0"
                      >
                        <Trash className="h-4 w-4" />
                      </Button>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  const canProceed = () => {
    switch (step) {
      case 0:
        return framework.name && framework.description && framework.group;
      case 1:
        return framework.details && framework.applications?.length > 0;
      case 2:
        return framework.glyphs?.length > 0;
      case 3:
        return framework.examples?.length > 0;
      default:
        return false;
    }
  };

  return (
    <>
      <Button
        onClick={() => setOpen(true)}
        className="w-full text-base sm:text-sm"
        variant="outline"
      >
        <Plus className="w-4 h-4 mr-2" />
        Create New Framework
      </Button>

      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto p-4 sm:p-6">
          <DialogHeader className="mb-4">
            <DialogTitle className="text-lg sm:text-xl">{STEPS[step].title}</DialogTitle>
            <p className="text-sm text-muted-foreground mt-1">
              {STEPS[step].description}
            </p>
          </DialogHeader>

          <div className="py-4">
            {renderStep()}
          </div>

          <div className="flex flex-col-reverse sm:flex-row justify-between gap-2 mt-4 pt-4 border-t">
            <Button
              variant="outline"
              onClick={handleBack}
              disabled={step === 0}
              className="w-full sm:w-auto text-base sm:text-sm"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back
            </Button>

            {step === STEPS.length - 1 ? (
              <Button
                onClick={handleSave}
                disabled={!canProceed()}
                className="w-full sm:w-auto text-base sm:text-sm"
              >
                <Save className="w-4 h-4 mr-2" />
                Save Framework
              </Button>
            ) : (
              <Button
                onClick={handleNext}
                disabled={!canProceed()}
                className="w-full sm:w-auto text-base sm:text-sm"
              >
                Next
                <ArrowRight className="w-4 h-4 ml-2" />
              </Button>
            )}
          </div>
        </DialogContent>
      </Dialog>
    </>
  );
};
