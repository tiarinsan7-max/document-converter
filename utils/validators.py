"""
File validation utilities
Validates file types, sizes, and content
"""

import os
import mimetypes
from pathlib import Path
from typing import Optional, Tuple, List
import chardet
from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


class FileValidator:
    """File validation class"""
    
    # MIME type mappings
    MIME_TYPES = {
        'pdf': ['application/pdf'],
        'docx': [
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/msword'
        ],
        'xlsx': [
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'application/vnd.ms-excel'
        ],
        'csv': ['text/csv', 'text/plain'],
        'json': ['application/json', 'text/plain'],
        'txt': ['text/plain']
    }
    
    def __init__(self):
        self.max_size = settings.MAX_UPLOAD_SIZE
        self.allowed_extensions = settings.ALLOWED_EXTENSIONS
        self.supported_formats = settings.SUPPORTED_FORMATS
    
    def validate_file(
        self, 
        file_path: str | Path,
        check_content: bool = True
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate a file
        
        Args:
            file_path: Path to file
            check_content: Whether to validate file content
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        file_path = Path(file_path)
        
        # Check if file exists
        if not file_path.exists():
            return False, f"File not found: {file_path}"
        
        # Check if it's a file
        if not file_path.is_file():
            return False, f"Not a file: {file_path}"
        
        # Check file size
        file_size = file_path.stat().st_size
        if file_size > self.max_size:
            max_mb = self.max_size / (1024 * 1024)
            actual_mb = file_size / (1024 * 1024)
            return False, f"File too large: {actual_mb:.2f}MB (max: {max_mb:.2f}MB)"
        
        # Check file extension
        extension = file_path.suffix.lower()
        if extension not in self.allowed_extensions:
            return False, f"Unsupported file extension: {extension}"
        
        # Check MIME type if content validation is enabled
        if check_content:
            mime_valid, mime_error = self._validate_mime_type(file_path)
            if not mime_valid:
                return False, mime_error
        
        logger.info(f"File validation passed: {file_path}")
        return True, None
    
    def _validate_mime_type(self, file_path: Path) -> Tuple[bool, Optional[str]]:
        """
        Validate file MIME type
        
        Args:
            file_path: Path to file
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Get MIME type
            mime_type, _ = mimetypes.guess_type(str(file_path))
            
            if mime_type is None:
                # Try to detect from content
                with open(file_path, 'rb') as f:
                    header = f.read(1024)
                    
                # Check for PDF
                if header.startswith(b'%PDF'):
                    mime_type = 'application/pdf'
                # Check for ZIP-based formats (DOCX, XLSX)
                elif header.startswith(b'PK\x03\x04'):
                    # Could be DOCX or XLSX
                    extension = file_path.suffix.lower()
                    if extension == '.docx':
                        mime_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                    elif extension == '.xlsx':
                        mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            
            if mime_type is None:
                return True, None  # Allow if we can't determine
            
            # Check if MIME type is allowed for this extension
            extension = file_path.suffix.lower().replace('.', '')
            allowed_mimes = self.MIME_TYPES.get(extension, [])
            
            if allowed_mimes and mime_type not in allowed_mimes:
                return False, f"Invalid file type: {mime_type} for .{extension}"
            
            return True, None
            
        except Exception as e:
            logger.warning(f"MIME type validation failed: {e}")
            return True, None  # Allow if validation fails
    
    def validate_encoding(self, file_path: Path) -> Tuple[str, float]:
        """
        Detect file encoding
        
        Args:
            file_path: Path to file
            
        Returns:
            Tuple of (encoding, confidence)
        """
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read(10000)  # Read first 10KB
                result = chardet.detect(raw_data)
                return result['encoding'], result['confidence']
        except Exception as e:
            logger.error(f"Encoding detection failed: {e}")
            return 'utf-8', 0.0
    
    def is_supported_format(self, format_name: str) -> bool:
        """
        Check if format is supported
        
        Args:
            format_name: Format name (e.g., 'pdf', 'docx')
            
        Returns:
            True if supported
        """
        return format_name.lower() in self.supported_formats
    
    def get_supported_conversions(self, input_format: str) -> List[str]:
        """
        Get list of supported output formats for input format
        
        Args:
            input_format: Input format (e.g., 'pdf')
            
        Returns:
            List of supported output formats
        """
        if not self.is_supported_format(input_format):
            return []
        
        # All formats can convert to all other formats
        return [fmt for fmt in self.supported_formats if fmt != input_format.lower()]


# Convenience function
def validate_file(file_path: str | Path, check_content: bool = True) -> Tuple[bool, Optional[str]]:
    """
    Validate a file (convenience function)
    
    Args:
        file_path: Path to file
        check_content: Whether to validate file content
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    validator = FileValidator()
    return validator.validate_file(file_path, check_content)


def validate_conversion(input_format: str, output_format: str) -> Tuple[bool, Optional[str]]:
    """
    Validate if conversion is supported
    
    Args:
        input_format: Input format
        output_format: Output format
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    validator = FileValidator()
    
    if not validator.is_supported_format(input_format):
        return False, f"Unsupported input format: {input_format}"
    
    if not validator.is_supported_format(output_format):
        return False, f"Unsupported output format: {output_format}"
    
    if input_format.lower() == output_format.lower():
        return False, "Input and output formats are the same"
    
    return True, None
