"""
Base benchmark scenario class.

This module defines the base class for benchmark scenarios, which provides
a common interface for all benchmark implementations.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass, field
import time
import uuid
from datetime import datetime


@dataclass
class BenchmarkResult:
    """
    Result of a benchmark execution.
    
    Attributes:
        scenario_name: Name of the benchmark scenario
        start_time: Time when the benchmark started (datetime or timestamp)
        end_time: Time when the benchmark completed
        duration_ms: Duration of the benchmark in milliseconds
        parameters: Parameters used for the benchmark
        metrics: Collected metrics from the benchmark
        metadata: Additional metadata about the benchmark
        id: Unique identifier for the benchmark result
    """
    scenario_name: str
    start_time: Union[datetime, float]
    end_time: Optional[datetime] = None
    duration_ms: Optional[float] = None
    parameters: Dict[str, Any] = field(default_factory=dict)
    metrics: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    def complete(self, metrics: Dict[str, Any]) -> None:
        """
        Mark the benchmark as complete and record metrics.
        
        Args:
            metrics: Metrics collected during the benchmark
        """
        self.end_time = datetime.now()
        
        # Calculate duration based on start_time type
        if isinstance(self.start_time, datetime):
            self.duration_ms = (self.end_time - self.start_time).total_seconds() * 1000
        elif isinstance(self.start_time, (int, float)):
            # If start_time is a timestamp (float or int)
            self.duration_ms = (datetime.now().timestamp() - self.start_time) * 1000
        else:
            # Default case
            self.duration_ms = 0
            
        self.metrics = metrics
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the benchmark result to a dictionary.
        
        Returns:
            Dictionary representation of the benchmark result
        """
        # Format start_time based on its type
        if isinstance(self.start_time, datetime):
            start_time_str = self.start_time.isoformat()
        else:
            # Convert timestamp to ISO format
            start_time_str = datetime.fromtimestamp(self.start_time).isoformat()
            
        return {
            "id": self.id,
            "scenario_name": self.scenario_name,
            "start_time": start_time_str,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_ms": self.duration_ms,
            "parameters": self.parameters,
            "metrics": self.metrics,
            "metadata": self.metadata
        }


class BenchmarkScenario(ABC):
    """
    Base class for benchmark scenarios.
    
    This abstract class defines the interface that all benchmark scenarios
    must implement, including setup, execution, and cleanup methods.
    """
    
    def __init__(self, name: str):
        """
        Initialize the benchmark scenario.
        
        Args:
            name: Name of the benchmark scenario
        """
        self.name = name
        self.parameters: Dict[str, Any] = {}
    
    @abstractmethod
    def setup(self, parameters: Dict[str, Any]) -> None:
        """
        Set up the benchmark with parameters.
        
        Args:
            parameters: Parameters for the benchmark
        """
        pass
    
    @abstractmethod
    def execute(self) -> BenchmarkResult:
        """
        Execute the benchmark and return results.
        
        Returns:
            BenchmarkResult containing metrics and metadata
        """
        pass
    
    def cleanup(self) -> None:
        """
        Clean up resources after benchmark execution.
        
        This method is called after the benchmark is complete to clean up
        any resources that were allocated during setup or execution.
        """
        pass
    
    def run(self, parameters: Dict[str, Any]) -> BenchmarkResult:
        """
        Run the benchmark with parameters.
        
        This method handles the complete benchmark lifecycle, including
        setup, execution, and cleanup.
        
        Args:
            parameters: Parameters for the benchmark
            
        Returns:
            BenchmarkResult containing metrics and metadata
        """
        try:
            self.setup(parameters)
            result = self.execute()
            return result
        finally:
            self.cleanup()