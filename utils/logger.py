"""
Logging utility for the document converter
Uses loguru for enhanced logging capabilities
"""

import sys
from pathlib import Path
from loguru import logger
from typing import Optional
from config.settings import settings


def setup_logger(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    rotation: str = "10 MB",
    retention: str = "1 week",
    compression: str = "zip"
) -> None:
    """
    Setup application logger with file and console output
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file (default: logs/app.log)
        rotation: When to rotate log file
        retention: How long to keep old logs
        compression: Compression format for old logs
    """
    # Remove default handler
    logger.remove()
    
    # Add console handler with colors
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level=log_level,
        colorize=True
    )
    
    # Add file handler for general logs
    if log_file is None:
        log_file = settings.LOG_DIR / "app.log"
    
    logger.add(
        log_file,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=log_level,
        rotation=rotation,
        retention=retention,
        compression=compression,
        enqueue=True  # Thread-safe
    )
    
    # Add separate error log file
    error_log = settings.LOG_DIR / "error.log"
    logger.add(
        error_log,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}\n{exception}",
        level="ERROR",
        rotation=rotation,
        retention=retention,
        compression=compression,
        enqueue=True,
        backtrace=True,
        diagnose=True
    )
    
    # Add conversion-specific log
    conversion_log = settings.LOG_DIR / "conversion.log"
    logger.add(
        conversion_log,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
        level="INFO",
        rotation=rotation,
        retention=retention,
        compression=compression,
        enqueue=True,
        filter=lambda record: "conversion" in record["extra"]
    )
    
    logger.info(f"Logger initialized - Level: {log_level}")


def get_logger(name: str = __name__):
    """
    Get a logger instance
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Logger instance
    """
    return logger.bind(name=name)


# Initialize logger on import
setup_logger(log_level=settings.LOG_LEVEL)


# Convenience functions for conversion logging
def log_conversion_start(input_file: str, output_format: str):
    """Log conversion start"""
    logger.bind(conversion=True).info(
        f"Starting conversion: {input_file} -> {output_format}"
    )


def log_conversion_success(input_file: str, output_file: str, duration: float):
    """Log successful conversion"""
    logger.bind(conversion=True).success(
        f"Conversion completed: {input_file} -> {output_file} ({duration:.2f}s)"
    )


def log_conversion_error(input_file: str, error: str):
    """Log conversion error"""
    logger.bind(conversion=True).error(
        f"Conversion failed: {input_file} - Error: {error}"
    )


def log_batch_start(total_files: int):
    """Log batch conversion start"""
    logger.bind(conversion=True).info(
        f"Starting batch conversion: {total_files} files"
    )


def log_batch_complete(successful: int, failed: int, duration: float):
    """Log batch conversion completion"""
    logger.bind(conversion=True).info(
        f"Batch conversion completed: {successful} successful, {failed} failed ({duration:.2f}s)"
    )
