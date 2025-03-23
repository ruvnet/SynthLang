"""
Cost benchmark scenario.

This module provides a benchmark scenario for analyzing cost implications,
including token usage, cost savings, and ROI calculations.
"""
from typing import Dict, Any, List, Optional
import time
import random
import logging
import json
from datetime import datetime
from pathlib import Path

from app.benchmark.core.scenario import BenchmarkScenario, BenchmarkResult
from app.benchmark.scenarios.compression import (
    get_sample_text, count_tokens, MODEL_TOKEN_COSTS, CompressionMetrics
)
from app.synthlang import compress_prompt


logger = logging.getLogger(__name__)


# Cost projection periods in months
PROJECTION_PERIODS = [1, 3, 6, 12, 24, 36]


class CostBenchmark(BenchmarkScenario):
    """
    Benchmark for analyzing cost implications.
    
    This benchmark analyzes the cost implications of different compression methods,
    including token usage, cost savings, and ROI calculations.
    """
    
    def __init__(self, name: str):
        """
        Initialize the cost benchmark.
        
        Args:
            name: Name of the benchmark
        """
        super().__init__(name)
        self.texts = []
        self.compression_methods = ["none", "synthlang", "synthlang+gzip"]
        self.model = "gpt-4o"
        self.monthly_request_volume = 10000
        self.average_prompt_tokens = 1000
        self.average_completion_tokens = 500
    
    def setup(self, parameters: Dict[str, Any]) -> None:
        """
        Set up the benchmark with parameters.
        
        Args:
            parameters: Parameters for the benchmark
        """
        self.parameters = parameters
        
        # Get compression methods to test
        self.compression_methods = parameters.get("compression_methods", ["none", "synthlang", "synthlang+gzip"])
        
        # Get model for token counting and cost calculation
        self.model = parameters.get("model", "gpt-4o")
        
        # Get text type
        text_type = parameters.get("text_type", "general")
        
        # Get sample size
        sample_size = parameters.get("sample_size", 5)
        
        # Get monthly request volume
        self.monthly_request_volume = parameters.get("monthly_request_volume", 10000)
        
        # Get average token counts
        self.average_prompt_tokens = parameters.get("average_prompt_tokens", 1000)
        self.average_completion_tokens = parameters.get("average_completion_tokens", 500)
        
        # Generate sample texts
        self.texts = [
            get_sample_text(text_type, 
                           min_length=parameters.get("min_length", 500),
                           max_length=parameters.get("max_length", 2000))
            for _ in range(sample_size)
        ]
        
        # Load real-world samples if specified
        if parameters.get("use_real_samples", False):
            samples_dir = Path(__file__).parent.parent / "data" / "samples"
            if samples_dir.exists():
                sample_files = list(samples_dir.glob("*.json"))
                if sample_files:
                    # Load up to sample_size files
                    for file_path in random.sample(sample_files, min(sample_size, len(sample_files))):
                        try:
                            with open(file_path, 'r') as f:
                                sample = json.load(f)
                                if "text" in sample:
                                    self.texts.append(sample["text"])
                        except Exception as e:
                            logger.error(f"Error loading sample file {file_path}: {e}")
    
    def _analyze_compression_method(self, method: str) -> Dict[str, Any]:
        """
        Analyze a compression method for cost implications.
        
        Args:
            method: Compression method to analyze
            
        Returns:
            Dictionary of cost metrics
        """
        use_gzip = "gzip" in method
        use_synthlang = "synthlang" in method
        
        total_original_tokens = 0
        total_compressed_tokens = 0
        compression_metrics_list = []
        
        for text in self.texts:
            # Count original tokens
            original_tokens = count_tokens(text, self.model)
            total_original_tokens += original_tokens
            
            # Apply compression if needed
            if use_synthlang:
                start_time = time.time()
                compressed_text = compress_prompt(text, use_gzip=use_gzip)
                compression_time = (time.time() - start_time) * 1000  # in milliseconds
            elif use_gzip:
                start_time = time.time()
                import gzip
                import base64
                compressed_bytes = gzip.compress(text.encode('utf-8'))
                compressed_text = f"gz:{base64.b64encode(compressed_bytes).decode('utf-8')}"
                compression_time = (time.time() - start_time) * 1000  # in milliseconds
            else:
                compressed_text = text
                compression_time = 0
            
            # Count compressed tokens
            compressed_tokens = count_tokens(compressed_text, self.model)
            total_compressed_tokens += compressed_tokens
            
            # Calculate compression metrics
            original_size = len(text.encode('utf-8'))
            compressed_size = len(compressed_text.encode('utf-8'))
            compression_ratio = compressed_size / original_size if original_size > 0 else 1.0
            token_reduction = (original_tokens - compressed_tokens) / original_tokens if original_tokens > 0 else 0.0
            
            compression_metrics = CompressionMetrics(
                original_size=original_size,
                compressed_size=compressed_size,
                compression_ratio=compression_ratio,
                original_tokens=original_tokens,
                compressed_tokens=compressed_tokens,
                token_reduction=token_reduction * 100,  # as percentage
                compression_time_ms=compression_time
            )
            
            compression_metrics_list.append(compression_metrics)
        
        # Calculate average metrics
        avg_token_reduction = (total_original_tokens - total_compressed_tokens) / total_original_tokens if total_original_tokens > 0 else 0.0
        
        # Calculate cost metrics
        token_cost_per_1k = MODEL_TOKEN_COSTS.get(self.model, 0.01)  # Default to gpt-4o cost
        
        # Calculate monthly costs
        monthly_prompt_tokens_original = self.monthly_request_volume * self.average_prompt_tokens
        monthly_prompt_tokens_compressed = monthly_prompt_tokens_original * (1 - avg_token_reduction)
        
        monthly_completion_tokens = self.monthly_request_volume * self.average_completion_tokens
        
        monthly_cost_original = (monthly_prompt_tokens_original / 1000) * token_cost_per_1k + (monthly_completion_tokens / 1000) * token_cost_per_1k
        monthly_cost_compressed = (monthly_prompt_tokens_compressed / 1000) * token_cost_per_1k + (monthly_completion_tokens / 1000) * token_cost_per_1k
        
        monthly_savings = monthly_cost_original - monthly_cost_compressed
        savings_percentage = (monthly_savings / monthly_cost_original) * 100 if monthly_cost_original > 0 else 0
        
        # Calculate projected savings for different periods
        projected_savings = {
            f"{period}_month": monthly_savings * period
            for period in PROJECTION_PERIODS
        }
        
        return {
            "method": method,
            "token_reduction_percentage": avg_token_reduction * 100,  # as percentage
            "monthly_prompt_tokens_original": monthly_prompt_tokens_original,
            "monthly_prompt_tokens_compressed": monthly_prompt_tokens_compressed,
            "monthly_completion_tokens": monthly_completion_tokens,
            "monthly_cost_original_usd": monthly_cost_original,
            "monthly_cost_compressed_usd": monthly_cost_compressed,
            "monthly_savings_usd": monthly_savings,
            "savings_percentage": savings_percentage,
            "projected_savings_usd": projected_savings,
            "sample_metrics": [vars(m) for m in compression_metrics_list],
            "sample_count": len(self.texts)
        }
    
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
        
        try:
            # Analyze each compression method
            method_results = {}
            for method in self.compression_methods:
                method_results[method] = self._analyze_compression_method(method)
            
            # Find the best method based on savings
            best_method = max(
                self.compression_methods,
                key=lambda m: method_results[m]["monthly_savings_usd"]
            )
            
            # Calculate ROI metrics
            implementation_cost_usd = self.parameters.get("implementation_cost_usd", 5000)
            monthly_maintenance_cost_usd = self.parameters.get("monthly_maintenance_cost_usd", 500)
            
            best_monthly_savings = method_results[best_method]["monthly_savings_usd"]
            
            # Calculate payback period in months
            if best_monthly_savings > monthly_maintenance_cost_usd:
                net_monthly_savings = best_monthly_savings - monthly_maintenance_cost_usd
                payback_period_months = implementation_cost_usd / net_monthly_savings if net_monthly_savings > 0 else float('inf')
            else:
                payback_period_months = float('inf')
            
            # Calculate 3-year ROI
            three_year_savings = best_monthly_savings * 36
            three_year_maintenance = monthly_maintenance_cost_usd * 36
            three_year_costs = implementation_cost_usd + three_year_maintenance
            three_year_roi_percentage = ((three_year_savings - three_year_costs) / three_year_costs) * 100 if three_year_costs > 0 else 0
            
            # Prepare metrics
            metrics = {
                "compression_methods": method_results,
                "best_method": best_method,
                "best_method_savings_percentage": method_results[best_method]["savings_percentage"],
                "roi": {
                    "implementation_cost_usd": implementation_cost_usd,
                    "monthly_maintenance_cost_usd": monthly_maintenance_cost_usd,
                    "payback_period_months": payback_period_months,
                    "three_year_savings_usd": three_year_savings,
                    "three_year_costs_usd": three_year_costs,
                    "three_year_roi_percentage": three_year_roi_percentage
                },
                "model": self.model,
                "token_cost_per_1k": MODEL_TOKEN_COSTS.get(self.model, 0.01),
                "monthly_request_volume": self.monthly_request_volume
            }
            
            # Complete the result
            result.complete(metrics)
        
        except Exception as e:
            logger.error(f"Error executing cost benchmark: {e}")
            result.complete({
                "error": str(e)
            })
        
        return result