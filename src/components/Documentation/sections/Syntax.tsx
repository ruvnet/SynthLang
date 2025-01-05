import { Brackets } from "lucide-react";
import { DocSection } from "../types";

export const Syntax: DocSection = {
  title: "Syntax Guide",
  icon: Brackets,
  content: [
    {
      title: "Basic Structure",
      text: `SynthLang follows a clear, consistent syntax pattern:`,
      example: `# Input operation
↹ text "content" ^modifier

# Process operation
⊕ analyze "data" ^modifier

# Output operation
Σ {
  key: ^modifier,
  result: ^format
}`
    },
    {
      title: "Core Operators",
      text: "Primary operators that form the foundation of SynthLang:",
      items: [
        "↹ (Input): Define input data or context",
        "⊕ (Process): Apply operations or transformations",
        "Σ (Output): Generate formatted output",
        "→ (Flow): Define processing sequence",
        "⇒ (Route): Specify conditional paths"
      ],
      example: `# Basic sequence
↹ text "analyze market trends" ^comprehensive
⊕ analyze "sentiment" ^detailed
⊕ extract "key points" ^brief
Σ {
  sentiment: ^analyzed,
  points: ^formatted
}`
    },
    {
      title: "Modifiers and Annotations",
      text: "Adjustments and specifications for operations:",
      items: [
        "^modifier: Operation modifier",
        "@context: Context annotation",
        "^urgent: Priority indicator",
        "^brief: Output format",
        "^detailed: Analysis depth"
      ],
      example: `# Using modifiers
↹ data "market analysis" ^urgent @finance
⊕ process "trends" ^comprehensive
Σ {
  analysis: ^detailed,
  summary: ^brief
}`
    },
    {
      title: "Flow Control",
      text: "Operators for controlling execution flow:",
      example: `# Sequential processing
↹ text "process this content" ^initial
⊕ analyze → extract → format
Σ {
  result: ^formatted
}

# Conditional routing
↹ data "check conditions" ^validate
⊕ process ⇒ {
  case "valid": → handle,
  case "error": → report
}
Σ {
  status: ^processed
}`
    },
    {
      title: "Advanced Patterns",
      text: "Complex syntax patterns for specialized tasks:",
      example: `# Multi-stage analysis
↹ text "complex analysis required" ^detailed
⊕ analyze "first stage" ^comprehensive
⊕ process "second stage" ^thorough
Σ {
  stage1: ^analyzed,
  stage2: ^processed,
  summary: ^brief
}

# Parallel processing
↹ data "parallel tasks" ^urgent
⊕ [
  analyze "task1" ^quick,
  process "task2" ^detailed
]
Σ {
  results: ^combined
}`
    },
    {
      title: "Error Handling",
      text: "Syntax for handling exceptions and errors:",
      example: `# Basic error handling
↹ text "validate this" ^careful
⊕ validate "content" ^strict
Σ {
  valid: ^checked,
  errors: ^listed
}

# With fallback
↹ primary "try this first" ^important
⊕ process || fallback "use this instead" ^backup
Σ {
  result: ^handled
}`
    },
    {
      title: "Composition Rules",
      text: "Guidelines for combining syntax elements:",
      example: `# Modifier order
↹ text "analyze carefully" ^urgent ^detailed ^thorough

# Context inheritance
↹ data "parent context" @global
⊕ process "child task" @local
Σ {
  result: ^formatted
}

# Priority handling
↹ task "important work" ^critical
⊕ process "urgent steps" ^high
Σ {
  status: ^tracked
}`
    }
  ]
};
