"""
Batch Processing Workflow
Automated batch conversion with advanced features
"""

import asyncio
from pathlib import Path
from typing import List, Optional, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from converters import ConverterFactory
from utils.logger import get_logger
from utils.progress import BatchProgressTracker
from utils.errors import ConversionError
from utils.config_loader import get_batch_settings
from utils.helpers import get_file_extension

logger = get_logger(__name__)


class BatchProcessor:
    """Process multiple file conversions"""
    
    def __init__(self, max_workers: Optional[int] = None):
        self.factory = ConverterFactory()
        self.batch_settings = get_batch_settings()
        self.max_workers = max_workers or self.batch_settings.get('max_concurrent', 4)
        self.timeout = self.batch_settings.get('timeout_seconds', 300)
        self.retry_attempts = self.batch_settings.get('retry_attempts', 3)
        self.skip_errors = self.batch_settings.get('skip_errors', True)
    
    def process_batch(
        self,
        input_files: List[Path],
        output_dir: Path,
        output_format: str,
        quality: str = 'high',
        callback: Optional[callable] = None
    ) -> Dict[str, Any]:
        """
        Process batch of files
        
        Args:
            input_files: List of input file paths
            output_dir: Output directory
            output_format: Target format
            quality: Conversion quality
            callback: Progress callback function
            
        Returns:
            Dictionary with results
        """
        start_time = time.time()
        
        # Ensure output directory exists
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize tracker
        tracker = BatchProgressTracker(total_files=len(input_files))
        
        # Results storage
        results = {
            'successful': [],
            'failed': [],
            'skipped': []
        }
        
        # Process files with thread pool
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_file = {
                executor.submit(
                    self._convert_with_retry,
                    file,
                    output_dir,
                    output_format,
                    quality
                ): file
                for file in input_files
            }
            
            # Process completed tasks
            for future in as_completed(future_to_file):
                file = future_to_file[future]
                tracker.start_file(file.name)
                
                try:
                    result = future.result(timeout=self.timeout)
                    
                    if result['success']:
                        tracker.complete_file(success=True)
                        results['successful'].append(result)
                        logger.info(f"Successfully converted: {file.name}")
                    else:
                        tracker.complete_file(success=False)
                        results['failed'].append(result)
                        logger.error(f"Failed to convert: {file.name}")
                    
                except Exception as e:
                    tracker.complete_file(success=False)
                    results['failed'].append({
                        'input_file': str(file),
                        'success': False,
                        'error': str(e)
                    })
                    logger.error(f"Error processing {file.name}: {e}")
                
                # Call progress callback
                if callback:
                    callback(tracker.get_status())
        
        # Calculate statistics
        total_time = time.time() - start_time
        
        return {
            'total_files': len(input_files),
            'successful': len(results['successful']),
            'failed': len(results['failed']),
            'skipped': len(results['skipped']),
            'results': results,
            'total_time': total_time,
            'average_time': total_time / len(input_files) if input_files else 0
        }
    
    def _convert_with_retry(
        self,
        input_file: Path,
        output_dir: Path,
        output_format: str,
        quality: str
    ) -> Dict[str, Any]:
        """
        Convert file with retry logic
        
        Args:
            input_file: Input file path
            output_dir: Output directory
            output_format: Target format
            quality: Conversion quality
            
        Returns:
            Result dictionary
        """
        last_error = None
        
        for attempt in range(self.retry_attempts):
            try:
                # Generate output path
                output_file = output_dir / f"{input_file.stem}.{output_format}"
                
                # Perform conversion
                result = self.factory.convert(
                    input_file,
                    output_file,
                    quality=quality
                )
                
                return {
                    'input_file': str(input_file),
                    'output_file': str(result),
                    'success': True,
                    'attempts': attempt + 1
                }
                
            except Exception as e:
                last_error = e
                logger.warning(
                    f"Conversion attempt {attempt + 1}/{self.retry_attempts} "
                    f"failed for {input_file.name}: {e}"
                )
                
                if attempt < self.retry_attempts - 1:
                    time.sleep(1)  # Wait before retry
        
        # All attempts failed
        return {
            'input_file': str(input_file),
            'success': False,
            'error': str(last_error),
            'attempts': self.retry_attempts
        }
    
    async def process_batch_async(
        self,
        input_files: List[Path],
        output_dir: Path,
        output_format: str,
        quality: str = 'high'
    ) -> Dict[str, Any]:
        """
        Process batch asynchronously
        
        Args:
            input_files: List of input files
            output_dir: Output directory
            output_format: Target format
            quality: Conversion quality
            
        Returns:
            Results dictionary
        """
        start_time = time.time()
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create tasks
        tasks = [
            self._convert_async(file, output_dir, output_format, quality)
            for file in input_files
        ]
        
        # Process all tasks
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Categorize results
        successful = []
        failed = []
        
        for result in results:
            if isinstance(result, Exception):
                failed.append({'error': str(result), 'success': False})
            elif result.get('success'):
                successful.append(result)
            else:
                failed.append(result)
        
        total_time = time.time() - start_time
        
        return {
            'total_files': len(input_files),
            'successful': len(successful),
            'failed': len(failed),
            'results': {'successful': successful, 'failed': failed},
            'total_time': total_time
        }
    
    async def _convert_async(
        self,
        input_file: Path,
        output_dir: Path,
        output_format: str,
        quality: str
    ) -> Dict[str, Any]:
        """Async conversion wrapper"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self._convert_with_retry,
            input_file,
            output_dir,
            output_format,
            quality
        )


def find_files(
    directory: Path,
    extensions: Optional[List[str]] = None,
    recursive: bool = False
) -> List[Path]:
    """
    Find files in directory
    
    Args:
        directory: Directory to search
        extensions: List of extensions to include (e.g., ['pdf', 'docx'])
        recursive: Search subdirectories
        
    Returns:
        List of file paths
    """
    if recursive:
        pattern = '**/*.*'
    else:
        pattern = '*.*'
    
    files = []
    for file in directory.glob(pattern):
        if file.is_file():
            if extensions is None:
                files.append(file)
            else:
                ext = get_file_extension(file)
                if ext in extensions:
                    files.append(file)
    
    return files


def batch_convert_directory(
    input_dir: str | Path,
    output_dir: str | Path,
    output_format: str,
    quality: str = 'high',
    recursive: bool = False,
    max_workers: Optional[int] = None
) -> Dict[str, Any]:
    """
    Batch convert all files in directory
    
    Args:
        input_dir: Input directory
        output_dir: Output directory
        output_format: Target format
        quality: Conversion quality
        recursive: Process subdirectories
        max_workers: Maximum concurrent workers
        
    Returns:
        Results dictionary
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    # Find files
    from converters import get_supported_formats
    supported_formats = get_supported_formats()
    files = find_files(input_path, extensions=supported_formats, recursive=recursive)
    
    if not files:
        logger.warning(f"No supported files found in {input_dir}")
        return {
            'total_files': 0,
            'successful': 0,
            'failed': 0,
            'results': {'successful': [], 'failed': []}
        }
    
    # Process batch
    processor = BatchProcessor(max_workers=max_workers)
    return processor.process_batch(files, output_path, output_format, quality)
