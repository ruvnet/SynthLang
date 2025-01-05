import { Introduction } from "./Introduction";
import { Syntax } from "./Syntax";
import { Examples } from "./Examples";
import { Applications } from "./Applications";
import { Research } from "./Research";
import { Implementation } from "./Implementation";
import { Security } from "./Security";
import { CostAnalysis } from "./CostAnalysis";
import { Dictionary } from "./Dictionary";
import { InteractiveExamples } from "./InteractiveExamples";
import { SystemPrompt } from "./SystemPrompt";

// Order sections logically for the documentation flow
export const SECTIONS = {
  introduction: Introduction,    // Start with introduction
  syntax: Syntax,               // Basic syntax understanding
  examples: Examples,           // Simple examples
  system_prompt: SystemPrompt,  // System prompt for implementation
  implementation: Implementation, // How to implement
  applications: Applications,    // Real-world applications
  security: Security,           // Security considerations
  cost_analysis: CostAnalysis,  // Performance and cost
  research: Research,           // Technical research
  dictionary: Dictionary,       // Reference
  interactive: InteractiveExamples // Try it live
} as const;
