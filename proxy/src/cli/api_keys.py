#!/usr/bin/env python
"""
CLI tool for managing API keys.

This tool allows users to create, list, and delete API keys,
and save them to the environment.
"""
import os
import sys
import argparse
import logging
import secrets
import json
from typing import Dict, List, Any, Optional
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "")))

from src.app.auth.api_keys import API_KEYS, RATE_LIMITS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("api-keys-cli")

# Path to store API keys
API_KEYS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".api_keys.json")

def load_api_keys() -> Dict[str, Any]:
    """
    Load API keys from file.
    
    Returns:
        Dictionary containing API keys and rate limits
    """
    if not os.path.exists(API_KEYS_FILE):
        return {"api_keys": {}, "rate_limits": {}}
    
    try:
        with open(API_KEYS_FILE, "r") as f:
            data = json.load(f)
        return data
    except Exception as e:
        logger.error(f"Error loading API keys: {e}")
        return {"api_keys": {}, "rate_limits": {}}

def save_api_keys(data: Dict[str, Any]) -> bool:
    """
    Save API keys to file.
    
    Args:
        data: Dictionary containing API keys and rate limits
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(API_KEYS_FILE, "w") as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        logger.error(f"Error saving API keys: {e}")
        return False

def generate_api_key(prefix: str = "sk_") -> str:
    """
    Generate a new API key.
    
    Args:
        prefix: Prefix for the API key
        
    Returns:
        A new API key
    """
    # Generate a random token
    token = secrets.token_hex(16)
    return f"{prefix}{token}"

def list_keys(args):
    """List all API keys."""
    data = load_api_keys()
    api_keys = data.get("api_keys", {})
    rate_limits = data.get("rate_limits", {})
    
    if not api_keys:
        print("No API keys found.")
        return
    
    print(f"Found {len(api_keys)} API keys:")
    print("-" * 80)
    
    for api_key, user_id in api_keys.items():
        rate_limit = rate_limits.get(user_id, "default")
        print(f"API Key: {api_key}")
        print(f"User ID: {user_id}")
        print(f"Rate Limit: {rate_limit} requests per minute")
        print("-" * 80)

def create_key(args):
    """Create a new API key."""
    data = load_api_keys()
    api_keys = data.get("api_keys", {})
    rate_limits = data.get("rate_limits", {})
    
    # Generate a new API key
    api_key = generate_api_key(args.prefix)
    
    # Add to API keys
    api_keys[api_key] = args.user_id
    
    # Set rate limit if specified
    if args.rate_limit is not None:
        rate_limits[args.user_id] = args.rate_limit
    
    # Update data
    data["api_keys"] = api_keys
    data["rate_limits"] = rate_limits
    
    # Save to file
    if save_api_keys(data):
        print(f"API key created successfully: {api_key}")
        
        # Save to .env file if requested
        if args.save_env:
            env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
            
            # Read existing .env file
            env_vars = {}
            if os.path.exists(env_file):
                with open(env_file, "r") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            key, value = line.split("=", 1)
                            env_vars[key] = value
            
            # Add API key
            env_vars["API_KEY"] = api_key
            
            # Write back to .env file
            with open(env_file, "w") as f:
                for key, value in env_vars.items():
                    f.write(f"{key}={value}\n")
            
            print(f"API key saved to .env file as API_KEY={api_key}")
            
            # Export to current environment
            os.environ["API_KEY"] = api_key
            print("API key exported to current environment as API_KEY")
    else:
        print("Failed to create API key.")

def delete_key(args):
    """Delete an API key."""
    data = load_api_keys()
    api_keys = data.get("api_keys", {})
    
    if args.api_key not in api_keys:
        print(f"API key '{args.api_key}' not found.")
        return
    
    # Remove API key
    user_id = api_keys.pop(args.api_key)
    
    # Update data
    data["api_keys"] = api_keys
    
    # Save to file
    if save_api_keys(data):
        print(f"API key '{args.api_key}' deleted successfully.")
    else:
        print(f"Failed to delete API key '{args.api_key}'.")

def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description="Manage API keys")
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # List API keys
    list_parser = subparsers.add_parser("list", help="List all API keys")
    list_parser.set_defaults(func=list_keys)
    
    # Create API key
    create_parser = subparsers.add_parser("create", help="Create a new API key")
    create_parser.add_argument("--user-id", "-u", required=True, help="User ID")
    create_parser.add_argument("--rate-limit", "-r", type=int, help="Rate limit in requests per minute")
    create_parser.add_argument("--prefix", "-p", default="sk_", help="API key prefix")
    create_parser.add_argument("--save-env", "-s", action="store_true", help="Save API key to .env file")
    create_parser.set_defaults(func=create_key)
    
    # Delete API key
    delete_parser = subparsers.add_parser("delete", help="Delete an API key")
    delete_parser.add_argument("api_key", help="API key to delete")
    delete_parser.set_defaults(func=delete_key)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    args.func(args)

if __name__ == "__main__":
    main()