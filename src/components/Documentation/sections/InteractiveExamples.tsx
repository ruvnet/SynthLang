import { PlayCircle } from "lucide-react";
import { DocSection } from "../types";
import { CodeExample, CodeExampleGrid, CodeExampleList } from "../CodeExample";

const basicExamples = [
  {
    title: "Text Analysis",
    description: "Analyze text sentiment and extract key points",
    code: `# Basic text analysis example
↹ text "Analyze this text for sentiment and key points"
⊕ analyze_sentiment ^thorough
⊕ extract_key_points ^comprehensive
Σ {
  sentiment: ^brief,
  points: ^bullet_points,
  confidence: ^percentage
}`
  },
  {
    title: "Content Generation",
    description: "Generate structured content with specific requirements",
    code: `# Content generation with research
↹ topic "AI in Healthcare" @medical_context
⊕ research → validate_sources
⊕ generate_outline ^structured
⊕ expand_content ^creative
Σ markdown ^professional`
  }
];

const advancedExamples = [
  {
    title: "Multi-stage Analysis",
    description: "Complex analysis pipeline with parallel processing",
    code: `# Advanced data analysis pipeline
↹ data @analysis_context
⊕ preprocess → validate_schema
⊕ analyze_patterns || extract_metrics || identify_trends
⊕ aggregate_results
⊕ synthesize @expert_system
Σ {
  insights: ^comprehensive,
  visualization: ^interactive_charts,
  recommendations: ^actionable
}`
  },
  {
    title: "Interactive Refinement",
    description: "Iterative content improvement with quality checks",
    code: `# Content refinement loop
↹ draft @content_guidelines
⊕ analyze_quality @criteria
⊕ identify_improvements
⊕ apply_enhancements
⊕ validate_changes
Σ {
  content: ^polished,
  quality_score: ^percentage,
  improvement_log: ^detailed
}`
  }
];

const workflowExamples = [
  {
    title: "Document Processing",
    description: "Automated document workflow with conditional processing",
    code: `# Document processing workflow
↹ documents @workflow_rules
⊕ detect_type
⊕ extract_metadata
⊕ validate_format
⊕ process_content @domain_specific
⊕ aggregate_results
Σ {
  processed: json ^structured,
  summary: markdown ^brief,
  metrics: dashboard ^interactive
}`
  },
  {
    title: "Data Transformation",
    description: "Complex data transformation with validation",
    code: `# Data transformation pipeline
↹ raw_data @source_schema
⊕ validate_input
⊕ clean_data
⊕ transform @rules
⊕ validate_output
Σ {
  data: ^transformed,
  validation: ^detailed,
  metrics: ^quality_scores
}`
  }
];

const commentOnlyExample = {
  title: "Comments and Documentation",
  description: "Example of using comments to document SynthLang code",
  code: `# SynthLang supports detailed comments for documentation
# Comments start with '#' and can appear anywhere in the code
# They are useful for:
# - Explaining complex operations
# - Documenting workflow steps
# - Adding context and notes

# Example of a documented workflow:
↹ input @context
⊕ process_data  # First step: process the raw data
⊕ analyze       # Second step: analyze processed data
⊕ validate      # Third step: validate results
Σ output ^formatted`
};

export const InteractiveExamples: DocSection = {
  title: "Try It Live",
  icon: PlayCircle,
  content: [
    {
      title: "Getting Started",
      text: "Try these simple examples to get familiar with SynthLang syntax and basic operations",
      example: "",
      component: () => <CodeExampleGrid examples={basicExamples} />
    },
    {
      title: "Advanced Patterns",
      text: "Explore more complex examples demonstrating advanced features and control flow",
      example: "",
      component: () => <CodeExampleGrid examples={advancedExamples} />
    },
    {
      title: "Real-world Workflows",
      text: "Complete examples of real-world automation and processing workflows",
      example: "",
      component: () => <CodeExampleList examples={workflowExamples} />
    },
    {
      title: "Documentation",
      text: "Learn how to document your SynthLang code effectively",
      example: "",
      component: () => <CodeExample {...commentOnlyExample} />
    }
  ]
};
