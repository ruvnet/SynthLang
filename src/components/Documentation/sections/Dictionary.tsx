import { BookOpen } from "lucide-react";
import { DocSection } from "../types";

export const Dictionary: DocSection = {
  title: "Dictionary",
  icon: BookOpen,
  content: [
    {
      title: "Basic Operators",
      text: "Core operators for controlling prompt behavior and flow",
      items: [
        "↹ (Tab) - Data input marker",
        "⊕ (Plus) - Operation marker",
        "Σ (Sigma) - Summary/output marker",
        "→ (Arrow) - Flow control",
        "∀ (Universal) - Apply to all",
        "∃ (Existential) - Apply to any"
      ],
      example: `# Basic sentiment analysis
↹ data "Analyze this text for sentiment"
⊕ analyze sentiment
⊕ extract key emotions
Σ summary ^concise

# Multiple inputs with universal operator
↹ data [
  "First document",
  "Second document",
  "Third document"
]
∀ document → {
  ⊕ analyze
  ⊕ summarize
}
Σ results ^formatted

# Existential operator for pattern matching
↹ documents
∃ doc where contains("keyword") → {
  ⊕ extract context
  ⊕ analyze deeply
}
Σ findings`
    },
    {
      title: "Modifiers",
      text: "Symbols that modify operator behavior",
      items: [
        "^ - Attribute marker (e.g., ^urgent, ^brief)",
        "# - Priority level (e.g., #1, #high)",
        "@ - Context reference",
        "$ - Variable reference",
        "& - Chain operations",
        "! - Force execution"
      ],
      example: `# Priority and urgency modifiers
↹ data ^urgent #1
⊕ analyze @previous_context
⊕ summarize ^brief
Σ output $format_template

# Chained operations with variables
↹ input $user_query
⊕ parse & validate & normalize
⊕ process ^thorough
Σ response $output_format !

# Context-aware processing
↹ query @user_context
⊕ analyze @domain_knowledge
⊕ enhance @historical_data
Σ result ^personalized`
    },
    {
      title: "Control Flow",
      text: "Operators for controlling execution flow",
      items: [
        "→ - Sequential flow",
        "⇒ - Conditional flow",
        "↺ - Loop/repeat",
        "|| - Parallel execution",
        "⊥ - Break/stop",
        "⊤ - Continue"
      ],
      example: `# Complex workflow with conditions
↹ data
⊕ analyze → validate
⊕ process ⇒ {
  case "error": → handle_error,
  case "incomplete": → request_more_info,
  case "valid": → proceed_processing
}
Σ result

# Parallel processing with aggregation
↹ dataset
⊕ [
  analyze_sentiment || 
  extract_topics || 
  identify_entities
]
⊕ aggregate_results
Σ comprehensive_analysis

# Iterative refinement with break condition
↹ draft
↺ {
  ⊕ improve_quality
  ⊕ check_metrics
  ⊥ when quality > 0.95
}
Σ final_version`
    },
    {
      title: "Data Manipulation",
      text: "Operators for handling and transforming data",
      items: [
        "⊗ - Transform data",
        "∩ - Intersection/combine",
        "∪ - Union/merge",
        "∆ - Change/diff",
        "≡ - Match/equals",
        "≠ - Not equals"
      ],
      example: `# Data transformation pipeline
↹ raw_data
⊕ clean ⊗ normalize
⊕ transform ⊗ format
⊕ validate ≡ schema
Σ processed_data

# Combining multiple data sources
↹ source1 ∪ source2
⊕ find_common ∩ relevant
⊕ analyze ∆ baseline
Σ insights

# Pattern matching and validation
↹ input
⊕ validate ≡ {
  format: "json",
  schema: $schema_definition,
  rules: $validation_rules
}
⊕ process ≠ previous_result
Σ output`
    },
    {
      title: "Output Controls",
      text: "Operators for controlling response format and style",
      items: [
        "Σ brief - Concise output",
        "Σ detailed - Comprehensive output",
        "Σ formatted - Structured output",
        "Σ raw - Unprocessed output",
        "Σ json - JSON format",
        "Σ markdown - Markdown format"
      ],
      example: `# Multi-format output
↹ data "Complex technical document"
⊕ analyze
⊕ extract key points
Σ {
  summary: markdown ^brief,
  details: json ^complete,
  metrics: formatted ^table
}

# Conditional formatting
↹ analysis_results
⊕ format ⇒ {
  case "technical": → json ^detailed,
  case "presentation": → markdown ^visual,
  case "report": → formatted ^professional
}
Σ output $preferred_format`
    },
    {
      title: "Advanced Patterns",
      text: "Complex combinations of operators for sophisticated workflows",
      example: `# Multi-stage analysis with error handling
↹ data ^urgent
try → {
  ⊕ analyze → validate #1
  ⊕ extract insights || extract metrics
  ⊕ synthesize ∩ previous_findings
} catch → {
  ⊕ log_error
  ⊕ fallback_analysis
} finally → {
  ⊕ cleanup
  ⊕ notify_completion
}
Σ report ^detailed

# Adaptive processing pipeline
↹ input @context
⊕ analyze ⇒ {
  case "technical": → {
    ⊕ parse_technical
    ⊕ validate_specs
    ⊕ generate_documentation
  },
  case "creative": → {
    ⊕ analyze_style
    ⊕ enhance_creativity
    ⊕ generate_variations
  },
  default: → basic_analysis
}
Σ output $template

# Interactive refinement loop
↹ draft
↺ {
  ⊕ improve @feedback
  ⊕ validate @criteria
  ⊕ update_metrics
  ⇒ {
    case "meets_criteria": → ⊥,
    case "needs_work": → ⊤
  }
}
Σ final ^polished`
    }
  ]
};
