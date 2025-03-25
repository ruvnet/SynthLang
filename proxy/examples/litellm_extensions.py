"""
Example of extending the LiteLLM provider with additional capabilities.

This example demonstrates how to use the modular LiteLLM provider to:
1. Add custom model mappings
2. Add pre and post-processing hooks
3. Register new capabilities
"""
import asyncio
import os
import sys
from typing import Dict, Any, List

# Add the src directory to the path so we can import the app modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.app.litellm_provider import provider


async def main():
    """Run the example."""
    print("LiteLLM Provider Extension Example")
    print("==================================")
    
    # 1. Add a custom model mapping
    provider.add_model_mapping("my-custom-model", "openai/gpt-4o")
    print(f"Added custom model mapping: my-custom-model -> openai/gpt-4o")
    
    # 2. Add a custom model fallback
    provider.add_model_fallback("my-custom-model", ["openai/gpt-4o", "openai/gpt-3.5-turbo"])
    print(f"Added custom model fallback for my-custom-model")
    
    # 3. Add a pre-processing hook to modify requests
    def add_system_message(params: Dict[str, Any]) -> Dict[str, Any]:
        """Add a system message to the beginning of the messages list."""
        messages = params.get("messages", [])
        
        # Check if there's already a system message
        has_system = any(msg.get("role") == "system" for msg in messages)
        
        if not has_system:
            messages.insert(0, {
                "role": "system",
                "content": "You are a helpful assistant that provides concise responses."
            })
            params["messages"] = messages
        
        print(f"Pre-processing hook added system message")
        return params
    
    provider.add_pre_process_hook(add_system_message)
    
    # 4. Add a post-processing hook to modify responses
    def add_metadata(response: Dict[str, Any]) -> Dict[str, Any]:
        """Add metadata to the response."""
        response["metadata"] = {
            "enhanced_by": "SynthLang",
            "version": "1.0.0"
        }
        print(f"Post-processing hook added metadata")
        return response
    
    provider.add_post_process_hook(add_metadata)
    
    # 5. Register a new capability - embedding with caching
    class CachedEmbedding:
        """A simple embedding service with caching."""
        
        def __init__(self):
            self.cache = {}
        
        async def get_embedding(self, text: str, model: str = "text-embedding-ada-002") -> List[float]:
            """Get an embedding for the given text, with caching."""
            if text in self.cache:
                print(f"Cache hit for embedding: {text[:20]}...")
                return self.cache[text]
            
            print(f"Cache miss for embedding: {text[:20]}...")
            # In a real implementation, this would call litellm.embedding()
            # For this example, we'll just return a dummy embedding
            embedding = [0.1, 0.2, 0.3, 0.4, 0.5]
            self.cache[text] = embedding
            return embedding
    
    # Register the new capability
    provider.register_capability("cached_embedding", CachedEmbedding())
    
    # 6. Use the provider with all the extensions
    try:
        # Use the custom model mapping
        response = await provider.complete_chat(
            model="my-custom-model",
            messages=[{"role": "user", "content": "Hello, how are you?"}],
            temperature=0.7
        )
        
        print("\nResponse from LiteLLM:")
        print(f"Model: {response['model']}")
        print(f"Content: {response['choices'][0]['message']['content']}")
        print(f"Metadata: {response.get('metadata', {})}")
        
        # Use the new capability
        embedding = await provider.cached_embedding.get_embedding("This is a test")
        print(f"\nEmbedding: {embedding}")
        
        # Test caching
        embedding2 = await provider.cached_embedding.get_embedding("This is a test")
        print(f"Second embedding (should be cached): {embedding2}")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # Set up API key for testing
    if not os.environ.get("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY not set. This example will not work without it.")
        print("Please set the OPENAI_API_KEY environment variable and try again.")
        sys.exit(1)
    
    asyncio.run(main())