"""File manipulation tools for SynthLang agents."""
import os
import json
from pathlib import Path
from typing import List, Optional, Dict, Any, Union

from synthlang.proxy.agents.registry import register_tool
from synthlang.utils.logger import get_logger

logger = get_logger(__name__)


@register_tool(description="Read the contents of a file")
def read_file(path: str) -> str:
    """Read the contents of a file.
    
    Args:
        path: Path to the file
        
    Returns:
        File contents as a string
        
    Raises:
        FileNotFoundError: If file does not exist
        PermissionError: If permission denied
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        logger.debug(f"Read file: {path}")
        return content
    except UnicodeDecodeError:
        logger.warning(f"File is not text: {path}")
        raise ValueError(f"File is not a text file: {path}")


@register_tool(description="Write content to a file")
def write_file(path: str, content: str, append: bool = False) -> bool:
    """Write content to a file.
    
    Args:
        path: Path to the file
        content: Content to write
        append: Whether to append to the file
        
    Returns:
        True if successful
        
    Raises:
        PermissionError: If permission denied
    """
    mode = 'a' if append else 'w'
    try:
        with open(path, mode, encoding='utf-8') as f:
            f.write(content)
        logger.debug(f"Wrote to file: {path}")
        return True
    except Exception as e:
        logger.error(f"Error writing to file {path}: {str(e)}")
        raise


@register_tool(description="List files in a directory")
def list_files(directory: str, pattern: Optional[str] = None) -> List[str]:
    """List files in a directory.
    
    Args:
        directory: Directory path
        pattern: Optional glob pattern to filter files
        
    Returns:
        List of file paths
        
    Raises:
        FileNotFoundError: If directory does not exist
        PermissionError: If permission denied
    """
    try:
        path = Path(directory)
        if pattern:
            files = list(path.glob(pattern))
        else:
            files = list(path.iterdir())
        
        # Convert to strings and sort
        file_paths = [str(f) for f in files]
        file_paths.sort()
        
        logger.debug(f"Listed {len(file_paths)} files in {directory}")
        return file_paths
    except Exception as e:
        logger.error(f"Error listing files in {directory}: {str(e)}")
        raise


@register_tool(description="Check if a file exists")
def file_exists(path: str) -> bool:
    """Check if a file exists.
    
    Args:
        path: Path to the file
        
    Returns:
        True if file exists, False otherwise
    """
    return os.path.isfile(path)


@register_tool(description="Get file information")
def file_info(path: str) -> Dict[str, Any]:
    """Get information about a file.
    
    Args:
        path: Path to the file
        
    Returns:
        Dictionary with file information
        
    Raises:
        FileNotFoundError: If file does not exist
        PermissionError: If permission denied
    """
    try:
        stat = os.stat(path)
        file_path = Path(path)
        
        return {
            "name": file_path.name,
            "path": str(file_path.absolute()),
            "size": stat.st_size,
            "created": stat.st_ctime,
            "modified": stat.st_mtime,
            "accessed": stat.st_atime,
            "is_directory": os.path.isdir(path),
            "extension": file_path.suffix,
        }
    except Exception as e:
        logger.error(f"Error getting file info for {path}: {str(e)}")
        raise


@register_tool(description="Read JSON from a file")
def read_json(path: str) -> Dict[str, Any]:
    """Read JSON from a file.
    
    Args:
        path: Path to the JSON file
        
    Returns:
        Parsed JSON data
        
    Raises:
        FileNotFoundError: If file does not exist
        json.JSONDecodeError: If JSON is invalid
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.debug(f"Read JSON from file: {path}")
        return data
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in file {path}: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error reading JSON from {path}: {str(e)}")
        raise


@register_tool(description="Write JSON to a file")
def write_json(path: str, data: Union[Dict[str, Any], List[Any]], indent: int = 2) -> bool:
    """Write JSON to a file.
    
    Args:
        path: Path to the file
        data: Data to write as JSON
        indent: Indentation level
        
    Returns:
        True if successful
        
    Raises:
        PermissionError: If permission denied
        TypeError: If data is not JSON serializable
    """
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent)
        logger.debug(f"Wrote JSON to file: {path}")
        return True
    except TypeError as e:
        logger.error(f"Data is not JSON serializable: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error writing JSON to {path}: {str(e)}")
        raise