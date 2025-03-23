"""
Keyword pattern registry for the SynthLang Proxy.

This module provides a registry for keyword patterns and functions for
detecting keywords in user messages.
"""
import re
import logging
import os
from typing import Dict, List, Optional, Tuple, Pattern, Any, Callable, Set
import json
from dataclasses import dataclass, field, asdict
from contextlib import contextmanager

# Logger for this module
logger = logging.getLogger(__name__)

@dataclass
class KeywordPattern:
    """
    A pattern for detecting keywords in user messages.
    
    Attributes:
        name: The name of the pattern
        pattern: The regex pattern to match
        tool: The name of the tool to invoke when the pattern matches
        description: A description of what the pattern detects
        required_role: The role required to use this pattern (optional)
        priority: The priority of the pattern (higher values are checked first)
        enabled: Whether the pattern is enabled
        _compiled_pattern: The compiled regex pattern (internal use)
    """
    name: str
    pattern: str
    tool: str
    description: str
    required_role: Optional[str] = None
    priority: int = 0
    enabled: bool = True
    _compiled_pattern: Optional[Pattern] = field(default=None, repr=False)
    
    def __post_init__(self):
        """Compile the regex pattern after initialization."""
        self.compile_pattern()
    
    def compile_pattern(self) -> None:
        """Compile the regex pattern for efficient matching."""
        try:
            self._compiled_pattern = re.compile(self.pattern, re.IGNORECASE)
        except re.error as e:
            logger.error(f"Invalid regex pattern '{self.pattern}' for keyword '{self.name}': {e}")
            self._compiled_pattern = None
    
    def match(self, text: str) -> Optional[re.Match]:
        """
        Check if the pattern matches the given text.
        
        Args:
            text: The text to check
            
        Returns:
            A match object if the pattern matches, None otherwise
        """
        if not self._compiled_pattern or not self.enabled:
            return None
        
        return self._compiled_pattern.search(text)
    
    def extract_params(self, match: re.Match) -> Dict[str, str]:
        """
        Extract parameters from a regex match.
        
        Args:
            match: The regex match object
            
        Returns:
            A dictionary of parameter names and values
        """
        # Extract named groups from the match
        params = match.groupdict()
        
        # If no named groups, use numbered groups
        if not params:
            params = {str(i): group for i, group in enumerate(match.groups(), 1)}
        
        return params
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the pattern to a dictionary for serialization."""
        # Use asdict but exclude the compiled pattern
        data = asdict(self)
        data.pop('_compiled_pattern', None)
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'KeywordPattern':
        """Create a pattern from a dictionary."""
        # Remove any extra fields not in the class
        valid_fields = {f.name for f in field(cls)}
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}
        
        # Create the pattern
        pattern = cls(**filtered_data)
        return pattern


# Global registry of keyword patterns
KEYWORD_REGISTRY: Dict[str, KeywordPattern] = {}

# Threshold for keyword detection confidence (0.0 to 1.0)
DETECTION_THRESHOLD = float(os.getenv("KEYWORD_DETECTION_THRESHOLD", "0.7"))

# Enable/disable keyword detection
ENABLE_KEYWORD_DETECTION = os.getenv("ENABLE_KEYWORD_DETECTION", "1").lower() in ("1", "true", "yes")


def register_pattern(pattern: KeywordPattern) -> None:
    """
    Register a keyword pattern in the registry.
    
    Args:
        pattern: The pattern to register
    """
    if not pattern.name:
        logger.error("Cannot register pattern with empty name")
        return
    
    # Ensure the pattern is compiled
    if not pattern._compiled_pattern:
        pattern.compile_pattern()
        if not pattern._compiled_pattern:
            logger.error(f"Failed to compile pattern '{pattern.name}', not registering")
            return
    
    # Add to registry
    KEYWORD_REGISTRY[pattern.name] = pattern
    logger.info(f"Registered keyword pattern '{pattern.name}' for tool '{pattern.tool}'")


def get_pattern(name: str) -> Optional[KeywordPattern]:
    """
    Get a pattern from the registry by name.
    
    Args:
        name: The name of the pattern
        
    Returns:
        The pattern if found, None otherwise
    """
    return KEYWORD_REGISTRY.get(name)


def list_patterns() -> List[KeywordPattern]:
    """
    List all patterns in the registry.
    
    Returns:
        A list of all registered patterns
    """
    return list(KEYWORD_REGISTRY.values())


@contextmanager
def disable_keyword_detection():
    """
    Context manager to temporarily disable keyword detection.
    
    This is useful for testing where you want to bypass the keyword detection system.
    
    Example:
        with disable_keyword_detection():
            # Keyword detection is disabled here
            result = process_message_with_keywords(message, user_id)
        # Keyword detection is re-enabled here
    """
    global ENABLE_KEYWORD_DETECTION
    original_value = ENABLE_KEYWORD_DETECTION
    ENABLE_KEYWORD_DETECTION = False
    try:
        yield
    finally:
        ENABLE_KEYWORD_DETECTION = original_value


def detect_keywords(text: str, user_roles: Optional[Set[str]] = None) -> List[Tuple[KeywordPattern, Dict[str, str]]]:
    """
    Detect keywords in a text and return matching patterns with extracted parameters.
    
    Args:
        text: The text to analyze
        user_roles: The roles of the user (for role-based filtering)
        
    Returns:
        A list of tuples containing the matching pattern and extracted parameters
    """
    if not ENABLE_KEYWORD_DETECTION:
        logger.debug("Keyword detection is disabled")
        return []
    
    if not text:
        return []
    
    # Default to empty set if no roles provided
    user_roles = user_roles or set()
    
    # Get all patterns sorted by priority (highest first)
    patterns = sorted(
        KEYWORD_REGISTRY.values(),
        key=lambda p: p.priority,
        reverse=True
    )
    
    # Filter out disabled patterns
    patterns = [p for p in patterns if p.enabled]
    
    # Filter out patterns that require roles the user doesn't have
    patterns = [
        p for p in patterns 
        if not p.required_role or p.required_role in user_roles
    ]
    
    # Find matches
    matches = []
    for pattern in patterns:
        match = pattern.match(text)
        if match:
            params = pattern.extract_params(match)
            matches.append((pattern, params))
    
    return matches


def load_patterns_from_file(file_path: str) -> int:
    """
    Load patterns from a JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        The number of patterns loaded
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        count = 0
        for item in data:
            try:
                pattern = KeywordPattern.from_dict(item)
                register_pattern(pattern)
                count += 1
            except Exception as e:
                logger.error(f"Error loading pattern: {e}")
        
        logger.info(f"Loaded {count} patterns from {file_path}")
        return count
    
    except Exception as e:
        logger.error(f"Error loading patterns from {file_path}: {e}")
        return 0


def save_patterns_to_file(file_path: str) -> int:
    """
    Save patterns to a JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        The number of patterns saved
    """
    try:
        patterns = [p.to_dict() for p in KEYWORD_REGISTRY.values()]
        
        with open(file_path, 'w') as f:
            json.dump(patterns, f, indent=2)
        
        logger.info(f"Saved {len(patterns)} patterns to {file_path}")
        return len(patterns)
    
    except Exception as e:
        logger.error(f"Error saving patterns to {file_path}: {e}")
        return 0