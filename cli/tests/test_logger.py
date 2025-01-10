"""Tests for logging functionality."""
import logging
from pathlib import Path

import pytest
from rich.console import Console

from synthlang.utils.logger import (
    setup_logger,
    get_logger,
    set_log_level,
    log_exception,
    logger
)

def test_logger_setup():
    """Test basic logger setup."""
    test_logger = setup_logger("test_logger")
    assert isinstance(test_logger, logging.Logger)
    assert test_logger.name == "test_logger"
    assert test_logger.level == logging.INFO
    assert len(test_logger.handlers) > 0
    assert any(isinstance(h, logging.Handler) for h in test_logger.handlers)

def test_logger_with_file(tmp_path):
    """Test logger with file output."""
    log_file = tmp_path / "test.log"
    test_logger = setup_logger("test_file_logger", log_file=log_file)
    
    # Verify file handler was added
    assert any(isinstance(h, logging.FileHandler) for h in test_logger.handlers)
    
    # Test logging to file
    test_message = "Test log message"
    test_logger.info(test_message)
    
    # Verify message was written to file
    assert log_file.exists()
    log_content = log_file.read_text()
    assert test_message in log_content

def test_log_levels():
    """Test different log levels."""
    test_logger = setup_logger("test_levels_logger", level="DEBUG")
    assert test_logger.level == logging.DEBUG
    
    # Change level
    set_log_level("ERROR")
    assert logger.level == logging.ERROR
    
    # Test invalid level defaults to INFO
    set_log_level("INVALID")
    assert logger.level == logging.INFO

def test_exception_logging(caplog):
    """Test exception logging."""
    test_exception = ValueError("Test error")
    
    with caplog.at_level(logging.ERROR):
        log_exception(test_exception)
        
    assert "Test error" in caplog.text
    assert "ValueError" in caplog.text

def test_get_logger():
    """Test logger retrieval."""
    logger_name = "test_get_logger"
    first_logger = get_logger(logger_name)
    second_logger = get_logger(logger_name)
    
    # Should return same logger instance
    assert first_logger is second_logger
    assert first_logger.name == logger_name

def test_rich_formatting():
    """Test rich console formatting."""
    test_logger = setup_logger("test_rich_logger")
    
    # Verify rich handler is present
    rich_handlers = [h for h in test_logger.handlers 
                    if "RichHandler" in h.__class__.__name__]
    assert len(rich_handlers) == 1
    
    rich_handler = rich_handlers[0]
    assert isinstance(rich_handler.console, Console)
    assert rich_handler.rich_tracebacks is True
    assert rich_handler.markup is True

def test_multiple_setup_calls():
    """Test multiple logger setup calls."""
    name = "test_multiple_logger"
    first_logger = setup_logger(name)
    second_logger = setup_logger(name)
    
    # Should return same logger but with reset handlers
    assert first_logger is second_logger
    assert len(first_logger.handlers) == len(second_logger.handlers)

def test_log_level_propagation():
    """Test log level changes propagate to handlers."""
    test_logger = setup_logger("test_propagation")
    initial_level = logging.INFO
    new_level = logging.DEBUG
    
    # Set initial level
    set_log_level("INFO")
    assert test_logger.level == initial_level
    for handler in test_logger.handlers:
        assert handler.level == initial_level
    
    # Change level
    set_log_level("DEBUG")
    assert test_logger.level == new_level
    for handler in test_logger.handlers:
        assert handler.level == new_level

def test_logger_with_different_levels(tmp_path):
    """Test logger with different levels for console and file."""
    log_file = tmp_path / "test_levels.log"
    test_logger = setup_logger(
        "test_different_levels",
        level="DEBUG",
        log_file=log_file
    )
    
    # Set console handler to INFO
    console_handler = next(h for h in test_logger.handlers 
                         if "RichHandler" in h.__class__.__name__)
    console_handler.setLevel(logging.INFO)
    
    # Set file handler to DEBUG
    file_handler = next(h for h in test_logger.handlers 
                       if isinstance(h, logging.FileHandler))
    file_handler.setLevel(logging.DEBUG)
    
    # Debug message should only go to file
    test_logger.debug("Debug message")
    log_content = log_file.read_text()
    assert "Debug message" in log_content
    
    # Info message should go to both
    test_logger.info("Info message")
    log_content = log_file.read_text()
    assert "Info message" in log_content
