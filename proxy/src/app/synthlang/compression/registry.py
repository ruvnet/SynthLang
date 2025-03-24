"""
Registry for SynthLang compression strategies.

This module provides a registry for managing and accessing different
compression strategies.
"""
import logging
from typing import Dict, Type, Optional

from .base import BaseCompressor

# Configure logging
logger = logging.getLogger(__name__)


class CompressorRegistry:
    """
    Registry for compression strategies.
    
    This class provides a central registry for all compression strategies,
    allowing them to be registered, retrieved, and managed by name.
    """
    
    def __init__(self):
        """Initialize an empty registry."""
        self._compressors: Dict[str, Type[BaseCompressor]] = {}
    
    def register(self, name: str, compressor_class: Type[BaseCompressor]) -> None:
        """
        Register a compressor class with the given name.
        
        Args:
            name: The name to register the compressor under
            compressor_class: The compressor class to register
        """
        if not issubclass(compressor_class, BaseCompressor):
            raise TypeError(f"Compressor must be a subclass of BaseCompressor, got {compressor_class}")
        
        self._compressors[name] = compressor_class
        logger.debug(f"Registered compressor '{name}': {compressor_class.__name__}")
    
    def unregister(self, name: str) -> None:
        """
        Unregister a compressor by name.
        
        Args:
            name: The name of the compressor to unregister
        """
        if name in self._compressors:
            del self._compressors[name]
            logger.debug(f"Unregistered compressor '{name}'")
    
    def get(self, name: str) -> Optional[Type[BaseCompressor]]:
        """
        Get a compressor class by name.
        
        Args:
            name: The name of the compressor to get
            
        Returns:
            The compressor class, or None if not found
        """
        return self._compressors.get(name)
    
    def list(self) -> Dict[str, Type[BaseCompressor]]:
        """
        Get a dictionary of all registered compressors.
        
        Returns:
            A dictionary mapping names to compressor classes
        """
        return self._compressors.copy()
    
    def __contains__(self, name: str) -> bool:
        """
        Check if a compressor is registered with the given name.
        
        Args:
            name: The name to check
            
        Returns:
            True if a compressor is registered with the name, False otherwise
        """
        return name in self._compressors