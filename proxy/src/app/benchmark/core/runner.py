"""
Benchmark runner for the benchmark framework.

This module provides the BenchmarkRunner class, which orchestrates the execution
of benchmark scenarios and collects results.
"""
from typing import Dict, Any, List, Optional, Type, Callable
import time
import json
import os
from datetime import datetime
import logging

from app.benchmark.core.scenario import BenchmarkScenario, BenchmarkResult
from app.benchmark.core.metrics import MetricsCollector


logger = logging.getLogger(__name__)


class BenchmarkRunner:
    """
    Orchestrates benchmark execution and collects results.
    
    This class manages the registration, execution, and result collection
    for benchmark scenarios.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize with configuration parameters.
        
        Args:
            config: Optional configuration parameters for the benchmark runner
        """
        self.config = config or {}
        self.scenarios: Dict[str, BenchmarkScenario] = {}
        self.results: List[BenchmarkResult] = []
        self.metrics_collector = MetricsCollector()
        
        # Configure output directory
        self.output_dir = self.config.get("output_dir", "benchmark_results")
        os.makedirs(self.output_dir, exist_ok=True)
    
    def register_scenario(self, scenario: BenchmarkScenario) -> None:
        """
        Register a benchmark scenario.
        
        Args:
            scenario: The benchmark scenario to register
        """
        self.scenarios[scenario.name] = scenario
        logger.info(f"Registered benchmark scenario: {scenario.name}")
    
    def register_scenario_class(self, scenario_class: Type[BenchmarkScenario], name: str, **kwargs) -> None:
        """
        Register a benchmark scenario class.
        
        Args:
            scenario_class: The benchmark scenario class to register
            name: Name for the scenario instance
            **kwargs: Additional arguments to pass to the scenario constructor
        """
        scenario = scenario_class(name, **kwargs)
        self.register_scenario(scenario)
    
    def get_scenario(self, scenario_name: str) -> Optional[BenchmarkScenario]:
        """
        Get a registered benchmark scenario by name.
        
        Args:
            scenario_name: Name of the scenario to retrieve
            
        Returns:
            The benchmark scenario, or None if not found
        """
        return self.scenarios.get(scenario_name)
    
    def list_scenarios(self) -> List[str]:
        """
        List all registered benchmark scenarios.
        
        Returns:
            List of scenario names
        """
        return list(self.scenarios.keys())
    
    def run_benchmark(self, scenario_name: str, parameters: Optional[Dict[str, Any]] = None) -> BenchmarkResult:
        """
        Run a specific benchmark scenario with parameters.
        
        Args:
            scenario_name: Name of the scenario to run
            parameters: Parameters for the benchmark
            
        Returns:
            BenchmarkResult containing metrics and metadata
            
        Raises:
            ValueError: If the scenario is not found
        """
        scenario = self.get_scenario(scenario_name)
        if not scenario:
            raise ValueError(f"Benchmark scenario not found: {scenario_name}")
        
        parameters = parameters or {}
        logger.info(f"Running benchmark: {scenario_name} with parameters: {parameters}")
        
        # Run the benchmark
        start_time = time.time()
        result = scenario.run(parameters)
        end_time = time.time()
        
        # Record execution time if not already set
        if result.duration_ms is None:
            result.duration_ms = (end_time - start_time) * 1000
        
        # Store the result
        self.results.append(result)
        
        # Save the result to disk
        self._save_result(result)
        
        logger.info(f"Benchmark completed: {scenario_name} in {result.duration_ms:.2f}ms")
        return result
    
    def run_all_benchmarks(self, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, BenchmarkResult]:
        """
        Run all registered benchmark scenarios.
        
        Args:
            parameters: Parameters for the benchmarks
            
        Returns:
            Dictionary mapping scenario names to benchmark results
        """
        results = {}
        for scenario_name in self.scenarios:
            try:
                result = self.run_benchmark(scenario_name, parameters)
                results[scenario_name] = result
            except Exception as e:
                logger.error(f"Error running benchmark {scenario_name}: {e}")
                # Continue with other benchmarks
        
        return results
    
    def compare_results(self, result1: BenchmarkResult, result2: BenchmarkResult) -> Dict[str, Any]:
        """
        Compare two benchmark results.
        
        Args:
            result1: First benchmark result
            result2: Second benchmark result
            
        Returns:
            Dictionary containing comparison metrics
        """
        comparison = {
            "scenario_name": f"Comparison: {result1.scenario_name} vs {result2.scenario_name}",
            "duration_diff_ms": result2.duration_ms - result1.duration_ms,
            "duration_diff_percent": ((result2.duration_ms - result1.duration_ms) / result1.duration_ms) * 100 if result1.duration_ms else 0,
            "metrics_comparison": {}
        }
        
        # Compare metrics that exist in both results
        for key in set(result1.metrics.keys()) & set(result2.metrics.keys()):
            if isinstance(result1.metrics[key], (int, float)) and isinstance(result2.metrics[key], (int, float)):
                diff = result2.metrics[key] - result1.metrics[key]
                diff_percent = (diff / result1.metrics[key]) * 100 if result1.metrics[key] else 0
                
                comparison["metrics_comparison"][key] = {
                    "value1": result1.metrics[key],
                    "value2": result2.metrics[key],
                    "diff": diff,
                    "diff_percent": diff_percent
                }
        
        return comparison
    
    def _save_result(self, result: BenchmarkResult) -> None:
        """
        Save a benchmark result to disk.
        
        Args:
            result: The benchmark result to save
        """
        # Create a timestamped filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{result.scenario_name}_{timestamp}_{result.id}.json"
        filepath = os.path.join(self.output_dir, filename)
        
        # Save as JSON
        with open(filepath, 'w') as f:
            json.dump(result.to_dict(), f, indent=2, default=str)
        
        logger.debug(f"Saved benchmark result to {filepath}")
    
    def load_result(self, filepath: str) -> BenchmarkResult:
        """
        Load a benchmark result from disk.
        
        Args:
            filepath: Path to the result file
            
        Returns:
            The loaded benchmark result
            
        Raises:
            FileNotFoundError: If the file is not found
            ValueError: If the file is not a valid benchmark result
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Convert the loaded data back to a BenchmarkResult
        result = BenchmarkResult(
            scenario_name=data["scenario_name"],
            start_time=datetime.fromisoformat(data["start_time"]),
            id=data["id"]
        )
        
        if data["end_time"]:
            result.end_time = datetime.fromisoformat(data["end_time"])
        
        result.duration_ms = data["duration_ms"]
        result.parameters = data["parameters"]
        result.metrics = data["metrics"]
        result.metadata = data["metadata"]
        
        return result
    
    def generate_report(self, format: str = "json") -> str:
        """
        Generate a report of all benchmark results.
        
        Args:
            format: Output format ("json" or "text")
            
        Returns:
            Report in the specified format
        """
        if format.lower() == "json":
            report = {
                "timestamp": datetime.now().isoformat(),
                "total_benchmarks": len(self.results),
                "results": [result.to_dict() for result in self.results]
            }
            return json.dumps(report, indent=2, default=str)
        
        elif format.lower() == "text":
            lines = [
                "Benchmark Report",
                "================",
                f"Generated: {datetime.now().isoformat()}",
                f"Total Benchmarks: {len(self.results)}",
                ""
            ]
            
            for result in self.results:
                lines.append(f"Scenario: {result.scenario_name}")
                lines.append(f"ID: {result.id}")
                lines.append(f"Duration: {result.duration_ms:.2f}ms")
                lines.append("Parameters:")
                for key, value in result.parameters.items():
                    lines.append(f"  {key}: {value}")
                lines.append("Metrics:")
                for key, value in result.metrics.items():
                    lines.append(f"  {key}: {value}")
                lines.append("")
            
            return "\n".join(lines)
        
        else:
            raise ValueError(f"Unsupported report format: {format}")
    
    def reset(self) -> None:
        """Reset the benchmark runner, clearing all results."""
        self.results.clear()
        self.metrics_collector.reset()
        logger.info("Benchmark runner reset")