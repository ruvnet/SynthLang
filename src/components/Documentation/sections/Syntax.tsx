import { Brackets } from "lucide-react";
import { DocSection } from "../types";

export const Syntax: DocSection = {
  title: "Syntax Guide",
  icon: Brackets,
  content: [
    {
      title: "Symbol Inventory",
      text: "Complete catalog of SynthLang symbols and their semantic meanings:",
      items: [
        "Core Symbols: ↹, Σ, ⊕, ⊗, ⊥",
        "Flow Control: ⇒, →, ↺, ∀, ∃",
        "Logical Operators: ∧, ∨, ¬, ⊢, ⊨",
        "Set Operations: ∪, ∩, ∖, ∈, ∉",
        "Priority Markers: !, ?, *, #, @"
      ],
      example: `Symbol Categories:
1. Processing: ⊕ (merge), ⊗ (transform)
2. Flow: → (sequence), ↺ (loop)
3. Logic: ∧ (and), ∨ (or), ¬ (not)
4. Sets: ∪ (union), ∩ (intersect)
5. Priority: ! (critical), ? (optional)`
    },
    {
      title: "Priority and Attention",
      text: "System for controlling processing priority and attention mechanisms:",
      example: `Priority Levels:
!critical: Highest priority execution
!high: Elevated priority
!normal: Standard processing
!low: Background processing

Attention Control:
@focus(entity): Direct attention
@context(scope): Set context
@weight(0.8): Attention weight
@mask([1,1,0]): Attention mask

Combined Usage:
↹ data !critical @focus(key_metrics)
⊕ analyze !high @context(market)
⊕ Σ !normal @weight(0.7)`
    },
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
    },
    {
      title: "Composition Rules",
      text: "Guidelines for combining syntax elements effectively:",
      example: `1. Operator Precedence:
! > @ > ⊕ > ↹ > Σ

2. Modifier Stacking:
↹ data ^urgent ^brief ^eng
(Modifiers apply left-to-right)

3. Context Inheritance:
↹ market @context(global) [
  ⊕ analyze(US) // inherits global
  ⊕ analyze(EU) // inherits global
]

4. Priority Propagation:
↹ data !critical [
  ⊕ process   // inherits critical
  ⊕ validate  // inherits critical
]`
    },
    {
      title: "Advanced Syntax Patterns",
      text: "Complex patterns for sophisticated operations:",
      example: `1. Nested Operations:
↹ data @context(finance) [
  ⊕ analyze !high [
    ↹ metrics @focus(risk)
    ⊕ validate ^strict
    ⊕ Σ ^brief
  ]
  ⊕ report ^detailed
]

2. Parallel with Dependencies:
[p1] ↹ market_data
[p2] ↹ news_feed
[p3] ⊕ analyze(p1 ∧ p2)
⊕ Σ ^comprehensive

3. Conditional Flows:
↹ data ⊕ IF risk>threshold => [
  !critical [
    ⊕ alert
    ⊕ mitigate
    ⊕ report ^urgent
  ]
] ELSE [
  !normal [
    ⊕ log
    ⊕ monitor
  ]
]`
    }
  ]
};
