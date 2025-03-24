"""
Base classes for SynthLang compression.

This module provides the base classes for the compression system,
including the BaseCompressor abstract class and the CompressorRegistry.
"""
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, Optional, Type

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class CompressionResult:
    """
    Result of a compression or decompression operation.
    
    Attributes:
        success: Whether the operation was successful
        text: The resulting text (compressed or decompressed)
        metrics: Metrics about the operation
        error: Error message if the operation failed
    """
    success: bool
    text: str
    metrics: Dict[str, Any] = None
    error: Optional[str] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.metrics is None:
            self.metrics = {}


class BaseCompressor(ABC):
    """
    Base class for all compressors.
    
    This abstract class defines the interface for all compressors
    and provides helper methods for creating result objects.
    """
    
    @abstractmethod
    def compress(self, text: str) -> CompressionResult:
        """
        Compress text.
        
        Args:
            text: The text to compress
            
        Returns:
            CompressionResult with the compressed text and metrics
        """
        pass
    
    @abstractmethod
    def decompress(self, text: str) -> CompressionResult:
        """
        Decompress text.
        
        Args:
            text: The compressed text to decompress
            
        Returns:
            CompressionResult with the decompressed text and metrics
        """
        pass
    
    def _create_success_result(self, text: str, metrics: Dict[str, Any] = None) -> CompressionResult:
        """
        Create a successful CompressionResult.
        
        Args:
            text: The resulting text
            metrics: Metrics about the operation
            
        Returns:
            CompressionResult with success=True
        """
        return CompressionResult(
            success=True,
            text=text,
            metrics=metrics or {},
            error=None
        )
    
    def _create_error_result(self, text: str, error: str) -> CompressionResult:
        """
        Create a failed CompressionResult.
        
        Args:
            text: The original text
            error: Error message
            
        Returns:
            CompressionResult with success=False
        """
        return CompressionResult(
            success=False,
            text=text,
            metrics={},
            error=error
        )


class CompressorRegistry:
    """
    Registry for compressors.
    
    This class provides a registry for compressors, allowing them to be
    registered by name and retrieved later.
    """
    
    def __init__(self):
        """Initialize an empty registry."""
        self._compressors = {}
    
    def register(self, name: str, compressor_class: Type[BaseCompressor]) -> None:
        """
        Register a compressor class.
        
        Args:
            name: The name to register the compressor under
            compressor_class: The compressor class to register
        """
        self._compressors[name] = compressor_class
        logger.debug(f"Registered compressor: {name}")
    
    def unregister(self, name: str) -> None:
        """
        Unregister a compressor.
        
        Args:
            name: The name of the compressor to unregister
        """
        if name in self._compressors:
            del self._compressors[name]
            logger.debug(f"Unregistered compressor: {name}")
    
    def get(self, name: str) -> Optional[Type[BaseCompressor]]:
        """
        Get a compressor class by name.
        
        Args:
            name: The name of the compressor to get
            
        Returns:
            The compressor class, or None if not found
        """
        return self._compressors.get(name)
    
    def __contains__(self, name: str) -> bool:
        """
        Check if a compressor is registered.
        
        Args:
            name: The name of the compressor to check
            
        Returns:
            True if the compressor is registered, False otherwise
        """
        return name in self._compressors
    
    def get_all(self) -> Dict[str, Type[BaseCompressor]]:
        """
        Get all registered compressors.
        
        Returns:
            Dictionary of compressor names to compressor classes
        """
        return self._compressors.copy()