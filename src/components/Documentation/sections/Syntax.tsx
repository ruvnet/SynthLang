import { Brackets } from "lucide-react";
import { DocSection } from "../types";

export const Syntax: DocSection = {
  title: "Syntax Guide",
  icon: Brackets,
  content: [
    {
      title: "Basic Structure",
      text: `SynthLang syntax follows a precise, hierarchical structure designed for maximum efficiency:`,
      example: `<operation> <subject> <modifiers>
↹ TSLA •price ^urgent
⊕ IF <210 => SELL
⊕ IF >220 => BUY
⊕ Σ ^rationale`
    },
    {
      title: "Core Operators",
      text: "Primary operators that form the foundation of SynthLang instructions:",
      items: [
        "↹ (Focus): Direct attention to specific data or context",
        "Σ (Summarize): Generate concise summaries or analyses",
        "⊕ (Combine): Merge multiple operations or results",
        "IF: Conditional logic and decision making",
        "=> (Implication): Define results or consequent actions"
      ]
    },
    {
      title: "Subject Markers",
      text: "Identifiers for data sources and objects:",
      items: [
        "•data: Generic data reference",
        "•price: Price-related data",
        "•report: Report or document",
        "•portfolio: Portfolio data",
        "•account: Account information"
      ],
      example: `Examples:
↹ •portfolio ^urgent
↹ •price AAPL ^1h
↹ •report Q4 ^brief`
    },
    {
      title: "Modifiers",
      text: "Adjustments and specifications for operations:",
      items: [
        "^4: Emphasis level (1-5)",
        "^eng: English language output",
        "^urgent: High priority processing",
        "^brief: Shortened output",
        "^1h: Time window (h=hours, d=days, w=weeks)",
        "^rationale: Include explanation"
      ],
      example: `Usage Examples:
Σ •report ^brief ^eng
↹ BTC •volatility ^1h ^urgent
⊕ analysis ^4 ^rationale`
    },
    {
      title: "Flow Control",
      text: "Operators for controlling execution flow:",
      example: `Conditional Execution:
IF price>100 => ALERT
IF vol>1M => ⊕ analysis

Sequential Operations:
↹ data
⊕ process
⊕ Σ ^brief

Parallel Processing:
[p1] ↹ AAPL
[p2] ↹ GOOGL
⊕ compare`
    },
    {
      title: "Advanced Patterns",
      text: "Complex syntax patterns for specialized tasks:",
      example: `Market Analysis:
↹ sector(Tech) •companies
⊕ IF marketCap>1B => analyze
⊕ Σ "top5" ^brief

Risk Assessment:
↹ •portfolio
⊕ risk>HIGH => [
  ↹ holdings
  ⊕ rebalance ^urgent
  ⊕ notify ^rationale
]`
    },
    {
      title: "Domain-Specific Extensions",
      text: "Specialized syntax for different domains:",
      items: [
        "Financial: price, vol, marketCap operators",
        "Analytics: groupBy, aggregate functions",
        "Compliance: verify, validate operators",
        "ML/AI: train, predict, evaluate operators"
      ],
      example: `Financial Analysis:
↹ TSLA
⊕ MA(50) cross MA(200) => ALERT

ML Operations:
↹ model.BERT
⊕ train(epochs=10) ^urgent
⊕ evaluate ^metrics`
    },
    {
      title: "Error Handling",
      text: "Syntax for handling exceptions and errors:",
      example: `Basic Error Handling:
↹ data ?exists => [
  success: process,
  error: notify ^urgent
]

Fallback Patterns:
↹ primary || fallback || default
⊕ process !timeout(5s) => retry`
    }
  ]
};
