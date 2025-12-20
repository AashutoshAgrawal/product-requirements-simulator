"""
Logging Utility Module

This module provides a centralized logging configuration for the application.
"""

import logging
import sys
from typing import Optional


def get_logger(
    name: str,
    level: Optional[int] = None,
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    Get or create a logger with standardized configuration.
    
    Args:
        name: Name of the logger (typically __name__ from calling module)
        level: Logging level (defaults to INFO)
        log_file: Optional file path for file logging
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    # Set level
    if level is None:
        level = logging.INFO
    logger.setLevel(level)
    
    # Create formatter
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def set_global_log_level(level: int) -> None:
    """
    Set the logging level for all loggers in the application.
    
    Args:
        level: Logging level (e.g., logging.DEBUG, logging.INFO)
    """
    logging.getLogger().setLevel(level)
    
    # Update all existing handlers
    for handler in logging.getLogger().handlers:
        handler.setLevel(level)


def configure_logging(
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    format: Optional[str] = None
) -> None:
    """
    Configure global logging settings for the entire application.
    
    Args:
        level: Global logging level
        log_file: Optional file path for logging
        format: Optional custom format string
    """
    if format is None:
        format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    logging.basicConfig(
        level=level,
        format=format,
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(logging.Formatter(format))
        logging.getLogger().addHandler(file_handler)


class LoggerContext:
    """
    Context manager for temporary logging level changes.
    
    Example:
        with LoggerContext(logging.DEBUG):
            # Code here runs with DEBUG logging
            pass
        # Original logging level restored
    """
    
    def __init__(self, level: int):
        """
        Initialize the context manager.
        
        Args:
            level: Temporary logging level
        """
        self.level = level
        self.original_level = None
    
    def __enter__(self):
        """Enter the context and set new logging level."""
        self.original_level = logging.getLogger().level
        set_global_log_level(self.level)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context and restore original logging level."""
        if self.original_level is not None:
            set_global_log_level(self.original_level)
