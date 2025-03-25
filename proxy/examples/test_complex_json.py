"""
Test script to verify that the /chat/completions endpoint can handle complex JSON data.

This script sends a request with complex nested JSON structures to the /chat/completions
endpoint to confirm that it works correctly with the LiteLLM provider.
"""
import asyncio
import json
import os
import sys
import httpx

# Add the src directory to the path so we can import the app modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


async def test_complex_json():
    """Test the /chat/completions endpoint with complex JSON data."""
    # Create a test client
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        # Create a complex JSON payload
        complex_payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": {
                    "main_text": "This is a complex message with nested structure",
                    "metadata": {
                        "source": "user interface",
                        "timestamp": 1677652288,
                        "client_info": {"browser": "Chrome", "version": "98.0.4758.102"}
                    },
                    "attachments": [
                        {"title": "Document 1", "content": "Some content here"},
                        {"title": "Document 2", "content": "More content here"}
                    ]
                }}
            ],
            "temperature": 0.7,
            "max_tokens": 100,
            "additional_params": {
                "custom_field": "custom value",
                "nested_field": {
                    "key1": "value1",
                    "key2": ["item1", "item2", "item3"]
                }
            }
        }
        
        # Get API key from environment
        api_key = os.environ.get("OPENAI_API_KEY", "")
        if not api_key:
            print("Warning: OPENAI_API_KEY not set. This test will not work without it.")
            return
        
        # Send the request
        try:
            response = await client.post(
                "/chat/completions",
                json=complex_payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}"
                }
            )
            
            # Check the response
            if response.status_code == 200:
                result = response.json()
                print("✅ Success! The endpoint can handle complex JSON data.")
                print("\nResponse:")
                print(f"Status code: {response.status_code}")
                print(f"Model: {result.get('model')}")
                print(f"Choices: {len(result.get('choices', []))}")
                if result.get('choices'):
                    print(f"Content: {result['choices'][0]['message']['content'][:100]}...")
            else:
                print(f"❌ Error: {response.status_code}")
                print(response.text)
                
        except Exception as e:
            print(f"❌ Exception: {e}")


async def test_direct_litellm():
    """Test LiteLLM directly with complex JSON data."""
    from src.app.litellm_provider import provider
    
    # Create a complex message
    complex_message = {
        "role": "user", 
        "content": {
            "main_text": "This is a complex message with nested structure",
            "metadata": {
                "source": "user interface",
                "timestamp": 1677652288,
                "client_info": {"browser": "Chrome", "version": "98.0.4758.102"}
            },
            "attachments": [
                {"title": "Document 1", "content": "Some content here"},
                {"title": "Document 2", "content": "More content here"}
            ]
        }
    }
    
    # Test with the provider
    try:
        response = await provider.complete_chat(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                complex_message
            ],
            temperature=0.7,
            max_tokens=100
        )
        
        print("\n✅ Success! LiteLLM provider can handle complex JSON data directly.")
        print(f"Model: {response.get('model')}")
        print(f"Choices: {len(response.get('choices', []))}")
        if response.get('choices'):
            print(f"Content: {response['choices'][0]['message']['content'][:100]}...")
            
    except Exception as e:
        print(f"❌ Exception in direct LiteLLM test: {e}")


async def main():
    """Run the tests."""
    print("Testing complex JSON handling with LiteLLM")
    print("=========================================")
    
    print("\n1. Testing direct LiteLLM provider:")
    await test_direct_litellm()
    
    print("\n2. Testing /chat/completions endpoint:")
    await test_complex_json()


if __name__ == "__main__":
    # Check if the server is running
    print("Note: This test assumes the SynthLang proxy server is running on http://localhost:8000")
    print("If it's not running, please start it with 'python -m src.app.main' from the proxy directory")
    
    # Run the tests
    asyncio.run(main())