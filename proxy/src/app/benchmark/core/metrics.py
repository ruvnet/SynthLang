"""
Metrics collection for the benchmark framework.

This module provides functionality for collecting, analyzing, and exporting
performance metrics from benchmark executions.
"""
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, field
import time
import json
import statistics
import csv
import io
from datetime import datetime


@dataclass
class MetricStatistics:
    """
    Statistical analysis of a metric.
    
    Attributes:
        count: Number of samples
        min: Minimum value
        max: Maximum value
        mean: Mean value
        median: Median value
        stddev: Standard deviation
        p90: 90th percentile
        p95: 95th percentile
        p99: 99th percentile
    """
    count: int
    min: float
    max: float
    mean: float
    median: float
    stddev: float
    p90: float
    p95: float
    p99: float


@dataclass
class MetricSample:
    """
    A single metric sample.
    
    Attributes:
        value: The metric value
        timestamp: When the metric was recorded
        tags: Optional tags for categorizing the metric
    """
    value: float
    timestamp: datetime = field(default_factory=datetime.now)
    tags: Dict[str, str] = field(default_factory=dict)


@dataclass
class CompressionMetrics:
    """
    Metrics for compression benchmarks.
    
    Attributes:
        original_size: Size of the original text in bytes
        compressed_size: Size of the compressed text in bytes
        compression_ratio: Ratio of compressed size to original size
        original_tokens: Number of tokens in the original text
        compressed_tokens: Number of tokens in the compressed text
        token_reduction: Percentage reduction in tokens
        compression_time_ms: Time taken to compress in milliseconds
    """
    original_size: int
    compressed_size: int
    compression_ratio: float
    original_tokens: int
    compressed_tokens: int
    token_reduction: float
    compression_time_ms: float


@dataclass
class TokenReductionMetrics:
    """
    Metrics for token reduction analysis.
    
    Attributes:
        model: The LLM model used for token counting
        original_tokens: Number of tokens in the original text
        compressed_tokens: Number of tokens in the compressed text
        token_reduction: Percentage reduction in tokens
        token_cost_original: Estimated cost of the original tokens
        token_cost_compressed: Estimated cost of the compressed tokens
        cost_savings: Percentage cost savings
    """
    model: str
    original_tokens: int
    compressed_tokens: int
    token_reduction: float
    token_cost_original: float
    token_cost_compressed: float
    cost_savings: float


class MetricsCollector:
    """
    Collects and processes performance metrics.
    
    This class provides functionality for recording, analyzing, and exporting
    metrics from benchmark executions.
    """
    
    def __init__(self):
        """Initialize the metrics collector."""
        self._metrics: Dict[str, List[MetricSample]] = {}
        self._latency_metrics: Dict[str, List[MetricSample]] = {}
        self._token_metrics: List[Dict[str, Any]] = []
    
    def record_metric(self, name: str, value: float, tags: Optional[Dict[str, str]] = None) -> None:
        """
        Record a single metric value with optional tags.
        
        Args:
            name: Name of the metric
            value: Value of the metric
            tags: Optional tags for categorizing the metric
        """
        if name not in self._metrics:
            self._metrics[name] = []
        
        self._metrics[name].append(MetricSample(
            value=value,
            tags=tags or {}
        ))
    
    def record_latency(self, operation: str, duration_ms: float, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Record a latency measurement for an operation.
        
        Args:
            operation: Name of the operation
            duration_ms: Duration of the operation in milliseconds
            metadata: Optional metadata about the operation
        """
        if operation not in self._latency_metrics:
            self._latency_metrics[operation] = []
        
        tags = {}
        if metadata:
            # Convert metadata to string tags for categorization
            for key, value in metadata.items():
                if isinstance(value, (str, int, float, bool)):
                    tags[key] = str(value)
        
        self._latency_metrics[operation].append(MetricSample(
            value=duration_ms,
            tags=tags
        ))
    
    def record_token_counts(self, original: int, compressed: int, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Record token counts before and after compression.
        
        Args:
            original: Number of tokens in the original text
            compressed: Number of tokens in the compressed text
            metadata: Optional metadata about the token counts
        """
        record = {
            "original_tokens": original,
            "compressed_tokens": compressed,
            "reduction_percentage": ((original - compressed) / original) * 100 if original > 0 else 0,
            "timestamp": datetime.now().isoformat()
        }
        
        if metadata:
            record.update(metadata)
        
        self._token_metrics.append(record)
    
    def get_statistics(self, metric_name: str, tags: Optional[Dict[str, str]] = None) -> Optional[MetricStatistics]:
        """
        Get statistical analysis for a metric.
        
        Args:
            metric_name: Name of the metric
            tags: Optional tags for filtering metrics
            
        Returns:
            Statistical analysis of the metric, or None if no data is available
        """
        if metric_name not in self._metrics:
            return None
        
        # Filter by tags if provided
        values = []
        for sample in self._metrics[metric_name]:
            if tags is None or all(sample.tags.get(k) == v for k, v in tags.items()):
                values.append(sample.value)
        
        if not values:
            return None
        
        # Calculate statistics
        sorted_values = sorted(values)
        count = len(values)
        
        return MetricStatistics(
            count=count,
            min=min(values),
            max=max(values),
            mean=statistics.mean(values),
            median=statistics.median(values),
            stddev=statistics.stdev(values) if count > 1 else 0,
            p90=sorted_values[int(count * 0.9)] if count > 10 else sorted_values[-1],
            p95=sorted_values[int(count * 0.95)] if count > 20 else sorted_values[-1],
            p99=sorted_values[int(count * 0.99)] if count > 100 else sorted_values[-1]
        )
    
    def get_token_reduction_summary(self) -> Dict[str, Any]:
        """
        Get a summary of token reduction metrics.
        
        Returns:
            Summary statistics for token reduction
        """
        if not self._token_metrics:
            return {
                "count": 0,
                "average_reduction_percentage": 0,
                "total_original_tokens": 0,
                "total_compressed_tokens": 0
            }
        
        total_original = sum(m["original_tokens"] for m in self._token_metrics)
        total_compressed = sum(m["compressed_tokens"] for m in self._token_metrics)
        reductions = [m["reduction_percentage"] for m in self._token_metrics]
        
        return {
            "count": len(self._token_metrics),
            "average_reduction_percentage": statistics.mean(reductions),
            "median_reduction_percentage": statistics.median(reductions),
            "min_reduction_percentage": min(reductions),
            "max_reduction_percentage": max(reductions),
            "total_original_tokens": total_original,
            "total_compressed_tokens": total_compressed,
            "overall_reduction_percentage": ((total_original - total_compressed) / total_original) * 100 if total_original > 0 else 0
        }
    
    def export_metrics(self, format: str = "json") -> str:
        """
        Export collected metrics in specified format.
        
        Args:
            format: Output format ("json" or "csv")
            
        Returns:
            String representation of the metrics in the specified format
        """
        if format.lower() == "json":
            data = {
                "metrics": {name: [s.__dict__ for s in samples] for name, samples in self._metrics.items()},
                "latency": {name: [s.__dict__ for s in samples] for name, samples in self._latency_metrics.items()},
                "token_metrics": self._token_metrics,
                "summaries": {
                    "token_reduction": self.get_token_reduction_summary()
                }
            }
            return json.dumps(data, default=str, indent=2)
        
        elif format.lower() == "csv":
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write metrics
            writer.writerow(["Type", "Name", "Value", "Timestamp", "Tags"])
            
            for name, samples in self._metrics.items():
                for sample in samples:
                    writer.writerow([
                        "metric",
                        name,
                        sample.value,
                        sample.timestamp,
                        json.dumps(sample.tags)
                    ])
            
            for name, samples in self._latency_metrics.items():
                for sample in samples:
                    writer.writerow([
                        "latency",
                        name,
                        sample.value,
                        sample.timestamp,
                        json.dumps(sample.tags)
                    ])
            
            # Add a separator
            writer.writerow([])
            
            # Write token metrics
            if self._token_metrics:
                # Get all possible keys
                keys = set()
                for metric in self._token_metrics:
                    keys.update(metric.keys())
                
                writer.writerow(["Token Metrics"])
                writer.writerow(list(keys))
                
                for metric in self._token_metrics:
                    writer.writerow([metric.get(key, "") for key in keys])
            
            return output.getvalue()
        
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def reset(self) -> None:
        """Reset all collected metrics."""
        self._metrics.clear()
        self._latency_metrics.clear()
        self._token_metrics.clear()