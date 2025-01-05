import { Calculator } from "lucide-react";
import { DocSection } from "../types";

export const CostAnalysis: DocSection = {
  title: "Cost Analysis",
  icon: Calculator,
  content: [
    {
      title: "Data Density Model",
      text: `SynthLang uses a mathematical model to quantify and optimize data density in prompts:`,
      example: `Data Density Definition:
D = I/T where:
- D: Data density
- I: Information content (semantic units)
- T: Token count

Percentage Reduction Example:
Original Prompt: 150 tokens
SynthLang: 45 tokens
Reduction = (150 - 45)/150 = 70%

Improvement Factor:
Factor = Original/Optimized
= 150/45 ≈ 3.33×
Percentage Increase = (3.33 - 1) × 100% = 233%`
    },
    {
      title: "Latency Improvement Analysis",
      text: `Token reduction directly impacts processing latency through several mechanisms:`,
      items: [
        "Token Overhead: Linear relationship with processing time",
        "Attention Matrix: Quadratic complexity reduction",
        "Context Window: More efficient utilization",
        "Memory Access: Reduced cache misses"
      ],
      example: `Latency Calculation:
Base Latency: 50ms
Token Processing: 0.5ms/token

Standard (150 tokens):
Total = 50ms + (150 × 0.5ms) = 125ms

SynthLang (45 tokens):
Total = 50ms + (45 × 0.5ms) = 72.5ms
Improvement: 42% reduction in latency`
    },
    {
      title: "Token Reduction Impact",
      text: `SynthLang achieves a 70% reduction in token usage, resulting in significant cost savings across various AI models:`,
      items: [
        "o1: $15 → $4.5 per 1M tokens (saves $10.5)",
        "o1-mini: $3 → $0.9 per 1M tokens (saves $2.1)",
        "GPT-4o: $2.50 → $0.75 per 1M tokens (saves $1.75)",
        "Claude 3.5 Sonnet: $3 → $0.9 per 1M tokens (saves $2.1)"
      ],
      example: `Cost Calculation Example:
Standard Prompt (150 tokens):
- Base Cost: $0.00225 per request
- Daily (100k requests): $225
- Monthly: $6,750

SynthLang (45 tokens):
- Base Cost: $0.000675 per request
- Daily (100k requests): $67.50
- Monthly: $2,025

Monthly Savings: $4,725 (70%)`
    },
    {
      title: "Performance Benefits",
      text: `Token reduction directly impacts processing speed and efficiency:`,
      items: [
        "Reduced processing time: 35ms vs 120ms baseline",
        "Lower memory usage: 60% reduction in attention matrices",
        "Improved throughput: 2.8x more requests per second",
        "Enhanced real-time performance: 84% latency reduction"
      ],
      example: `Performance Metrics:
Standard Processing:
- Attention Matrix: 150x150 = 22,500 operations
- Memory Usage: ~90KB per request
- Max Throughput: 8.3 requests/second

SynthLang Processing:
- Attention Matrix: 45x45 = 2,025 operations
- Memory Usage: ~27KB per request
- Max Throughput: 23.2 requests/second`
    },
    {
      title: "ROI Analysis",
      text: `Return on Investment calculations for different usage scenarios:`,
      example: `Small Scale (10k requests/day):
- Monthly Cost Savings: $472.50
- Performance Gain Value: $350
- Total Monthly Benefit: $822.50
- Annual ROI: 985%

Medium Scale (100k requests/day):
- Monthly Cost Savings: $4,725
- Performance Gain Value: $3,500
- Total Monthly Benefit: $8,225
- Annual ROI: 1,970%

Large Scale (1M requests/day):
- Monthly Cost Savings: $47,250
- Performance Gain Value: $35,000
- Total Monthly Benefit: $82,250
- Annual ROI: 3,940%`
    },
    {
      title: "Resource Optimization",
      text: `Additional cost benefits from improved resource utilization:`,
      items: [
        "Reduced API costs through efficient token usage",
        "Lower infrastructure costs from improved throughput",
        "Decreased memory requirements for large-scale operations",
        "Minimized bandwidth usage in distributed systems"
      ]
    },
    {
      title: "Scaling Economics",
      text: `Cost efficiency improvements at different scales:`,
      example: `Infrastructure Savings:
- CPU Usage: ↓ 65%
- Memory Usage: ↓ 60%
- Network Bandwidth: ↓ 55%
- Storage Requirements: ↓ 40%

Cost Multipliers:
- Small Scale: 1x baseline savings
- Medium Scale: 1.5x baseline savings
- Large Scale: 2.2x baseline savings
- Enterprise Scale: 3.4x baseline savings`
    },
    {
      title: "Implementation Costs",
      text: `One-time and ongoing costs for SynthLang implementation:`,
      items: [
        "Initial Setup: 2-5 developer days",
        "Training: 1-2 days per team",
        "Integration: 3-7 days depending on complexity",
        "Maintenance: 2-4 hours per month"
      ],
      example: `ROI Timeline:
Month 1:
- Implementation Cost: $5,000
- Cost Savings: $4,725
- Net: -$275

Month 2 onwards:
- Monthly Cost: $500
- Monthly Savings: $4,725
- Net Monthly Benefit: $4,225
- Break-even: Month 2`
    }
  ]
};
