"""
Tests for the SynthLang integration.

This module contains tests for the SynthLang compression and decompression functions.
"""
import pytest
from unittest.mock import patch, MagicMock
import subprocess

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