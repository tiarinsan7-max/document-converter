"""
CLI Main Module
Command-line interface for document conversion
"""

import sys
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint
from converters import ConverterFactory, get_supported_formats, get_supported_conversions
from utils.logger import get_logger
from utils.progress import CLIProgressBar, BatchProgressTracker
from utils.errors import ConversionError
from utils.helpers import format_file_size, get_file_size

logger = get_logger(__name__)
console = Console()

# Initialize factory
factory = ConverterFactory()


def convert_file(
    input_file: str,
    output_file: str,
    quality: str = 'high'
) -> bool:
    """
    Convert a single file
    
    Args:
        input_file: Path to input file
        output_file: Path to output file
        quality: Conversion quality
        
    Returns:
        True if successful
    """
    try:
        input_path = Path(input_file)
        output_path = Path(output_file)
        
        # Check if input exists
        if not input_path.exists():
            console.print(f"[red]Error: Input file not found: {input_file}[/red]")
            return False
        
        # Get formats
        input_format = input_path.suffix.lower().replace('.', '')
        output_format = output_path.suffix.lower().replace('.', '')
        
        # Display info
        console.print(Panel.fit(
            f"[bold cyan]Converting:[/bold cyan] {input_path.name}\n"
            f"[bold cyan]From:[/bold cyan] {input_format.upper()}\n"
            f"[bold cyan]To:[/bold cyan] {output_format.upper()}\n"
            f"[bold cyan]Quality:[/bold cyan] {quality}",
            title="Document Conversion",
            border_style="cyan"
        ))
        
        # Convert with progress
        with CLIProgressBar(total=100, description="Converting") as pbar:
            pbar.update(20)
            result = factory.convert(input_path, output_path, quality=quality)
            pbar.update(80)
        
        # Display success
        output_size = get_file_size(result)
        console.print(f"\n[green]✓ Conversion successful![/green]")
        console.print(f"[cyan]Output file:[/cyan] {result}")
        console.print(f"[cyan]File size:[/cyan] {format_file_size(output_size)}")
        
        return True
        
    except ConversionError as e:
        console.print(f"\n[red]✗ Conversion failed:[/red] {e}")
        logger.error(f"Conversion failed: {e}")
        return False
        
    except Exception as e:
        console.print(f"\n[red]✗ Unexpected error:[/red] {e}")
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return False


def batch_convert(
    input_dir: str,
    output_dir: str,
    output_format: str,
    recursive: bool = False,
    quality: str = 'high'
) -> bool:
    """
    Convert multiple files in a directory
    
    Args:
        input_dir: Input directory path
        output_dir: Output directory path
        output_format: Target output format
        recursive: Process subdirectories
        quality: Conversion quality
        
    Returns:
        True if at least one file converted successfully
    """
    try:
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        
        # Check if input directory exists
        if not input_path.exists():
            console.print(f"[red]Error: Input directory not found: {input_dir}[/red]")
            return False
        
        # Create output directory
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Find files
        if recursive:
            files = list(input_path.rglob('*.*'))
        else:
            files = list(input_path.glob('*.*'))
        
        # Filter supported files
        supported_formats = get_supported_formats()
        files = [
            f for f in files
            if f.is_file() and f.suffix.lower().replace('.', '') in supported_formats
        ]
        
        if not files:
            console.print("[yellow]No supported files found in directory[/yellow]")
            return False
        
        # Display info
        console.print(Panel.fit(
            f"[bold cyan]Batch Conversion[/bold cyan]\n"
            f"[cyan]Input directory:[/cyan] {input_path}\n"
            f"[cyan]Output directory:[/cyan] {output_path}\n"
            f"[cyan]Output format:[/cyan] {output_format.upper()}\n"
            f"[cyan]Files found:[/cyan] {len(files)}\n"
            f"[cyan]Quality:[/cyan] {quality}",
            title="Batch Processing",
            border_style="cyan"
        ))
        
        # Initialize tracker
        tracker = BatchProgressTracker(total_files=len(files))
        
        # Process files
        with CLIProgressBar(total=len(files), description="Processing files") as pbar:
            for file in files:
                tracker.start_file(file.name)
                
                try:
                    # Generate output filename
                    output_file = output_path / f"{file.stem}.{output_format}"
                    
                    # Convert
                    factory.convert(file, output_file, quality=quality)
                    
                    tracker.complete_file(success=True)
                    pbar.set_description(f"✓ {file.name}")
                    
                except Exception as e:
                    tracker.complete_file(success=False)
                    logger.error(f"Failed to convert {file.name}: {e}")
                    pbar.set_description(f"✗ {file.name}")
                
                pbar.update(1)
        
        # Display summary
        console.print()
        tracker.print_summary()
        
        return tracker.successful > 0
        
    except Exception as e:
        console.print(f"\n[red]✗ Batch conversion failed:[/red] {e}")
        logger.error(f"Batch conversion failed: {e}", exc_info=True)
        return False


def list_formats():
    """Display supported formats and conversions"""
    
    # Get formats
    formats = get_supported_formats()
    
    # Create formats table
    formats_table = Table(title="Supported Formats", show_header=True, header_style="bold cyan")
    formats_table.add_column("Format", style="cyan", width=10)
    formats_table.add_column("Extension", style="yellow", width=12)
    formats_table.add_column("Description", style="white")
    
    format_descriptions = {
        'pdf': ('PDF', 'Portable Document Format'),
        'docx': ('DOCX', 'Microsoft Word Document'),
        'xlsx': ('XLSX', 'Microsoft Excel Spreadsheet'),
        'csv': ('CSV', 'Comma-Separated Values'),
        'json': ('JSON', 'JavaScript Object Notation'),
        'txt': ('TXT', 'Plain Text File')
    }
    
    for fmt in formats:
        ext, desc = format_descriptions.get(fmt, (fmt.upper(), 'Document format'))
        formats_table.add_row(fmt.upper(), f".{fmt}", desc)
    
    console.print(formats_table)
    console.print()
    
    # Create conversion matrix table
    matrix_table = Table(title="Conversion Matrix", show_header=True, header_style="bold cyan")
    matrix_table.add_column("From \\ To", style="cyan", width=10)
    
    for fmt in formats:
        matrix_table.add_column(fmt.upper(), justify="center", width=6)
    
    for input_fmt in formats:
        row = [input_fmt.upper()]
        conversions = get_supported_conversions(input_fmt)
        
        for output_fmt in formats:
            if input_fmt == output_fmt:
                row.append("[dim]-[/dim]")
            elif output_fmt in conversions:
                row.append("[green]✓[/green]")
            else:
                row.append("[red]✗[/red]")
        
        matrix_table.add_row(*row)
    
    console.print(matrix_table)
    console.print()
    
    # Display statistics
    total_conversions = sum(len(get_supported_conversions(fmt)) for fmt in formats)
    console.print(Panel.fit(
        f"[bold cyan]Total Formats:[/bold cyan] {len(formats)}\n"
        f"[bold cyan]Total Conversions:[/bold cyan] {total_conversions}",
        title="Statistics",
        border_style="cyan"
    ))


def show_help():
    """Display help information"""
    
    help_text = """
[bold cyan]Universal Document Converter - CLI[/bold cyan]

[bold]USAGE:[/bold]
    python main.py <command> [options]

[bold]COMMANDS:[/bold]
    [cyan]convert[/cyan] <input> <output>           Convert a single file
    [cyan]batch[/cyan] --input-dir <dir> ...        Batch convert files
    [cyan]formats[/cyan]                            List supported formats
    [cyan]api[/cyan] [--port 8000]                  Start API server
    [cyan]streamlit[/cyan] [--port 8501]            Start Streamlit UI
    [cyan]version[/cyan]                            Show version

[bold]EXAMPLES:[/bold]
    # Convert single file
    python main.py convert document.pdf output.docx

    # Batch convert
    python main.py batch --input-dir ./docs --output-format pdf

    # List formats
    python main.py formats

    # Start API
    python main.py api --port 8000 --reload

[bold]OPTIONS:[/bold]
    --quality <low|medium|high>    Conversion quality (default: high)
    --recursive                    Process subdirectories
    --help                         Show this help message
    """
    
    console.print(Panel(help_text, title="Help", border_style="cyan"))


def display_banner():
    """Display application banner"""
    
    banner = """
[bold cyan]
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║     Universal Document Converter                         ║
║     Convert between PDF, DOCX, XLSX, CSV, JSON, TXT      ║
║                                                           ║
║     Version 1.0.0                                         ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
[/bold cyan]
    """
    
    console.print(banner)
