"""
Tests for the benchmark framework.

This module contains tests for the benchmark framework functionality.
"""
import pytest
from unittest.mock import patch, MagicMock
import os
import sys
from datetime import datetime

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from app.benchmark.core.scenario import BenchmarkScenario, BenchmarkResult
from app.benchmark.core.metrics import MetricsCollector
from app.benchmark.core.runner import BenchmarkRunner


class SimpleBenchmark(BenchmarkScenario):
    """A simple benchmark scenario for testing."""
    
    def setup(self, parameters):
        self.parameters = parameters
        self.value = parameters.get("value", 42)
    
    def execute(self):
        result = BenchmarkResult(
            scenario_name=self.name,
            start_time=datetime.now()
        )
        result.complete({"value": self.value})
        return result


def test_benchmark_scenario_execution():
    """Test that a benchmark scenario can be executed."""
    # Create a benchmark scenario
    scenario = SimpleBenchmark("simple")
    
    # Run the benchmark
    result = scenario.run({"value": 123})
    
    # Verify the result
    assert result.scenario_name == "simple"
    assert result.metrics["value"] == 123


def test_benchmark_runner():
    """Test that the benchmark runner can execute scenarios."""
    # Create a benchmark runner
    runner = BenchmarkRunner()
    
    # Register a benchmark scenario
    runner.register_scenario(SimpleBenchmark("simple"))
    
    # Run the benchmark
    result = runner.run_benchmark("simple", {"value": 456})
    
    # Verify the result
    assert result.scenario_name == "simple"
    assert result.metrics["value"] == 456


def test_metrics_collector():
    """Test that the metrics collector can record and analyze metrics."""
    # Create a metrics collector
    collector = MetricsCollector()
    
    # Record some metrics
    collector.record_metric("test_metric", 1.0)
    collector.record_metric("test_metric", 2.0)
    collector.record_metric("test_metric", 3.0)
    
    # Get statistics
    stats = collector.get_statistics("test_metric")
    
    # Verify the statistics
    assert stats is not None
    assert stats.count == 3
    assert stats.min == 1.0
    assert stats.max == 3.0
    assert stats.mean == 2.0
    assert stats.median == 2.0


def test_token_reduction_metrics():
    """Test that token reduction metrics can be recorded and analyzed."""
    # Create a metrics collector
    collector = MetricsCollector()
    
    # Record token counts
    collector.record_token_counts(original=100, compressed=60)
    collector.record_token_counts(original=200, compressed=100)
    
    # Get token reduction summary
    summary = collector.get_token_reduction_summary()
    
    # Verify the summary
    assert summary["count"] == 2
    assert summary["average_reduction_percentage"] == 45.0  # (40% + 50%) / 2
    assert summary["total_original_tokens"] == 300
    assert summary["total_compressed_tokens"] == 160
    assert summary["overall_reduction_percentage"] == pytest.approx(46.67, 0.01)  # (300-160)/300 * 100