"""
Agent tool for running benchmarks.

This module provides an agent tool for running benchmarks and analyzing
performance, including direct tool invocation via #benchmark syntax and
natural language interfaces.
"""
from typing import Dict, Any, Optional, Tuple, List
import re
import json
import logging
from datetime import datetime

from app.agents.registry import register_tool
from app.benchmark.core.runner import BenchmarkRunner
from app.benchmark.scenarios.compression import CompressionBenchmark
from app.benchmark.scenarios.latency import LatencyBenchmark
from app.benchmark.scenarios.throughput import ThroughputBenchmark
from app.benchmark.scenarios.cost import CostBenchmark


logger = logging.getLogger(__name__)


# Global benchmark runner instance
_benchmark_runner = BenchmarkRunner()


def _initialize_benchmark_scenarios():
    """Initialize and register default benchmark scenarios."""
    try:
        # Register compression benchmark
        _benchmark_runner.register_scenario(CompressionBenchmark("compression"))
        
        # Register latency benchmark
        _benchmark_runner.register_scenario(LatencyBenchmark("latency"))
        
        # Register throughput benchmark
        _benchmark_runner.register_scenario(ThroughputBenchmark("throughput"))
        
        # Register cost benchmark
        _benchmark_runner.register_scenario(CostBenchmark("cost"))
        
        logger.info("Initialized benchmark scenarios")
    except Exception as e:
        logger.error(f"Error initializing benchmark scenarios: {e}")


def parse_tool_invocation(message: str) -> Tuple[Optional[str], str]:
    """
    Parse a message for tool invocation syntax.
    
    Args:
        message: The user message
        
    Returns:
        Tuple of (tool_name, remaining_message) or (None, original_message)
    """
    # Check for #tool_name syntax
    if message.startswith('#'):
        parts = message.split(' ', 1)
        tool_name = parts[0][1:]  # Remove the # prefix
        remaining_message = parts[1] if len(parts) > 1 else ""
        return tool_name, remaining_message
    
    # No explicit tool invocation
    return None, message


def _parse_benchmark_parameters(query: str) -> Dict[str, Any]:
    """
    Parse benchmark parameters from a natural language query.
    
    Args:
        query: Natural language query
        
    Returns:
        Dictionary of parameters
    """
    parameters = {}
    
    # Extract compression method
    compression_match = re.search(r'compression(?:\s+method)?[:\s]+(\w+)', query, re.IGNORECASE)
    if compression_match:
        parameters["compression_method"] = compression_match.group(1).lower()
    
    # Extract model name
    model_match = re.search(r'model[:\s]+([a-zA-Z0-9\-]+)', query, re.IGNORECASE)
    if model_match:
        parameters["model"] = model_match.group(1)
    
    # Extract text type
    text_type_match = re.search(r'text(?:\s+type)?[:\s]+(\w+)', query, re.IGNORECASE)
    if text_type_match:
        parameters["text_type"] = text_type_match.group(1).lower()
    
    # Extract sample size
    sample_size_match = re.search(r'sample(?:\s+size)?[:\s]+(\d+)', query, re.IGNORECASE)
    if sample_size_match:
        parameters["sample_size"] = int(sample_size_match.group(1))
    
    # Extract use_gzip flag
    if re.search(r'\bgzip\b', query, re.IGNORECASE):
        parameters["use_gzip"] = True
    
    return parameters


def _get_scenario_from_query(query: str) -> Optional[str]:
    """
    Determine the benchmark scenario from a natural language query.
    
    Args:
        query: Natural language query
        
    Returns:
        Scenario name or None if not determined
    """
    # Check for explicit scenario mentions
    if re.search(r'\bcompression\b', query, re.IGNORECASE):
        return "compression"
    elif re.search(r'\blatency\b', query, re.IGNORECASE):
        return "latency"
    elif re.search(r'\bthroughput\b', query, re.IGNORECASE):
        return "throughput"
    elif re.search(r'\bcost\b', query, re.IGNORECASE):
        return "cost"
    
    # Default to compression if not specified
    return "compression"


def benchmark_tool(query: Optional[str] = None, scenario: Optional[str] = None, 
                  parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Run a benchmark and return the results.
    
    This function can be called directly or via the agent framework. It supports
    both natural language queries and direct parameter specification.
    
    Args:
        query: Natural language query describing the benchmark to run
        scenario: Specific benchmark scenario to run
        parameters: Parameters for the benchmark
        
    Returns:
        Dictionary containing benchmark results and formatted content
    """
    # Initialize scenarios if not already done
    if not _benchmark_runner.scenarios:
        _initialize_benchmark_scenarios()
    
    # Parse parameters from query if provided
    parsed_parameters = {}
    if query:
        parsed_parameters = _parse_benchmark_parameters(query)
        
        # Determine scenario from query if not explicitly provided
        if not scenario:
            scenario = _get_scenario_from_query(query)
    
    # Merge parameters, with explicit parameters taking precedence
    effective_parameters = parsed_parameters.copy()
    if parameters:
        effective_parameters.update(parameters)
    
    # Default to compression benchmark if not specified
    if not scenario:
        scenario = "compression"
    
    try:
        # Run the benchmark
        logger.info(f"Running benchmark: {scenario} with parameters: {effective_parameters}")
        result = _benchmark_runner.run_benchmark(scenario, effective_parameters)
        
        # Format the result for display
        formatted_result = _format_benchmark_result(result)
        
        return {
            "content": formatted_result,
            "raw_result": result.to_dict()
        }
    except Exception as e:
        logger.error(f"Error running benchmark: {e}")
        return {
            "content": f"Error running benchmark: {e}",
            "error": str(e)
        }


def _format_benchmark_result(result: Any) -> str:
    """
    Format a benchmark result for display.
    
    Args:
        result: Benchmark result
        
    Returns:
        Formatted string for display
    """
    lines = [
        f"# Benchmark Results: {result.scenario_name}",
        f"Run ID: {result.id}",
        f"Duration: {result.duration_ms:.2f}ms",
        "",
        "## Parameters"
    ]
    
    for key, value in result.parameters.items():
        lines.append(f"- {key}: {value}")
    
    lines.append("")
    lines.append("## Metrics")
    
    for key, value in result.metrics.items():
        if isinstance(value, dict):
            lines.append(f"### {key}")
            for subkey, subvalue in value.items():
                if isinstance(subvalue, float):
                    lines.append(f"- {subkey}: {subvalue:.2f}")
                else:
                    lines.append(f"- {subkey}: {subvalue}")
        elif isinstance(value, float):
            lines.append(f"- {key}: {value:.2f}")
        else:
            lines.append(f"- {key}: {value}")
    
    # Add summary section for specific benchmark types
    if result.scenario_name == "compression":
        if "token_reduction_percentage" in result.metrics:
            lines.append("")
            lines.append("## Summary")
            lines.append(f"Token reduction: {result.metrics['token_reduction_percentage']:.2f}%")
            
            if "cost_savings_percentage" in result.metrics:
                lines.append(f"Cost savings: {result.metrics['cost_savings_percentage']:.2f}%")
    
    return "\n".join(lines)


def list_available_benchmarks() -> Dict[str, Any]:
    """
    List all available benchmark scenarios.
    
    Returns:
        Dictionary containing the list of available benchmarks
    """
    # Initialize scenarios if not already done
    if not _benchmark_runner.scenarios:
        _initialize_benchmark_scenarios()
    
    scenarios = _benchmark_runner.list_scenarios()
    
    return {
        "content": f"Available benchmark scenarios: {', '.join(scenarios)}",
        "scenarios": scenarios
    }


# Register the benchmark tool with the agent registry
register_tool("benchmark", benchmark_tool)
register_tool("list_benchmarks", list_available_benchmarks)