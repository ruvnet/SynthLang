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
              <label className="text-sm font-medium">Framework Name</label>
              <Input
                value={framework.name}
                onChange={e => setFramework(prev => ({ ...prev, name: e.target.value }))}
                placeholder="Enter framework name"
              />
            </div>
            <div>
              <label className="text-sm font-medium">Framework Group</label>
              <Select
                value={framework.group}
                onValueChange={value => setFramework(prev => ({ ...prev, group: value as typeof FRAMEWORK_GROUPS[number] }))}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select a group" />
                </SelectTrigger>
                <SelectContent>
                  {FRAMEWORK_GROUPS.map(group => (
                    <SelectItem key={group} value={group}>
                      {group.charAt(0).toUpperCase() + group.slice(1)}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div>
              <label className="text-sm font-medium">Short Description</label>
              <Input
                value={framework.description}
                onChange={e => setFramework(prev => ({ ...prev, description: e.target.value }))}
                placeholder="Brief description of the framework"
              />
            </div>
          </div>
        );

      case 1:
        return (
          <div className="space-y-4">
            <div>
              <label className="text-sm font-medium">Detailed Description</label>
              <Textarea
                value={framework.details}
                onChange={e => setFramework(prev => ({ ...prev, details: e.target.value }))}
                placeholder="Detailed explanation of your framework"
                className="min-h-[100px]"
              />
            </div>
            <div>
              <label className="text-sm font-medium">Applications</label>
              <div className="space-y-2">
                <div className="flex gap-2">
                  <Input
                    value={newApplication}
                    onChange={e => setNewApplication(e.target.value)}
                    placeholder="Add an application"
                  />
                  <Button onClick={addApplication} type="button">Add</Button>
                </div>
                <div className="space-y-2">
                  {framework.applications?.map((app, index) => (
                    <div key={index} className="flex items-center justify-between bg-accent/20 p-2 rounded">
                      <span>{app}</span>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => removeApplication(index)}
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
            <div className="space-y-2">
              <div>
                <label className="text-sm font-medium">Symbol</label>
                <Input
                  value={newGlyph.symbol}
                  onChange={e => setNewGlyph(prev => ({ ...prev, symbol: e.target.value }))}
                  placeholder="Glyph symbol"
                />
              </div>
              <div>
                <label className="text-sm font-medium">Name</label>
                <Input
                  value={newGlyph.name}
                  onChange={e => setNewGlyph(prev => ({ ...prev, name: e.target.value }))}
                  placeholder="Glyph name"
                />
              </div>
              <div>
                <label className="text-sm font-medium">Description</label>
                <Input
                  value={newGlyph.description}
                  onChange={e => setNewGlyph(prev => ({ ...prev, description: e.target.value }))}
                  placeholder="Glyph description"
                />
              </div>
              <div>
                <label className="text-sm font-medium">Usage</label>
                <Input
                  value={newGlyph.usage}
                  onChange={e => setNewGlyph(prev => ({ ...prev, usage: e.target.value }))}
                  placeholder="Usage example"
                />
              </div>
              <Button onClick={addGlyph} type="button" className="w-full">
                Add Glyph
              </Button>
            </div>
            <div className="space-y-2">
              {framework.glyphs?.map((glyph, index) => (
                <div key={index} className="flex items-center justify-between bg-accent/20 p-2 rounded">
                  <div>
                    <span className="text-lg mr-2">{glyph.symbol}</span>
                    <span className="font-medium">{glyph.name}</span>
                    <p className="text-sm text-muted-foreground">{glyph.description}</p>
                    <p className="text-sm font-mono">{glyph.usage}</p>
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => removeGlyph(index)}
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
              <label className="text-sm font-medium">Examples</label>
              <div className="space-y-2">
                <div className="flex gap-2">
                  <Input
                    value={newExample}
                    onChange={e => setNewExample(e.target.value)}
                    placeholder="Add an example"
                  />
                  <Button onClick={addExample} type="button">Add</Button>
                </div>
                <div className="space-y-2">
                  {framework.examples?.map((example, index) => (
                    <div key={index} className="flex items-center justify-between bg-accent/20 p-2 rounded">
                      <span className="font-mono">{example}</span>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => removeExample(index)}
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
        className="w-full"
        variant="outline"
      >
        <Plus className="w-4 h-4 mr-2" />
        Create New Framework
      </Button>

      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>{STEPS[step].title}</DialogTitle>
            <p className="text-sm text-muted-foreground">
              {STEPS[step].description}
            </p>
          </DialogHeader>

          <div className="py-4">
            {renderStep()}
          </div>

          <div className="flex justify-between mt-4">
            <Button
              variant="outline"
              onClick={handleBack}
              disabled={step === 0}
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back
            </Button>

            {step === STEPS.length - 1 ? (
              <Button
                onClick={handleSave}
                disabled={!canProceed()}
              >
                <Save className="w-4 h-4 mr-2" />
                Save Framework
              </Button>
            ) : (
              <Button
                onClick={handleNext}
                disabled={!canProceed()}
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
