# SynthLang CLI Usage Guide

## Installation

Install from PyPI:
```bash
pip install synthlang
```

Or install from source:
```bash
git clone https://github.com/ruvnet/SynthLang.git
cd SynthLang/cli
pip install -e .
```

## Configuration

1. Set up environment:
```bash
# Create .env file
cp .env.sample .env

# Add OpenAI API key
echo "OPENAI_API_KEY=your-key-here" >> .env
```

2. Initialize configuration:
```bash
synthlang init --config config.json
```

## Basic Usage

### Translation

Translate natural language to SynthLang format:

```bash
synthlang translate \
  --config config.json \
  --source "analyze customer feedback data and generate insights" \
  --target-framework synthlang
```

Output:
```
Translation complete

Source prompt:
analyze customer feedback data and generate insights

Translated prompt:
↹ feedback•data
⊕ sentiment>0 => pos
⊕ sentiment<0 => neg
Σ insights + trends
```

### System Prompts

Generate system prompts:

```bash
synthlang generate \
  --config config.json \
  --task "Create a chatbot that helps users learn Python"
```

## SynthLang Format

### Core Symbols

1. Input/Output Symbols:
   - ↹ (input): Marks input data or sources
   - ⊕ (process): Indicates processing or transformation steps
   - Σ (output): Represents final output or results

2. Operators:
   - • (join): Connects related items
   - => (transform): Shows data transformation
   - +, >, <, ^ (math): Mathematical operations

### Format Rules

1. Line Structure:
   - Maximum 30 characters per line
   - Each line starts with a symbol (↹, ⊕, Σ)
   - No quotes or descriptions

2. Data Flow:
   - Start with input (↹)
   - Process with one or more steps (⊕)
   - End with output (Σ)

### Examples

1. Basic Analysis:
```
↹ data•source
⊕ process => transform
Σ result + output
```

2. Sentiment Analysis:
```
↹ feedback•sources
⊕ sentiment>0 => pos
⊕ sentiment<0 => neg
Σ insights + trends
```

3. Data Pipeline:
```
↹ stream•data
⊕ filter>threshold
⊕ transform => clean
Σ output^2 + cache
```

## Advanced Features

### Framework Translation

1. Basic Translation:
```bash
synthlang translate \
  --source "process data" \
  --target-framework synthlang
```

2. With Format Specification:
```bash
synthlang translate \
  --source "analyze logs" \
  --target-framework synthlang \
  --format "json"
```

3. With Multiple Steps:
```bash
synthlang translate \
  --source "fetch data, analyze trends, generate report" \
  --target-framework synthlang \
  --steps 3
```

### System Prompts

1. Basic Generation:
```bash
synthlang generate \
  --task "Create documentation"
```

2. With Templates:
```bash
synthlang generate \
  --task "API documentation" \
  --template technical
```

3. With Constraints:
```bash
synthlang generate \
  --task "Error handling" \
  --max-tokens 500
```

### Optimization

1. Token Optimization:
```bash
synthlang optimize \
  --prompt "Long prompt here" \
  --target-tokens 100
```

2. Format Optimization:
```bash
synthlang optimize \
  --prompt "Unformatted prompt" \
  --format strict
```

## DSPy Integration

### Custom Modules

Create custom DSPy modules:

```python
from synthlang.core.modules import SynthLangModule

class CustomTranslator(SynthLangModule):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.predictor = dspy.Predict(CustomSignature)
    
    def translate(self, text: str) -> str:
        return self.predictor(source=text).target
```

### Chain Composition

Build translation chains:

```python
from synthlang.core.modules import ChainComposer

chain = ChainComposer([
    FrameworkTranslator(),
    PromptOptimizer(),
    FormatValidator()
])

result = chain.process("Your prompt here")
```

### Evaluation

Run evaluations:

```bash
synthlang evaluate \
  --test-file tests.json \
  --metrics accuracy,format \
  --output report.json
```

## Environment Variables

Required:
- `OPENAI_API_KEY`: OpenAI API key

Optional:
- `SYNTHLANG_MODEL`: Default model (default: gpt-4o-mini)
- `SYNTHLANG_ENV`: Environment (default: production)
- `SYNTHLANG_LOG_LEVEL`: Logging level (default: INFO)

## Error Handling

Common errors and solutions:

1. API Key Error:
```
Error: OPENAI_API_KEY not found
Solution: Set OPENAI_API_KEY in .env or environment
```

2. Format Error:
```
Error: Invalid SynthLang format
Solution: Ensure output follows format rules
```

3. Token Limit:
```
Error: Token limit exceeded
Solution: Use optimize command to reduce tokens
```

## Best Practices

1. Format Guidelines:
   - Keep lines under 30 characters
   - Use appropriate symbols
   - Follow input → process → output flow

2. Optimization:
   - Use token optimization for long prompts
   - Validate format compliance
   - Test with example inputs

3. Integration:
   - Use environment variables
   - Handle errors gracefully
   - Follow DSPy patterns

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for:
- Development setup
- Testing guidelines
- Pull request process

## Support

- GitHub Issues: [SynthLang Issues](https://github.com/ruvnet/SynthLang/issues)
- Documentation: [SynthLang Docs](https://synthlang.ai/docs)
