"""Proxy commands for SynthLang CLI."""
import json
from typing import Optional, List, Dict, Any

import click

from synthlang.utils.logger import get_logger

logger = get_logger(__name__)


def register_proxy_commands(main):
    """Register proxy commands with the main CLI group.
    
    Args:
        main: Main CLI group
    """
    @main.group()
    def proxy():
        """Commands for working with SynthLang Proxy."""
        pass

    @proxy.command()
    @click.option("--host", help="Host to bind to")
    @click.option("--port", type=int, help="Port to bind to")
    @click.option("--log-level", default="info", help="Logging level")
    @click.option("--reload", is_flag=True, help="Enable auto-reload")
    def serve(host: Optional[str], port: Optional[int], log_level: str, reload: bool):
        """Start a local proxy server.
        
        Example:
            synthlang proxy serve --port 8000
        """
        try:
            from synthlang.proxy.server import start_server
            
            click.echo(f"Starting proxy server...")
            start_server(host=host, port=port, log_level=log_level, reload=reload)
        except Exception as e:
            raise click.ClickException(f"Failed to start server: {str(e)}")

    @proxy.command()
    @click.option("--api-key", required=True, help="API key for proxy service")
    @click.option("--endpoint", help="Proxy endpoint URL")
    def login(api_key: str, endpoint: Optional[str]):
        """Save credentials for proxy service.
        
        Example:
            synthlang proxy login --api-key "your-key" --endpoint "https://api.example.com"
        """
        try:
            from synthlang.proxy.auth import save_credentials
            
            save_credentials(api_key, endpoint)
            click.echo(f"Credentials saved successfully")
            if endpoint:
                click.echo(f"Endpoint: {endpoint}")
        except Exception as e:
            raise click.ClickException(f"Failed to save credentials: {str(e)}")

    @proxy.command()
    def logout():
        """Clear saved proxy credentials.
        
        Example:
            synthlang proxy logout
        """
        try:
            from synthlang.proxy.auth import clear_credentials
            
            clear_credentials()
            click.echo("Credentials cleared successfully")
        except Exception as e:
            raise click.ClickException(f"Failed to clear credentials: {str(e)}")

    @proxy.group()
    def apikey():
        """Manage API keys for the proxy server."""
        pass

    @apikey.command()
    def list():
        """List all API keys.
        
        Example:
            synthlang proxy apikey list
        """
        try:
            import sys
            import os
            
            # Add the parent directory to the Python path
            sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "")))
            
            from src.cli.api_keys import list_keys
            
            # Create a mock args object
            class Args:
                pass
            
            args = Args()
            list_keys(args)
        except Exception as e:
            raise click.ClickException(f"Failed to list API keys: {str(e)}")

    @apikey.command()
    @click.option("--user-id", "-u", required=True, help="User ID")
    @click.option("--rate-limit", "-r", type=int, help="Rate limit in requests per minute")
    @click.option("--prefix", "-p", default="sk_", help="API key prefix")
    @click.option("--save-env", "-s", is_flag=True, help="Save API key to .env file")
    def create(user_id: str, rate_limit: Optional[int], prefix: str, save_env: bool):
        """Create a new API key.
        
        Example:
            synthlang proxy apikey create --user-id "test_user" --rate-limit 100 --save-env
        """
        try:
            import sys
            import os
            
            # Add the parent directory to the Python path
            sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "")))
            
            from src.cli.api_keys import create_key
            
            # Create a mock args object
            class Args:
                pass
            
            args = Args()
            args.user_id = user_id
            args.rate_limit = rate_limit
            args.prefix = prefix
            args.save_env = save_env
            
            create_key(args)
        except Exception as e:
            raise click.ClickException(f"Failed to create API key: {str(e)}")

    @apikey.command()
    @click.argument("api_key")
    def delete(api_key: str):
        """Delete an API key.
        
        Example:
            synthlang proxy apikey delete "sk_1234567890abcdef"
        """
        try:
            import sys
            import os
            
            # Add the parent directory to the Python path
            sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "")))
            
            from src.cli.api_keys import delete_key
            
            # Create a mock args object
            class Args:
                pass
            
            args = Args()
            args.api_key = api_key
            
            delete_key(args)
        except Exception as e:
            raise click.ClickException(f"Failed to delete API key: {str(e)}")

    @proxy.command()
    @click.option("--model", help="Model to use")
    @click.option("--system", help="System message")
    @click.option("--temperature", type=float, default=0.7, help="Temperature for sampling")
    @click.option("--max-tokens", type=int, help="Maximum tokens to generate")
    @click.argument("prompt")
    def chat(model: Optional[str], system: Optional[str], temperature: float, 
             max_tokens: Optional[int], prompt: str):
        """Send a chat request to the proxy.
        
        Example:
            synthlang proxy chat --model "gpt-4o" "What is the capital of France?"
        """
        try:
            from synthlang.proxy.api import ProxyClient
            from synthlang.proxy.auth import get_credentials
            from synthlang.proxy.config import get_proxy_config
            
            config = get_proxy_config()
            creds = get_credentials()
            
            if "api_key" not in creds:
                raise click.ClickException(
                    "No API key found. Run 'synthlang proxy login' first."
                )
            
            endpoint = creds.get("endpoint", config.endpoint)
            client = ProxyClient(endpoint, creds["api_key"])
            
            # Build messages
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})
            
            # Set up parameters
            params = {
                "temperature": temperature
            }
            if max_tokens:
                params["max_tokens"] = max_tokens
            
            # Send request
            response = client.chat_completion(
                messages, 
                model=model or config.default_model,
                **params
            )
            
            # Extract and print response
            if "choices" in response and len(response["choices"]) > 0:
                content = response["choices"][0]["message"]["content"]
                click.echo(content)
            else:
                click.echo("No response received")
        except Exception as e:
            raise click.ClickException(f"Chat failed: {str(e)}")

    @proxy.command()
    @click.option("--use-gzip", is_flag=True, help="Use gzip compression")
    @click.argument("prompt")
    def compress(use_gzip: bool, prompt: str):
        """Compress a prompt using SynthLang compression.
        
        Example:
            synthlang proxy compress --use-gzip "Your prompt here"
        """
        try:
            from synthlang.proxy.compression import compress_prompt, get_compression_stats
            
            # Compress the prompt
            compressed = compress_prompt(prompt, use_gzip)
            
            # Get stats
            stats = get_compression_stats(prompt, compressed)
            
            # Print results
            click.echo(f"Original ({stats['original_length']} chars):")
            click.echo(prompt)
            click.echo(f"\nCompressed ({stats['compressed_length']} chars):")
            click.echo(compressed)
            click.echo(f"\nCompression ratio: {stats['compression_ratio']:.2f}x")
            click.echo(f"Space saving: {stats['space_savings_percent']:.1f}%")
            click.echo(f"Method: {'gzip+synthlang' if use_gzip else 'synthlang'}")
        except Exception as e:
            raise click.ClickException(f"Compression failed: {str(e)}")

    @proxy.command()
    @click.argument("compressed")
    def decompress(compressed: str):
        """Decompress a SynthLang-compressed prompt.
        
        Example:
            synthlang proxy decompress "↹ compressed•text"
        """
        try:
            from synthlang.proxy.compression import decompress_prompt
            
            # Decompress the prompt
            decompressed = decompress_prompt(compressed)
            
            # Print results
            click.echo(f"Compressed ({len(compressed)} chars):")
            click.echo(compressed)
            click.echo(f"\nDecompressed ({len(decompressed)} chars):")
            click.echo(decompressed)
        except Exception as e:
            raise click.ClickException(f"Decompression failed: {str(e)}")

    @proxy.command()
    def clear_cache():
        """Clear the semantic cache.
        
        Example:
            synthlang proxy clear-cache
        """
        try:
            from synthlang.proxy.cache import get_semantic_cache
            
            cache = get_semantic_cache()
            count = cache.clear()
            click.echo(f"Cleared {count} cache entries")
        except Exception as e:
            raise click.ClickException(f"Failed to clear cache: {str(e)}")

    @proxy.command()
    def cache_stats():
        """Show semantic cache statistics.
        
        Example:
            synthlang proxy cache-stats
        """
        try:
            from synthlang.proxy.cache import get_semantic_cache
            
            cache = get_semantic_cache()
            stats = cache.get_stats()
            
            click.echo("\nCache Statistics:")
            click.echo(f"Total entries: {stats['total_entries']}")
            click.echo(f"Total size: {stats['total_size_bytes'] / 1024:.1f} KB")
            click.echo(f"Expired entries: {stats['expired_entries']}")
            click.echo(f"Cache directory: {stats['cache_dir']}")
            click.echo(f"Default TTL: {stats['default_ttl']} seconds")
        except Exception as e:
            raise click.ClickException(f"Failed to get cache stats: {str(e)}")

    @proxy.command()
    def tools():
        """List available agent tools.
        
        Example:
            synthlang proxy tools
        """
        try:
            from synthlang.proxy.agents.registry import list_tools, get_tool_schema
            
            tool_names = list_tools()
            
            if not tool_names:
                click.echo("No tools registered")
                return
            
            click.echo(f"\nAvailable Tools ({len(tool_names)}):")
            for name in sorted(tool_names):
                try:
                    schema = get_tool_schema(name)
                    description = schema.get("description", "No description")
                    click.echo(f"\n{name}:")
                    click.echo(f"  Description: {description}")
                    
                    # Show parameters
                    params = schema.get("parameters", {})
                    if params:
                        click.echo("  Parameters:")
                        for param_name, param_info in params.items():
                            required = "required" if param_info.get("required", False) else "optional"
                            param_type = param_info.get("type", "any")
                            click.echo(f"    {param_name} ({param_type}, {required})")
                except Exception as e:
                    click.echo(f"{name}: Error getting schema - {str(e)}")
        except Exception as e:
            raise click.ClickException(f"Failed to list tools: {str(e)}")

    @proxy.command()
    @click.option("--tool", required=True, help="Tool name")
    @click.option("--args", required=True, help="JSON-encoded arguments")
    def call_tool(tool: str, args: str):
        """Call an agent tool with arguments.
        
        Example:
            synthlang proxy call-tool --tool "calculate" --args '{"expression": "2 + 2"}'
        """
        try:
            from synthlang.proxy.agents.registry import call_tool_with_json
            
            result = call_tool_with_json(tool, args)
            click.echo(f"Result: {json.dumps(result, indent=2)}")
        except Exception as e:
            raise click.ClickException(f"Tool call failed: {str(e)}")

    @proxy.command()
    def health():
        """Check the health of the proxy service.
        
        Example:
            synthlang proxy health
        """
        try:
            from synthlang.proxy.api import ProxyClient
            from synthlang.proxy.auth import get_credentials
            from synthlang.proxy.config import get_proxy_config
            
            config = get_proxy_config()
            creds = get_credentials()
            
            if "api_key" not in creds:
                raise click.ClickException(
                    "No API key found. Run 'synthlang proxy login' first."
                )
            
            endpoint = creds.get("endpoint", config.endpoint)
            client = ProxyClient(endpoint, creds["api_key"])
            
            response = client.health_check()
            click.echo(f"Proxy service is healthy")
            click.echo(f"Status: {response.get('status', 'unknown')}")
            click.echo(f"Version: {response.get('version', 'unknown')}")
        except Exception as e:
            raise click.ClickException(f"Health check failed: {str(e)}")

    return proxy