# CLI Benchmark Integration Plan

## Overview

This plan outlines the integration of benchmarking capabilities into the SynthLang CLI. The goal is to provide users with tools to measure and optimize the performance of various SynthLang components, with a focus on both API-related operations and local-only capabilities that don't require LLM access.

## Objectives

1. Integrate existing benchmark functionality into the CLI
2. Add benchmarking commands for compression, caching, and other local operations
3. Implement API-related benchmarking for LLM operations
4. Provide cost analysis tools for estimating and optimizing LLM usage
5. Create reporting capabilities for benchmark results
6. Support the DSPy optimization process planned for phase 19

## Current State Analysis

### Existing Benchmark Functionality

- Benchmark framework in `proxy/tests/test_benchmark.py`
- Benchmark scenarios in `proxy/tests/test_benchmark_scenarios.py`
- Results stored in JSON format in `proxy/benchmark_results/`
- Support for measuring execution time, token usage, and costs

### CLI Structure

- Command-line interface with proxy capabilities
- Compression, caching, and agent tools already implemented
- Modular design that can be extended with benchmarking commands

## Implementation Plan

### Phase 1: Core Benchmark Command Structure

#### 1.1. Create Benchmark Command Group

Add a new command group for benchmarking:

```python
@proxy.group()
def benchmark():
    """Benchmark SynthLang components and operations."""
    pass
```

#### 1.2. Implement Benchmark Configuration

Create configuration options for benchmarks:

```python
@benchmark.command()
@click.option("--output-dir", help="Directory to store benchmark results")
@click.option("--runs", type=int, default=3, help="Number of benchmark runs")
@click.option("--warmup", type=int, default=1, help="Number of warmup runs")
@click.option("--timeout", type=int, default=60, help="Timeout in seconds")
def configure(output_dir, runs, warmup, timeout):
    """Configure benchmark settings."""
    # Implementation
```

#### 1.3. Implement Result Reporting

Create commands for viewing and analyzing benchmark results:

```python
@benchmark.command()
@click.option("--result-file", help="Benchmark result file to view")
@click.option("--format", type=click.Choice(["text", "json", "csv"]), default="text")
def report(result_file, format):
    """View benchmark results."""
    # Implementation
```

### Phase 2: Local-Only Benchmarks

#### 2.1. Compression Benchmarks

Implement benchmarks for compression operations:

```python
@benchmark.command()
@click.option("--input-file", help="File containing text to compress")
@click.option("--use-gzip", is_flag=True, help="Use gzip compression")
@click.option("--iterations", type=int, default=100, help="Number of iterations")
def compression(input_file, use_gzip, iterations):
    """Benchmark compression performance."""
    # Implementation
```

#### 2.2. Cache Benchmarks

Implement benchmarks for cache operations:

```python
@benchmark.command()
@click.option("--size", type=int, default=1000, help="Number of items to cache")
@click.option("--item-size", type=int, default=1000, help="Size of each item in bytes")
@click.option("--read-ratio", type=float, default=0.8, help="Ratio of reads to writes")
def cache(size, item_size, read_ratio):
    """Benchmark cache performance."""
    # Implementation
```

#### 2.3. Tool Registry Benchmarks

Implement benchmarks for agent tool operations:

```python
@benchmark.command()
@click.option("--tools", help="Comma-separated list of tools to benchmark")
@click.option("--iterations", type=int, default=100, help="Number of iterations")
def tools(tools, iterations):
    """Benchmark agent tool performance."""
    # Implementation
```

### Phase 3: API-Related Benchmarks

#### 3.1. LLM Request Benchmarks

Implement benchmarks for LLM API requests:

```python
@benchmark.command()
@click.option("--model", help="Model to benchmark")
@click.option("--prompt-file", help="File containing prompts to use")
@click.option("--iterations", type=int, default=5, help="Number of iterations")
@click.option("--concurrent", type=int, default=1, help="Number of concurrent requests")
def llm(model, prompt_file, iterations, concurrent):
    """Benchmark LLM API performance."""
    # Implementation
```

#### 3.2. Cost Analysis

Implement cost analysis tools:

```python
@benchmark.command()
@click.option("--model", help="Model to analyze")
@click.option("--prompt-file", help="File containing prompts to analyze")
@click.option("--with-compression", is_flag=True, help="Analyze with compression")
def cost(model, prompt_file, with_compression):
    """Analyze cost of LLM operations."""
    # Implementation
```

#### 3.3. Streaming Benchmarks

Implement benchmarks for streaming operations:

```python
@benchmark.command()
@click.option("--model", help="Model to benchmark")
@click.option("--prompt-file", help="File containing prompts to use")
@click.option("--chunk-size", type=int, default=16, help="Chunk size in tokens")
def streaming(model, prompt_file, chunk_size):
    """Benchmark streaming performance."""
    # Implementation
```

### Phase 4: DSPy Integration Benchmarks

#### 4.1. DSPy Module Benchmarks

Implement benchmarks for DSPy modules:

```python
@benchmark.command()
@click.option("--module", help="DSPy module to benchmark")
@click.option("--input-file", help="File containing inputs")
@click.option("--iterations", type=int, default=5, help="Number of iterations")
def dspy_module(module, input_file, iterations):
    """Benchmark DSPy module performance."""
    # Implementation
```

#### 4.2. Optimization Metrics

Implement metrics for optimization:

```python
@benchmark.command()
@click.option("--before", help="Benchmark result before optimization")
@click.option("--after", help="Benchmark result after optimization")
def optimization_metrics(before, after):
    """Calculate optimization metrics."""
    # Implementation
```

### Phase 5: Benchmark Scenarios

#### 5.1. Predefined Scenarios

Implement predefined benchmark scenarios:

```python
@benchmark.command()
@click.option("--scenario", type=click.Choice(["compression", "cache", "llm", "e2e"]), required=True)
@click.option("--output-file", help="File to store results")
def scenario(scenario, output_file):
    """Run a predefined benchmark scenario."""
    # Implementation
```

#### 5.2. Custom Scenarios

Support for custom benchmark scenarios:

```python
@benchmark.command()
@click.option("--scenario-file", help="JSON file defining the scenario", required=True)
@click.option("--output-file", help="File to store results")
def custom_scenario(scenario_file, output_file):
    """Run a custom benchmark scenario."""
    # Implementation
```

### Phase 6: Integration with Phase 19 (DSPy Optimization)

#### 6.1. Optimization Preparation

Implement commands for preparing optimization:

```python
@benchmark.command()
@click.option("--target", help="Target to optimize", required=True)
@click.option("--metric", help="Metric to optimize for", required=True)
@click.option("--output-file", help="File to store optimization plan")
def prepare_optimization(target, metric, output_file):
    """Prepare for DSPy optimization."""
    # Implementation
```

#### 6.2. Optimization Evaluation

Implement commands for evaluating optimization:

```python
@benchmark.command()
@click.option("--before", help="Benchmark result before optimization", required=True)
@click.option("--after", help="Benchmark result after optimization", required=True)
@click.option("--output-file", help="File to store evaluation results")
def evaluate_optimization(before, after, output_file):
    """Evaluate optimization results."""
    # Implementation
```

## Implementation Details

### Benchmark Module Structure

```
synthlang/
├── proxy/
│   ├── benchmark/
│   │   ├── __init__.py
│   │   ├── config.py          # Benchmark configuration
│   │   ├── runner.py          # Benchmark runner
│   │   ├── reporter.py        # Result reporting
│   │   ├── scenarios.py       # Predefined scenarios
│   │   ├── metrics.py         # Benchmark metrics
│   │   └── utils.py           # Utility functions
│   ├── benchmark_scenarios/
│   │   ├── __init__.py
│   │   ├── compression.py     # Compression benchmarks
│   │   ├── cache.py           # Cache benchmarks
│   │   ├── llm.py             # LLM benchmarks
│   │   ├── tools.py           # Tool benchmarks
│   │   └── dspy.py            # DSPy benchmarks
```

### Benchmark Result Format

```json
{
  "id": "benchmark_20250323_123456_abcdef",
  "timestamp": "2025-03-23T12:34:56Z",
  "scenario": "compression",
  "config": {
    "iterations": 100,
    "warmup": 1,
    "timeout": 60
  },
  "results": {
    "execution_time": {
      "mean": 0.0123,
      "median": 0.0120,
      "min": 0.0100,
      "max": 0.0150,
      "std_dev": 0.0010
    },
    "memory_usage": {
      "mean": 1024,
      "median": 1024,
      "min": 1000,
      "max": 1100,
      "std_dev": 20
    },
    "compression_ratio": {
      "mean": 0.5,
      "median": 0.5,
      "min": 0.4,
      "max": 0.6,
      "std_dev": 0.05
    }
  },
  "metadata": {
    "platform": "Linux-5.15.0-x86_64",
    "python_version": "3.9.5",
    "synthlang_version": "0.2.0"
  }
}
```

### CLI Command Examples

```bash
# Run compression benchmark
synthlang proxy benchmark compression --input-file prompts.txt --iterations 100

# Run LLM benchmark
synthlang proxy benchmark llm --model gpt-4o-mini --prompt-file prompts.txt --iterations 5

# Run predefined scenario
synthlang proxy benchmark scenario --scenario compression --output-file results.json

# View benchmark results
synthlang proxy benchmark report --result-file results.json --format text

# Analyze cost
synthlang proxy benchmark cost --model gpt-4o-mini --prompt-file prompts.txt --with-compression

# Prepare for optimization
synthlang proxy benchmark prepare-optimization --target compression --metric ratio --output-file optimization_plan.json
```

## Timeline

1. Phase 1 (Core Benchmark Command Structure): 1 day
2. Phase 2 (Local-Only Benchmarks): 2 days
3. Phase 3 (API-Related Benchmarks): 2 days
4. Phase 4 (DSPy Integration Benchmarks): 1 day
5. Phase 5 (Benchmark Scenarios): 1 day
6. Phase 6 (Integration with Phase 19): 1 day

Total: 8 days

## Dependencies

- Python 3.8+
- Click for CLI interface
- Existing benchmark framework
- DSPy for optimization (Phase 19)

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Performance variability | Run multiple iterations and report statistical measures |
| API rate limiting | Implement backoff and retry mechanisms |
| Cost of API calls | Provide dry-run options and cost estimates |
| Integration with Phase 19 | Design with clear interfaces for future integration |

## Success Criteria

1. All benchmark commands function correctly
2. Results are accurate and reproducible
3. Reports provide actionable insights
4. Integration with Phase 19 is well-defined
5. Documentation is complete and clear