# SynthLang CLI

A powerful command-line interface for the SynthLang framework, providing advanced prompt engineering, framework translation, and optimization capabilities using DSPy.

## What is SynthLang?
Reduce AI costs by up to 95% with SynthLang's efficient prompt optimization. Experience up to 1100% faster processing while maintaining effectiveness.

Transform your AI interactions with mathematically-structured prompts. Symbolic Scribe brings academic rigor to prompt engineering, helping you create more precise, reliable, and powerful AI interactions.
SynthLang is a revolutionary framework for prompt engineering and language model optimization. It introduces a structured, mathematical approach to prompt design that makes prompts more consistent, measurable, and effective. The framework uses a unique symbolic notation system that bridges natural language and computational thinking.

### Core Concepts

- **Symbolic Notation**: A sophisticated system that uses mathematical symbols to represent different aspects of prompt engineering:
  - ↹ (Input): Represents data ingestion and parameter definition
  - ⊕ (Process): Denotes transformations and computational operations
  - Σ (Output): Specifies result formats and expectations
  - These symbols create a standardized way to express prompt logic

- **Compositional Design**: A modular approach to prompt engineering that:
  - Breaks down complex prompts into smaller, manageable components
  - Enables reuse of common prompt patterns
  - Facilitates testing and optimization of individual components
  - Allows for easy composition of complex workflows

- **Measurable Quality**: A comprehensive metrics system that:
  - Evaluates prompt effectiveness using quantitative measures
  - Tracks performance across multiple dimensions
  - Provides actionable feedback for improvement
  - Enables data-driven optimization

- **Evolutionary Optimization**: An advanced genetic algorithm system that:
  - Automatically improves prompts through successive generations
  - Uses mutation and crossover operations
  - Selects the best-performing variants
  - Adapts to specific use cases and requirements

- **Framework Translation**: A sophisticated translation system that:
  - Converts between different prompt engineering approaches
  - Maintains semantic equivalence
  - Optimizes for target framework characteristics
  - Preserves intent and functionality

### How It Works

SynthLang transforms natural language prompts into a structured format through a multi-step process:

1. **Input (↹)**: 
   - Defines data sources and their characteristics
   - Specifies input parameters and their types
   - Establishes validation rules
   - Sets up preprocessing requirements

2. **Process (⊕)**:
   - Details transformation steps
   - Defines computational operations
   - Specifies conditional logic
   - Establishes processing pipelines

3. **Output (Σ)**:
   - Describes expected result formats
   - Specifies success criteria
   - Defines error handling
   - Sets quality thresholds

4. **Operators**:
   - Mathematical symbols for relationship definition:
     - (+) Addition/Combination
     - (>) Greater than/Progression
     - (<) Less than/Regression
     - (^) Power/Amplification

5. **Joins (•)**:
   - Connect related concepts
   - Establish hierarchical relationships
   - Define concept groupings
   - Create logical bridges

## Metrics & Performance

SynthLang evaluates prompts across multiple dimensions with sophisticated scoring systems:

### Clarity Score (0-1)
Measures the structural quality of prompts:
- **Symbol Usage Correctness**: Evaluates proper application of symbolic notation
- **Structure Adherence**: Assesses compliance with SynthLang patterns
- **Concept Separation**: Measures clear delineation between components
- **Line Length Optimization**: Analyzes prompt formatting efficiency

### Specificity Score (0-1)
Evaluates the precision of prompt instructions:
- **Operator Precision**: Measures accuracy of mathematical operators
- **Join Relationships**: Assesses the quality of concept connections
- **Transformation Clarity**: Evaluates process step definitions
- **Parameter Definition**: Analyzes input/output specifications

### Consistency Score (0-1)
Measures prompt reliability and standardization:
- **Symbol Alignment**: Evaluates symbolic notation consistency
- **Format Compliance**: Assesses adherence to style guidelines
- **Terminology Usage**: Measures vocabulary standardization
- **Pattern Adherence**: Analyzes structural consistency

### Task Completion Score (0-1)
Evaluates practical effectiveness:
- **Test Case Success**: Measures performance on standard tests
- **Output Matching**: Evaluates result accuracy
- **Error Handling**: Assesses robustness
- **Edge Case Coverage**: Analyzes comprehensive handling

## Features

- 🔄 **Framework Translation**: 
  - Converts natural language to SynthLang format
  - Preserves semantic meaning
  - Optimizes structure
  - Maintains context
  - Supports multiple frameworks
  - Provides bidirectional translation

- ⚡ **Prompt Optimization**: 
  - Enhances prompts using DSPy techniques
  - Improves efficiency
  - Reduces token usage
  - Maintains accuracy
  - Implements best practices
  - Provides optimization suggestions

- 🧬 **Evolutionary Algorithms**: 
  - Evolves prompts through genetic algorithms
  - Implements mutation strategies
  - Uses crossover techniques
  - Selects optimal variants
  - Adapts to requirements
  - Tracks evolutionary history

- 📊 **Performance Metrics**: 
  - Tracks clarity scores
  - Measures specificity
  - Evaluates consistency
  - Analyzes effectiveness
  - Provides detailed reports
  - Suggests improvements

- 🎯 **Task-Based Testing**: 
  - Evaluates against test cases
  - Measures success rates
  - Tracks performance
  - Identifies weaknesses
  - Suggests improvements
  - Maintains test history

- 🔍 **Smart Classification**: 
  - Categorizes prompts
  - Analyzes patterns
  - Identifies similarities
  - Groups related prompts
  - Suggests optimizations
  - Maintains taxonomies

- 🛠️ **Extensible Architecture**: 
  - Supports custom modules
  - Enables pipeline creation
  - Allows framework extension
  - Facilitates integration
  - Provides plugin system
  - Enables customization

## Benefits

- **Improved Efficiency**: 
  - Streamline prompt engineering workflow
  - Reduce development time
  - Optimize resource usage
  - Automate repetitive tasks
  - Enhance productivity

- **Better Results**: 
  - Generate more effective prompts
  - Improve consistency
  - Enhance reliability
  - Reduce errors
  - Optimize performance

- **Rapid Iteration**: 
  - Quick experimentation
  - Fast optimization
  - Efficient testing
  - Easy refinement
  - Continuous improvement

- **Quality Metrics**: 
  - Quantitative feedback
  - Performance tracking
  - Quality assurance
  - Progress monitoring
  - Improvement suggestions

- **Framework Integration**: 
  - Seamless tool integration
  - Easy adoption
  - Flexible deployment
  - Extensible design
  - Broad compatibility

- **DSPy Powered**: 
  - Advanced language model techniques
  - State-of-the-art optimization
  - Efficient processing
  - Robust performance
  - Continuous updates

## Installation

```bash
pip install synthlang
```

## Basic Usage

1. **Translate Natural Language to SynthLang**
```bash
synthlang translate "Analyze customer feedback and generate sentiment insights"
```

2. **Optimize a Prompt**
```bash
synthlang optimize "path/to/prompt.txt" --iterations 5
```

3. **Evolve Prompts**
```bash
synthlang evolve "initial_prompt" --generations 10 --population 5
```

4. **Classify Prompts**
```bash
synthlang classify "prompt_text" --labels "task,query,instruction"
```

## Advanced Usage

### Custom Evolution Parameters

```bash
synthlang evolve "prompt" \
  --generations 20 \
  --population 10 \
  --mutation-rate 0.3 \
  --tournament-size 3 \
  --fitness-type hybrid
```

### Test-Driven Optimization

```bash
synthlang optimize "prompt" \
  --test-cases tests.json \
  --target-score 0.95 \
  --max-iterations 50
```

### Batch Processing

```bash
synthlang batch-translate prompts.txt \
  --output translated/ \
  --format json \
  --parallel 4
```

### Environment Configuration

Create a `.env` file:
```env
OPENAI_API_KEY=your_key_here
SYNTHLANG_MODEL=gpt-4o-mini
SYNTHLANG_TEMPERATURE=0.7
```

## Examples

### Framework Translation
```bash
# Input
synthlang translate "Get news articles about AI and analyze their sentiment"

# Output
↹ news•ai
⊕ fetch => articles
⊕ analyze => sentiment
Σ results + metrics
```

### Prompt Evolution
```bash
# Start with basic prompt
synthlang evolve "Summarize text" \
  --test-cases summary_tests.json \
  --generations 5

# Evolution produces optimized versions:
# Generation 1: "Extract key points and create concise summary"
# Generation 2: "Identify main themes and synthesize core message"
# Generation 3: "Analyze content, extract insights, generate summary"
```

### Classification Pipeline
```bash
# Classify multiple prompts
synthlang classify-batch prompts.txt \
  --labels "query,task,instruction,conversation" \
  --output classifications.json
```

### Metrics Analysis
```bash
# Get detailed metrics for a prompt
synthlang analyze "prompt.txt" --detailed

# Output
{
  "clarity_score": 0.95,
  "specificity_score": 0.87,
  "consistency_score": 0.92,
  "task_score": 0.89,
  "overall_quality": 0.91
}
```

## Development

1. Clone the repository:
```bash
git clone https://github.com/ruvnet/SynthLang.git
cd SynthLang/cli
```

2. Install development dependencies:
```bash
pip install -e ".[dev]"
```

3. Run tests:
```bash
pytest
```

## Credits

SynthLang CLI is part of the SynthLang Framework created by [@ruvnet](https://github.com/ruvnet).

- **Framework**: [SynthLang](https://github.com/ruvnet/SynthLang)
- **Creator**: [@ruvnet](https://github.com/ruvnet)
- **Documentation**: [synthlang.org](https://synthlang.org)
- **License**: MIT

## Contributing

Contributions are welcome! Please check out our [Contributing Guidelines](CONTRIBUTING.md) for details on how to submit pull requests, report issues, and contribute to the project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
