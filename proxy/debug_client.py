"""
Debug client for the SynthLang Proxy API.

This script helps debug issues with the API by printing detailed information
about the request and response.
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

# Request payload
payload = {
    "model": "gpt-4o-mini",  # Required
    "messages": [  # Required
        {
            "role": "user",  # Must be one of: "system", "user", "assistant"
            "content": "Hello, how are you today?"  # Required
        }
    ],
    "stream": False,  # Optional
    "temperature": 0.7,  # Optional
    "top_p": 1.0,  # Optional
    "n": 1  # Optional
}

# Headers
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

print("=== REQUEST ===")
print(f"URL: {API_URL}")
print(f"Headers: {json.dumps(headers, indent=2)}")
print(f"Payload: {json.dumps(payload, indent=2)}")

# Make the request
response = requests.post(API_URL, headers=headers, json=payload)

print("\n=== RESPONSE ===")
print(f"Status code: {response.status_code}")
print(f"Headers: {json.dumps(dict(response.headers), indent=2)}")

if response.status_code == 200:
    print(f"Response body: {json.dumps(response.json(), indent=2)}")
else:
    print(f"Error: {response.text}")

# Now let's try to mimic what Cline might be sending
print("\n=== TESTING POTENTIAL CLINE REQUEST FORMAT ===")

# Cline might be sending a different format or missing required fields
cline_payload = {
    # Let's try without the model field to see if that's the issue
    "messages": [
        {
            "role": "user",
            "content": "Hello, how are you today?"
        }
    ]
}

print(f"Cline-like payload: {json.dumps(cline_payload, indent=2)}")

cline_response = requests.post(API_URL, headers=headers, json=cline_payload)

print(f"Status code: {cline_response.status_code}")
if cline_response.status_code == 200:
    print(f"Response body: {json.dumps(cline_response.json(), indent=2)}")
else:
    print(f"Error: {cline_response.text}")