import { Code } from "lucide-react";
import { DocSection } from "../types";

export const Examples: DocSection = {
  title: "Examples",
  icon: Code,
  content: [
    {
      title: "Content Generation",
      text: "Examples of using SynthLang for content creation and refinement",
      example: `# Blog post generation with SEO optimization
↹ topic "AI in Healthcare" @industry_context
⊕ research → outline
⊕ generate_draft ^creative
↺ {
  ⊕ improve_content @seo_guidelines
  ⊕ check_metrics {
    readability: true,
    seo_score: true,
    engagement: true
  }
  ⊥ when all_metrics > 0.8
}
Σ {
  content: markdown ^professional,
  meta: json ^seo,
  stats: formatted ^metrics
}

# Technical documentation generator
↹ code_files @project_context
∀ file → {
  ⊕ analyze_structure
  ⊕ extract_api_specs
  ⊕ generate_docs ⊗ format
}
⊕ aggregate_docs
⊕ validate_completeness
Σ documentation ^comprehensive`
    },
    {
      title: "Data Analysis",
      text: "Examples of data processing and analysis workflows",
      example: `# Market analysis report
↹ market_data ^urgent @industry_trends
⊕ [
  analyze_trends ||
  identify_patterns ||
  calculate_metrics
] → validate_findings
⊕ synthesize_insights @expert_knowledge
Σ report {
  executive_summary: ^brief,
  detailed_analysis: ^comprehensive,
  recommendations: ^actionable,
  metrics: json ^dashboard
}

# Data cleaning and transformation pipeline
↹ raw_data @data_schema
⊕ validate → clean ⊗ normalize
⊕ transform ⇒ {
  case "missing_values": → impute,
  case "outliers": → handle_outliers,
  case "invalid": → correct_or_remove
}
⊕ format ≡ target_schema
Σ processed_data ^quality_metrics`
    },
    {
      title: "Language Processing",
      text: "Examples of natural language processing tasks",
      example: `# Multi-language translation system
↹ text @source_language
⊕ analyze_context
⊕ translate ⇒ {
  target: ["es", "fr", "de"],
  preserve: ["entities", "formatting"],
  style: $tone_preferences
}
⊕ validate_translations
Σ {
  translations: json ^formatted,
  quality_metrics: formatted ^detailed
}

# Advanced text analysis
↹ document @domain_context
⊕ [
  extract_topics ||
  analyze_sentiment ||
  identify_entities ||
  detect_intent
]
⊕ synthesize_analysis
⊕ generate_insights
Σ analysis ^comprehensive`
    },
    {
      title: "AI Model Interaction",
      text: "Examples of complex AI model interactions and chaining",
      example: `# Multi-model processing pipeline
↹ input @task_context
⊕ route_to_model ⇒ {
  case "vision": → process_image,
  case "text": → process_text,
  case "audio": → process_audio
}
⊕ enhance_results @expert_system
⊕ validate_quality
Σ output $preferred_format

# Interactive AI assistant
↹ user_query @conversation_history
⊕ analyze_intent
⊕ process ⇒ {
  case "question": → {
    ⊕ search_knowledge_base
    ⊕ formulate_response ^helpful
  },
  case "task": → {
    ⊕ break_down_steps
    ⊕ execute_sequence
  }
}
⊕ enhance_response @personality
Σ response ^natural`
    },
    {
      title: "Cross-Language Examples",
      text: "Examples of SynthLang syntax across different languages with equivalent functionality",
      example: `# English Prompt (150 tokens)
Write a comprehensive analysis of the current market trends 
in renewable energy, focusing on solar and wind power. 
Include recent technological developments, cost analysis, 
and future projections. Consider both residential and 
commercial applications.

# Chinese Prompt (140 tokens)
撰写一份关于可再生能源市场趋势的综合分析，重点关注太阳能
和风能。包括最近的技术发展、成本分析和未来预测。考虑住宅
和商业应用。

# SynthLang Prompt (45 tokens)
↹ market_analysis @renewable_energy
⊕ focus [solar, wind] ^comprehensive
⊕ analyze {
  tech: ^recent,
  cost: ^detailed,
  forecast: ^future
}
⊕ scope [residential, commercial]
Σ report ^analysis

Benefits:
- Language-agnostic structure
- Consistent token reduction (70%)
- Preserved semantic content
- Improved processing efficiency`
    },
    {
      title: "Workflow Automation",
      text: "Examples of automated workflow processes",
      example: `# Document processing workflow
↹ documents @workflow_rules
∀ doc → {
  ⊕ classify_type
  ⊕ extract_info
  ⊕ validate_data
  ⇒ {
    case "invoice": → process_invoice,
    case "contract": → process_contract,
    case "report": → process_report
  }
}
⊕ aggregate_results
Σ {
  processed: json ^structured,
  summary: markdown ^brief,
  metrics: formatted ^dashboard
}

# Quality assurance pipeline
↹ project_data @quality_standards
↺ {
  ⊕ run_tests || analyze_coverage
  ⊕ identify_issues
  ⊕ generate_fixes
  ⊕ apply_improvements
  ⊕ validate_changes
  ⊥ when quality_score > 0.95
}
Σ report ^comprehensive`
    }
  ]
};
