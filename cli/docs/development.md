# SynthLang CLI Development Guide

## Overview

The SynthLang CLI is built using DSPy, a framework for programming with language models. This guide covers the implementation details, DSPy integration, and planned features.

## Architecture

The CLI follows a modular architecture:

```
cli/
├── synthlang/
│   ├── core/
│   │   ├── modules.py      # DSPy module implementations
│   │   └── signatures.py   # DSPy signatures
│   ├── cli.py             # CLI interface
│   ├── config.py          # Configuration management
│   └── utils/             # Utility functions
└── tests/                 # Test suite
```

## DSPy Integration

### Adapters

DSPy adapters provide interfaces to different language models. SynthLang uses:

```python
from dspy import OpenAI

# Initialize with model and API key
lm = OpenAI(
    model="gpt-4o-mini",  # Required model
    api_key=api_key
)
```

Planned adapters:
- Anthropic Claude
- Local models via LlamaCpp
- Azure OpenAI

### Evaluation

DSPy's evaluation framework will be used for:

```python
from dspy import Evaluate, Example

# Define evaluation metrics
evaluator = Evaluate(
    metrics=['accuracy', 'format_compliance'],
    num_threads=4
)

# Create test examples
examples = [
    Example(
        source="analyze customer feedback",
        target="↹ feedback•data\n⊕ sentiment>0 => pos\nΣ insights"
    )
]

# Run evaluation
results = evaluator(examples)
```

### Models

Model configuration and management:

```python
class ModelConfig:
    """Model configuration and settings."""
    def __init__(self, name: str, context_window: int):
        self.name = name
        self.context_window = context_window
        self.temperature = 0.1  # Low temperature for consistent output
```

### Modules

Core DSPy modules implemented:

1. FrameworkTranslator
```python
class FrameworkTranslator(dspy.Module):
    """Translates natural language to SynthLang format."""
    def forward(self, source: str) -> Dict[str, str]:
        return {
            "source": source,
            "target": translated,
            "explanation": rationale
        }
```

2. SystemPromptGenerator
```python
class SystemPromptGenerator(dspy.Module):
    """Generates system prompts from task descriptions."""
    def forward(self, task: str) -> Dict[str, Any]:
        return {
            "prompt": generated,
            "rationale": explanation,
            "metadata": meta
        }
```

Planned modules:
- PromptOptimizer
- ChainComposer
- MetricsAnalyzer

### Optimizers

DSPy optimizers for improving output:

```python
from dspy import ChainOfThought, ReAct

# Add reasoning capabilities
reasoner = ChainOfThought(
    max_steps=3,
    temperature=0.1
)

# Add interactive refinement
reactor = ReAct(
    max_attempts=2,
    reflection=True
)
```

### Primitives

Core DSPy primitives used:

```python
from dspy import Predict, Generate, TypedPredictor

# Basic prediction
predictor = Predict(signature)

# Structured generation
generator = Generate(
    output_schema={
        "type": "object",
        "properties": {
            "translation": {"type": "string"},
            "confidence": {"type": "number"}
        }
    }
)

# Type-safe prediction
typed_predictor = TypedPredictor[TranslationOutput](signature)
```

### Signatures

DSPy signatures define module interfaces:

```python
class TranslateSignature(dspy.Signature):
    """Translation signature."""
    source = dspy.InputField(desc="Source text")
    target = dspy.OutputField(desc="Translated text")
    explanation = dspy.OutputField(desc="Translation rationale")
```

### Tools

Planned DSPy tool integrations:

```python
from dspy import Tool

# File operations
class FileProcessor(Tool):
    def process(self, content: str) -> str:
        """Process file content."""
        pass

# Web retrieval
class WebRetriever(Tool):
    def fetch(self, url: str) -> str:
        """Fetch web content."""
        pass
```

### Utils

Utility functions and helpers:

```python
from dspy.utils import format_prompt, validate_output

def ensure_format(text: str) -> str:
    """Ensure output follows SynthLang format."""
    return validate_output(
        text,
        schema=SYNTHLANG_SCHEMA
    )
```

## Planned Features

1. Advanced Translation
   - Multi-stage translation pipeline
   - Format validation and correction
   - Confidence scoring

2. Optimization
   - Token usage optimization
   - Semantic preservation checks
   - Performance benchmarking

3. Chain Composition
   - Custom translation chains
   - Framework combinations
   - Pipeline optimization

4. Interactive Mode
   - REPL interface
   - Real-time suggestions
   - Format validation

5. Integration Features
   - Git hooks
   - CI/CD pipeline integration
   - API endpoints

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for development setup and guidelines.

## Testing

Run tests with pytest:
```bash
pytest cli/tests/
```

Coverage report:
```bash
pytest --cov=synthlang cli/tests/
