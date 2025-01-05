import { Lightbulb } from "lucide-react";
import { DocSection } from "../types";
import { CodeExample, CodeExampleGrid } from "../CodeExample";

const simpleExample = {
  title: "Simple Example: Text Summary",
  description: "Compare a traditional prompt with SynthLang syntax",
  code: `# Traditional prompt:
"Summarize this text in 3 bullet points and analyze its sentiment:
The new AI model demonstrated remarkable capabilities in creative tasks,
showing human-like understanding in art and music composition. However,
researchers noted some limitations in handling complex logical reasoning."

# SynthLang equivalent:
↹ text "The new AI model demonstrated remarkable capabilities in creative tasks,
showing human-like understanding in art and music composition. However,
researchers noted some limitations in handling complex logical reasoning."
⊕ summarize ^bullet_points ^limit_3
⊕ analyze_sentiment ^brief
Σ {
  summary: ^formatted,
  sentiment: ^concise
}`
};

const complexExample = {
  title: "Advanced Example: Multi-step Analysis",
  description: "See how SynthLang simplifies complex operations",
  code: `# Traditional prompt:
"First, analyze the following research paper for key findings. Then,
translate the findings to Japanese, maintaining academic terminology.
Finally, create a comparison table showing similarities with previous
research in the field. Make sure to highlight any novel contributions."

# SynthLang equivalent:
↹ paper @research_context
⊕ extract_key_findings ^comprehensive
⊕ translate → 日本語 ^academic
⊕ compare_research ^previous_studies
Σ {
  findings: ^structured,
  translation: ^preserve_terms,
  comparison: ^table_format,
  novel_aspects: ^highlighted
}`
};

export const Introduction: DocSection = {
  title: "Introduction",
  icon: Lightbulb,
  content: [
    {
      title: "What is SynthLang?",
      text: `SynthLang is a hyper-efficient prompt language designed for LLMs, using compact glyphs and logographic scripts to reduce token usage and improve prompt clarity. It provides a structured way to compose complex prompts while maintaining readability and reducing potential biases.`,
      example: ""
    },
    {
      title: "Getting Started",
      text: "Try these simple examples to get familiar with SynthLang syntax and basic operations. Compare traditional prompts with their SynthLang equivalents to see how the syntax improves clarity and efficiency.",
      example: "",
      component: () => (
        <div className="space-y-8">
          <CodeExample {...simpleExample} />
          <CodeExample {...complexExample} />
        </div>
      )
    },
    {
      title: "Key Benefits",
      text: `
• Token Efficiency: Compact syntax reduces token usage by up to 40%
• Improved Clarity: Structured format makes prompts easier to read and maintain
• Reduced Bias: Standardized syntax helps minimize unintended biases
• Better Control: Fine-grained control over output format and style
• Composability: Easy to combine and chain operations
`,
      example: ""
    },
    {
      title: "Core Concepts",
      text: `SynthLang is built around a few core concepts:

1. Operations (↹, ⊕, Σ): Define input, processing, and output
2. Modifiers (^, @, #): Control behavior and output format
3. Flow Control (→, ||, ⊗): Direct operation flow and combinations
4. Context Management: Handle scope and data flow efficiently`,
      example: ""
    }
  ]
};
