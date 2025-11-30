"""
Base converter class
Abstract base class for all document converters
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Dict, Any
import time
from utils.logger import get_logger, log_conversion_start, log_conversion_success, log_conversion_error
from utils.validators import validate_file, validate_conversion
from utils.file_handler import FileHandler
from utils.errors import ConversionError, FileValidationError
from utils.config_loader import get_format_rules, get_quality_settings

logger = get_logger(__name__)


class BaseConverter(ABC):
    """Abstract base class for all converters"""
    
    def __init__(self):
        self.file_handler = FileHandler()
        self.supported_input_formats = []
        self.supported_output_formats = []
    
    @abstractmethod
    def convert(
        self,
        input_file: str | Path,
        output_file: str | Path,
        **kwargs
    ) -> Path:
        """
        Convert file from one format to another
        
        Args:
            input_file: Path to input file
            output_file: Path to output file
            **kwargs: Additional conversion options
            
        Returns:
            Path to converted file
            
        Raises:
            ConversionError: If conversion fails
        """
        pass
    
    def convert_with_validation(
        self,
        input_file: str | Path,
        output_file: str | Path,
        quality: str = 'high',
        **kwargs
    ) -> Path:
        """
        Convert file with validation and error handling
        
        Args:
            input_file: Path to input file
            output_file: Path to output file
            quality: Conversion quality ('low', 'medium', 'high')
            **kwargs: Additional conversion options
            
        Returns:
            Path to converted file
        """
        input_file = Path(input_file)
        output_file = Path(output_file)
        
        start_time = time.time()
        
        try:
            # Validate input file
            is_valid, error = validate_file(input_file)
            if not is_valid:
                raise FileValidationError(error, str(input_file))
            
            # Get file formats
            input_format = input_file.suffix.lower().replace('.', '')
            output_format = output_file.suffix.lower().replace('.', '')
            
            # Validate conversion
            is_valid, error = validate_conversion(input_format, output_format)
            if not is_valid:
                raise ConversionError(error)
            
            # Log conversion start
            log_conversion_start(str(input_file), output_format)
            
            # Get quality settings
            quality_settings = get_quality_settings(output_format, quality)
            kwargs['quality_settings'] = quality_settings
            
            # Perform conversion
            result = self.convert(input_file, output_file, **kwargs)
            
            # Log success
            duration = time.time() - start_time
            log_conversion_success(str(input_file), str(result), duration)
            
            return result
            
        except Exception as e:
            # Log error
            log_conversion_error(str(input_file), str(e))
            
            # Re-raise as ConversionError if not already
            if isinstance(e, ConversionError):
                raise
            else:
                raise ConversionError(
                    message=f"Conversion failed: {str(e)}",
                    input_file=str(input_file),
                    output_format=output_format,
                    original_error=e
                )
    
    def supports_conversion(self, input_format: str, output_format: str) -> bool:
        """
        Check if converter supports this conversion
        
        Args:
            input_format: Input format
            output_format: Output format
            
        Returns:
            True if supported
        """
        return (
            input_format.lower() in self.supported_input_formats and
            output_format.lower() in self.supported_output_formats
        )
    
    def get_supported_conversions(self) -> Dict[str, list]:
        """
        Get supported conversions
        
        Returns:
            Dictionary mapping input formats to output formats
        """
        return {
            fmt: self.supported_output_formats
            for fmt in self.supported_input_formats
        }
    
    def _ensure_output_directory(self, output_file: Path):
        """Ensure output directory exists"""
        output_file.parent.mkdir(parents=True, exist_ok=True)
    
    def _get_format_rules(self, format_name: str) -> Dict[str, Any]:
        """Get format-specific rules"""
        return get_format_rules(format_name)
    
    def _log_info(self, message: str):
        """Log info message"""
        logger.info(message)
    
    def _log_error(self, message: str):
        """Log error message"""
        logger.error(message)
    
    def _log_warning(self, message: str):
        """Log warning message"""
        logger.warning(message)
