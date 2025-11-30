"""
Configuration loader
Load and manage conversion rules and settings
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class ConfigLoader:
    """Load and manage configuration"""
    
    def __init__(self):
        self.rules_file = settings.RULES_DIR / "conversion_rules.json"
        self._rules_cache = None
    
    def load_conversion_rules(self) -> Dict[str, Any]:
        """
        Load conversion rules from JSON file
        
        Returns:
            Dictionary with conversion rules
        """
        if self._rules_cache is not None:
            return self._rules_cache
        
        try:
            if not self.rules_file.exists():
                logger.warning(f"Rules file not found: {self.rules_file}")
                return self._get_default_rules()
            
            with open(self.rules_file, 'r', encoding='utf-8') as f:
                rules = json.load(f)
            
            self._rules_cache = rules
            logger.info("Conversion rules loaded successfully")
            return rules
            
        except Exception as e:
            logger.error(f"Failed to load conversion rules: {e}")
            return self._get_default_rules()
    
    def get_format_rules(self, format_name: str) -> Dict[str, Any]:
        """
        Get rules for specific format
        
        Args:
            format_name: Format name (e.g., 'pdf', 'docx')
            
        Returns:
            Format-specific rules
        """
        rules = self.load_conversion_rules()
        conversion_rules = rules.get('conversion_rules', {})
        return conversion_rules.get(format_name.lower(), {})
    
    def get_quality_settings(self, format_name: str, quality: str = 'high') -> Dict[str, Any]:
        """
        Get quality settings for format
        
        Args:
            format_name: Format name
            quality: Quality level ('low', 'medium', 'high')
            
        Returns:
            Quality settings
        """
        format_rules = self.get_format_rules(format_name)
        quality_settings = format_rules.get('quality_settings', {})
        return quality_settings.get(quality, quality_settings.get('high', {}))
    
    def get_batch_settings(self) -> Dict[str, Any]:
        """
        Get batch processing settings
        
        Returns:
            Batch settings
        """
        rules = self.load_conversion_rules()
        return rules.get('batch_processing', {
            'max_concurrent': 4,
            'timeout_seconds': 300,
            'retry_attempts': 3,
            'skip_errors': True
        })
    
    def get_validation_settings(self) -> Dict[str, Any]:
        """
        Get file validation settings
        
        Returns:
            Validation settings
        """
        rules = self.load_conversion_rules()
        return rules.get('file_validation', {
            'max_file_size_mb': 100,
            'scan_for_viruses': False,
            'validate_content': True
        })
    
    def reload_rules(self):
        """Reload rules from file"""
        self._rules_cache = None
        return self.load_conversion_rules()
    
    def _get_default_rules(self) -> Dict[str, Any]:
        """
        Get default conversion rules
        
        Returns:
            Default rules dictionary
        """
        return {
            'conversion_rules': {
                'pdf': {
                    'quality_settings': {
                        'low': {'dpi': 72, 'compression': 'high'},
                        'medium': {'dpi': 150, 'compression': 'medium'},
                        'high': {'dpi': 300, 'compression': 'low'}
                    },
                    'ocr_enabled': True,
                    'preserve_images': True,
                    'preserve_links': True
                },
                'docx': {
                    'preserve_formatting': True,
                    'preserve_styles': True,
                    'preserve_tables': True,
                    'preserve_images': True
                },
                'xlsx': {
                    'preserve_formulas': True,
                    'preserve_formatting': True,
                    'max_rows': 1048576,
                    'max_columns': 16384
                },
                'csv': {
                    'delimiter': ',',
                    'encoding': 'utf-8',
                    'quote_char': '"',
                    'escape_char': '\\',
                    'line_terminator': '\n'
                },
                'json': {
                    'indent': 2,
                    'ensure_ascii': False,
                    'sort_keys': False,
                    'encoding': 'utf-8'
                },
                'txt': {
                    'encoding': 'utf-8',
                    'line_ending': 'auto',
                    'preserve_whitespace': True
                }
            },
            'batch_processing': {
                'max_concurrent': 4,
                'timeout_seconds': 300,
                'retry_attempts': 3,
                'skip_errors': True
            },
            'file_validation': {
                'max_file_size_mb': 100,
                'scan_for_viruses': False,
                'validate_content': True
            }
        }


# Global instance
config_loader = ConfigLoader()


# Convenience functions
def get_format_rules(format_name: str) -> Dict[str, Any]:
    """Get rules for specific format"""
    return config_loader.get_format_rules(format_name)


def get_quality_settings(format_name: str, quality: str = 'high') -> Dict[str, Any]:
    """Get quality settings for format"""
    return config_loader.get_quality_settings(format_name, quality)


def get_batch_settings() -> Dict[str, Any]:
    """Get batch processing settings"""
    return config_loader.get_batch_settings()
