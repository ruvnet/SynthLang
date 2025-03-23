"""
SynthLang integration module.

This module provides integration with SynthLang for advanced prompt engineering capabilities.
"""
from app.synthlang.compression import (
    compress_prompt,
    decompress_prompt,
    is_synthlang_available,
    set_synthlang_enabled,
    ENABLE_SYNTHLANG
)

__all__ = [
    'compress_prompt',
    'decompress_prompt',
    'is_synthlang_available',
    'set_synthlang_enabled',
    'ENABLE_SYNTHLANG'
]