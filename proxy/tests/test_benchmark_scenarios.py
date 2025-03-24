"""
Tests for benchmark scenarios.

This module contains tests for the specific benchmark scenarios.
"""
import pytest
from unittest.mock import patch, MagicMock
import os
import sys
from datetime import datetime

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from app.benchmark.scenarios.compression import CompressionBenchmark, get_sample_text, count_tokens


def test_get_sample_text():
    """Test that get_sample_text returns text of the correct type and length."""
    # Get a general text
    text = get_sample_text(text_type="general", min_length=100, max_length=1000)
    assert isinstance(text, str)
    assert len(text) >= 100
    assert len(text) <= 1000
    
    # Get a technical text
    text = get_sample_text(text_type="technical", min_length=200, max_length=500)
    assert isinstance(text, str)
    assert len(text) >= 200
    assert len(text) <= 500
    
    # Get a creative text
    text = get_sample_text(text_type="creative", min_length=150, max_length=300)
    assert isinstance(text, str)
    assert len(text) >= 150
    assert len(text) <= 300
    
    # Get a code text
    text = get_sample_text(text_type="code", min_length=300, max_length=1000)
    assert isinstance(text, str)
    assert len(text) >= 300
    assert len(text) <= 1000


def test_count_tokens():
    """Test that count_tokens returns a reasonable token count."""
    # Count tokens in a short text
    text = "This is a short text."
    tokens = count_tokens(text, model="gpt-4o")
    assert tokens > 0
    assert tokens <= len(text)  # Tokens should be fewer than characters
    
    # Count tokens in a longer text
    text = "This is a longer text that should have more tokens. " * 10
    tokens = count_tokens(text, model="gpt-4o")
    assert tokens > 0
    assert tokens <= len(text)


@pytest.mark.parametrize("compression_method", ["none", "synthlang", "synthlang+gzip"])
def test_compression_benchmark(compression_method):
    """Test that the compression benchmark can be executed with different methods."""
    # Mock the compress_prompt function
    with patch("app.benchmark.scenarios.compression.compress_prompt") as mock_compress:
        # Set up the mock to return a compressed version
        mock_compress.side_effect = lambda text, use_gzip=False: f"compressed: {text[:len(text)//2]}"
        
        # Create a benchmark scenario
        benchmark = CompressionBenchmark("compression")
        
        # Set up the benchmark
        benchmark.setup({
            "compression_method": compression_method,
            "model": "gpt-4o",
            "text_type": "general",
            "sample_size": 2,
            "min_length": 100,
            "max_length": 200
        })
        
        # Execute the benchmark
        result = benchmark.execute()
        
        # Verify the result
        assert result.scenario_name == "compression"
        assert "compression_ratio" in result.metrics
        assert "token_reduction_percentage" in result.metrics
        assert "cost_savings_percentage" in result.metrics
        
        # Check that the compression method was used correctly
        if compression_method == "synthlang" or compression_method == "synthlang+gzip":
            mock_compress.assert_called()
            if compression_method == "synthlang+gzip":
                # Check that gzip was enabled
                assert any(call_args[1].get("use_gzip", False) for call_args in mock_compress.call_args_list)


def test_compression_benchmark_with_real_samples():
    """Test that the compression benchmark can use real-world samples."""
    # Mock the load_real_world_samples function
    with patch("app.benchmark.scenarios.compression.load_real_world_samples") as mock_load:
        # Set up the mock to return some sample texts
        mock_load.return_value = [
            {"text": "This is a real-world sample text."},
            {"text": "This is another real-world sample text."}
        ]
        
        # Create a benchmark scenario
        benchmark = CompressionBenchmark("compression")
        
        # Set up the benchmark with real samples
        benchmark.setup({
            "compression_method": "none",  # Use no compression for simplicity
            "model": "gpt-4o",
            "use_real_samples": True,
            "sample_size": 2
        })
        
        # Verify that the real samples were loaded
        mock_load.assert_called_once()
        assert len(benchmark.texts) == 2
        
        # Execute the benchmark
        result = benchmark.execute()
        
        # Verify the result
        assert result.scenario_name == "compression"
        assert "compression_ratio" in result.metrics