"""
Streamlit Web UI for Document Converter
Interactive web interface for file conversion
"""

import streamlit as st
import sys
from pathlib import Path
import time
import io

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from converters import ConverterFactory, get_supported_formats, get_supported_conversions
from utils.validators import validate_file
from utils.helpers import format_file_size, get_file_size
from utils.errors import ConversionError
from Workflows import batch_convert_directory
import tempfile
import shutil

# Page configuration
st.set_page_config(
    page_title="Universal Document Converter",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize factory
@st.cache_resource
def get_factory():
    return ConverterFactory()

factory = get_factory()

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
    
    # Quality settings
    quality = st.select_slider(
        "Quality",
        options=["low", "medium", "high"],
        value="high",
        help="Higher quality = better output but slower conversion"
    )
    
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
    st.metric("Total Conversions", total_conversions)

# Main content
if mode == "Single File":
    st.header("📤 Single File Conversion")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Upload File")
        uploaded_file = st.file_uploader(
            "Choose a file to convert",
            type=['pdf', 'docx', 'xlsx', 'csv', 'json', 'txt'],
            help="Upload a file in any supported format"
        )
        
        if uploaded_file:
            st.success(f"✓ File uploaded: {uploaded_file.name}")
            file_size = len(uploaded_file.getvalue())
            st.info(f"📦 Size: {format_file_size(file_size)}")
    
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
                
                # Cleanup
                tmp_input_path.unlink(missing_ok=True)
                tmp_output_path.unlink(missing_ok=True)
                
            except Exception as e:
                st.error(f"❌ Conversion failed: {str(e)}")
                progress_bar.empty()
                status_text.empty()

elif mode == "Batch Conversion":
    st.header("📦 Batch Conversion")
    
    st.info("💡 Upload multiple files to convert them all at once")
    
    # File uploader for multiple files
    uploaded_files = st.file_uploader(
        "Choose files to convert",
        type=['pdf', 'docx', 'xlsx', 'csv', 'json', 'txt'],
        accept_multiple_files=True,
        help="Upload multiple files for batch conversion"
    )
    
    if uploaded_files:
        st.success(f"✓ {len(uploaded_files)} files uploaded")
        
        # Show file list
        with st.expander("📋 View uploaded files"):
            for file in uploaded_files:
                file_size = len(file.getvalue())
                st.text(f"• {file.name} ({format_file_size(file_size)})")
        
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
                
                for idx, file in enumerate(uploaded_files):
                    try:
                        status_text.text(f"🔄 Converting {file.name}...")
                        
                        input_path = input_dir / file.name
                        input_format = Path(file.name).suffix.lower().replace('.', '')
                        
                        # Check if conversion is supported
                        if factory.supports_conversion(input_format, output_format):
                            output_path = output_dir / f"{Path(file.name).stem}.{output_format}"
                            
                            factory.convert(input_path, output_path, quality=quality)
                            
                            # Read converted file
                            with open(output_path, 'rb') as f:
                                converted_data = f.read()
                            
                            results['successful'].append({
                                'name': file.name,
                                'output_name': output_path.name,
                                'data': converted_data
                            })
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
                    
                    # Update progress
                    progress = int((idx + 1) / len(uploaded_files) * 100)
                    progress_bar.progress(progress)
                
                status_text.text("✅ Batch conversion complete!")
                
                # Display results
                st.divider()
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Files", len(uploaded_files))
                with col2:
                    st.metric("Successful", len(results['successful']), delta_color="normal")
                with col3:
                    st.metric("Failed", len(results['failed']), delta_color="inverse")
                
                # Show successful conversions
                if results['successful']:
                    st.success(f"✅ {len(results['successful'])} files converted successfully!")
                    
                    st.subheader("⬇️ Download Converted Files")
                    
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

else:  # About
    st.header("ℹ️ About Universal Document Converter")
    
    st.markdown("""
    ### 🎯 Features
    
    - **30+ Conversion Pairs** - Convert between 6 different formats
    - **High Quality** - Preserve formatting and content
    - **Batch Processing** - Convert multiple files at once
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
       - Upload a file
       - Select output format
       - Click "Convert File"
       - Download the result
    
    2. **Batch Mode:**
       - Upload multiple files
       - Select output format for all
       - Click "Convert All"
       - Download each converted file
    
    ### ⚙️ Quality Settings
    
    - **Low:** Fast conversion, smaller files
    - **Medium:** Balanced speed and quality
    - **High:** Best quality, larger files (recommended)
    
    ### 📚 Documentation
    
    - [README.md](https://github.com/yourusername/converter) - Project overview
    - [API Documentation](http://localhost:8000/docs) - REST API reference
    - [Quick Start Guide](https://github.com/yourusername/converter/QUICKSTART.md)
    
    ### 🔧 Technology Stack
    
    - **Backend:** Python, FastAPI
    - **UI:** Streamlit
    - **Converters:** PyPDF2, python-docx, pandas, reportlab
    
    ### 📄 Version
    
    **Version:** 1.0.0  
    **Last Updated:** 2024
    
    ---
    
    Made with ❤️ by the Universal Document Converter Team
    """)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>Universal Document Converter v1.0.0</p>
    <p>Convert • Transform • Simplify</p>
</div>
""", unsafe_allow_html=True)
