"""
LiteLLM provider module for SynthLang proxy.

This module provides a unified interface to multiple LLM providers
through LiteLLM, handling complex requests more robustly.
"""
import os
import time
import logging
import importlib
from typing import List, Dict, Any, AsyncGenerator, Optional, Union, Callable, Type

import litellm

logger = logging.getLogger("app.litellm_provider")


class LiteLLMProvider:
    """
    A modular interface to LiteLLM capabilities.
    
    This class encapsulates all LiteLLM functionality and provides extension
    points for adding new capabilities in the future.
    """
    
    def __init__(self):
        """Initialize the LiteLLM provider with default configuration."""
        self.configure_litellm()
        self.patch_litellm_errors()
        self.load_api_keys()
        self.setup_callbacks()
        
        # Default settings
        self.timeout = int(os.environ.get("LITELLM_TIMEOUT", "30"))
        self.max_retries = int(os.environ.get("LITELLM_MAX_RETRIES", "3"))
        
        # Model configuration
        self.model_map = self._get_default_model_map()
        self.model_fallbacks = self._get_default_model_fallbacks()
        
        # Extension points - can be modified by users of this class
        self.pre_process_hooks = []
        self.post_process_hooks = []
        
    def configure_litellm(self):
        """Configure global LiteLLM settings."""
        litellm.set_verbose = False  # Set to True for debugging
        litellm.drop_params = True  # Drop unsupported params instead of erroring
        
        # Additional configuration options can be added here
        litellm.telemetry = False  # Disable telemetry to avoid logging errors
        
    def patch_litellm_errors(self):
        """Patch known issues in LiteLLM."""
        try:
            # Import the module that contains the problematic function
            model_param_helper = importlib.import_module("litellm.litellm_core_utils.model_param_helper")
            
            # Define a replacement function that doesn't use __annotations__
            def get_litellm_supported_transcription_kwargs():
                """Return an empty set to avoid the __annotations__ error"""
                return set()
            
            # Replace the problematic function
            model_param_helper.ModelParamHelper._get_litellm_supported_transcription_kwargs = get_litellm_supported_transcription_kwargs
            
            logger.info("Successfully patched LiteLLM to fix __annotations__ error")
        except Exception as e:
            logger.warning(f"Failed to patch LiteLLM: {e}")
    
    def load_api_keys(self):
        """Load API keys from environment variables."""
        # Get API keys from environment
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")
        
        # In newer versions of LiteLLM, API keys are set via environment variables
        # or directly in the completion call
        if openai_api_key:
            os.environ["OPENAI_API_KEY"] = openai_api_key
            logger.info("OpenAI API key loaded from environment")
        
        if anthropic_api_key:
            os.environ["ANTHROPIC_API_KEY"] = anthropic_api_key
            logger.info("Anthropic API key loaded from environment")
            
        # Additional providers can be added here
    
    def setup_callbacks(self):
        """Set up LiteLLM callbacks for logging and monitoring."""
        # Define custom callback functions
        def log_success_response(response_obj, kwargs):
            """Log successful responses"""
            model = response_obj.get("model", "unknown")
            logger.info(f"LiteLLM response from model {model}")
        
        def log_error_response(error, kwargs):
            """Log errors with context"""
            model = kwargs.get("model", "unknown")
            messages = kwargs.get("messages", [])
            logger.error(f"LiteLLM error with model {model}: {error}")
            
            # Get message lengths for debugging
            message_lengths = []
            if messages:
                for msg in messages:
                    content = msg.get("content", "")
                    if isinstance(content, str):
                        message_lengths.append(len(content))
                    else:
                        message_lengths.append("non-string content")
                        
            logger.error(f"Message lengths: {message_lengths}")
        
        # Set up callbacks
        litellm.success_callback = [log_success_response]
        litellm.failure_callback = [log_error_response]
    
    def _get_default_model_map(self) -> Dict[str, str]:
        """
        Get the default model mapping from internal names to provider-specific names.
        
        Returns:
            A dictionary mapping internal model names to provider-specific model names
        """
        return {
            # OpenAI models
            "gpt-4o-mini": "openai/gpt-4o-mini",
            "gpt-4o": "openai/gpt-4o",
            "gpt-4": "openai/gpt-4-turbo",
            "gpt-3.5-turbo": "openai/gpt-3.5-turbo",
            
            # Anthropic models - using correct model names
            "claude-3-opus": "anthropic/claude-3-opus-20240229",
            "claude-3-sonnet": "anthropic/claude-3-sonnet-20240229",
            "claude-3-haiku": "anthropic/claude-3-haiku-20240307",
            "claude-3.5-sonnet": "anthropic/claude-3-5-sonnet-20240620",
            "claude-3-7-sonnet-latest": "anthropic/claude-3-sonnet-20240229"  # Fallback to a known working model
        }
    
    def _get_default_model_fallbacks(self) -> Dict[str, List[str]]:
        """
        Get the default model fallbacks.
        
        Returns:
            A dictionary mapping model names to lists of fallback models
        """
        return {
            # OpenAI fallbacks
            "gpt-4o-mini": ["openai/gpt-4o-mini", "openai/gpt-3.5-turbo"],
            
            # Anthropic fallbacks - using correct model names
            "claude-3-sonnet": ["anthropic/claude-3-sonnet-20240229", "anthropic/claude-3-haiku-20240307", "openai/gpt-4o"],
            "claude-3.5-sonnet": ["anthropic/claude-3-5-sonnet-20240620", "anthropic/claude-3-sonnet-20240229", "openai/gpt-4o"],
            "claude-3-7-sonnet-latest": ["anthropic/claude-3-sonnet-20240229", "openai/gpt-4o"]
        }
    
    def map_model_name(self, model: str) -> str:
        """
        Map internal model names to provider-specific model names.
        
        Args:
            model: The internal model name
            
        Returns:
            The provider-specific model name
        """
        # Handle compressed model names by checking for partial matches
        if model not in self.model_map:
            # Check if this is a compressed model name
            for full_name, provider_name in self.model_map.items():
                # Check for key parts of the model name to identify it
                if "claud" in model.lower() and "3-7" in model and "sonnet" in model.lower() and "latest" in model.lower():
                    logger.info(f"Detected compressed model name '{model}', mapping to claude-3-7-sonnet-latest")
                    return self.model_map["claude-3-7-sonnet-latest"]
                elif "claud" in model.lower() and "3.5" in model and "sonnet" in model.lower():
                    logger.info(f"Detected compressed model name '{model}', mapping to claude-3.5-sonnet")
                    return self.model_map["claude-3.5-sonnet"]
                elif "claud" in model.lower() and "3" in model and "sonnet" in model.lower():
                    logger.info(f"Detected compressed model name '{model}', mapping to claude-3-sonnet")
                    return self.model_map["claude-3-sonnet"]
                elif "claud" in model.lower() and "3" in model and "opus" in model.lower():
                    logger.info(f"Detected compressed model name '{model}', mapping to claude-3-opus")
                    return self.model_map["claude-3-opus"]
                elif "claud" in model.lower() and "3" in model and "haiku" in model.lower():
                    logger.info(f"Detected compressed model name '{model}', mapping to claude-3-haiku")
                    return self.model_map["claude-3-haiku"]
                elif "gpt-4o" in model.lower() and "mini" in model.lower():
                    logger.info(f"Detected compressed model name '{model}', mapping to gpt-4o-mini")
                    return self.model_map["gpt-4o-mini"]
                elif "gpt-4o" in model.lower():
                    logger.info(f"Detected compressed model name '{model}', mapping to gpt-4o")
                    return self.model_map["gpt-4o"]
                elif "gpt-4" in model.lower():
                    logger.info(f"Detected compressed model name '{model}', mapping to gpt-4")
                    return self.model_map["gpt-4"]
                elif "gpt-3.5" in model.lower() or "gpt-3" in model.lower():
                    logger.info(f"Detected compressed model name '{model}', mapping to gpt-3.5-turbo")
                    return self.model_map["gpt-3.5-turbo"]
        
        provider_model = self.model_map.get(model, model)
        logger.info(f"Mapping model {model} to {provider_model}")
        return provider_model
    
    def add_model_mapping(self, internal_name: str, provider_name: str):
        """
        Add a new model mapping.
        
        Args:
            internal_name: The internal model name
            provider_name: The provider-specific model name
        """
        self.model_map[internal_name] = provider_name
    
    def add_model_fallback(self, model: str, fallbacks: List[str]):
        """
        Add a new model fallback configuration.
        
        Args:
            model: The model name
            fallbacks: List of fallback models
        """
        self.model_fallbacks[model] = fallbacks
    
    def add_pre_process_hook(self, hook: Callable):
        """
        Add a pre-processing hook that will be called before each request.
        
        Args:
            hook: A callable that takes and returns a dictionary of request parameters
        """
        self.pre_process_hooks.append(hook)
    
    def add_post_process_hook(self, hook: Callable):
        """
        Add a post-processing hook that will be called after each response.
        
        Args:
            hook: A callable that takes and returns a response object
        """
        self.post_process_hooks.append(hook)
    
    def _process_messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """
        Process messages to ensure content is string.
        
        Args:
            messages: The conversation messages
            
        Returns:
            Processed messages with string content
        """
        processed_messages = []
        for msg in messages:
            content = msg.get("content", "")
            # Convert non-string content to string
            if not isinstance(content, str):
                content = str(content)
            
            processed_messages.append({
                "role": msg.get("role", "user"),
                "content": content
            })
        return processed_messages
    
    def _get_retry_config(self) -> Dict[str, Any]:
        """
        Get the retry configuration.
        
        Returns:
            A dictionary with retry configuration parameters
        """
        return {
            "max_retries": self.max_retries,
            "timeout": self.timeout,
        }
    
    def _normalize_response(self, response: Dict[str, Any], model: str) -> Dict[str, Any]:
        """
        Normalize the response to ensure consistent format.
        
        Args:
            response: The raw response from LiteLLM
            model: The original model name
            
        Returns:
            A normalized response
        """
        # Ensure choices has the correct format
        choices = response.get("choices", [])
        normalized_choices = []
        
        for choice in choices:
            # Make sure each choice has the expected structure
            normalized_choice = {
                "index": choice.get("index", 0),
                "message": choice.get("message", {}),
                "finish_reason": choice.get("finish_reason", "stop")
            }
            normalized_choices.append(normalized_choice)
        
        normalized = {
            "id": response.get("id", f"chatcmpl-{int(time.time())}"),
            "object": "chat.completion",
            "created": response.get("created", int(time.time())),
            "model": model,
            "choices": normalized_choices,
            "usage": response.get("usage", {})
        }
        
        # Apply post-processing hooks
        for hook in self.post_process_hooks:
            normalized = hook(normalized)
            
        return normalized
    
    def _normalize_chunk(self, chunk: Dict[str, Any], model: str) -> Dict[str, Any]:
        """
        Normalize a streaming chunk to ensure consistent format.
        
        Args:
            chunk: The raw chunk from LiteLLM
            model: The original model name
            
        Returns:
            A normalized chunk
        """
        # Ensure choices has the correct format
        choices = chunk.get("choices", [])
        normalized_choices = []
        
        for choice in choices:
            # Make sure each choice has the expected structure
            normalized_choice = {
                "index": choice.get("index", 0),
                "delta": choice.get("delta", {}),
                "finish_reason": choice.get("finish_reason", None)
            }
            normalized_choices.append(normalized_choice)
        
        normalized = {
            "id": chunk.get("id", f"chatcmpl-{int(time.time())}"),
            "object": "chat.completion.chunk",
            "created": chunk.get("created", int(time.time())),
            "model": model,
            "choices": normalized_choices
        }
        
        # Apply post-processing hooks
        for hook in self.post_process_hooks:
            normalized = hook(normalized)
            
        return normalized
    
    async def complete_chat(
        self,
        model: str, 
        messages: List[Dict[str, Any]], 
        temperature: float = 1.0, 
        top_p: float = 1.0, 
        n: int = 1, 
        max_tokens: Optional[int] = None,
        user_id: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Send a chat completion request to the LLM provider using LiteLLM.
        
        Args:
            model: The model to use
            messages: The conversation messages
            temperature: Controls randomness (higher = more random)
            top_p: Controls diversity via nucleus sampling
            n: How many completions to generate
            max_tokens: Maximum number of tokens to generate
            user_id: A unique identifier for the end-user
            **kwargs: Additional parameters to pass to LiteLLM
            
        Returns:
            The chat completion response
        """
        try:
            # Map model name
            provider_model = self.map_model_name(model)
            
            # Process messages
            processed_messages = self._process_messages(messages)
            
            # Configure retry parameters
            retry_config = self._get_retry_config()
            
            # Prepare parameters
            params = {
                "model": provider_model,
                "messages": processed_messages,
                "temperature": temperature,
                "top_p": top_p,
                "n": n,
                "max_tokens": max_tokens,
                "user": user_id,
                "fallbacks": self.model_fallbacks.get(model, []),
                **retry_config,
                **kwargs
            }
            
            # Apply pre-processing hooks
            for hook in self.pre_process_hooks:
                params = hook(params)
            
            # Make the API call through LiteLLM
            logger.info(f"Sending request to LiteLLM with model {provider_model}")
            response = await litellm.acompletion(**params)
            logger.info(f"Received response from LiteLLM for model {provider_model}")
            
            # Normalize and return the response
            return self._normalize_response(response, model)
            
        except Exception as e:
            logger.error(f"LiteLLM completion error: {e}")
            raise
    
    async def stream_chat(
        self,
        model: str, 
        messages: List[Dict[str, Any]], 
        temperature: float = 1.0, 
        top_p: float = 1.0, 
        n: int = 1,
        max_tokens: Optional[int] = None,
        user_id: Optional[str] = None,
        **kwargs
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Stream a chat completion from the LLM provider using LiteLLM.
        
        Args:
            model: The model to use
            messages: The conversation messages
            temperature: Controls randomness (higher = more random)
            top_p: Controls diversity via nucleus sampling
            n: How many completions to generate
            max_tokens: Maximum number of tokens to generate
            user_id: A unique identifier for the end-user
            **kwargs: Additional parameters to pass to LiteLLM
            
        Yields:
            Streaming chunks of the chat completion response
        """
        try:
            # Map model name
            provider_model = self.map_model_name(model)
            
            # Process messages
            processed_messages = self._process_messages(messages)
            
            # Configure retry parameters
            retry_config = self._get_retry_config()
            
            # Prepare parameters
            params = {
                "model": provider_model,
                "messages": processed_messages,
                "temperature": temperature,
                "top_p": top_p,
                "n": n,
                "max_tokens": max_tokens,
                "user": user_id,
                "stream": True,
                "fallbacks": self.model_fallbacks.get(model, []),
                **retry_config,
                **kwargs
            }
            
            # Apply pre-processing hooks
            for hook in self.pre_process_hooks:
                params = hook(params)
            
            # Make the streaming API call through LiteLLM
            logger.info(f"Sending streaming request to LiteLLM with model {provider_model}")
            response_stream = await litellm.acompletion(**params)
            
            # Stream the response chunks
            async for chunk in response_stream:
                yield self._normalize_chunk(chunk, model)
                
        except Exception as e:
            logger.error(f"LiteLLM streaming error: {e}")
            raise
    
    # Extension point for future capabilities
    def register_capability(self, name: str, implementation: Any):
        """
        Register a new capability with the provider.
        
        Args:
            name: The name of the capability
            implementation: The implementation of the capability
        """
        setattr(self, name, implementation)


# Create a singleton instance
_provider = LiteLLMProvider()

# Backward compatibility functions
async def complete_chat(
    model: str, 
    messages: List[Dict[str, Any]], 
    temperature: float = 1.0, 
    top_p: float = 1.0, 
    n: int = 1, 
    max_tokens: Optional[int] = None,
    user_id: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Backward compatibility function for complete_chat.
    
    Args:
        model: The model to use
        messages: The conversation messages
        temperature: Controls randomness (higher = more random)
        top_p: Controls diversity via nucleus sampling
        n: How many completions to generate
        max_tokens: Maximum number of tokens to generate
        user_id: A unique identifier for the end-user
        **kwargs: Additional parameters to pass to LiteLLM
        
    Returns:
        The chat completion response
    """
    return await _provider.complete_chat(
        model=model,
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        n=n,
        max_tokens=max_tokens,
        user_id=user_id,
        **kwargs
    )

async def stream_chat(
    model: str, 
    messages: List[Dict[str, Any]], 
    temperature: float = 1.0, 
    top_p: float = 1.0, 
    n: int = 1,
    max_tokens: Optional[int] = None,
    user_id: Optional[str] = None,
    **kwargs
) -> AsyncGenerator[Dict[str, Any], None]:
    """
    Backward compatibility function for stream_chat.
    
    Args:
        model: The model to use
        messages: The conversation messages
        temperature: Controls randomness (higher = more random)
        top_p: Controls diversity via nucleus sampling
        n: How many completions to generate
        max_tokens: Maximum number of tokens to generate
        user_id: A unique identifier for the end-user
        **kwargs: Additional parameters to pass to LiteLLM
        
    Yields:
        Streaming chunks of the chat completion response
    """
    async for chunk in _provider.stream_chat(
        model=model,
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        n=n,
        max_tokens=max_tokens,
        user_id=user_id,
        **kwargs
    ):
        yield chunk

# Expose the provider instance for advanced usage
provider = _provider

# Expose the map_model_name function for backward compatibility
map_model_name = _provider.map_model_name