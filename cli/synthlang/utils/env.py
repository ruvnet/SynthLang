"""Environment variable utilities."""
from pathlib import Path
from typing import Dict

def load_env_file(env_path: Path) -> Dict[str, str]:
    """Load environment variables from a .env file.
    
    Args:
        env_path: Path to the .env file
        
    Returns:
        Dictionary of environment variables
    """
    if not env_path.exists():
        return {}

    env_vars = {}
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            # Handle basic variable assignment
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                # Remove quotes if present
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                    
                env_vars[key] = value
                
    return env_vars
