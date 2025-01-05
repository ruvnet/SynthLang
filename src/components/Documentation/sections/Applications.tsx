import { Globe } from "lucide-react";
import { DocSection } from "../types";

export const Applications: DocSection = {
  title: "Applications",
  icon: Globe,
  content: [
    {
      title: "High-Frequency Trading",
      text: `SynthLang excels in high-frequency trading scenarios where milliseconds matter:`,
      items: [
        "Real-time market analysis with minimal latency",
        "Instant trade signal generation and execution",
        "Portfolio rebalancing with complex conditions",
        "Risk assessment and management"
      ],
      example: `Market Signal Generation:
↹ TSLA •price ^realtime
⊕ IF <210 => SELL
⊕ IF >220 => BUY
⊕ Σ ^rationale

Portfolio Rebalancing:
↹ •portfolio
IF Tech|Energy >30% => shift5%->Healthcare
⊕ validate ^risk
⊕ execute ^urgent

Risk Management:
↹ •positions ^realtime
⊕ IF drawdown>2% => hedge
⊕ IF volatility>threshold => reduce_exposure`
    },
    {
      title: "Real-Time Analytics",
      text: `Process and analyze data streams with maximum efficiency:`,
      items: [
        "Live market data processing",
        "Sentiment analysis on news feeds",
        "Trend detection and alerting",
        "Performance monitoring and reporting"
      ],
      example: `Market Sentiment Analysis:
↹ NewsStream ^realtime
⊕ sentiment => [POS|NEG|NEU]
⊕ IF NEG => alert(stakeholders)

Performance Monitoring:
↹ SystemMetrics ^1m
⊕ IF latency>threshold => scale
⊕ Σ "health" ^brief

Trend Detection:
↹ MarketData ^5m
⊕ patterns.identify
⊕ IF significance>0.8 => notify`
    },
    {
      title: "Compliance Checks",
      text: `Automated regulatory compliance and risk monitoring:`,
      items: [
        "AML transaction monitoring",
        "KYC verification processes",
        "Regulatory reporting automation",
        "Risk limit monitoring"
      ],
      example: `Transaction Monitoring:
↹ •account Tx ^realtime
⊕ IF amount>10k => [
  verify_source
  check_patterns
  report_suspicious
]

KYC Verification:
↹ •customer
⊕ verify_identity ^urgent
⊕ check_sanctions
⊕ risk_score => [HIGH|MED|LOW]`
    },
    {
      title: "Cross-Language Processing",
      text: `Efficient multilingual operations with minimal bias:`,
      items: [
        "Real-time translation",
        "Cross-cultural sentiment analysis",
        "Multilingual document processing",
        "Language-agnostic pattern matching"
      ],
      example: `Document Translation:
↹ doc:"report.pdf"
⊕ translate ZH->EN ^preserve_format
⊕ Σ ^key_points

Multilingual Sentiment:
↹ reviews[EN,ES,FR,DE]
⊕ sentiment.analyze
⊕ aggregate ^by_language`
    },
    {
      title: "Financial Research",
      text: `Advanced financial analysis and research automation:`,
      items: [
        "Automated report generation",
        "Financial modeling",
        "Market research synthesis",
        "Competitive analysis"
      ],
      example: `Earnings Analysis:
↹ earnings_call AAPL ^latest
⊕ extract_metrics
⊕ compare_historical
⊕ Σ "insights" ^5bullets

Competitor Analysis:
↹ sector(Tech) •competitors
⊕ metrics[revenue,growth,margins]
⊕ rank ^by_performance
⊕ Σ "market_position"`
    },
    {
      title: "Risk Management",
      text: `Comprehensive risk assessment and mitigation:`,
      items: [
        "Real-time risk monitoring",
        "Exposure analysis",
        "Stress testing",
        "Scenario analysis"
      ],
      example: `Portfolio Risk:
↹ •portfolio ^realtime
⊕ calculate_var
⊕ stress_test scenarios[recession,inflation]
⊕ IF risk>tolerance => adjust_allocation

Market Risk:
↹ market_indicators ^1h
⊕ correlations.analyze
⊕ IF systemic_risk => hedge`
    }
  ]
};
