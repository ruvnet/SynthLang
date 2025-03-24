"""
Configuration management for the benchmark framework.

This module provides functionality for managing benchmark configurations,
including loading, validating, and accessing configuration parameters.
"""
from typing import Dict, Any, Optional, List, Union
import json
import os
import logging
from dataclasses import dataclass, field


logger = logging.getLogger(__name__)


@dataclass
class BenchmarkConfig:
    """
    Configuration for the benchmark framework.
    
    Attributes:
        output_dir: Directory for storing benchmark results
        default_parameters: Default parameters for benchmarks
        scenarios: Configuration for specific scenarios
        metrics: Configuration for metrics collection
        reporting: Configuration for report generation
    """
    output_dir: str = "benchmark_results"
    default_parameters: Dict[str, Any] = field(default_factory=dict)
    scenarios: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    metrics: Dict[str, Any] = field(default_factory=dict)
    reporting: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the configuration to a dictionary.
        
        Returns:
            Dictionary representation of the configuration
        """
        return {
            "output_dir": self.output_dir,
            "default_parameters": self.default_parameters,
            "scenarios": self.scenarios,
            "metrics": self.metrics,
            "reporting": self.reporting
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BenchmarkConfig':
        """
        Create a configuration from a dictionary.
        
        Args:
            data: Dictionary containing configuration parameters
            
        Returns:
            BenchmarkConfig instance
        """
        return cls(
            output_dir=data.get("output_dir", "benchmark_results"),
            default_parameters=data.get("default_parameters", {}),
            scenarios=data.get("scenarios", {}),
            metrics=data.get("metrics", {}),
            reporting=data.get("reporting", {})
        )


class ConfigurationManager:
    """
    Manages benchmark configurations.
    
    This class provides functionality for loading, validating, and accessing
    benchmark configurations.
    """
    
    def __init__(self, config: Optional[Union[Dict[str, Any], BenchmarkConfig]] = None):
        """
        Initialize the configuration manager.
        
        Args:
            config: Optional initial configuration
        """
        if isinstance(config, BenchmarkConfig):
            self.config = config
        elif isinstance(config, dict):
            self.config = BenchmarkConfig.from_dict(config)
        else:
            self.config = BenchmarkConfig()
    
    def load_from_file(self, filepath: str) -> None:
        """
        Load configuration from a JSON file.
        
        Args:
            filepath: Path to the configuration file
            
        Raises:
            FileNotFoundError: If the file is not found
            ValueError: If the file contains invalid JSON
        """
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            self.config = BenchmarkConfig.from_dict(data)
            logger.info(f"Loaded configuration from {filepath}")
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {filepath}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in configuration file: {e}")
            raise ValueError(f"Invalid JSON in configuration file: {e}")
    
    def save_to_file(self, filepath: str) -> None:
        """
        Save configuration to a JSON file.
        
        Args:
            filepath: Path to save the configuration file
        """
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(self.config.to_dict(), f, indent=2)
        
        logger.info(f"Saved configuration to {filepath}")
    
    def get_scenario_config(self, scenario_name: str) -> Dict[str, Any]:
        """
        Get configuration for a specific scenario.
        
        Args:
            scenario_name: Name of the scenario
            
        Returns:
            Configuration for the scenario, or an empty dict if not found
        """
        return self.config.scenarios.get(scenario_name, {})
    
    def set_scenario_config(self, scenario_name: str, config: Dict[str, Any]) -> None:
        """
        Set configuration for a specific scenario.
        
        Args:
            scenario_name: Name of the scenario
            config: Configuration for the scenario
        """
        self.config.scenarios[scenario_name] = config
    
    def get_default_parameters(self) -> Dict[str, Any]:
        """
        Get default parameters for benchmarks.
        
        Returns:
            Default parameters
        """
        return self.config.default_parameters
    
    def set_default_parameters(self, parameters: Dict[str, Any]) -> None:
        """
        Set default parameters for benchmarks.
        
        Args:
            parameters: Default parameters
        """
        self.config.default_parameters = parameters
    
    def get_output_dir(self) -> str:
        """
        Get the output directory for benchmark results.
        
        Returns:
            Output directory path
        """
        return self.config.output_dir
    
    def set_output_dir(self, output_dir: str) -> None:
        """
        Set the output directory for benchmark results.
        
        Args:
            output_dir: Output directory path
        """
        self.config.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def get_metrics_config(self) -> Dict[str, Any]:
        """
        Get configuration for metrics collection.
        
        Returns:
            Metrics configuration
        """
        return self.config.metrics
    
    def get_reporting_config(self) -> Dict[str, Any]:
        """
        Get configuration for report generation.
        
        Returns:
            Reporting configuration
        """
        return self.config.reporting
    
    def validate(self) -> List[str]:
        """
        Validate the configuration.
        
        Returns:
            List of validation errors, or an empty list if valid
        """
        errors = []
        
        # Check output directory
        if not self.config.output_dir:
            errors.append("Output directory is not specified")
        
        # Check scenario configurations
        for scenario_name, scenario_config in self.config.scenarios.items():
            if not isinstance(scenario_config, dict):
                errors.append(f"Invalid configuration for scenario {scenario_name}: must be a dictionary")
        
        return errors
    
    def merge(self, other: Union[Dict[str, Any], BenchmarkConfig]) -> None:
        """
        Merge another configuration into this one.
        
        Args:
            other: Configuration to merge
        """
        if isinstance(other, BenchmarkConfig):
            other_dict = other.to_dict()
        else:
            other_dict = other
        
        # Merge output directory if specified
        if "output_dir" in other_dict and other_dict["output_dir"]:
            self.config.output_dir = other_dict["output_dir"]
        
        # Merge default parameters
        if "default_parameters" in other_dict:
            self.config.default_parameters.update(other_dict["default_parameters"])
        
        # Merge scenario configurations
        if "scenarios" in other_dict:
            for scenario_name, scenario_config in other_dict["scenarios"].items():
                if scenario_name in self.config.scenarios:
                    self.config.scenarios[scenario_name].update(scenario_config)
                else:
                    self.config.scenarios[scenario_name] = scenario_config
        
        # Merge metrics configuration
        if "metrics" in other_dict:
            self.config.metrics.update(other_dict["metrics"])
        
        # Merge reporting configuration
        if "reporting" in other_dict:
            self.config.reporting.update(other_dict["reporting"])