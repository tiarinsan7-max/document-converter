"""
JSON Converter
Handles JSON conversions
"""

from pathlib import Path
import json
from .base_converter import BaseConverter
from utils.errors import ConversionError


class JSONConverter(BaseConverter):
    """Convert JSON to other formats"""
    
    def __init__(self):
        super().__init__()
        self.supported_input_formats = ['json']
        self.supported_output_formats = ['txt']
    
    def convert(
        self,
        input_file: str | Path,
        output_file: str | Path,
        **kwargs
    ) -> Path:
        """
        Convert JSON file
        
        Args:
            input_file: Path to JSON file
            output_file: Path to output file
            **kwargs: Additional options
            
        Returns:
            Path to converted file
        """
        input_file = Path(input_file)
        output_file = Path(output_file)
        
        self._ensure_output_directory(output_file)
        
        output_format = output_file.suffix.lower().replace('.', '')
        
        # Route to appropriate converter
        if output_format == 'txt':
            return self._json_to_txt(input_file, output_file, **kwargs)
        else:
            raise ConversionError(f"Unsupported output format: {output_format}")
    
    def _json_to_txt(self, input_file: Path, output_file: Path, **kwargs) -> Path:
        """Convert JSON to TXT"""
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Format JSON as readable text
            pretty_json = json.dumps(data, indent=2, ensure_ascii=False)
            
            # Write to file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(pretty_json)
            
            self._log_info(f"Converted JSON to TXT: {output_file}")
            return output_file
            
        except Exception as e:
            raise ConversionError(f"JSON to TXT conversion failed: {e}")


class ToJSONConverter(BaseConverter):
    """Convert other formats to JSON"""
    
    def __init__(self):
        super().__init__()
        self.supported_input_formats = ['txt']
        self.supported_output_formats = ['json']
    
    def convert(
        self,
        input_file: str | Path,
        output_file: str | Path,
        **kwargs
    ) -> Path:
        """Convert to JSON"""
        input_file = Path(input_file)
        output_file = Path(output_file)
        
        self._ensure_output_directory(output_file)
        
        input_format = input_file.suffix.lower().replace('.', '')
        
        # Route to appropriate converter
        if input_format == 'txt':
            return self._txt_to_json(input_file, output_file, **kwargs)
        else:
            raise ConversionError(f"Unsupported input format: {input_format}")
    
    def _txt_to_json(self, input_file: Path, output_file: Path, **kwargs) -> Path:
        """Convert TXT to JSON"""
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Try to parse as JSON first
            try:
                data = json.loads(content)
            except json.JSONDecodeError:
                # If not valid JSON, structure as lines
                lines = content.split('\n')
                data = {
                    'content': content,
                    'lines': [line for line in lines if line.strip()],
                    'line_count': len([line for line in lines if line.strip()])
                }
            
            # Write to JSON
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self._log_info(f"Converted TXT to JSON: {output_file}")
            return output_file
            
        except Exception as e:
            raise ConversionError(f"TXT to JSON conversion failed: {e}")
