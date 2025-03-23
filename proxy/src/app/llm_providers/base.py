"""
Base class for LLM providers.

This module defines the abstract base class that all LLM providers must implement.
"""
import abc
from typing import List, Dict, Any, AsyncGenerator


class BaseLLMProvider(abc.ABC):
    """
    Abstract base class for LLM providers.
    
    This class defines the interface that all LLM providers must implement.
    """
    
    @abc.abstractmethod
    async def list_models(self) -> List[Dict[str, Any]]:
        """
        List available models from the provider.
        
        Returns:
            A list of model information dictionaries
        """
        pass
    
    @abc.abstractmethod
    async def complete_chat(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: float = 1.0,
        top_p: float = 1.0,
        n: int = 1,
        user_id: str = None
    ) -> Dict[str, Any]:
        """
        Generate a chat completion (non-streaming).
        
        Args:
            model: The model to use
            messages: List of message dictionaries with 'role' and 'content' keys
            temperature: Controls randomness (higher = more random)
            top_p: Controls diversity via nucleus sampling
            n: How many completions to generate
            user_id: A unique identifier for the end-user
            
        Returns:
            The raw response from the provider
        """
        pass
    
    @abc.abstractmethod
    async def stream_chat(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: float = 1.0,
        top_p: float = 1.0,
        n: int = 1,
        user_id: str = None
    ) -> AsyncGenerator:
        """
        Generate a streaming chat completion.
        
        Args:
            model: The model to use
            messages: List of message dictionaries with 'role' and 'content' keys
            temperature: Controls randomness (higher = more random)
            top_p: Controls diversity via nucleus sampling
            n: How many completions to generate
            user_id: A unique identifier for the end-user
            
        Returns:
            An async generator that yields chunks from the streaming response
        """
        pass
    
    @abc.abstractmethod
    def get_embedding(self, text: str) -> List[float]:
        """
        Get embeddings for a single text.
        
        Args:
            text: The text to embed
            
        Returns:
            The embedding vector as a list of floats
        """
        pass
    
    @abc.abstractmethod
    async def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Get embeddings for multiple texts.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        pass