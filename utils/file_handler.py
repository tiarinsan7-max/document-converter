"""
File handling utilities
Manages file operations, uploads, and downloads
"""

import shutil
from pathlib import Path
from typing import Optional, BinaryIO, List
import aiofiles
from config.settings import settings
from utils.logger import get_logger
from utils.helpers import (
    ensure_directory,
    generate_unique_filename,
    sanitize_filename,
    get_file_extension
)

logger = get_logger(__name__)


class FileHandler:
    """Handle file operations"""
    
    def __init__(self):
        self.upload_dir = settings.UPLOAD_DIR
        self.output_dir = settings.OUTPUT_DIR
        self.chunk_size = settings.CHUNK_SIZE
        
        # Ensure directories exist
        ensure_directory(self.upload_dir)
        ensure_directory(self.output_dir)
    
    def save_upload(
        self,
        file_data: BinaryIO,
        filename: str,
        destination: Optional[str | Path] = None
    ) -> Path:
        """
        Save uploaded file
        
        Args:
            file_data: File data (binary)
            filename: Original filename
            destination: Destination directory (default: upload_dir)
            
        Returns:
            Path to saved file
        """
        if destination is None:
            destination = self.upload_dir
        else:
            destination = Path(destination)
            ensure_directory(destination)
        
        # Sanitize filename
        safe_filename = sanitize_filename(filename)
        
        # Generate unique filename
        unique_filename = generate_unique_filename(safe_filename, destination)
        file_path = destination / unique_filename
        
        # Save file
        try:
            with open(file_path, 'wb') as f:
                shutil.copyfileobj(file_data, f)
            
            logger.info(f"File saved: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Failed to save file: {e}")
            raise
    
    async def save_upload_async(
        self,
        file_data: bytes,
        filename: str,
        destination: Optional[str | Path] = None
    ) -> Path:
        """
        Save uploaded file asynchronously
        
        Args:
            file_data: File data (bytes)
            filename: Original filename
            destination: Destination directory
            
        Returns:
            Path to saved file
        """
        if destination is None:
            destination = self.upload_dir
        else:
            destination = Path(destination)
            ensure_directory(destination)
        
        safe_filename = sanitize_filename(filename)
        unique_filename = generate_unique_filename(safe_filename, destination)
        file_path = destination / unique_filename
        
        try:
            async with aiofiles.open(file_path, 'wb') as f:
                await f.write(file_data)
            
            logger.info(f"File saved (async): {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Failed to save file (async): {e}")
            raise
    
    def copy_file(self, source: str | Path, destination: str | Path) -> Path:
        """
        Copy file to destination
        
        Args:
            source: Source file path
            destination: Destination path
            
        Returns:
            Path to copied file
        """
        source = Path(source)
        destination = Path(destination)
        
        # If destination is directory, keep original filename
        if destination.is_dir():
            destination = destination / source.name
        
        # Ensure destination directory exists
        ensure_directory(destination.parent)
        
        try:
            shutil.copy2(source, destination)
            logger.info(f"File copied: {source} -> {destination}")
            return destination
            
        except Exception as e:
            logger.error(f"Failed to copy file: {e}")
            raise
    
    def move_file(self, source: str | Path, destination: str | Path) -> Path:
        """
        Move file to destination
        
        Args:
            source: Source file path
            destination: Destination path
            
        Returns:
            Path to moved file
        """
        source = Path(source)
        destination = Path(destination)
        
        if destination.is_dir():
            destination = destination / source.name
        
        ensure_directory(destination.parent)
        
        try:
            shutil.move(str(source), str(destination))
            logger.info(f"File moved: {source} -> {destination}")
            return destination
            
        except Exception as e:
            logger.error(f"Failed to move file: {e}")
            raise
    
    def delete_file(self, file_path: str | Path) -> bool:
        """
        Delete file
        
        Args:
            file_path: Path to file
            
        Returns:
            True if successful
        """
        file_path = Path(file_path)
        
        try:
            if file_path.exists() and file_path.is_file():
                file_path.unlink()
                logger.info(f"File deleted: {file_path}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Failed to delete file: {e}")
            return False
    
    def delete_files(self, file_paths: List[str | Path]) -> int:
        """
        Delete multiple files
        
        Args:
            file_paths: List of file paths
            
        Returns:
            Number of files deleted
        """
        count = 0
        for file_path in file_paths:
            if self.delete_file(file_path):
                count += 1
        
        logger.info(f"Deleted {count}/{len(file_paths)} files")
        return count
    
    def cleanup_temp_files(self, max_age_hours: int = 24):
        """
        Clean up old temporary files
        
        Args:
            max_age_hours: Maximum age in hours
        """
        import time
        
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        
        count = 0
        for file_path in self.upload_dir.glob('*'):
            if file_path.is_file():
                file_age = current_time - file_path.stat().st_mtime
                if file_age > max_age_seconds:
                    if self.delete_file(file_path):
                        count += 1
        
        logger.info(f"Cleaned up {count} temporary files")
        return count
    
    def get_output_path(
        self,
        input_file: str | Path,
        output_format: str,
        output_dir: Optional[str | Path] = None
    ) -> Path:
        """
        Generate output file path
        
        Args:
            input_file: Input file path
            output_format: Output format (extension without dot)
            output_dir: Output directory (default: output_dir from settings)
            
        Returns:
            Output file path
        """
        input_file = Path(input_file)
        
        if output_dir is None:
            output_dir = self.output_dir
        else:
            output_dir = Path(output_dir)
        
        ensure_directory(output_dir)
        
        # Create output filename
        output_filename = f"{input_file.stem}.{output_format.lower()}"
        output_filename = generate_unique_filename(output_filename, output_dir)
        
        return output_dir / output_filename
    
    def read_file_chunks(self, file_path: str | Path, chunk_size: Optional[int] = None):
        """
        Read file in chunks (generator)
        
        Args:
            file_path: Path to file
            chunk_size: Chunk size in bytes
            
        Yields:
            File chunks
        """
        if chunk_size is None:
            chunk_size = self.chunk_size
        
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                yield chunk
    
    async def read_file_chunks_async(
        self,
        file_path: str | Path,
        chunk_size: Optional[int] = None
    ):
        """
        Read file in chunks asynchronously (async generator)
        
        Args:
            file_path: Path to file
            chunk_size: Chunk size in bytes
            
        Yields:
            File chunks
        """
        if chunk_size is None:
            chunk_size = self.chunk_size
        
        async with aiofiles.open(file_path, 'rb') as f:
            while True:
                chunk = await f.read(chunk_size)
                if not chunk:
                    break
                yield chunk
    
    def get_file_info(self, file_path: str | Path) -> dict:
        """
        Get file information
        
        Args:
            file_path: Path to file
            
        Returns:
            Dictionary with file info
        """
        from utils.helpers import parse_file_path
        return parse_file_path(file_path)


# Convenience instance
file_handler = FileHandler()
