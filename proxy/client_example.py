"""
Example client for the SynthLang Proxy API.

This script demonstrates how to make requests to the SynthLang Proxy API.
"""
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API endpoint
API_URL = "https://synthlang-proxy.fly.dev/chat/completions"

# API key (from environment variable)
API_KEY = os.getenv("ADMIN_API_KEY")

if not API_KEY:
    raise ValueError("ADMIN_API_KEY environment variable is not set. Please set it in your .env file.")

# Headers
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# Example 1: With explicit model
print("\n=== EXAMPLE 1: WITH EXPLICIT MODEL ===")
payload1 = {
    "model": "gpt-4o-mini",  # Explicitly specify the model
    "messages": [
        {
            "role": "user",
            "content": "Hello, how are you today?"
        }
    ],
    "temperature": 0.7
}

print(f"Request payload: {json.dumps(payload1, indent=2)}")
response1 = requests.post(API_URL, headers=headers, json=payload1)

print(f"Status code: {response1.status_code}")
if response1.status_code == 200:
    print(f"Response: {json.dumps(response1.json(), indent=2)}")
else:
    print(f"Error: {response1.text}")

# Example 2: Without model (uses default)
print("\n=== EXAMPLE 2: WITHOUT MODEL (USES DEFAULT) ===")
payload2 = {
    # No model specified - will use default "gpt-4o-mini"
    "messages": [
        {
            "role": "user",
            "content": "What's the weather like today?"
        }
    ],
    "temperature": 0.7
}

print(f"Request payload: {json.dumps(payload2, indent=2)}")
response2 = requests.post(API_URL, headers=headers, json=payload2)

print(f"Status code: {response2.status_code}")
if response2.status_code == 200:
    print(f"Response: {json.dumps(response2.json(), indent=2)}")
else:
    print(f"Error: {response2.text}")