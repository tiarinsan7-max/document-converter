"""Utility modules for the document converter"""

from .logger import setup_logger, get_logger
from .validators import FileValidator, validate_file, validate_conversion
from .helpers import (
    get_file_extension,
    get_file_size,
    format_file_size,
    sanitize_filename,
    generate_unique_filename,
    ensure_directory,
    parse_file_path
)
from .file_handler import FileHandler, file_handler
from .progress import (
    ProgressTracker,
    CLIProgressBar,
    RichProgressBar,
    BatchProgressTracker
)
from .errors import (
    ConverterError,
    ConversionError,
    FileValidationError,
    UnsupportedFormatError,
    handle_conversion_error
)
from .config_loader import (
    ConfigLoader,
    config_loader,
    get_format_rules,
    get_quality_settings,
    get_batch_settings
)

__all__ = [
    # Logger
    'setup_logger',
    'get_logger',
    # Validators
    'FileValidator',
    'validate_file',
    'validate_conversion',
    # Helpers
    'get_file_extension',
    'get_file_size',
    'format_file_size',
    'sanitize_filename',
    'generate_unique_filename',
    'ensure_directory',
    'parse_file_path',
    # File Handler
    'FileHandler',
    'file_handler',
    # Progress
    'ProgressTracker',
    'CLIProgressBar',
    'RichProgressBar',
    'BatchProgressTracker',
    # Errors
    'ConverterError',
    'ConversionError',
    'FileValidationError',
    'UnsupportedFormatError',
    'handle_conversion_error',
    # Config
    'ConfigLoader',
    'config_loader',
    'get_format_rules',
    'get_quality_settings',
    'get_batch_settings'
]
