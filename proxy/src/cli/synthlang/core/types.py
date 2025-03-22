"""Type definitions for SynthLang modules."""
from typing import Dict, List, TypedDict

class TranslationResult(TypedDict):
    """Result from framework translation."""
    source: str
    target: str
    explanation: str

class GenerationResult(TypedDict):
    """Result from system prompt generation."""
    prompt: str
    rationale: str
    metadata: Dict[str, str]

class OptimizationResult(TypedDict):
    """Result from prompt optimization."""
    optimized: str
    improvements: List[str]
    metrics: Dict[str, float]
    original: str

class SynthLangSymbols:
    """SynthLang syntax symbols."""
    INPUT = "↹"
    PROCESS = "⊕"
    OUTPUT = "Σ"
    JOIN = "•"
    TRANSFORM = "=>"

class FormatRules:
    """SynthLang formatting rules."""
    MAX_LINE_LENGTH = 30
    VALID_OPERATORS = ["+", "-", "*", "/", ">", "<", "^"]
