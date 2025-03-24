"""
SynthLang module.

This module provides tools for natural language processing and generation,
including compression, optimization, and symbolic representation.
"""
from src.app.synthlang.compression import (
    compress_prompt,
    decompress_prompt,
    is_synthlang_available,
    set_synthlang_enabled,
    ENABLE_SYNTHLANG
)