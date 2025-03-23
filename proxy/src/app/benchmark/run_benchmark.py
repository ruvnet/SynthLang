"""
Benchmark runner script.

This script provides a command-line interface for running benchmarks.
"""
import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from app.benchmark import default_runner
from app.benchmark.scenarios.compression import CompressionBenchmark
from app.benchmark.scenarios.latency import LatencyBenchmark
from app.benchmark.scenarios.throughput import ThroughputBenchmark
from app.benchmark.scenarios.cost import CostBenchmark


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def save_results(result, output_dir=None):
    """
    Save benchmark results to a JSON file.
    
    Args:
        result: Benchmark result to save
        output_dir: Directory to save results in (default: benchmark_results)
    """
    # Create output directory if it doesn't exist
    if output_dir is None:
        output_dir = Path(__file__).parent.parent.parent.parent / "benchmark_results"
    else:
        output_dir = Path(output_dir)
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{result.scenario_name}_{timestamp}_{result.id}.json"
    filepath = output_dir / filename
    
    # Convert result to dictionary
    result_dict = result.to_dict()
    
    # Save to file
    with open(filepath, 'w') as f:
        json.dump(result_dict, f, indent=2)
    
    logger.info(f"Results saved to {filepath}")
    return filepath


def run_compression_benchmark(args):
    """
    Run the compression benchmark with the specified parameters.
    
    Args:
        args: Command-line arguments
    """
    # Register the compression benchmark
    benchmark = CompressionBenchmark("compression")
    default_runner.register_scenario(benchmark)
    
    # Prepare parameters
    parameters = {
        "compression_method": args.method,
        "model": args.model,
        "text_type": args.text_type,
        "sample_size": args.sample_size,
        "min_length": args.min_length,
        "max_length": args.max_length,
        "use_real_samples": args.use_real_samples
    }
    
    # Run the benchmark
    logger.info(f"Running compression benchmark with parameters: {parameters}")
    result = default_runner.run_benchmark("compression", parameters)
    
    # Save results
    save_results(result, args.output_dir)
    
    # Print summary
    print("\nCompression Benchmark Results:")
    print(f"Compression Ratio: {result.metrics['compression_ratio']:.2f}")
    print(f"Token Reduction: {result.metrics['token_reduction_percentage']:.2f}%")
    print(f"Cost Savings: {result.metrics['cost_savings_percentage']:.2f}%")
    print(f"Average Compression Time: {result.metrics['average_compression_time_ms']:.2f} ms")
    print(f"Original Tokens: {result.metrics['total_original_tokens']}")
    print(f"Compressed Tokens: {result.metrics['total_compressed_tokens']}")
    print(f"Token Reduction: {result.metrics['token_reduction_count']}")
    print(f"Cost Savings: ${result.metrics['cost_savings_usd']:.6f}")


def run_latency_benchmark(args):
    """
    Run the latency benchmark with the specified parameters.
    
    Args:
        args: Command-line arguments
    """
    # Register the latency benchmark
    benchmark = LatencyBenchmark("latency")
    default_runner.register_scenario(benchmark)
    
    # Prepare parameters
    parameters = {
        "model": args.model,
        "request_count": args.request_count,
        "prompt_length": args.prompt_length,
        "concurrent_requests": args.concurrent_requests
    }
    
    # Run the benchmark
    logger.info(f"Running latency benchmark with parameters: {parameters}")
    result = default_runner.run_benchmark("latency", parameters)
    
    # Save results
    save_results(result, args.output_dir)
    
    # Print summary
    print("\nLatency Benchmark Results:")
    print(f"Average Latency: {result.metrics['average_latency_ms']:.2f} ms")
    print(f"P50 Latency: {result.metrics['p50_latency_ms']:.2f} ms")
    print(f"P90 Latency: {result.metrics['p90_latency_ms']:.2f} ms")
    print(f"P99 Latency: {result.metrics['p99_latency_ms']:.2f} ms")
    print(f"Time to First Token: {result.metrics['average_ttft_ms']:.2f} ms")
    print(f"Processing Time: {result.metrics['average_processing_time_ms']:.2f} ms")


def run_throughput_benchmark(args):
    """
    Run the throughput benchmark with the specified parameters.
    
    Args:
        args: Command-line arguments
    """
    # Register the throughput benchmark
    benchmark = ThroughputBenchmark("throughput")
    default_runner.register_scenario(benchmark)
    
    # Prepare parameters
    parameters = {
        "model": args.model,
        "duration_seconds": args.duration,
        "concurrent_users": args.concurrent_users,
        "request_interval_ms": args.request_interval
    }
    
    # Run the benchmark
    logger.info(f"Running throughput benchmark with parameters: {parameters}")
    result = default_runner.run_benchmark("throughput", parameters)
    
    # Save results
    save_results(result, args.output_dir)
    
    # Print summary
    print("\nThroughput Benchmark Results:")
    print(f"Requests Per Second: {result.metrics['requests_per_second']:.2f}")
    print(f"Total Requests: {result.metrics['total_requests']}")
    print(f"Successful Requests: {result.metrics['successful_requests']}")
    print(f"Failed Requests: {result.metrics['failed_requests']}")
    print(f"Average Response Time: {result.metrics['average_response_time_ms']:.2f} ms")
    print(f"CPU Utilization: {result.metrics['cpu_utilization_percentage']:.2f}%")
    print(f"Memory Utilization: {result.metrics['memory_utilization_percentage']:.2f}%")


def run_cost_benchmark(args):
    """
    Run the cost benchmark with the specified parameters.
    
    Args:
        args: Command-line arguments
    """
    # Register the cost benchmark
    benchmark = CostBenchmark("cost")
    default_runner.register_scenario(benchmark)
    
    # Prepare parameters
    parameters = {
        "model": args.model,
        "request_count": args.request_count,
        "compression_enabled": args.compression_enabled,
        "caching_enabled": args.caching_enabled
    }
    
    # Run the benchmark
    logger.info(f"Running cost benchmark with parameters: {parameters}")
    result = default_runner.run_benchmark("cost", parameters)
    
    # Save results
    save_results(result, args.output_dir)
    
    # Print summary
    print("\nCost Benchmark Results:")
    print(f"Total Cost: ${result.metrics['total_cost']:.6f}")
    print(f"Cost Per Request: ${result.metrics['cost_per_request']:.6f}")
    print(f"Cost Savings with Compression: ${result.metrics['compression_savings']:.6f}")
    print(f"Cost Savings with Caching: ${result.metrics['caching_savings']:.6f}")
    print(f"Total Tokens: {result.metrics['total_tokens']}")
    print(f"Average Tokens Per Request: {result.metrics['average_tokens_per_request']:.2f}")


def main():
    """Main entry point for the benchmark runner."""
    parser = argparse.ArgumentParser(description="Run benchmarks for the SynthLang Proxy")
    subparsers = parser.add_subparsers(dest="benchmark", help="Benchmark to run")
    
    # Common arguments
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument("--model", type=str, default="gpt-4o", help="Model to use for the benchmark")
    common_parser.add_argument("--output-dir", type=str, help="Directory to save results in")
    
    # Compression benchmark
    compression_parser = subparsers.add_parser("compression", parents=[common_parser], help="Run compression benchmark")
    compression_parser.add_argument("--method", type=str, default="synthlang", choices=["none", "synthlang", "synthlang+gzip", "gzip"], help="Compression method to use")
    compression_parser.add_argument("--text-type", type=str, default="general", choices=["general", "technical", "creative", "code"], help="Type of text to use")
    compression_parser.add_argument("--sample-size", type=int, default=5, help="Number of samples to use")
    compression_parser.add_argument("--min-length", type=int, default=200, help="Minimum length of text samples")
    compression_parser.add_argument("--max-length", type=int, default=2000, help="Maximum length of text samples")
    compression_parser.add_argument("--use-real-samples", action="store_true", help="Use real-world samples instead of synthetic ones")
    compression_parser.set_defaults(func=run_compression_benchmark)
    
    # Latency benchmark
    latency_parser = subparsers.add_parser("latency", parents=[common_parser], help="Run latency benchmark")
    latency_parser.add_argument("--request-count", type=int, default=10, help="Number of requests to make")
    latency_parser.add_argument("--prompt-length", type=int, default=500, help="Length of prompts to use")
    latency_parser.add_argument("--concurrent-requests", type=int, default=1, help="Number of concurrent requests")
    latency_parser.set_defaults(func=run_latency_benchmark)
    
    # Throughput benchmark
    throughput_parser = subparsers.add_parser("throughput", parents=[common_parser], help="Run throughput benchmark")
    throughput_parser.add_argument("--duration", type=int, default=60, help="Duration of the benchmark in seconds")
    throughput_parser.add_argument("--concurrent-users", type=int, default=5, help="Number of concurrent users")
    throughput_parser.add_argument("--request-interval", type=int, default=1000, help="Interval between requests in milliseconds")
    throughput_parser.set_defaults(func=run_throughput_benchmark)
    
    # Cost benchmark
    cost_parser = subparsers.add_parser("cost", parents=[common_parser], help="Run cost benchmark")
    cost_parser.add_argument("--request-count", type=int, default=10, help="Number of requests to make")
    cost_parser.add_argument("--compression-enabled", action="store_true", help="Enable compression")
    cost_parser.add_argument("--caching-enabled", action="store_true", help="Enable caching")
    cost_parser.set_defaults(func=run_cost_benchmark)
    
    # Parse arguments
    args = parser.parse_args()
    
    if args.benchmark is None:
        parser.print_help()
        return
    
    # Run the selected benchmark
    args.func(args)


if __name__ == "__main__":
    main()