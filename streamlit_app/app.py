"""
Streamlit Web UI for Document Converter - IMPROVED VERSION
Interactive web interface for file conversion with enhanced features
"""

import streamlit as st
import sys
from pathlib import Path
import time
import io
import zipfile
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from converters import ConverterFactory, get_supported_formats, get_supported_conversions
from utils.validators import validate_file
from utils.helpers import format_file_size, get_file_size
from utils.errors import ConversionError, UnsupportedFormatError
from Workflows import batch_convert_directory
import tempfile
import shutil

# Constants
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
VERSION = "1.1.0"

# Page configuration
st.set_page_config(
    page_title="Universal Document Converter",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'conversion_history' not in st.session_state:
    st.session_state.conversion_history = []
if 'quality_preference' not in st.session_state:
    st.session_state.quality_preference = 'high'
if 'total_conversions' not in st.session_state:
    st.session_state.total_conversions = 0
if 'total_files_converted' not in st.session_state:
    st.session_state.total_files_converted = 0

# Initialize factory
@st.cache_resource
def get_factory():
    return ConverterFactory()

factory = get_factory()

# Helper function to estimate conversion time
def estimate_conversion_time(file_size_bytes):
    """Estimate conversion time based on file size"""
    mb_size = file_size_bytes / (1024 * 1024)
    # Rough estimate: ~2 seconds per MB
    estimated_seconds = max(1, int(mb_size * 2))
    return estimated_seconds

# Helper function to add to conversion history
def add_to_history(input_file, input_format, output_format, file_size, conversion_time, success=True):
    """Add conversion to history"""
    st.session_state.conversion_history.insert(0, {
        'timestamp': datetime.now(),
        'input_file': input_file,
        'input_format': input_format.upper(),
        'output_format': output_format.upper(),
        'size': file_size,
        'time': conversion_time,
        'success': success
    })
    # Keep only last 20 conversions
    st.session_state.conversion_history = st.session_state.conversion_history[:20]
    
    if success:
        st.session_state.total_conversions += 1
        st.session_state.total_files_converted += 1

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        text-align: center;
        color: #666;
        margin-bottom: 3rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
    }
    .history-item {
        padding: 0.5rem;
        margin: 0.25rem 0;
        border-left: 3px solid #1f77b4;
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">📄 Universal Document Converter</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Convert between PDF, DOCX, XLSX, CSV, JSON, and TXT</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Mode selection
    mode = st.radio(
        "Conversion Mode",
        ["Single File", "Batch Conversion", "About"],
        index=0
    )
    
    st.divider()
    
    # Quality settings with saved preference
    quality = st.select_slider(
        "Quality",
        options=["low", "medium", "high"],
        value=st.session_state.quality_preference,
        help="Higher quality = better output but slower conversion"
    )
    # Save preference
    st.session_state.quality_preference = quality
    
    st.divider()
    
    # Supported formats
    st.subheader("📋 Supported Formats")
    formats = get_supported_formats()
    for fmt in formats:
        st.text(f"• {fmt.upper()}")
    
    st.divider()
    
    # Statistics
    st.subheader("📊 Statistics")
    st.metric("Total Formats", len(formats))
    total_conversions = sum(len(get_supported_conversions(fmt)) for fmt in formats)
    st.metric("Available Conversions", total_conversions)
    st.metric("Your Conversions", st.session_state.total_conversions)
    
    st.divider()
    
    # Conversion History
    if st.session_state.conversion_history:
        st.subheader("📜 Recent Conversions")
        
        for idx, item in enumerate(st.session_state.conversion_history[:5]):
            if item['success']:
                icon = "✅"
                color = "#28a745"
            else:
                icon = "❌"
                color = "#dc3545"
            
            time_str = item['timestamp'].strftime("%H:%M")
            st.markdown(f"""
            <div style='font-size: 0.85rem; padding: 0.3rem; margin: 0.2rem 0; 
                        border-left: 3px solid {color}; background-color: #f8f9fa;'>
                {icon} <b>{item['input_file'][:20]}...</b><br/>
                <span style='color: #666;'>{item['input_format']} → {item['output_format']} • {time_str}</span>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.conversion_history = []
            st.rerun()

# Main content
if mode == "Single File":
    st.header("📤 Single File Conversion")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Upload File")
        uploaded_file = st.file_uploader(
            "Choose a file to convert",
            type=['pdf', 'docx', 'xlsx', 'csv', 'json', 'txt'],
            help=f"Upload a file in any supported format (Max: {format_file_size(MAX_FILE_SIZE)})"
        )
        
        if uploaded_file:
            file_size = len(uploaded_file.getvalue())
            
            # Check file size limit
            if file_size > MAX_FILE_SIZE:
                st.error(f"❌ File too large! Maximum size: {format_file_size(MAX_FILE_SIZE)}")
                st.info(f"💡 Your file: {format_file_size(file_size)}")
                st.stop()
            
            st.success(f"✓ File uploaded: {uploaded_file.name}")
            
            # Show file info
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("File Size", format_file_size(file_size))
            with col_b:
                est_time = estimate_conversion_time(file_size)
                st.metric("Est. Time", f"~{est_time}s")
    
    with col2:
        st.subheader("Output Format")
        
        if uploaded_file:
            # Get input format
            input_format = Path(uploaded_file.name).suffix.lower().replace('.', '')
            
            # Get available conversions
            available_formats = get_supported_conversions(input_format)
            
            if available_formats:
                output_format = st.selectbox(
                    "Select output format",
                    available_formats,
                    format_func=lambda x: x.upper()
                )
                
                st.info(f"🔄 Converting from {input_format.upper()} to {output_format.upper()}")
            else:
                st.error("No conversions available for this format")
                output_format = None
        else:
            st.info("Upload a file to see available formats")
            output_format = None
    
    # Convert button
    if uploaded_file and output_format:
        st.divider()
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            convert_button = st.button(
                "🚀 Convert File",
                type="primary",
                use_container_width=True
            )
        
        if convert_button:
            tmp_input_path = None
            tmp_output_path = None
            
            try:
                # Create progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Save uploaded file to temp
                status_text.text("📥 Saving uploaded file...")
                progress_bar.progress(20)
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_input:
                    tmp_input.write(uploaded_file.getvalue())
                    tmp_input_path = Path(tmp_input.name)
                
                # Create output path
                status_text.text("🔄 Converting file...")
                progress_bar.progress(40)
                
                tmp_output_path = tmp_input_path.parent / f"{tmp_input_path.stem}.{output_format}"
                
                # Convert
                start_time = time.time()
                result = factory.convert(
                    tmp_input_path,
                    tmp_output_path,
                    quality=quality
                )
                conversion_time = time.time() - start_time
                
                progress_bar.progress(80)
                status_text.text("✅ Conversion complete!")
                
                # Read converted file
                with open(result, 'rb') as f:
                    converted_data = f.read()
                
                progress_bar.progress(100)
                
                # Success message
                st.success("🎉 Conversion successful!")
                
                # Add to history
                add_to_history(
                    uploaded_file.name,
                    input_format,
                    output_format,
                    file_size,
                    conversion_time,
                    success=True
                )
                
                # Display info
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Input Format", input_format.upper())
                with col2:
                    st.metric("Output Format", output_format.upper())
                with col3:
                    st.metric("Conversion Time", f"{conversion_time:.2f}s")
                
                # Download button
                st.download_button(
                    label="⬇️ Download Converted File",
                    data=converted_data,
                    file_name=f"{Path(uploaded_file.name).stem}.{output_format}",
                    mime="application/octet-stream",
                    type="primary",
                    use_container_width=True
                )
                
            except ConversionError as e:
                st.error(f"❌ Conversion failed: {str(e)}")
                st.info("💡 **Suggestions:**\n- Check if the file is corrupted\n- Try a different output format\n- Reduce quality setting\n- Ensure the file is a valid format")
                add_to_history(uploaded_file.name, input_format, output_format, file_size, 0, success=False)
                
            except UnsupportedFormatError as e:
                st.error(f"❌ Unsupported conversion: {str(e)}")
                st.info("💡 This conversion pair is not supported. Try a different output format.")
                
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")
                st.warning("⚠️ Please report this issue with the file type and size")
                add_to_history(uploaded_file.name, input_format, output_format, file_size, 0, success=False)
                
            finally:
                # Always cleanup temp files
                if tmp_input_path:
                    tmp_input_path.unlink(missing_ok=True)
                if tmp_output_path:
                    tmp_output_path.unlink(missing_ok=True)
                
                # Clear progress indicators
                if 'progress_bar' in locals():
                    progress_bar.empty()
                if 'status_text' in locals():
                    status_text.empty()

elif mode == "Batch Conversion":
    st.header("📦 Batch Conversion")
    
    st.info("💡 Upload multiple files to convert them all at once")
    
    # File uploader for multiple files
    uploaded_files = st.file_uploader(
        "Choose files to convert",
        type=['pdf', 'docx', 'xlsx', 'csv', 'json', 'txt'],
        accept_multiple_files=True,
        help=f"Upload multiple files for batch conversion (Max per file: {format_file_size(MAX_FILE_SIZE)})"
    )
    
    if uploaded_files:
        # Check total size and individual file sizes
        total_size = sum(len(f.getvalue()) for f in uploaded_files)
        oversized_files = [f for f in uploaded_files if len(f.getvalue()) > MAX_FILE_SIZE]
        
        if oversized_files:
            st.error(f"❌ {len(oversized_files)} file(s) exceed the size limit!")
            for f in oversized_files:
                st.warning(f"• {f.name}: {format_file_size(len(f.getvalue()))} (Max: {format_file_size(MAX_FILE_SIZE)})")
            st.stop()
        
        # Show upload summary
        col1, col2 = st.columns([3, 1])
        with col1:
            st.success(f"✓ {len(uploaded_files)} files uploaded")
        with col2:
            if st.button("🗑️ Clear All"):
                st.rerun()
        
        # Show file list with total size
        with st.expander("📋 View uploaded files"):
            for file in uploaded_files:
                file_size = len(file.getvalue())
                st.text(f"• {file.name} ({format_file_size(file_size)})")
            st.divider()
            st.text(f"Total size: {format_file_size(total_size)}")
        
        # Output format selection
        output_format = st.selectbox(
            "Select output format for all files",
            get_supported_formats(),
            format_func=lambda x: x.upper()
        )
        
        # Convert button
        st.divider()
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            batch_convert_button = st.button(
                f"🚀 Convert All to {output_format.upper()}",
                type="primary",
                use_container_width=True
            )
        
        if batch_convert_button:
            # Create temp directory
            with tempfile.TemporaryDirectory() as tmp_dir:
                tmp_path = Path(tmp_dir)
                input_dir = tmp_path / "input"
                output_dir = tmp_path / "output"
                input_dir.mkdir()
                output_dir.mkdir()
                
                # Save all files
                st.info("📥 Saving uploaded files...")
                for file in uploaded_files:
                    file_path = input_dir / file.name
                    with open(file_path, 'wb') as f:
                        f.write(file.getvalue())
                
                # Progress tracking
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Convert files
                results = {
                    'successful': [],
                    'failed': []
                }
                
                batch_start_time = time.time()
                
                for idx, file in enumerate(uploaded_files):
                    try:
                        status_text.text(f"🔄 Converting {file.name}... ({idx + 1}/{len(uploaded_files)})")
                        
                        input_path = input_dir / file.name
                        input_format = Path(file.name).suffix.lower().replace('.', '')
                        
                        # Check if conversion is supported
                        if factory.supports_conversion(input_format, output_format):
                            output_path = output_dir / f"{Path(file.name).stem}.{output_format}"
                            
                            file_start_time = time.time()
                            factory.convert(input_path, output_path, quality=quality)
                            file_conversion_time = time.time() - file_start_time
                            
                            # Read converted file
                            with open(output_path, 'rb') as f:
                                converted_data = f.read()
                            
                            results['successful'].append({
                                'name': file.name,
                                'output_name': output_path.name,
                                'data': converted_data,
                                'time': file_conversion_time
                            })
                            
                            # Add to history
                            add_to_history(
                                file.name,
                                input_format,
                                output_format,
                                len(file.getvalue()),
                                file_conversion_time,
                                success=True
                            )
                        else:
                            results['failed'].append({
                                'name': file.name,
                                'error': f"Conversion from {input_format} to {output_format} not supported"
                            })
                        
                    except Exception as e:
                        results['failed'].append({
                            'name': file.name,
                            'error': str(e)
                        })
                        add_to_history(file.name, input_format, output_format, len(file.getvalue()), 0, success=False)
                    
                    # Update progress
                    progress = int((idx + 1) / len(uploaded_files) * 100)
                    progress_bar.progress(progress)
                
                total_batch_time = time.time() - batch_start_time
                status_text.text("✅ Batch conversion complete!")
                
                # Display results
                st.divider()
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Files", len(uploaded_files))
                with col2:
                    st.metric("Successful", len(results['successful']), delta_color="normal")
                with col3:
                    st.metric("Failed", len(results['failed']), delta_color="inverse")
                with col4:
                    st.metric("Total Time", f"{total_batch_time:.1f}s")
                
                # Show successful conversions
                if results['successful']:
                    st.success(f"✅ {len(results['successful'])} files converted successfully!")
                    
                    st.subheader("⬇️ Download Converted Files")
                    
                    # Create ZIP file for bulk download
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                        for result in results['successful']:
                            zip_file.writestr(result['output_name'], result['data'])
                    
                    zip_buffer.seek(0)
                    
                    # Bulk download button
                    st.download_button(
                        label=f"📦 Download All as ZIP ({len(results['successful'])} files)",
                        data=zip_buffer,
                        file_name=f"converted_files_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                        mime="application/zip",
                        type="primary",
                        use_container_width=True
                    )
                    
                    st.divider()
                    
                    # Individual download buttons
                    st.caption("Or download files individually:")
                    for result in results['successful']:
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.text(f"📄 {result['output_name']}")
                        with col2:
                            st.download_button(
                                label="Download",
                                data=result['data'],
                                file_name=result['output_name'],
                                mime="application/octet-stream",
                                key=f"download_{result['output_name']}"
                            )
                
                # Show failed conversions
                if results['failed']:
                    st.error(f"❌ {len(results['failed'])} files failed to convert")
                    
                    with st.expander("View errors"):
                        for result in results['failed']:
                            st.text(f"• {result['name']}: {result['error']}")
                        st.info("💡 **Common solutions:**\n- Check if files are corrupted\n- Verify file formats are correct\n- Try converting failed files individually\n- Reduce quality setting")

else:  # About
    st.header("ℹ️ About Universal Document Converter")
    
    st.markdown(f"""
    ### 🎯 Features
    
    - **30+ Conversion Pairs** - Convert between 6 different formats
    - **High Quality** - Preserve formatting and content
    - **Batch Processing** - Convert multiple files at once
    - **Bulk Download** - Download all converted files as ZIP
    - **Conversion History** - Track your recent conversions
    - **Smart Limits** - File size validation (Max: {format_file_size(MAX_FILE_SIZE)})
    - **Fast & Efficient** - Optimized conversion algorithms
    - **Easy to Use** - Simple drag-and-drop interface
    
    ### 📋 Supported Formats
    
    | Format | Description | Extensions |
    |--------|-------------|------------|
    | PDF | Portable Document Format | .pdf |
    | DOCX | Microsoft Word Document | .docx |
    | XLSX | Microsoft Excel Spreadsheet | .xlsx |
    | CSV | Comma-Separated Values | .csv |
    | JSON | JavaScript Object Notation | .json |
    | TXT | Plain Text File | .txt |
    
    ### 🔄 Conversion Matrix
    
    All formats can be converted to all other formats (30 total conversions).
    
    ### 🚀 How to Use
    
    1. **Single File Mode:**
       - Upload a file (max {format_file_size(MAX_FILE_SIZE)})
       - Select output format
       - Click "Convert File"
       - Download the result
    
    2. **Batch Mode:**
       - Upload multiple files
       - Select output format for all
       - Click "Convert All"
       - Download as ZIP or individually
    
    ### ⚙️ Quality Settings
    
    - **Low:** Fast conversion, smaller files
    - **Medium:** Balanced speed and quality
    - **High:** Best quality, larger files (recommended)
    
    ### ✨ New in Version {VERSION}
    
    - ✅ File size limits and validation
    - ✅ Bulk ZIP download for batch conversions
    - ✅ Conversion history tracking
    - ✅ Improved error messages with suggestions
    - ✅ Better progress indicators
    - ✅ Estimated conversion time
    - ✅ Session statistics
    - ✅ Saved user preferences
    
    ### 📚 Documentation
    
    - [README.md](https://github.com/yourusername/converter) - Project overview
    - [API Documentation](http://localhost:8000/docs) - REST API reference
    - [Quick Start Guide](https://github.com/yourusername/converter/QUICKSTART.md)
    
    ### 🔧 Technology Stack
    
    - **Backend:** Python, FastAPI
    - **UI:** Streamlit
    - **Converters:** PyPDF2, python-docx, pandas, reportlab
    
    ### 📄 Version
    
    **Version:** {VERSION}  
    **Last Updated:** 2025
    
    ---
    
    Made with ❤️ by the Universal Document Converter Team
    """)

# Footer
st.divider()
st.markdown(f"""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>Universal Document Converter v{VERSION}</p>
    <p>Convert • Transform • Simplify</p>
    <p style='font-size: 0.8rem; margin-top: 1rem;'>
        Session Stats: {st.session_state.total_conversions} conversions • 
        {st.session_state.total_files_converted} files processed
    </p>
</div>
""", unsafe_allow_html=True)
