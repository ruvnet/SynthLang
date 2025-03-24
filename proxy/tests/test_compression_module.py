"""
Tests for the modular SynthLang compression system.

This module contains tests for the new modular compression system.
"""
import pytest
import gzip
import base64
import re
from unittest.mock import patch, MagicMock

from src.app.synthlang.compression import (
    compress_prompt,
    decompress_prompt,
    is_synthlang_available,
    set_synthlang_enabled,
    ENABLE_SYNTHLANG,
    registry,
    BaseCompressor,
    CompressionResult,
    BasicCompressor,
    SymbolCompressor,
    GzipCompressor,
    VowelRemovalCompressor,
    AbbreviationCompressor
)


def test_registry_operations():
    """Test registry operations."""
    # Create a test compressor
    class TestCompressor(BaseCompressor):
        def compress(self, text):
            return CompressionResult(True, f"compressed:{text}", {}, None)
        
        def decompress(self, text):
            if text.startswith("compressed:"):
                return CompressionResult(True, text[11:], {}, None)
            return CompressionResult(False, text, {}, "Not a compressed text")
    
    # Register the test compressor
    registry.register("test", TestCompressor)
    
    # Check if it's registered
    assert "test" in registry
    
    # Get the compressor class
    compressor_class = registry.get("test")
    assert compressor_class == TestCompressor
    
    # Create an instance and test it
    compressor = compressor_class()
    result = compressor.compress("hello")
    assert result.success
    assert result.text == "compressed:hello"
    
    # Unregister the compressor
    registry.unregister("test")
    assert "test" not in registry


def test_base_compressor_methods():
    """Test BaseCompressor helper methods."""
    class TestCompressor(BaseCompressor):
        def compress(self, text):
            return self._create_success_result(f"compressed:{text}", {"metric": 123})
        
        def decompress(self, text):
            if not text.startswith("compressed:"):
                return self._create_error_result(text, "Not a compressed text")
            return self._create_success_result(text[11:])
    
    compressor = TestCompressor()
    
    # Test success result
    success_result = compressor._create_success_result("test", {"key": "value"})
    assert success_result.success
    assert success_result.text == "test"
    assert success_result.metrics == {"key": "value"}
    assert success_result.error is None
    
    # Test error result
    error_result = compressor._create_error_result("original", "Error message")
    assert not error_result.success
    assert error_result.text == "original"
    assert error_result.metrics == {}
    assert error_result.error == "Error message"
    
    # Test compress and decompress
    compress_result = compressor.compress("hello")
    assert compress_result.success
    assert compress_result.text == "compressed:hello"
    assert compress_result.metrics == {"metric": 123}
    
    decompress_result = compressor.decompress("compressed:hello")
    assert decompress_result.success
    assert decompress_result.text == "hello"
    
    error_decompress = compressor.decompress("not_compressed")
    assert not error_decompress.success
    assert error_decompress.text == "not_compressed"
    assert error_decompress.error == "Not a compressed text"


def test_basic_compressor():
    """Test BasicCompressor."""
    compressor = BasicCompressor()
    
    # Test with normal text
    text = "This   is  a   test   with   extra   spaces."
    result = compressor.compress(text)
    assert result.success
    assert result.text == "This is a test with extra spaces."
    assert result.metrics["original_length"] == len(text)
    assert result.metrics["compressed_length"] == len(result.text)
    
    # Test with empty text
    empty_result = compressor.compress("")
    assert empty_result.success
    assert empty_result.text == ""
    
    # Test decompression (which is a no-op for BasicCompressor)
    decompress_result = compressor.decompress("Test text")
    assert decompress_result.success
    assert decompress_result.text == "Test text"


def test_abbreviation_compressor():
    """Test AbbreviationCompressor."""
    compressor = AbbreviationCompressor()
    
    # Test with abbreviatable text
    text = "This is the information about the function implementation."
    result = compressor.compress(text)
    assert result.success
    assert "t " in result.text  # "the" should be replaced with "t"
    assert "info" in result.text  # "information" should be replaced with "info"
    assert "fn" in result.text  # "function" should be replaced with "fn"
    assert "impl" in result.text  # "implementation" should be replaced with "impl"
    
    # Test decompression
    decompress_result = compressor.decompress(result.text)
    assert decompress_result.success
    # The decompression won't be perfect due to ambiguities, but should contain expanded words
    assert "the" in decompress_result.text
    assert "information" in decompress_result.text
    assert "function" in decompress_result.text
    assert "implementation" in decompress_result.text


def test_vowel_removal_compressor():
    """Test VowelRemovalCompressor."""
    compressor = VowelRemovalCompressor(min_word_length=4, preserve_first_vowel=True)
    
    # Test with text containing words that can have vowels removed
    text = "Testing the vowel removal algorithm implementation"
    result = compressor.compress(text)
    assert result.success
    
    # Check that vowels were removed from longer words
    assert "Tstng" in result.text or "Tsting" in result.text  # "Testing" with vowels removed
    assert "lgrthm" in result.text or "algrthm" in result.text  # "algorithm" with vowels removed
    assert "mplmntn" in result.text or "implmntn" in result.text  # "implementation" with vowels removed
    
    # Check that short words and excluded words are preserved
    assert "the" in result.text  # "the" should be preserved
    
    # Test decompression (which is not fully reversible)
    decompress_result = compressor.decompress(result.text)
    assert decompress_result.success
    assert decompress_result.text == result.text  # Should return the same text


def test_symbol_compressor():
    """Test SymbolCompressor."""
    compressor = SymbolCompressor()
    
    # Test with text containing patterns that can be symbolized
    text = "input data and process algorithm to output results"
    result = compressor.compress(text)
    assert result.success
    
    # The text should contain SynthLang symbols
    from src.app.synthlang.core import SynthLangSymbols
    assert SynthLangSymbols.INPUT in result.text
    assert SynthLangSymbols.PROCESS in result.text
    assert SynthLangSymbols.TRANSFORM in result.text
    
    # Test decompression
    decompress_result = compressor.decompress(result.text)
    assert decompress_result.success
    # The decompression should restore the original pattern
    assert "input" in decompress_result.text.lower()
    assert "process" in decompress_result.text.lower()
    assert "output" in decompress_result.text.lower()


def test_gzip_compressor():
    """Test GzipCompressor."""
    compressor = GzipCompressor()
    
    # Test with normal text
    text = "This is a test text for gzip compression. " * 10  # Repeat to make it more compressible
    result = compressor.compress(text)
    assert result.success
    assert result.text.startswith("gz:")
    assert len(result.text) < len(text)  # Should be shorter
    
    # Test decompression
    decompress_result = compressor.decompress(result.text)
    assert decompress_result.success
    assert decompress_result.text == text  # Should restore the original text exactly
    
    # Test with non-gzipped text
    non_gzip_result = compressor.decompress("This is not gzipped")
    assert non_gzip_result.success
    assert non_gzip_result.text == "This is not gzipped"  # Should return unchanged


def test_compression_pipeline():
    """Test the compression pipeline."""
    # Test with a custom pipeline
    text = "This is a test of the compression pipeline with multiple strategies."
    pipeline = ["basic", "abbreviation", "vowel"]
    
    compressed = compress_prompt(text, use_gzip=False, pipeline=pipeline)
    assert len(compressed) < len(text)
    
    # Test with gzip
    gzipped = compress_prompt(text, use_gzip=True)
    assert gzipped.startswith("gz:")
    assert len(gzipped) < len(text)
    
    # Test decompression
    decompressed = decompress_prompt(compressed)
    # The decompression won't be perfect, but should contain parts of the original
    assert "test" in decompressed.lower() or "tst" in decompressed.lower()
    assert "compression" in decompressed.lower() or "cmprssn" in decompressed.lower()
    
    # Test gzip decompression
    gzip_decompressed = decompress_prompt(gzipped)
    assert "test" in gzip_decompressed.lower() or "tst" in gzip_decompressed.lower()
    assert "compression" in gzip_decompressed.lower() or "cmprssn" in gzip_decompressed.lower()


def test_synthlang_disabled():
    """Test behavior when SynthLang is disabled."""
    # Save original state
    original_state = ENABLE_SYNTHLANG
    
    try:
        # Disable SynthLang
        set_synthlang_enabled(False)
        assert not is_synthlang_available()
        
        text = "This text should not be compressed when SynthLang is disabled."
        compressed = compress_prompt(text)
        assert compressed == text  # Should return the original text unchanged
        
        decompressed = decompress_prompt(compressed)
        assert decompressed == text  # Should return the original text unchanged
    finally:
        # Restore original state
        set_synthlang_enabled(original_state)


def test_error_handling():
    """Test error handling in compression and decompression."""
    # Test compression with a failing compressor
    with patch("src.app.synthlang.compression.registry.get") as mock_get:
        # Set up the mock to return a compressor that raises an exception
        mock_compressor = MagicMock()
        mock_compressor.return_value.compress.side_effect = Exception("Test error")
        mock_get.return_value = mock_compressor
        
        text = "This text should be returned unchanged when compression fails."
        compressed = compress_prompt(text, pipeline=["mock"])
        assert compressed == text  # Should return the original text on error
    
    # Test decompression with a failing compressor
    with patch("src.app.synthlang.compression.registry.get") as mock_get:
        # Set up the mock to return a compressor that raises an exception
        mock_compressor = MagicMock()
        mock_compressor.return_value.decompress.side_effect = Exception("Test error")
        mock_get.return_value = mock_compressor
        
        text = "This text should be returned unchanged when decompression fails."
        decompressed = decompress_prompt(text, pipeline=["mock"])
        assert decompressed == text  # Should return the original text on error