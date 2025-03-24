# SynthLang Proxy Benchmarking Framework

The SynthLang Proxy includes a comprehensive benchmarking framework for measuring and analyzing various performance aspects of the system. This document provides an overview of the benchmarking capabilities and instructions for running benchmarks.

## Overview

The benchmarking framework allows you to measure:

- **Compression Efficiency**: Evaluate token reduction and cost savings from SynthLang's compression techniques
- **Latency**: Measure response times and time-to-first-token under various conditions
- **Throughput**: Test the system's capacity to handle concurrent requests
- **Cost**: Analyze the financial impact of different optimization strategies

## Benchmark Types

### Compression Benchmark

Evaluates the efficiency of SynthLang's compression techniques by comparing token counts before and after compression.

**Metrics:**
- Compression ratio
- Token reduction percentage
- Cost savings percentage
- Average compression time
- Total original tokens vs. compressed tokens

**Parameters:**
- Compression method (none, synthlang, synthlang+gzip, gzip)
- Text type (general, technical, creative, code)
- Sample size
- Text length constraints
- Option to use real-world samples

### Latency Benchmark

Measures response times and processing speed under various conditions.

**Metrics:**
- Average latency
- Percentile latencies (P50, P90, P99)
- Time to first token (TTFT)
- Processing time

**Parameters:**
- Model to use
- Number of requests
- Prompt length
- Concurrent request count

### Throughput Benchmark

Tests the system's capacity to handle multiple concurrent users and requests.

**Metrics:**
- Requests per second
- Total, successful, and failed requests
- Average response time
- System resource utilization (CPU, memory)

**Parameters:**
- Test duration
- Concurrent user count
- Request interval

### Cost Benchmark

Analyzes the financial impact of different optimization strategies.

**Metrics:**
- Total cost
- Cost per request
- Savings from compression and caching
- Token usage statistics

**Parameters:**
- Request count
- Compression enablement
- Caching enablement

## Running Benchmarks

The benchmarking framework can be run from the command line using the `run_benchmark.py` script.

### Command Line Interface

```bash
python -m app.benchmark.run_benchmark [benchmark_type] [options]
```

Where `benchmark_type` is one of:
- `compression`
- `latency`
- `throughput`
- `cost`

### Common Options

All benchmark types support these options:

```
--model MODEL           Model to use for the benchmark (default: gpt-4o)
--output-dir DIR        Directory to save results in
```

### Compression Benchmark Options

```
--method {none,synthlang,synthlang+gzip,gzip}
                        Compression method to use (default: synthlang)
--text-type {general,technical,creative,code}
                        Type of text to use (default: general)
--sample-size SIZE      Number of samples to use (default: 5)
--min-length LENGTH     Minimum length of text samples (default: 200)
--max-length LENGTH     Maximum length of text samples (default: 2000)
--use-real-samples      Use real-world samples instead of synthetic ones
```

### Latency Benchmark Options

```
--request-count COUNT   Number of requests to make (default: 10)
--prompt-length LENGTH  Length of prompts to use (default: 500)
--concurrent-requests N Number of concurrent requests (default: 1)
```

### Throughput Benchmark Options

```
--duration SECONDS      Duration of the benchmark in seconds (default: 60)
--concurrent-users N    Number of concurrent users (default: 5)
--request-interval MS   Interval between requests in milliseconds (default: 1000)
```

### Cost Benchmark Options

```
--request-count COUNT   Number of requests to make (default: 10)
--compression-enabled   Enable compression
--caching-enabled       Enable caching
```

## Examples

### Running a Compression Benchmark

```bash
python -m app.benchmark.run_benchmark compression --method synthlang+gzip --text-type technical --sample-size 10
```

This will run a compression benchmark using the SynthLang+gzip compression method on 10 technical text samples.

### Running a Latency Benchmark

```bash
python -m app.benchmark.run_benchmark latency --model gpt-4o-mini --request-count 20 --concurrent-requests 5
```

This will measure latency using the gpt-4o-mini model with 20 total requests, 5 of which will be concurrent.

### Running a Throughput Benchmark

```bash
python -m app.benchmark.run_benchmark throughput --duration 120 --concurrent-users 10 --request-interval 500
```

This will run a throughput test for 2 minutes with 10 concurrent users sending requests every 500ms.

### Running a Cost Benchmark

```bash
python -m app.benchmark.run_benchmark cost --request-count 50 --compression-enabled --caching-enabled
```

This will analyze the cost implications of 50 requests with both compression and caching enabled.

## Benchmark Results

Benchmark results are saved as JSON files in the `benchmark_results` directory by default. Each result file includes:

- Benchmark configuration
- All measured metrics
- Timestamp and unique identifier
- Raw data points for detailed analysis

Example result filename: `compression_20250322_235212_1ef46ca1-34c6-4ee1-a4a2-e8f8ad46b5ef.json`

## Programmatic Usage

You can also use the benchmarking framework programmatically in your code:

```python
from app.benchmark import default_runner
from app.benchmark.scenarios.compression import CompressionBenchmark

# Create and register a benchmark
benchmark = CompressionBenchmark("compression")
default_runner.register_scenario(benchmark)

# Configure parameters
parameters = {
    "compression_method": "synthlang",
    "model": "gpt-4o",
    "text_type": "general",
    "sample_size": 5,
    "min_length": 200,
    "max_length": 2000,
    "use_real_samples": False
}

# Run the benchmark
result = default_runner.run_benchmark("compression", parameters)

# Access metrics
compression_ratio = result.metrics["compression_ratio"]
token_reduction = result.metrics["token_reduction_percentage"]
cost_savings = result.metrics["cost_savings_percentage"]

# Save results
result_dict = result.to_dict()
```

## Creating Custom Benchmarks

You can create custom benchmark scenarios by extending the `BenchmarkScenario` class:

```python
from app.benchmark import BenchmarkScenario, BenchmarkResult
from datetime import datetime

class MyCustomBenchmark(BenchmarkScenario):
    def setup(self, parameters):
        # Initialize your benchmark with the given parameters
        self.parameters = parameters
        
    def execute(self):
        # Create a result object
        result = BenchmarkResult(
            scenario_name=self.name,
            start_time=datetime.now()
        )
        
        # Run your benchmark logic
        # ...
        
        # Record metrics
        metrics = {
            "metric1": value1,
            "metric2": value2,
            # ...
        }
        
        # Complete the result with metrics
        result.complete(metrics)
        return result

# Register your custom benchmark
from app.benchmark import default_runner
benchmark = MyCustomBenchmark("my_custom_benchmark")
default_runner.register_scenario(benchmark)
```

## Integration with Agent Framework

The benchmarking framework is integrated with the SynthLang Proxy agent framework, allowing benchmarks to be run via the agent tools interface:

```
#tool_benchmark compression --method synthlang --sample-size 5
```

This enables automated benchmarking and performance monitoring as part of your workflow.

## Best Practices

1. **Run multiple iterations**: For more reliable results, run each benchmark multiple times and average the results.

2. **Control the environment**: Ensure consistent system conditions when comparing benchmark results.

3. **Vary parameters systematically**: When comparing different configurations, change only one parameter at a time.

4. **Use realistic data**: For the most relevant results, use text samples that match your actual use case.

5. **Monitor system resources**: Keep an eye on CPU, memory, and network usage during benchmarks to identify bottlenecks.

6. **Benchmark in production-like environments**: For the most accurate results, run benchmarks in an environment similar to your production setup.