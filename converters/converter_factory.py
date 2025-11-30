"""
Converter Factory
Routes conversions to appropriate converter classes
"""

from pathlib import Path
from typing import Optional
from .base_converter import BaseConverter
from .pdf_converter import PDFConverter, ToPDFConverter
from .excel_converter import ExcelConverter, FromExcelConverter
from .word_converter import WordConverter, ToWordConverter
from .json_converter import JSONConverter, ToJSONConverter
from utils.errors import ConversionError, UnsupportedFormatError
from utils.logger import get_logger

logger = get_logger(__name__)


class ConverterFactory:
    """Factory class to get appropriate converter"""
    
    def __init__(self):
        # Initialize all converters
        self.converters = [
            PDFConverter(),
            ToPDFConverter(),
            ExcelConverter(),
            FromExcelConverter(),
            WordConverter(),
            ToWordConverter(),
            JSONConverter(),
            ToJSONConverter()
        ]
        
        # Build conversion map
        self.conversion_map = self._build_conversion_map()
    
    def _build_conversion_map(self) -> dict:
        """Build map of supported conversions"""
        conversion_map = {}
        
        for converter in self.converters:
            for input_fmt in converter.supported_input_formats:
                if input_fmt not in conversion_map:
                    conversion_map[input_fmt] = {}
                
                for output_fmt in converter.supported_output_formats:
                    conversion_map[input_fmt][output_fmt] = converter
        
        return conversion_map
    
    def get_converter(
        self,
        input_format: str,
        output_format: str
    ) -> Optional[BaseConverter]:
        """
        Get appropriate converter for format pair
        
        Args:
            input_format: Input file format
            output_format: Output file format
            
        Returns:
            Converter instance or None
        """
        input_format = input_format.lower()
        output_format = output_format.lower()
        
        if input_format in self.conversion_map:
            if output_format in self.conversion_map[input_format]:
                return self.conversion_map[input_format][output_format]
        
        return None
    
    def convert(
        self,
        input_file: str | Path,
        output_file: str | Path,
        quality: str = 'high',
        **kwargs
    ) -> Path:
        """
        Convert file using appropriate converter
        
        Args:
            input_file: Path to input file
            output_file: Path to output file
            quality: Conversion quality
            **kwargs: Additional options
            
        Returns:
            Path to converted file
        """
        input_file = Path(input_file)
        output_file = Path(output_file)
        
        # Get formats
        input_format = input_file.suffix.lower().replace('.', '')
        output_format = output_file.suffix.lower().replace('.', '')
        
        # Get converter
        converter = self.get_converter(input_format, output_format)
        
        if converter is None:
            raise UnsupportedFormatError(
                f"{input_format} to {output_format}",
                self.get_supported_formats()
            )
        
        # Perform conversion
        logger.info(f"Converting {input_format} to {output_format} using {converter.__class__.__name__}")
        
        return converter.convert_with_validation(
            input_file,
            output_file,
            quality=quality,
            **kwargs
        )
    
    def supports_conversion(self, input_format: str, output_format: str) -> bool:
        """
        Check if conversion is supported
        
        Args:
            input_format: Input format
            output_format: Output format
            
        Returns:
            True if supported
        """
        return self.get_converter(input_format, output_format) is not None
    
    def get_supported_formats(self) -> list:
        """Get list of all supported formats"""
        formats = set()
        for input_fmt in self.conversion_map.keys():
            formats.add(input_fmt)
            for output_fmt in self.conversion_map[input_fmt].keys():
                formats.add(output_fmt)
        return sorted(list(formats))
    
    def get_supported_conversions(self, input_format: str) -> list:
        """
        Get supported output formats for input format
        
        Args:
            input_format: Input format
            
        Returns:
            List of supported output formats
        """
        input_format = input_format.lower()
        if input_format in self.conversion_map:
            return sorted(list(self.conversion_map[input_format].keys()))
        return []
    
    def get_all_conversions(self) -> dict:
        """
        Get all supported conversions
        
        Returns:
            Dictionary mapping input formats to output formats
        """
        return {
            input_fmt: sorted(list(output_fmts.keys()))
            for input_fmt, output_fmts in self.conversion_map.items()
        }


# Global factory instance
_factory = None


def get_converter_factory() -> ConverterFactory:
    """Get global converter factory instance"""
    global _factory
    if _factory is None:
        _factory = ConverterFactory()
    return _factory


def get_converter(input_format: str, output_format: str) -> Optional[BaseConverter]:
    """
    Get converter for format pair (convenience function)
    
    Args:
        input_format: Input format
        output_format: Output format
        
    Returns:
        Converter instance or None
    """
    factory = get_converter_factory()
    return factory.get_converter(input_format, output_format)


def convert_file(
    input_file: str | Path,
    output_file: str | Path,
    quality: str = 'high',
    **kwargs
) -> Path:
    """
    Convert file (convenience function)
    
    Args:
        input_file: Path to input file
        output_file: Path to output file
        quality: Conversion quality
        **kwargs: Additional options
        
    Returns:
        Path to converted file
    """
    factory = get_converter_factory()
    return factory.convert(input_file, output_file, quality=quality, **kwargs)


def get_supported_formats() -> list:
    """Get all supported formats (convenience function)"""
    factory = get_converter_factory()
    return factory.get_supported_formats()


def get_supported_conversions(input_format: str) -> list:
    """Get supported conversions for format (convenience function)"""
    factory = get_converter_factory()
    return factory.get_supported_conversions(input_format)
