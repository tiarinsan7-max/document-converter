"""
Helper utility functions
Common utilities used throughout the application
"""

import os
import re
import uuid
import hashlib
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
import json
from utils.logger import get_logger

logger = get_logger(__name__)


def get_file_extension(file_path: str | Path) -> str:
    """
    Get file extension without the dot
    
    Args:
        file_path: Path to file
        
    Returns:
        File extension (lowercase, without dot)
    """
    return Path(file_path).suffix.lower().replace('.', '')


def get_file_size(file_path: str | Path) -> int:
    """
    Get file size in bytes
    
    Args:
        file_path: Path to file
        
    Returns:
        File size in bytes
    """
    return Path(file_path).stat().st_size


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing invalid characters
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    
    # Remove multiple underscores
    filename = re.sub(r'_+', '_', filename)
    
    # Limit length
    name, ext = os.path.splitext(filename)
    if len(name) > 200:
        name = name[:200]
    
    return name + ext


def generate_unique_filename(
    original_filename: str,
    output_dir: Optional[str | Path] = None,
    prefix: str = "",
    suffix: str = ""
) -> str:
    """
    Generate unique filename to avoid conflicts
    
    Args:
        original_filename: Original filename
        output_dir: Output directory to check for conflicts
        prefix: Prefix to add
        suffix: Suffix to add (before extension)
        
    Returns:
        Unique filename
    """
    name, ext = os.path.splitext(original_filename)
    name = sanitize_filename(name)
    
    # Add prefix and suffix
    if prefix:
        name = f"{prefix}_{name}"
    if suffix:
        name = f"{name}_{suffix}"
    
    # If no output directory specified, add timestamp
    if output_dir is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{name}_{timestamp}{ext}"
    
    # Check for conflicts in output directory
    output_dir = Path(output_dir)
    base_name = name
    counter = 1
    
    while (output_dir / f"{name}{ext}").exists():
        name = f"{base_name}_{counter}"
        counter += 1
    
    return f"{name}{ext}"


def generate_file_hash(file_path: str | Path, algorithm: str = 'md5') -> str:
    """
    Generate hash of file content
    
    Args:
        file_path: Path to file
        algorithm: Hash algorithm (md5, sha1, sha256)
        
    Returns:
        File hash
    """
    hash_func = hashlib.new(algorithm)
    
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            hash_func.update(chunk)
    
    return hash_func.hexdigest()


def create_temp_filename(extension: str = '') -> str:
    """
    Create temporary filename with UUID
    
    Args:
        extension: File extension (with or without dot)
        
    Returns:
        Temporary filename
    """
    if extension and not extension.startswith('.'):
        extension = f'.{extension}'
    
    return f"temp_{uuid.uuid4().hex}{extension}"


def ensure_directory(directory: str | Path) -> Path:
    """
    Ensure directory exists, create if it doesn't
    
    Args:
        directory: Directory path
        
    Returns:
        Path object
    """
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def clean_directory(directory: str | Path, pattern: str = '*', recursive: bool = False):
    """
    Clean files from directory matching pattern
    
    Args:
        directory: Directory path
        pattern: File pattern to match (e.g., '*.tmp')
        recursive: Whether to clean recursively
    """
    directory = Path(directory)
    
    if not directory.exists():
        return
    
    if recursive:
        files = directory.rglob(pattern)
    else:
        files = directory.glob(pattern)
    
    count = 0
    for file in files:
        if file.is_file():
            try:
                file.unlink()
                count += 1
            except Exception as e:
                logger.warning(f"Failed to delete {file}: {e}")
    
    logger.info(f"Cleaned {count} files from {directory}")


def load_json_file(file_path: str | Path) -> Dict[Any, Any]:
    """
    Load JSON file
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Parsed JSON data
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json_file(data: Dict[Any, Any], file_path: str | Path, indent: int = 2):
    """
    Save data to JSON file
    
    Args:
        data: Data to save
        file_path: Path to JSON file
        indent: JSON indentation
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def get_mime_type(file_path: str | Path) -> Optional[str]:
    """
    Get MIME type of file
    
    Args:
        file_path: Path to file
        
    Returns:
        MIME type or None
    """
    import mimetypes
    mime_type, _ = mimetypes.guess_type(str(file_path))
    return mime_type


def format_duration(seconds: float) -> str:
    """
    Format duration in human-readable format
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration (e.g., "1m 30s")
    """
    if seconds < 60:
        return f"{seconds:.2f}s"
    
    minutes = int(seconds // 60)
    remaining_seconds = seconds % 60
    
    if minutes < 60:
        return f"{minutes}m {remaining_seconds:.0f}s"
    
    hours = int(minutes // 60)
    remaining_minutes = minutes % 60
    
    return f"{hours}h {remaining_minutes}m"


def truncate_string(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate string to maximum length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated string
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def parse_file_path(file_path: str | Path) -> Dict[str, str]:
    """
    Parse file path into components
    
    Args:
        file_path: Path to file
        
    Returns:
        Dictionary with path components
    """
    path = Path(file_path)
    
    return {
        'full_path': str(path.absolute()),
        'directory': str(path.parent),
        'filename': path.name,
        'stem': path.stem,
        'extension': path.suffix.lower().replace('.', ''),
        'size': get_file_size(path) if path.exists() else 0,
        'size_formatted': format_file_size(get_file_size(path)) if path.exists() else '0 B'
    }
