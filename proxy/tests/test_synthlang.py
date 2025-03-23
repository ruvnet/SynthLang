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
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        assert is_synthlang_available() is True
        mock_run.assert_called_once_with(
            ["synthlang", "--version"],
            capture_output=True,
            text=True,
            check=False
        )


def test_is_synthlang_available_not_found():
    """Test that is_synthlang_available returns False when SynthLang is not found."""
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = FileNotFoundError("No such file or directory")
        assert is_synthlang_available() is False


def test_is_synthlang_available_error():
    """Test that is_synthlang_available returns False when there's an error."""
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=1)
        assert is_synthlang_available() is False


def test_compress_prompt_success():
    """Test that compress_prompt successfully compresses text."""
    original_text = "This is a long text to be compressed."
    compressed_text = "Compressed text"
    
    with patch("subprocess.run") as mock_run:
        mock_process = MagicMock()
        mock_process.stdout = compressed_text
        mock_run.return_value = mock_process
        
        result = compress_prompt(original_text)
        
        assert result == compressed_text
        mock_run.assert_called_once_with(
            ["synthlang", "compress"],
            input=original_text,
            text=True,
            capture_output=True,
            check=True
        )


def test_compress_prompt_with_gzip():
    """Test that compress_prompt with gzip option applies additional compression."""
    original_text = "This is a long text to be compressed with gzip."
    synthlang_compressed = "Compressed text"
    
    with patch("subprocess.run") as mock_run, \
         patch("gzip.compress") as mock_gzip:
        # Mock SynthLang compression
        mock_process = MagicMock()
        mock_process.stdout = synthlang_compressed
        mock_run.return_value = mock_process
        
        # Mock gzip compression
        mock_gzipped_data = b'gzipped data'
        mock_gzip.return_value = mock_gzipped_data
        
        # Mock base64 encoding
        expected_b64 = base64.b64encode(mock_gzipped_data).decode('ascii')
        expected_result = f"gz:{expected_b64}"
        
        # Call the function with gzip=True
        result = compress_prompt(original_text, use_gzip=True)
        
        # Verify the result
        assert result == expected_result
        
        # Verify SynthLang was called
        mock_run.assert_called_once_with(
            ["synthlang", "compress"],
            input=original_text,
            text=True,
            capture_output=True,
            check=True
        )
        
        # Verify gzip was called with the SynthLang compressed text
        mock_gzip.assert_called_once_with(synthlang_compressed.encode('utf-8'))


def test_compress_prompt_gzip_error_fallback():
    """Test that compress_prompt falls back to regular compression if gzip fails."""
    original_text = "This is a text that will cause gzip to fail."
    synthlang_compressed = "Compressed text"
    
    with patch("subprocess.run") as mock_run, \
         patch("gzip.compress") as mock_gzip:
        # Mock SynthLang compression
        mock_process = MagicMock()
        mock_process.stdout = synthlang_compressed
        mock_run.return_value = mock_process
        
        # Mock gzip compression to fail
        mock_gzip.side_effect = Exception("Gzip error")
        
        # Call the function with gzip=True
        result = compress_prompt(original_text, use_gzip=True)
        
        # Should fall back to regular SynthLang compression
        assert result == synthlang_compressed


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
    
    with patch("subprocess.run") as mock_run:
        mock_process = MagicMock()
        mock_process.stdout = ""  # Empty result
        mock_run.return_value = mock_process
        
        result = compress_prompt(original_text)
        
        assert result == original_text


def test_compress_prompt_file_not_found():
    """Test that compress_prompt returns original text when SynthLang CLI is not found."""
    original_text = "This is a text that won't be compressed due to missing CLI."
    
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = FileNotFoundError("No such file or directory")
        
        result = compress_prompt(original_text)
        
        assert result == original_text


def test_compress_prompt_process_error():
    """Test that compress_prompt returns original text when subprocess raises an error."""
    original_text = "This is a text that won't be compressed due to process error."
    
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = subprocess.CalledProcessError(1, "synthlang compress", stderr="Error")
        
        result = compress_prompt(original_text)
        
        assert result == original_text


def test_decompress_prompt_success():
    """Test that decompress_prompt successfully decompresses text."""
    compressed_text = "Compressed text"
    decompressed_text = "This is the original decompressed text."
    
    with patch("subprocess.run") as mock_run:
        mock_process = MagicMock()
        mock_process.stdout = decompressed_text
        mock_run.return_value = mock_process
        
        result = decompress_prompt(compressed_text)
        
        assert result == decompressed_text
        mock_run.assert_called_once_with(
            ["synthlang", "decompress"],
            input=compressed_text,
            text=True,
            capture_output=True,
            check=True
        )


def test_decompress_prompt_with_gzip():
    """Test that decompress_prompt automatically decompresses gzipped content."""
    original_text = "Original decompressed text"
    synthlang_compressed = "Synthlang compressed text"
    
    # Create a gzipped version of the synthlang compressed text
    gzipped_data = gzip.compress(synthlang_compressed.encode('utf-8'))
    b64_data = base64.b64encode(gzipped_data).decode('ascii')
    gzipped_input = f"gz:{b64_data}"
    
    with patch("subprocess.run") as mock_run, \
         patch("gzip.decompress") as mock_gzip_decompress:
        # Mock gzip decompression
        mock_gzip_decompress.return_value = synthlang_compressed.encode('utf-8')
        
        # Mock SynthLang decompression
        mock_process = MagicMock()
        mock_process.stdout = original_text
        mock_run.return_value = mock_process
        
        # Call the function with gzipped input
        result = decompress_prompt(gzipped_input)
        
        # Verify the result
        assert result == original_text
        
        # Verify gzip.decompress was called
        mock_gzip_decompress.assert_called_once()
        
        # Verify SynthLang was called with the ungzipped text
        mock_run.assert_called_once_with(
            ["synthlang", "decompress"],
            input=synthlang_compressed,
            text=True,
            capture_output=True,
            check=True
        )


def test_decompress_prompt_gzip_error_fallback():
    """Test that decompress_prompt falls back to regular decompression if gzip fails."""
    gzipped_input = "gz:invalid_base64_data"
    
    with patch("subprocess.run") as mock_run:
        mock_process = MagicMock()
        mock_process.stdout = "Decompressed text"
        mock_run.return_value = mock_process
        
        # Should attempt to decompress with SynthLang after gzip fails
        result = decompress_prompt(gzipped_input)
        
        assert result == "Decompressed text"
        mock_run.assert_called_once()


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
    
    with patch("subprocess.run") as mock_run:
        mock_process = MagicMock()
        mock_process.stdout = ""  # Empty result
        mock_run.return_value = mock_process
        
        result = decompress_prompt(compressed_text)
        
        assert result == compressed_text


def test_decompress_prompt_file_not_found():
    """Test that decompress_prompt returns original text when SynthLang CLI is not found."""
    compressed_text = "This is a text that won't be decompressed due to missing CLI."
    
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = FileNotFoundError("No such file or directory")
        
        result = decompress_prompt(compressed_text)
        
        assert result == compressed_text


def test_decompress_prompt_process_error():
    """Test that decompress_prompt returns original text when subprocess raises an error."""
    compressed_text = "This is a text that won't be decompressed due to process error."
    
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = subprocess.CalledProcessError(1, "synthlang decompress", stderr="Error")
        
        result = decompress_prompt(compressed_text)
        
        assert result == compressed_text


def test_round_trip_compression_decompression():
    """Test that text compressed and then decompressed returns to the original."""
    original_text = "This is a text to test round-trip compression and decompression."
    compressed_text = "Compressed version"
    
    with patch("subprocess.run") as mock_run:
        # Mock compression
        mock_process_compress = MagicMock()
        mock_process_compress.stdout = compressed_text
        
        # Mock decompression to return the original text
        mock_process_decompress = MagicMock()
        mock_process_decompress.stdout = original_text
        
        # Set up the mock to return different values on successive calls
        mock_run.side_effect = [mock_process_compress, mock_process_decompress]
        
        # Compress the text
        compressed = compress_prompt(original_text)
        assert compressed == compressed_text
        
        # Decompress the text
        decompressed = decompress_prompt(compressed)
        assert decompressed == original_text


def test_round_trip_with_gzip():
    """Test round-trip compression and decompression with gzip."""
    original_text = "This is a text to test round-trip compression and decompression with gzip."
    synthlang_compressed = "Synthlang compressed version"
    
    with patch("subprocess.run") as mock_run, \
         patch("gzip.compress") as mock_gzip_compress, \
         patch("gzip.decompress") as mock_gzip_decompress:
        
        # Mock SynthLang compression
        mock_process_compress = MagicMock()
        mock_process_compress.stdout = synthlang_compressed
        
        # Mock SynthLang decompression
        mock_process_decompress = MagicMock()
        mock_process_decompress.stdout = original_text
        
        # Set up the subprocess mock to return different values on successive calls
        mock_run.side_effect = [mock_process_compress, mock_process_decompress]
        
        # Mock gzip compression
        gzipped_data = b'gzipped data'
        mock_gzip_compress.return_value = gzipped_data
        
        # Mock gzip decompression to return the synthlang compressed text
        mock_gzip_decompress.return_value = synthlang_compressed.encode('utf-8')
        
        # Compress with gzip
        compressed = compress_prompt(original_text, use_gzip=True)
        
        # Verify it starts with the gzip prefix
        assert compressed.startswith("gz:")
        
        # Decompress
        decompressed = decompress_prompt(compressed)
        
        # Verify we got the original text back
        assert decompressed == original_text
        
        # Verify the correct sequence of calls
        assert mock_gzip_compress.called
        assert mock_gzip_decompress.called
        assert mock_run.call_count == 2