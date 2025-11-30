#!/usr/bin/env python3
"""
Universal Document Converter - Main Entry Point
Supports CLI, API, and Web interfaces
"""

import sys
import argparse
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))


def main():
    """Main entry point for the application"""
    parser = argparse.ArgumentParser(
        description="Universal Document Converter",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert single file
  python main.py convert input.pdf output.docx
  
  # Start API server
  python main.py api --port 8000
  
  # Start Streamlit UI
  python main.py streamlit
  
  # Batch convert
  python main.py batch --input-dir ./docs --output-format pdf
  
  # List supported formats
  python main.py formats
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Convert command
    convert_parser = subparsers.add_parser('convert', help='Convert a single file')
    convert_parser.add_argument('input', help='Input file path')
    convert_parser.add_argument('output', help='Output file path')
    convert_parser.add_argument('--quality', choices=['low', 'medium', 'high'], 
                                default='high', help='Conversion quality')
    
    # Batch convert command
    batch_parser = subparsers.add_parser('batch', help='Batch convert files')
    batch_parser.add_argument('--input-dir', required=True, help='Input directory')
    batch_parser.add_argument('--output-dir', help='Output directory (default: ./outputs)')
    batch_parser.add_argument('--output-format', required=True, 
                             choices=['pdf', 'docx', 'xlsx', 'csv', 'json', 'txt'],
                             help='Target format')
    batch_parser.add_argument('--recursive', action='store_true', 
                             help='Process subdirectories')
    
    # API command
    api_parser = subparsers.add_parser('api', help='Start API server')
    api_parser.add_argument('--host', default='0.0.0.0', help='Host address')
    api_parser.add_argument('--port', type=int, default=8000, help='Port number')
    api_parser.add_argument('--reload', action='store_true', help='Enable auto-reload')
    
    # Streamlit command
    streamlit_parser = subparsers.add_parser('streamlit', help='Start Streamlit UI')
    streamlit_parser.add_argument('--port', type=int, default=8501, help='Port number')
    
    # Formats command
    formats_parser = subparsers.add_parser('formats', help='List supported formats')
    
    # Version command
    version_parser = subparsers.add_parser('version', help='Show version')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Route to appropriate handler
    if args.command == 'convert':
        from cli.main import convert_file
        convert_file(args.input, args.output, quality=args.quality)
        
    elif args.command == 'batch':
        from cli.main import batch_convert
        batch_convert(
            args.input_dir, 
            args.output_dir or './outputs',
            args.output_format,
            recursive=args.recursive
        )
        
    elif args.command == 'api':
        import uvicorn
        uvicorn.run(
            "api.main:app",
            host=args.host,
            port=args.port,
            reload=args.reload
        )
        
    elif args.command == 'streamlit':
        import subprocess
        subprocess.run([
            'streamlit', 'run', 
            'streamlit_app/app.py',
            '--server.port', str(args.port)
        ])
        
    elif args.command == 'formats':
        from cli.main import list_formats
        list_formats()
        
    elif args.command == 'version':
        print("Universal Document Converter v1.0.0")


if __name__ == '__main__':
    main()
