"""
Factory for creating LLM provider instances.

This module provides a factory class for creating LLM provider instances.
"""
import logging
from typing import Dict, Type, List

from .base import BaseLLMProvider

# Configure logging
logger = logging.getLogger(__name__)


class LLMProviderFactory:
    """
    Factory class for creating LLM provider instances.
    """
    
    _providers: Dict[str, Type[BaseLLMProvider]] = {}
    
    @classmethod
    def register_provider(cls, name: str, provider_class: Type[BaseLLMProvider]):
        """
        Register a new provider class.
        
        Args:
            name: The name of the provider
            provider_class: The provider class
        """
        cls._providers[name] = provider_class
        logger.info(f"Registered LLM provider: {name}")
    
    @classmethod
    def create_provider(cls, name: str) -> BaseLLMProvider:
        """
        Create a provider instance by name.
        
        Args:
            name: The name of the provider
            
        Returns:
            An instance of the provider
            
        Raises:
            ValueError: If the provider is not registered
        """
        if name not in cls._providers:
            raise ValueError(f"LLM provider '{name}' is not registered")
        
        provider_class = cls._providers[name]
        return provider_class()
    
    @classmethod
    def get_available_providers(cls) -> List[str]:
        """
        Get a list of available provider names.
        
        Returns:
            A list of provider names
        """
        return list(cls._providers.keys())