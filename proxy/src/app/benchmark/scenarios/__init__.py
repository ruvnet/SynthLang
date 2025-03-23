"""
Benchmark scenarios for the benchmark framework.

This module provides benchmark scenarios for measuring different aspects of
the SynthLang Proxy, including compression efficiency, latency, throughput,
and cost implications.
"""
from app.benchmark.scenarios.compression import CompressionBenchmark
from app.benchmark.scenarios.latency import LatencyBenchmark
from app.benchmark.scenarios.throughput import ThroughputBenchmark
from app.benchmark.scenarios.cost import CostBenchmark


__all__ = [
    'CompressionBenchmark',
    'LatencyBenchmark',
    'ThroughputBenchmark',
    'CostBenchmark'
]