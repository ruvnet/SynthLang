import { Lightbulb } from "lucide-react";
import { DocSection } from "../types";
import { CodeExample, CodeExampleGrid } from "../CodeExample";

const simpleTraditional = {
  title: "Traditional Prompt",
  description: "Standard natural language prompt format",
  code: `Summarize this text in 3 bullet points and analyze its sentiment:
The new AI model demonstrated remarkable capabilities in creative tasks,
showing human-like understanding in art and music composition. However,
researchers noted some limitations in handling complex logical reasoning.`,
  language: "text"
};

const simpleSynthLang = {
  title: "SynthLang Equivalent",
  description: "More efficient and structured format",
  code: `↹ text "The new AI model demonstrated remarkable capabilities in creative tasks,
showing human-like understanding in art and music composition. However,
researchers noted some limitations in handling complex logical reasoning."
⊕ summarize ^bullet_points ^limit_3
⊕ analyze_sentiment ^brief
Σ {
  summary: ^formatted,
  sentiment: ^concise
}`
};

const complexTraditional = {
  title: "Traditional Prompt",
  description: "Complex multi-step instruction",
  code: `First, analyze the following research paper for key findings. Then,
translate the findings to Japanese, maintaining academic terminology.
Finally, create a comparison table showing similarities with previous
research in the field. Make sure to highlight any novel contributions.`,
  language: "text"
};

const complexSynthLang = {
  title: "SynthLang Equivalent",
  description: "Structured multi-step process",
  code: `↹ paper @research_context
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
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Simple Example: Text Summary</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <CodeExample {...simpleTraditional} />
              <CodeExample {...simpleSynthLang} />
            </div>
          </div>
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Advanced Example: Multi-step Analysis</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <CodeExample {...complexTraditional} />
              <CodeExample {...complexSynthLang} />
            </div>
          </div>
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
