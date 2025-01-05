import { useState, useEffect, useMemo } from "react";
import { Copy, Check } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { FRAMEWORK_OPTIONS } from "../AdvancedCalculator/constants";
import { getCustomFrameworks } from "../../services/frameworkStorage";
import { FrameworksConfig } from "../AdvancedCalculator/types";

interface SystemPromptDisplayProps {
  frameworks: FrameworksConfig;
}

export const SystemPromptDisplay = ({ frameworks }: SystemPromptDisplayProps) => {
  const [copied, setCopied] = useState(false);
  const [systemPrompt, setSystemPrompt] = useState("");

  const allFrameworkOptions = useMemo(() => [...FRAMEWORK_OPTIONS, ...getCustomFrameworks()], []);

  const generateSystemPrompt = useMemo(() => async () => {
    const frameworkInstructions = Object.entries(frameworks)
      .filter(([_, state]) => state.enabled)
      .map(([id]) => {
        const framework = allFrameworkOptions.find(f => f.id === id)!;
        const selectedGlyphs = framework.glyphs
          .filter(g => frameworks[id].selectedGlyphs.includes(g.symbol))
          .map(g => `${g.symbol} (${g.name}): ${g.description}\nUsage: ${g.usage}`);
        
        return `${framework.name}:\n${framework.description}\nAvailable Glyphs:\n${selectedGlyphs.join('\n')}`;
      })
      .join('\n\n');

    const basePrompt = `You are a SynthLang translator that converts standard prompts into SynthLang's hyper-efficient format. Follow these rules precisely:

[Framework Integration]
1. Mathematical Frameworks:
   - Use provided framework glyphs appropriately in the translation
   - Apply framework-specific notation where relevant
   - Maintain mathematical rigor according to each framework's rules
   - Preserve semantic relationships using framework symbols
   - Combine multiple frameworks coherently when specified

2. Optimization Frameworks:
   - Apply compression and optimization techniques to maximize efficiency
   - Use machine-level patterns for low-level optimization
   - Maintain semantic clarity while achieving maximum density
   - Combine optimization techniques coherently

3. Framework Combinations:
   - Integrate mathematical and optimization frameworks seamlessly
   - Use optimization techniques to enhance mathematical expressions
   - Preserve mathematical precision while maximizing efficiency
   - Apply framework-specific optimizations where appropriate

[Grammar Rules]
1. Task Glyphs:
   - ↹ (Focus/Filter) for main tasks and instructions
   - Σ (Summarize) for condensing information
   - ⊕ (Combine/Merge) for context and data integration
   - ? (Query/Clarify) for validation checks
   - IF for conditional operations

2. Subject Markers:
   - Use • before datasets (e.g., •customerData)
   - Use 花 for abstract concepts
   - Use 山 for hierarchical structures

3. Modifiers:
   - ^format(type) for output format
   - ^n for importance level
   - ^lang for language specification
   - ^t{n} for time constraints

4. Flow Control:
   - [p=n] for priority (1-5)
   - -> for sequential operations
   - + for parallel tasks
   - | for alternatives

[Translation Process]
1. Structure:
   - Start with model selection: ↹ model.{name}
   - Add format specification: ⊕ format(json)
   - Group related operations with []
   - Separate major sections with blank lines

2. Data Sources:
   - Convert datasets to •name format
   - Link related data with :
   - Use ⊕ to merge multiple sources
   - Add ^t{timeframe} for temporal data

3. Tasks:
   - Convert objectives to task glyphs
   - Add priority levels based on impact
   - Chain dependent operations with ->
   - Group parallel tasks with +
   - Use ? for validation steps

4. Optimization:
   - Remove articles (a, an, the)
   - Convert verbose phrases to symbols
   - Use abbreviations (e.g., cfg, eval, impl)
   - Maintain semantic relationships
   - Group similar operations
   - Chain related analyses`;

    const prompt = frameworkInstructions
      ? `${basePrompt}\n\n[Active Frameworks]\n${frameworkInstructions}`
      : basePrompt;

    setSystemPrompt(prompt);
  }, [frameworks, allFrameworkOptions]);

  useEffect(() => {
    generateSystemPrompt();
  }, [generateSystemPrompt]);

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(systemPrompt);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  return (
    <Card className="overflow-hidden">
      <CardHeader className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 p-4 sm:p-6">
        <CardTitle className="text-lg sm:text-xl">System Prompt</CardTitle>
        <button
          onClick={copyToClipboard}
          className="console-button flex items-center gap-2 text-sm w-full sm:w-auto justify-center"
        >
          {copied ? (
            <>
              <Check className="w-4 h-4" />
              Copied!
            </>
          ) : (
            <>
              <Copy className="w-4 h-4" />
              Copy
            </>
          )}
        </button>
      </CardHeader>
      <CardContent className="p-0">
        <div className="relative">
          <pre className="whitespace-pre-wrap text-xs sm:text-sm bg-accent/20 p-4 sm:p-6 rounded-none sm:rounded-lg overflow-auto max-h-[300px] sm:max-h-[500px] font-mono leading-relaxed">
            {systemPrompt}
          </pre>
          <div className="absolute inset-x-0 bottom-0 h-8 bg-gradient-to-t from-background to-transparent pointer-events-none" />
        </div>
      </CardContent>
    </Card>
  );
};
