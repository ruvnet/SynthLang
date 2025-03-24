"""
Throughput benchmark scenario.

This module provides a benchmark scenario for measuring system throughput,
including requests per second, tokens per second, and resource utilization.
"""
from typing import Dict, Any, List, Optional, Tuple
import time
import random
import logging
import asyncio
import statistics
import threading
import psutil
from datetime import datetime

from app.benchmark.core.scenario import BenchmarkScenario, BenchmarkResult
from app.benchmark.scenarios.compression import get_sample_text, count_tokens
from app import llm_provider


logger = logging.getLogger(__name__)


class ResourceMonitor(threading.Thread):
    """
    Monitor system resource utilization during benchmark execution.
    
    This class runs in a separate thread and periodically collects CPU, memory,
    and network usage statistics.
    """
    
    def __init__(self, interval: float = 0.5):
        """
        Initialize the resource monitor.
        
        Args:
            interval: Sampling interval in seconds
        """
        super().__init__()
        self.interval = interval
        self.running = False
        self.cpu_percent = []
        self.memory_percent = []
        self.memory_used_mb = []
        self.network_sent_bytes = []
        self.network_recv_bytes = []
        self.start_time = None
        self.end_time = None
    
    def run(self):
        """Run the resource monitor thread."""
        self.running = True
        self.start_time = time.time()
        
        # Get initial network counters
        net_io_start = psutil.net_io_counters()
        last_sent = net_io_start.bytes_sent
        last_recv = net_io_start.bytes_recv
        
        while self.running:
            # Collect CPU usage
            self.cpu_percent.append(psutil.cpu_percent(interval=None))
            
            # Collect memory usage
            memory = psutil.virtual_memory()
            self.memory_percent.append(memory.percent)
            self.memory_used_mb.append(memory.used / (1024 * 1024))  # Convert to MB
            
            # Collect network usage (delta since last sample)
            net_io = psutil.net_io_counters()
            self.network_sent_bytes.append(net_io.bytes_sent - last_sent)
            self.network_recv_bytes.append(net_io.bytes_recv - last_recv)
            last_sent = net_io.bytes_sent
            last_recv = net_io.bytes_recv
            
            # Sleep for the specified interval
            time.sleep(self.interval)
        
        self.end_time = time.time()
    
    def stop(self):
        """Stop the resource monitor thread."""
        self.running = False
        self.join()
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get collected resource metrics.
        
        Returns:
            Dictionary of resource metrics
        """
        duration = self.end_time - self.start_time if self.end_time else 0
        
        # Calculate network throughput in KB/s
        net_sent_kbps = sum(self.network_sent_bytes) / 1024 / duration if duration > 0 else 0
        net_recv_kbps = sum(self.network_recv_bytes) / 1024 / duration if duration > 0 else 0
        
        return {
            "cpu": {
                "min_percent": min(self.cpu_percent) if self.cpu_percent else 0,
                "max_percent": max(self.cpu_percent) if self.cpu_percent else 0,
                "mean_percent": statistics.mean(self.cpu_percent) if self.cpu_percent else 0,
                "samples": len(self.cpu_percent)
            },
            "memory": {
                "min_percent": min(self.memory_percent) if self.memory_percent else 0,
                "max_percent": max(self.memory_percent) if self.memory_percent else 0,
                "mean_percent": statistics.mean(self.memory_percent) if self.memory_percent else 0,
                "min_used_mb": min(self.memory_used_mb) if self.memory_used_mb else 0,
                "max_used_mb": max(self.memory_used_mb) if self.memory_used_mb else 0,
                "mean_used_mb": statistics.mean(self.memory_used_mb) if self.memory_used_mb else 0,
                "samples": len(self.memory_percent)
            },
            "network": {
                "sent_kb": sum(self.network_sent_bytes) / 1024,
                "recv_kb": sum(self.network_recv_bytes) / 1024,
                "sent_kbps": net_sent_kbps,
                "recv_kbps": net_recv_kbps,
                "samples": len(self.network_sent_bytes)
            },
            "duration_seconds": duration
        }


class ThroughputBenchmark(BenchmarkScenario):
    """
    Benchmark for measuring system throughput.
    
    This benchmark measures the throughput of the SynthLang Proxy under load,
    including requests per second, tokens per second, and resource utilization.
    """
    
    def __init__(self, name: str):
        """
        Initialize the throughput benchmark.
        
        Args:
            name: Name of the benchmark
        """
        super().__init__(name)
        self.texts = []
        self.compression_method = "synthlang"
        self.model = "gpt-4o"
        self.use_gzip = False
        self.duration_seconds = 10
        self.concurrency = 5
        self.resource_monitor = None
    
    def setup(self, parameters: Dict[str, Any]) -> None:
        """
        Set up the benchmark with parameters.
        
        Args:
            parameters: Parameters for the benchmark
        """
        self.parameters = parameters
        
        # Get compression method
        self.compression_method = parameters.get("compression_method", "synthlang")
        
        # Get model
        self.model = parameters.get("model", "gpt-4o")
        
        # Get text type
        text_type = parameters.get("text_type", "general")
        
        # Get use_gzip flag
        self.use_gzip = parameters.get("use_gzip", False)
        
        # Get duration
        self.duration_seconds = parameters.get("duration_seconds", 10)
        
        # Get concurrency level
        self.concurrency = parameters.get("concurrency", 5)
        
        # Generate sample texts (one per concurrent request)
        self.texts = [
            get_sample_text(text_type, 
                           min_length=parameters.get("min_length", 200),
                           max_length=parameters.get("max_length", 1000))
            for _ in range(self.concurrency)
        ]
    
    async def _process_request(self, text: str, request_id: int) -> Dict[str, Any]:
        """
        Process a single request and measure performance.
        
        Args:
            text: Text to use for the request
            request_id: Unique identifier for the request
            
        Returns:
            Dictionary of performance metrics
        """
        # Prepare the request
        messages = [{"role": "user", "content": text}]
        
        # Measure request time
        start_time = time.time()
        
        try:
            # Make the request
            response = await llm_provider.complete_chat(
                model=self.model,
                messages=messages,
                user_id=f"benchmark_user_{request_id}",
                compression_method=self.compression_method,
                use_gzip=self.use_gzip
            )
            
            end_time = time.time()
            
            # Calculate metrics
            latency_ms = (end_time - start_time) * 1000
            
            # Count tokens
            prompt_tokens = response.get("usage", {}).get("prompt_tokens", count_tokens(text, self.model))
            completion_tokens = response.get("usage", {}).get("completion_tokens", 0)
            total_tokens = prompt_tokens + completion_tokens
            
            return {
                "request_id": request_id,
                "start_time": start_time,
                "end_time": end_time,
                "latency_ms": latency_ms,
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens,
                "success": True,
                "error": None
            }
        
        except Exception as e:
            end_time = time.time()
            latency_ms = (end_time - start_time) * 1000
            
            logger.error(f"Error in request {request_id}: {e}")
            
            return {
                "request_id": request_id,
                "start_time": start_time,
                "end_time": end_time,
                "latency_ms": latency_ms,
                "prompt_tokens": count_tokens(text, self.model),
                "completion_tokens": 0,
                "total_tokens": count_tokens(text, self.model),
                "success": False,
                "error": str(e)
            }
    
    async def _run_load_test(self) -> Tuple[List[Dict[str, Any]], float]:
        """
        Run a load test with concurrent requests.
        
        Returns:
            Tuple of (request_results, total_duration)
        """
        all_results = []
        request_id = 0
        start_time = time.time()
        end_time = start_time + self.duration_seconds
        
        # Start resource monitoring
        self.resource_monitor = ResourceMonitor()
        self.resource_monitor.start()
        
        try:
            # Keep sending requests until the duration is reached
            while time.time() < end_time:
                # Create tasks for concurrent execution
                tasks = []
                for i in range(self.concurrency):
                    text = self.texts[i % len(self.texts)]
                    tasks.append(self._process_request(text, request_id))
                    request_id += 1
                
                # Run tasks concurrently
                batch_results = await asyncio.gather(*tasks)
                all_results.extend(batch_results)
        
        finally:
            # Stop resource monitoring
            if self.resource_monitor:
                self.resource_monitor.stop()
        
        total_duration = time.time() - start_time
        return all_results, total_duration
    
    def execute(self) -> BenchmarkResult:
        """
        Execute the benchmark and return results.
        
        Returns:
            BenchmarkResult containing metrics and metadata
        """
        # Create result object
        result = BenchmarkResult(
            scenario_name=self.name,
            start_time=datetime.now(),
            parameters=self.parameters
        )
        
        # Run the benchmark
        try:
            # Create event loop if needed
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            # Run load test
            request_results, total_duration = loop.run_until_complete(self._run_load_test())
            
            # Calculate metrics
            successful_results = [r for r in request_results if r["success"]]
            failed_results = [r for r in request_results if not r["success"]]
            
            # Calculate throughput metrics
            requests_per_second = len(request_results) / total_duration if total_duration > 0 else 0
            successful_requests_per_second = len(successful_results) / total_duration if total_duration > 0 else 0
            
            # Calculate token metrics
            total_prompt_tokens = sum(r["prompt_tokens"] for r in request_results)
            total_completion_tokens = sum(r["completion_tokens"] for r in successful_results)
            total_tokens = total_prompt_tokens + total_completion_tokens
            
            tokens_per_second = total_tokens / total_duration if total_duration > 0 else 0
            
            # Calculate latency metrics
            if successful_results:
                latencies = [r["latency_ms"] for r in successful_results]
                
                latency_metrics = {
                    "min_ms": min(latencies),
                    "max_ms": max(latencies),
                    "mean_ms": statistics.mean(latencies),
                    "median_ms": statistics.median(latencies),
                    "stddev_ms": statistics.stdev(latencies) if len(latencies) > 1 else 0,
                    "p90_ms": sorted(latencies)[int(len(latencies) * 0.9)] if len(latencies) >= 10 else max(latencies),
                    "p95_ms": sorted(latencies)[int(len(latencies) * 0.95)] if len(latencies) >= 20 else max(latencies),
                    "p99_ms": sorted(latencies)[int(len(latencies) * 0.99)] if len(latencies) >= 100 else max(latencies)
                }
            else:
                latency_metrics = {
                    "min_ms": 0,
                    "max_ms": 0,
                    "mean_ms": 0,
                    "median_ms": 0,
                    "stddev_ms": 0,
                    "p90_ms": 0,
                    "p95_ms": 0,
                    "p99_ms": 0
                }
            
            # Get resource metrics
            resource_metrics = self.resource_monitor.get_metrics() if self.resource_monitor else {}
            
            # Prepare metrics
            metrics = {
                "throughput": {
                    "requests_per_second": requests_per_second,
                    "successful_requests_per_second": successful_requests_per_second,
                    "tokens_per_second": tokens_per_second,
                    "prompt_tokens_per_second": total_prompt_tokens / total_duration if total_duration > 0 else 0,
                    "completion_tokens_per_second": total_completion_tokens / total_duration if total_duration > 0 else 0
                },
                "latency": latency_metrics,
                "tokens": {
                    "total_prompt_tokens": total_prompt_tokens,
                    "total_completion_tokens": total_completion_tokens,
                    "total_tokens": total_tokens,
                    "average_tokens_per_request": total_tokens / len(request_results) if request_results else 0
                },
                "requests": {
                    "total": len(request_results),
                    "successful": len(successful_results),
                    "failed": len(failed_results),
                    "success_rate": len(successful_results) / len(request_results) * 100 if request_results else 0
                },
                "duration_seconds": total_duration,
                "resources": resource_metrics
            }
            
            # Complete the result
            result.complete(metrics)
        
        except Exception as e:
            logger.error(f"Error executing throughput benchmark: {e}")
            result.complete({
                "error": str(e),
                "requests": {
                    "total": 0,
                    "successful": 0,
                    "failed": 0,
                    "success_rate": 0
                },
                "duration_seconds": 0
            })
        
        return result
    
    def cleanup(self) -> None:
        """Clean up resources after benchmark execution."""
        # Ensure resource monitor is stopped
        if self.resource_monitor and self.resource_monitor.is_alive():
            self.resource_monitor.stop()