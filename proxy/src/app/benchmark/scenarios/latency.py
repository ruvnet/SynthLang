"""
Latency benchmark scenario.

This module provides a benchmark scenario for measuring response latency,
including end-to-end latency, time to first token, and processing time.
"""
from typing import Dict, Any, List, Optional
import time
import random
import logging
import asyncio
import statistics
from datetime import datetime

from app.benchmark.core.scenario import BenchmarkScenario, BenchmarkResult
from app.benchmark.scenarios.compression import get_sample_text, count_tokens
from app import llm_provider


logger = logging.getLogger(__name__)


class LatencyBenchmark(BenchmarkScenario):
    """
    Benchmark for measuring response latency.
    
    This benchmark measures various latency metrics for the SynthLang Proxy,
    including end-to-end latency, time to first token, and processing time.
    """
    
    def __init__(self, name: str):
        """
        Initialize the latency benchmark.
        
        Args:
            name: Name of the benchmark
        """
        super().__init__(name)
        self.texts = []
        self.compression_method = "synthlang"
        self.model = "gpt-4o"
        self.use_gzip = False
        self.iterations = 3
        self.concurrency = 1
    
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
        
        # Get number of iterations
        self.iterations = parameters.get("iterations", 3)
        
        # Get concurrency level
        self.concurrency = parameters.get("concurrency", 1)
        
        # Generate sample texts
        self.texts = [
            get_sample_text(text_type, 
                           min_length=parameters.get("min_length", 200),
                           max_length=parameters.get("max_length", 1000))
            for _ in range(self.iterations)
        ]
    
    async def _measure_latency(self, text: str, index: int) -> Dict[str, Any]:
        """
        Measure latency for a single request.
        
        Args:
            text: Text to use for the request
            index: Index of the request
            
        Returns:
            Dictionary of latency metrics
        """
        # Prepare the request
        messages = [{"role": "user", "content": text}]
        
        # Measure end-to-end latency
        start_time = time.time()
        
        try:
            # Make the request
            response = await llm_provider.complete_chat(
                model=self.model,
                messages=messages,
                user_id="benchmark_user",
                compression_method=self.compression_method,
                use_gzip=self.use_gzip
            )
            
            end_time = time.time()
            
            # Calculate latency
            latency_ms = (end_time - start_time) * 1000
            
            # Extract additional metrics from response if available
            time_to_first_token_ms = response.get("time_to_first_token_ms", None)
            processing_time_ms = response.get("processing_time_ms", None)
            
            # Count tokens
            prompt_tokens = response.get("usage", {}).get("prompt_tokens", count_tokens(text, self.model))
            completion_tokens = response.get("usage", {}).get("completion_tokens", 0)
            
            return {
                "request_index": index,
                "latency_ms": latency_ms,
                "time_to_first_token_ms": time_to_first_token_ms,
                "processing_time_ms": processing_time_ms,
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": prompt_tokens + completion_tokens,
                "success": True,
                "error": None
            }
        
        except Exception as e:
            end_time = time.time()
            latency_ms = (end_time - start_time) * 1000
            
            logger.error(f"Error in request {index}: {e}")
            
            return {
                "request_index": index,
                "latency_ms": latency_ms,
                "time_to_first_token_ms": None,
                "processing_time_ms": None,
                "prompt_tokens": count_tokens(text, self.model),
                "completion_tokens": 0,
                "total_tokens": count_tokens(text, self.model),
                "success": False,
                "error": str(e)
            }
    
    async def _run_concurrent_requests(self) -> List[Dict[str, Any]]:
        """
        Run concurrent requests and measure latency.
        
        Returns:
            List of latency metrics for each request
        """
        all_results = []
        
        for i in range(0, len(self.texts), self.concurrency):
            # Get a batch of texts
            batch_texts = self.texts[i:i+self.concurrency]
            batch_indices = list(range(i, i+len(batch_texts)))
            
            # Create tasks for concurrent execution
            tasks = [
                self._measure_latency(text, index)
                for text, index in zip(batch_texts, batch_indices)
            ]
            
            # Run tasks concurrently
            batch_results = await asyncio.gather(*tasks)
            all_results.extend(batch_results)
        
        return all_results
    
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
            
            # Run concurrent requests
            latency_results = loop.run_until_complete(self._run_concurrent_requests())
            
            # Calculate metrics
            successful_results = [r for r in latency_results if r["success"]]
            failed_results = [r for r in latency_results if not r["success"]]
            
            if successful_results:
                latencies = [r["latency_ms"] for r in successful_results]
                
                # Extract time to first token and processing time if available
                time_to_first_token = [r["time_to_first_token_ms"] for r in successful_results if r["time_to_first_token_ms"] is not None]
                processing_times = [r["processing_time_ms"] for r in successful_results if r["processing_time_ms"] is not None]
                
                # Calculate token metrics
                prompt_tokens = [r["prompt_tokens"] for r in successful_results]
                completion_tokens = [r["completion_tokens"] for r in successful_results]
                total_tokens = [r["total_tokens"] for r in successful_results]
                
                # Calculate tokens per second
                tokens_per_second = []
                for r in successful_results:
                    if r["latency_ms"] > 0:
                        tps = (r["total_tokens"] * 1000) / r["latency_ms"]
                        tokens_per_second.append(tps)
                
                # Prepare metrics
                metrics = {
                    "latency": {
                        "min_ms": min(latencies),
                        "max_ms": max(latencies),
                        "mean_ms": statistics.mean(latencies),
                        "median_ms": statistics.median(latencies),
                        "stddev_ms": statistics.stdev(latencies) if len(latencies) > 1 else 0,
                        "p90_ms": sorted(latencies)[int(len(latencies) * 0.9)] if len(latencies) >= 10 else max(latencies),
                        "p95_ms": sorted(latencies)[int(len(latencies) * 0.95)] if len(latencies) >= 20 else max(latencies),
                        "p99_ms": sorted(latencies)[int(len(latencies) * 0.99)] if len(latencies) >= 100 else max(latencies)
                    },
                    "tokens": {
                        "prompt_tokens_mean": statistics.mean(prompt_tokens),
                        "completion_tokens_mean": statistics.mean(completion_tokens),
                        "total_tokens_mean": statistics.mean(total_tokens),
                        "tokens_per_second_mean": statistics.mean(tokens_per_second) if tokens_per_second else 0
                    },
                    "success_rate": len(successful_results) / len(latency_results) * 100,
                    "request_count": len(latency_results),
                    "successful_requests": len(successful_results),
                    "failed_requests": len(failed_results)
                }
                
                # Add time to first token metrics if available
                if time_to_first_token:
                    metrics["time_to_first_token"] = {
                        "min_ms": min(time_to_first_token),
                        "max_ms": max(time_to_first_token),
                        "mean_ms": statistics.mean(time_to_first_token),
                        "median_ms": statistics.median(time_to_first_token)
                    }
                
                # Add processing time metrics if available
                if processing_times:
                    metrics["processing_time"] = {
                        "min_ms": min(processing_times),
                        "max_ms": max(processing_times),
                        "mean_ms": statistics.mean(processing_times),
                        "median_ms": statistics.median(processing_times)
                    }
                
                # Add detailed results
                metrics["detailed_results"] = latency_results
                
                # Complete the result
                result.complete(metrics)
            else:
                # No successful requests
                result.complete({
                    "success_rate": 0,
                    "request_count": len(latency_results),
                    "successful_requests": 0,
                    "failed_requests": len(failed_results),
                    "detailed_results": latency_results
                })
        
        except Exception as e:
            logger.error(f"Error executing latency benchmark: {e}")
            result.complete({
                "error": str(e),
                "success_rate": 0,
                "request_count": 0,
                "successful_requests": 0,
                "failed_requests": 0
            })
        
        return result