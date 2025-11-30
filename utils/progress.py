"""
Progress tracking utilities
Track conversion progress for CLI and API
"""

from typing import Optional, Callable
from tqdm import tqdm
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TimeRemainingColumn,
    TimeElapsedColumn
)
from rich.console import Console
from utils.logger import get_logger

logger = get_logger(__name__)
console = Console()


class ProgressTracker:
    """Track conversion progress"""
    
    def __init__(self, total: int = 100, description: str = "Processing"):
        self.total = total
        self.current = 0
        self.description = description
        self.callbacks = []
    
    def update(self, amount: int = 1):
        """Update progress"""
        self.current += amount
        self._notify_callbacks()
    
    def set_progress(self, value: int):
        """Set progress to specific value"""
        self.current = value
        self._notify_callbacks()
    
    def add_callback(self, callback: Callable):
        """Add progress callback"""
        self.callbacks.append(callback)
    
    def _notify_callbacks(self):
        """Notify all callbacks"""
        for callback in self.callbacks:
            try:
                callback(self.current, self.total)
            except Exception as e:
                logger.error(f"Progress callback error: {e}")
    
    def get_percentage(self) -> float:
        """Get progress percentage"""
        if self.total == 0:
            return 0.0
        return (self.current / self.total) * 100
    
    def is_complete(self) -> bool:
        """Check if progress is complete"""
        return self.current >= self.total


class CLIProgressBar:
    """CLI progress bar using tqdm"""
    
    def __init__(
        self,
        total: int,
        description: str = "Processing",
        unit: str = "file"
    ):
        self.pbar = tqdm(
            total=total,
            desc=description,
            unit=unit,
            bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]'
        )
    
    def update(self, amount: int = 1):
        """Update progress"""
        self.pbar.update(amount)
    
    def set_description(self, description: str):
        """Update description"""
        self.pbar.set_description(description)
    
    def close(self):
        """Close progress bar"""
        self.pbar.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class RichProgressBar:
    """Rich progress bar with multiple columns"""
    
    def __init__(self):
        self.progress = Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            TimeRemainingColumn(),
            console=console
        )
        self.tasks = {}
    
    def add_task(
        self,
        name: str,
        total: int,
        description: str = ""
    ) -> int:
        """Add a new task"""
        task_id = self.progress.add_task(
            description or name,
            total=total
        )
        self.tasks[name] = task_id
        return task_id
    
    def update(self, name: str, advance: int = 1):
        """Update task progress"""
        if name in self.tasks:
            self.progress.update(self.tasks[name], advance=advance)
    
    def set_description(self, name: str, description: str):
        """Update task description"""
        if name in self.tasks:
            self.progress.update(
                self.tasks[name],
                description=description
            )
    
    def start(self):
        """Start progress display"""
        self.progress.start()
    
    def stop(self):
        """Stop progress display"""
        self.progress.stop()
    
    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()


class BatchProgressTracker:
    """Track batch conversion progress"""
    
    def __init__(self, total_files: int):
        self.total_files = total_files
        self.completed = 0
        self.successful = 0
        self.failed = 0
        self.current_file = ""
        self.callbacks = []
    
    def start_file(self, filename: str):
        """Mark file conversion start"""
        self.current_file = filename
        logger.info(f"Processing: {filename}")
    
    def complete_file(self, success: bool = True):
        """Mark file conversion complete"""
        self.completed += 1
        if success:
            self.successful += 1
        else:
            self.failed += 1
        
        self._notify_callbacks()
    
    def add_callback(self, callback: Callable):
        """Add progress callback"""
        self.callbacks.append(callback)
    
    def _notify_callbacks(self):
        """Notify all callbacks"""
        for callback in self.callbacks:
            try:
                callback(self.get_status())
            except Exception as e:
                logger.error(f"Batch progress callback error: {e}")
    
    def get_status(self) -> dict:
        """Get current status"""
        return {
            'total': self.total_files,
            'completed': self.completed,
            'successful': self.successful,
            'failed': self.failed,
            'remaining': self.total_files - self.completed,
            'current_file': self.current_file,
            'percentage': (self.completed / self.total_files * 100) if self.total_files > 0 else 0
        }
    
    def print_summary(self):
        """Print conversion summary"""
        console.print("\n[bold]Conversion Summary:[/bold]")
        console.print(f"Total files: {self.total_files}")
        console.print(f"[green]Successful: {self.successful}[/green]")
        console.print(f"[red]Failed: {self.failed}[/red]")
        
        if self.total_files > 0:
            success_rate = (self.successful / self.total_files) * 100
            console.print(f"Success rate: {success_rate:.1f}%")


def create_progress_bar(
    total: int,
    description: str = "Processing",
    style: str = "tqdm"
) -> CLIProgressBar | RichProgressBar:
    """
    Create progress bar
    
    Args:
        total: Total items
        description: Progress description
        style: Progress bar style ('tqdm' or 'rich')
        
    Returns:
        Progress bar instance
    """
    if style == "rich":
        pbar = RichProgressBar()
        pbar.add_task("main", total, description)
        return pbar
    else:
        return CLIProgressBar(total, description)
