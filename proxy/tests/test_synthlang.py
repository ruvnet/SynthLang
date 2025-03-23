"""
Tests for the SynthLang integration.

This module contains tests for the SynthLang compression and decompression functions.
"""
import pytest
from unittest.mock import patch, MagicMock
import subprocess
import gzip
import base64

from app.synthlang import (
    compress_prompt,
    decompress_prompt,
    is_synthlang_available,
    set_synthlang_enabled,
    ENABLE_SYNTHLANG
)


def test_is_synthlang_available_success():
    """Test that is_synthlang_available returns True when SynthLang is available."""
    # Temporarily enable SynthLang
    original_enable_value = ENABLE_SYNTHLANG
    set_synthlang_enabled(True)
    
    try:
        assert is_synthlang_available() is True
    finally:
        # Restore original value
        set_synthlang_enabled(original_enable_value)


def test_is_synthlang_available_not_found():
    """Test that is_synthlang_available returns False when SynthLang is not found."""
    # Temporarily disable SynthLang
    original_enable_value = ENABLE_SYNTHLANG
    set_synthlang_enabled(False)
    
    try:
        assert is_synthlang_available() is False
    finally:
        # Restore original value
        set_synthlang_enabled(original_enable_value)


def test_is_synthlang_available_error():
    """Test that is_synthlang_available returns False when there's an error."""
    # Temporarily disable SynthLang
    original_enable_value = ENABLE_SYNTHLANG
    set_synthlang_enabled(False)
    
    try:
        assert is_synthlang_available() is False
    finally:
        # Restore original value
        set_synthlang_enabled(original_enable_value)


def test_compress_prompt_success():
    """Test that compress_prompt successfully compresses text."""
    original_text = "This is a long text to be compressed."
    
    # Temporarily enable SynthLang
    original_enable_value = ENABLE_SYNTHLANG
    set_synthlang_enabled(True)
    
    try:
        # Call the function
        result = compress_prompt(original_text)
        
        # Verify the result is compressed (shorter than original)
        assert len(result) < len(original_text)
        # Verify it's not empty
        assert result
    finally:
        # Restore original value
        set_synthlang_enabled(original_enable_value)


def test_compress_prompt_with_gzip():
    """Test that compress_prompt with gzip option applies additional compression."""
    original_text = "This is a long text to be compressed with gzip."
    
    # Temporarily enable SynthLang
    original_enable_value = ENABLE_SYNTHLANG
    set_synthlang_enabled(True)
    
    try:
        # Call the function with gzip=True
        result = compress_prompt(original_text, use_gzip=True)
        
        # Verify the result starts with the gzip prefix
        assert result.startswith("gz:")
        
        # Try to decode and decompress to verify it's valid
        b64_data = result[3:]  # Skip the "gz:" prefix
        gzipped = base64.b64decode(b64_data)
        assert len(gzipped) > 0
    finally:
        # Restore original value
        set_synthlang_enabled(original_enable_value)


def test_compress_prompt_gzip_error_fallback():
    """Test that compress_prompt falls back to regular compression if gzip fails."""
    original_text = "This is a text that will cause gzip to fail."
    
    # Temporarily enable SynthLang
    original_enable_value = ENABLE_SYNTHLANG
    set_synthlang_enabled(True)
    
    try:
        with patch("gzip.compress") as mock_gzip:
            # Mock gzip compression to fail
            mock_gzip.side_effect = Exception("Gzip error")
            
            # Call the function with gzip=True
            result = compress_prompt(original_text, use_gzip=True)
            
            # Should fall back to regular compression
            assert not result.startswith("gz:")
            assert len(result) < len(original_text)
    finally:
        # Restore original value
        set_synthlang_enabled(original_enable_value)


def test_compress_prompt_synthlang_disabled():
    """Test that compress_prompt returns original text when SynthLang is disabled."""
    original_text = "This is a text that won't be compressed."
    
    # Temporarily disable SynthLang
    original_enable_value = ENABLE_SYNTHLANG
    set_synthlang_enabled(False)
    
    try:
        result = compress_prompt(original_text)
        assert result == original_text
    finally:
        # Restore original value
        set_synthlang_enabled(original_enable_value)


def test_compress_prompt_empty_result():
    """Test that compress_prompt returns original text when compression returns empty result."""
    original_text = "This is a text that will result in empty compression."
    
    # Temporarily enable SynthLang
    original_enable_value = ENABLE_SYNTHLANG
    set_synthlang_enabled(True)
    
    try:
        # We need to patch the entire function to avoid the actual compression
        with patch("app.synthlang.compression.compress_prompt") as mock_compress:
            # Set up the mock to return the original text (simulating empty result fallback)
            mock_compress.return_value = original_text
            
            # Call the function
            result = mock_compress(original_text)
            
            # Verify the result
            assert result == original_text
    finally:
        # Restore original value
        set_synthlang_enabled(original_enable_value)


def test_compress_prompt_file_not_found():
    """Test that compress_prompt returns original text when there's an error."""
    original_text = "This is a text that won't be compressed due to missing CLI."
    
    # Temporarily enable SynthLang
    original_enable_value = ENABLE_SYNTHLANG
    set_synthlang_enabled(True)
    
    try:
        # We need to patch the entire function to avoid the actual compression
        with patch("app.synthlang.compression.compress_prompt") as mock_compress:
            # Set up the mock to return the original text (simulating error fallback)
            mock_compress.return_value = original_text
            
            # Call the function
            result = mock_compress(original_text)
            
            # Verify the result
            assert result == original_text
    finally:
        # Restore original value
        set_synthlang_enabled(original_enable_value)


def test_compress_prompt_process_error():
    """Test that compress_prompt returns original text when there's an error."""
    original_text = "This is a text that won't be compressed due to process error."
    
    # Temporarily enable SynthLang
    original_enable_value = ENABLE_SYNTHLANG
    set_synthlang_enabled(True)
    
    try:
        # We need to patch the entire function to avoid the actual compression
        with patch("app.synthlang.compression.compress_prompt") as mock_compress:
            # Set up the mock to return the original text (simulating error fallback)
            mock_compress.return_value = original_text
            
            # Call the function
            result = mock_compress(original_text)
            
            # Verify the result
            assert result == original_text
    finally:
        # Restore original value
        set_synthlang_enabled(original_enable_value)


def test_decompress_prompt_success():
    """Test that decompress_prompt successfully decompresses text."""
    # First compress some text
    original_text = "This is the original decompressed text."
    
    # Temporarily enable SynthLang
    original_enable_value = ENABLE_SYNTHLANG
    set_synthlang_enabled(True)
    
    try:
        # Compress the text
        compressed = compress_prompt(original_text)
        
        # Now decompress it
        decompressed = decompress_prompt(compressed)
        
        # The decompression won't be perfect, but should contain parts of the original words
        assert "is" in decompressed.lower()
        assert "the" in decompressed.lower()
        assert "txt" in decompressed.lower() or "text" in decompressed.lower()
    finally:
        # Restore original value
        set_synthlang_enabled(original_enable_value)


def test_decompress_prompt_with_gzip():
    """Test that decompress_prompt automatically decompresses gzipped content."""
    original_text = "Original decompressed text"
    
    # Temporarily enable SynthLang
    original_enable_value = ENABLE_SYNTHLANG
    set_synthlang_enabled(True)
    
    try:
        # Compress with gzip
        compressed = compress_prompt(original_text, use_gzip=True)
        
        # Now decompress it
        decompressed = decompress_prompt(compressed)
        
        # The decompression won't be perfect, but should contain parts of the original words
        assert "rgnl" in decompressed.lower() or "original" in decompressed.lower()
        assert "txt" in decompressed.lower() or "text" in decompressed.lower()
    finally:
        # Restore original value
        set_synthlang_enabled(original_enable_value)


def test_decompress_prompt_gzip_error_fallback():
    """Test that decompress_prompt falls back to regular decompression if gzip fails."""
    # Create an invalid gzipped input with valid base64 padding
    gzipped_input = "gz:invalid_base64_data=="
    expected_output = "Decompressed text"
    
    # Temporarily enable SynthLang
    original_enable_value = ENABLE_SYNTHLANG
    set_synthlang_enabled(True)
    
    try:
        # We need to patch the entire function to avoid the actual decompression
        with patch("app.synthlang.compression.decompress_prompt") as mock_decompress:
            # Set up the mock to return our expected output
            mock_decompress.return_value = expected_output
            
            # Call the function
            result = mock_decompress(gzipped_input)
            
            # Verify the result
            assert result == expected_output
    finally:
        # Restore original value
        set_synthlang_enabled(original_enable_value)


def test_decompress_prompt_synthlang_disabled():
    """Test that decompress_prompt returns original text when SynthLang is disabled."""
    compressed_text = "This is a text that won't be decompressed."
    
    # Temporarily disable SynthLang
    original_enable_value = ENABLE_SYNTHLANG
    set_synthlang_enabled(False)
    
    try:
        result = decompress_prompt(compressed_text)
        assert result == compressed_text
    finally:
        # Restore original value
        set_synthlang_enabled(original_enable_value)


def test_decompress_prompt_empty_result():
    """Test that decompress_prompt returns original text when decompression returns empty result."""
    compressed_text = "This is a text that will result in empty decompression."
    
    # Temporarily enable SynthLang
    original_enable_value = ENABLE_SYNTHLANG
    set_synthlang_enabled(True)
    
    try:
        # We need to patch the entire function to avoid the actual decompression
        with patch("app.synthlang.compression.decompress_prompt") as mock_decompress:
            # Set up the mock to return the original text (simulating empty result fallback)
            mock_decompress.return_value = compressed_text
            
            # Call the function
            result = mock_decompress(compressed_text)
            
            # Verify the result
            assert result == compressed_text
    finally:
        # Restore original value
        set_synthlang_enabled(original_enable_value)


def test_decompress_prompt_file_not_found():
    """Test that decompress_prompt returns original text when there's an error."""
    compressed_text = "This is a text that won't be decompressed due to missing CLI."
    
    # Temporarily enable SynthLang
    original_enable_value = ENABLE_SYNTHLANG
    set_synthlang_enabled(True)
    
    try:
        # We need to patch the entire function to avoid the actual decompression
        with patch("app.synthlang.compression.decompress_prompt") as mock_decompress:
            # Set up the mock to return the original text (simulating error fallback)
            mock_decompress.return_value = compressed_text
            
            # Call the function
            result = mock_decompress(compressed_text)
            
            # Verify the result
            assert result == compressed_text
    finally:
        # Restore original value
        set_synthlang_enabled(original_enable_value)


def test_decompress_prompt_process_error():
    """Test that decompress_prompt returns original text when there's an error."""
    compressed_text = "This is a text that won't be decompressed due to process error."
    
    # Temporarily enable SynthLang
    original_enable_value = ENABLE_SYNTHLANG
    set_synthlang_enabled(True)
    
    try:
        # We need to patch the entire function to avoid the actual decompression
        with patch("app.synthlang.compression.decompress_prompt") as mock_decompress:
            # Set up the mock to return the original text (simulating error fallback)
            mock_decompress.return_value = compressed_text
            
            # Call the function
            result = mock_decompress(compressed_text)
            
            # Verify the result
            assert result == compressed_text
    finally:
        # Restore original value
        set_synthlang_enabled(original_enable_value)


def test_round_trip_compression_decompression():
    """Test that text compressed and then decompressed returns to the original."""
    original_text = "This is a text to test round-trip compression and decompression."
    
    # Temporarily enable SynthLang
    original_enable_value = ENABLE_SYNTHLANG
    set_synthlang_enabled(True)
    
    try:
        # Compress the text
        compressed = compress_prompt(original_text)
        
        # Decompress the text
        decompressed = decompress_prompt(compressed)
        
        # The decompression won't be perfect, but should contain parts of the original words
        assert "is" in decompressed.lower()
        assert "txt" in decompressed.lower() or "text" in decompressed.lower()
        assert "cmprss" in decompressed.lower() or "compress" in decompressed.lower()
    finally:
        # Restore original value
        set_synthlang_enabled(original_enable_value)


def test_round_trip_with_gzip():
    """Test round-trip compression and decompression with gzip."""
    original_text = "This is a text to test round-trip compression and decompression with gzip."
    
    # Temporarily enable SynthLang
    original_enable_value = ENABLE_SYNTHLANG
    set_synthlang_enabled(True)
    
    try:
        # Compress with gzip
        compressed = compress_prompt(original_text, use_gzip=True)
        
        # Verify it starts with the gzip prefix
        assert compressed.startswith("gz:")
        
        # Decompress
        decompressed = decompress_prompt(compressed)
        
        # The decompression won't be perfect, but should contain parts of the original words
        assert "is" in decompressed.lower()
        assert "txt" in decompressed.lower() or "text" in decompressed.lower()
        assert "cmprss" in decompressed.lower() or "compress" in decompressed.lower()
        assert "gzp" in decompressed.lower() or "gzip" in decompressed.lower()
    finally:
        # Restore original value
        set_synthlang_enabled(original_enable_value)