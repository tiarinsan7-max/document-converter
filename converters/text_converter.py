"""
Text Converter
Handles TXT conversions (mostly handled by other converters)
"""

from pathlib import Path
from .base_converter import BaseConverter
from utils.errors import ConversionError


class TextConverter(BaseConverter):
    """Convert TXT files (placeholder - most conversions handled by specific converters)"""
    
    def __init__(self):
        super().__init__()
        self.supported_input_formats = ['txt']
        self.supported_output_formats = []  # Handled by other converters
    
    def convert(
        self,
        input_file: str | Path,
        output_file: str | Path,
        **kwargs
    ) -> Path:
        """
        Convert TXT file
        
        Note: Most TXT conversions are handled by specific converters
        (ToPDFConverter, ToWordConverter, ToJSONConverter, etc.)
        """
        raise ConversionError(
            "TXT conversions are handled by format-specific converters"
        )
