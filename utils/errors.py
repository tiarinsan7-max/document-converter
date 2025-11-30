"""
Custom exceptions and error handling
Defines application-specific exceptions
"""

from typing import Optional, Dict, Any


class ConverterError(Exception):
    """Base exception for converter errors"""
    
    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code or "CONVERTER_ERROR"
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary"""
        return {
            'error': self.__class__.__name__,
            'message': self.message,
            'error_code': self.error_code,
            'details': self.details
        }


class FileValidationError(ConverterError):
    """File validation failed"""
    
    def __init__(self, message: str, filename: Optional[str] = None):
        super().__init__(
            message=message,
            error_code="FILE_VALIDATION_ERROR",
            details={'filename': filename} if filename else {}
        )


class UnsupportedFormatError(ConverterError):
    """Unsupported file format"""
    
    def __init__(self, format_name: str, supported_formats: Optional[list] = None):
        message = f"Unsupported format: {format_name}"
        if supported_formats:
            message += f". Supported formats: {', '.join(supported_formats)}"
        
        super().__init__(
            message=message,
            error_code="UNSUPPORTED_FORMAT",
            details={
                'format': format_name,
                'supported_formats': supported_formats
            }
        )


class ConversionError(ConverterError):
    """Conversion process failed"""
    
    def __init__(
        self,
        message: str,
        input_file: Optional[str] = None,
        output_format: Optional[str] = None,
        original_error: Optional[Exception] = None
    ):
        super().__init__(
            message=message,
            error_code="CONVERSION_ERROR",
            details={
                'input_file': input_file,
                'output_format': output_format,
                'original_error': str(original_error) if original_error else None
            }
        )
        self.original_error = original_error


class FileSizeError(ConverterError):
    """File size exceeds limit"""
    
    def __init__(self, file_size: int, max_size: int):
        message = f"File size ({file_size} bytes) exceeds maximum ({max_size} bytes)"
        super().__init__(
            message=message,
            error_code="FILE_SIZE_ERROR",
            details={
                'file_size': file_size,
                'max_size': max_size
            }
        )


class FileNotFoundError(ConverterError):
    """File not found"""
    
    def __init__(self, file_path: str):
        super().__init__(
            message=f"File not found: {file_path}",
            error_code="FILE_NOT_FOUND",
            details={'file_path': file_path}
        )


class PermissionError(ConverterError):
    """Permission denied"""
    
    def __init__(self, file_path: str, operation: str):
        super().__init__(
            message=f"Permission denied: {operation} on {file_path}",
            error_code="PERMISSION_ERROR",
            details={
                'file_path': file_path,
                'operation': operation
            }
        )


class ConfigurationError(ConverterError):
    """Configuration error"""
    
    def __init__(self, message: str, config_key: Optional[str] = None):
        super().__init__(
            message=message,
            error_code="CONFIGURATION_ERROR",
            details={'config_key': config_key} if config_key else {}
        )


class BatchConversionError(ConverterError):
    """Batch conversion error"""
    
    def __init__(
        self,
        message: str,
        total_files: int,
        failed_files: int,
        errors: Optional[list] = None
    ):
        super().__init__(
            message=message,
            error_code="BATCH_CONVERSION_ERROR",
            details={
                'total_files': total_files,
                'failed_files': failed_files,
                'errors': errors or []
            }
        )


class OCRError(ConverterError):
    """OCR processing error"""
    
    def __init__(self, message: str, page_number: Optional[int] = None):
        super().__init__(
            message=message,
            error_code="OCR_ERROR",
            details={'page_number': page_number} if page_number else {}
        )


class EncodingError(ConverterError):
    """File encoding error"""
    
    def __init__(self, message: str, encoding: Optional[str] = None):
        super().__init__(
            message=message,
            error_code="ENCODING_ERROR",
            details={'encoding': encoding} if encoding else {}
        )


class TimeoutError(ConverterError):
    """Operation timeout"""
    
    def __init__(self, operation: str, timeout_seconds: int):
        super().__init__(
            message=f"Operation '{operation}' timed out after {timeout_seconds} seconds",
            error_code="TIMEOUT_ERROR",
            details={
                'operation': operation,
                'timeout_seconds': timeout_seconds
            }
        )


def handle_conversion_error(error: Exception, input_file: str = "") -> ConverterError:
    """
    Convert generic exception to ConverterError
    
    Args:
        error: Original exception
        input_file: Input file path
        
    Returns:
        ConverterError instance
    """
    if isinstance(error, ConverterError):
        return error
    
    # Map common exceptions
    error_type = type(error).__name__
    error_message = str(error)
    
    if "permission" in error_message.lower():
        return PermissionError(input_file, "conversion")
    
    if "not found" in error_message.lower():
        return FileNotFoundError(input_file)
    
    if "encoding" in error_message.lower():
        return EncodingError(error_message)
    
    # Generic conversion error
    return ConversionError(
        message=f"Conversion failed: {error_message}",
        input_file=input_file,
        original_error=error
    )
