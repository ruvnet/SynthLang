# SynthLang Classification System

## Introduction

The SynthLang Classification System is a DSPy-based module that enables automatic classification and finetuning of prompts. Using bootstrapped few-shot learning, it can learn to categorize prompts into different types and provide explanations for its classifications.

## Features

1. **Prompt Classification**
   - Classify prompts into predefined categories
   - Provide explanations for classifications
   - Support for multiple labels
   - Model persistence and loading

2. **DSPy Integration**
   - Uses DSPy's Predict and BootstrapFewShot
   - Automatic few-shot example selection
   - Self-improving through bootstrapping

3. **Training and Evaluation**
   - Train on example prompts
   - Evaluate on test sets
   - Track accuracy metrics
   - Save and load trained models

## Usage

### Basic Classification

```bash
# Classify a single prompt
synthlang classify predict \
    --text "↹ data•sales\n⊕ analyze => insights\nΣ report" \
    --labels "analysis,sentiment,reporting,translation,code"

# Output:
# Classification result:
# Input: ↹ data•sales\n⊕ analyze => insights\nΣ report
# Label: analysis
# Explanation: This prompt focuses on analyzing sales data and generating insights
```

### Training

```bash
# Train a new classifier
synthlang classify train \
    --train-data examples/train_data.json \
    --labels "analysis,sentiment,reporting,translation,code" \
    --save-model models/classifier.json

# Output:
# Training complete!
# Examples used: 5
# Training rounds: 2
# Final accuracy: 0.85
```

### Evaluation

```bash
# Evaluate a trained classifier
synthlang classify evaluate \
    --test-data examples/test_data.json \
    --model models/classifier.json

# Output:
# Evaluation complete!
# Test examples: 5
# Accuracy: 0.90
```

## Data Formats

### Training Data

```json
{
    "examples": [
        {
            "input": "↹ data•sales\n⊕ analyze => insights\nΣ report",
            "label": "analysis",
            "explanation": "This prompt focuses on analyzing sales data"
        }
    ]
}
```

### Test Data

```json
{
    "examples": [
        {
            "input": "↹ data•revenue\n⊕ analyze => trends\nΣ insights",
            "label": "analysis"
        }
    ]
}
```

## Implementation Details

### DSPy Integration

The system uses DSPy's powerful features:

1. **Signatures**
   ```python
   class ClassificationSignature(dspy.Signature):
       input = dspy.InputField()
       label = dspy.OutputField(desc="Classification label")
       explanation = dspy.OutputField(desc="Explanation for the classification")
   ```

2. **Bootstrapping**
   ```python
   bootstrapper = BootstrapFewShot(
       metric=dspy.metrics.Accuracy(),
       num_threads=4,
       num_samples=3,
       num_trials=3,
       max_bootstrapped_demos=3,
       max_labeled_demos=5,
       max_rounds=2
   )
   ```

### Training Process

1. **Data Preparation**
   - Load training examples
   - Parse labels and explanations
   - Prepare bootstrap examples

2. **Model Training**
   - Initialize DSPy predictor
   - Run bootstrapping rounds
   - Select best examples
   - Compile final model

3. **Evaluation**
   - Test on holdout examples
   - Calculate accuracy metrics
   - Generate performance report

## Best Practices

1. **Training Data**
   - Include diverse examples
   - Balance label distribution
   - Provide clear explanations
   - Use real-world prompts

2. **Model Selection**
   - Start with small example sets
   - Gradually increase complexity
   - Monitor accuracy metrics
   - Use cross-validation

3. **Deployment**
   - Save trained models
   - Version control models
   - Monitor performance
   - Retrain periodically

## Advanced Features

1. **Custom Labels**
   - Define your own categories
   - Add new labels dynamically
   - Create hierarchical labels

2. **Model Management**
   - Save multiple models
   - Compare model versions
   - Export/import models

3. **Integration**
   - Use with prompt evolution
   - Combine with optimization
   - Automate classification

## Future Enhancements

1. **Planned Features**
   - Multi-label classification
   - Confidence scores
   - Active learning
   - Online training

2. **Improvements**
   - Better few-shot selection
   - Enhanced explanations
   - Faster training
   - Higher accuracy

## Command Reference

```bash
# Full classification workflow
synthlang classify train \
    --train-data train.json \
    --labels "label1,label2,label3" \
    --save-model model.json

synthlang classify evaluate \
    --test-data test.json \
    --model model.json

synthlang classify predict \
    --text "your prompt here" \
    --labels "label1,label2,label3" \
    --model model.json
```

This classification system enables automatic categorization of prompts, helping users organize and understand their prompt libraries better. Through DSPy integration and few-shot learning, it provides accurate classifications with explanations, making it a valuable tool for prompt engineering workflows.
