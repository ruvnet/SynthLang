"""
Benchmark framework for the SynthLang Proxy.

This package provides a comprehensive benchmark framework for measuring and
analyzing the performance of the SynthLang Proxy, including compression
efficiency, latency, throughput, and cost implications.

The framework includes:
- Core components for running benchmarks and collecting metrics
- Predefined benchmark scenarios for different aspects of performance
- Tools for integrating benchmarks with the agent framework
- Data management for benchmark samples and results
- Report generation for visualizing benchmark results
"""
from app.benchmark.core import (
    BenchmarkScenario, BenchmarkResult, BenchmarkRunner,
    MetricsCollector, BenchmarkConfig, ConfigurationManager
)
from app.benchmark.scenarios import (
    CompressionBenchmark, LatencyBenchmark,
    ThroughputBenchmark, CostBenchmark
)


__all__ = [
    # Core components
    'BenchmarkScenario',
    'BenchmarkResult',
    'BenchmarkRunner',
    'MetricsCollector',
    'BenchmarkConfig',
    'ConfigurationManager',
    
    # Benchmark scenarios
    'CompressionBenchmark',
    'LatencyBenchmark',
    'ThroughputBenchmark',
    'CostBenchmark'
]


# Initialize the benchmark framework
def initialize_benchmark_framework():
    """Initialize the benchmark framework."""
    # Import the benchmark tool to register it with the agent framework
    from app.benchmark.tools import benchmark_tool
    
    # Return the benchmark tool for convenience
    return benchmark_tool


# Create a default benchmark runner instance
default_runner = BenchmarkRunner()