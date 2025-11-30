# Utilities Module Documentation

This document describes the utility modules available in the converter application.

## 📁 Module Overview

### 1. **logger.py** - Logging System
Advanced logging with file rotation and multiple log levels.

**Key Functions:**
- `setup_logger()` - Initialize logging system
- `get_logger(name)` - Get logger instance
- `log_conversion_start()` - Log conversion start
- `log_conversion_success()` - Log successful conversion
- `log_conversion_error()` - Log conversion error
- `log_batch_start()` - Log batch start
- `log_batch_complete()` - Log batch completion

**Log Files:**
- `logs/app.log` - General application logs
- `logs/error.log` - Error logs only
- `logs/conversion.log` - Conversion activity logs

**Example:**
```python
from utils.logger import get_logger

logger = get_logger(__name__)
logger.info("Processing file...")
logger.error("Conversion failed")
```

---

### 2. **validators.py** - File Validation
Validate files before conversion.

**Classes:**
- `FileValidator` - Main validation class
- `ValidationError` - Custom validation exception

**Key Functions:**
- `validate_file(file_path)` - Validate file
- `validate_conversion(input_fmt, output_fmt)` - Validate conversion
- `is_supported_format(format)` - Check format support
- `get_supported_conversions(format)` - Get available conversions

**Example:**
```python
from utils.validators import validate_file, validate_conversion

# Validate file
is_valid, error = validate_file("document.pdf")
if not is_valid:
    print(f"Validation failed: {error}")

# Validate conversion
is_valid, error = validate_conversion("pdf", "docx")
```

---

### 3. **helpers.py** - Helper Functions
Common utility functions.

**File Operations:**
- `get_file_extension(path)` - Get file extension
- `get_file_size(path)` - Get file size in bytes
- `format_file_size(bytes)` - Format size (e.g., "1.5 MB")
- `sanitize_filename(name)` - Clean filename
- `generate_unique_filename(name)` - Create unique filename
- `parse_file_path(path)` - Parse path components

**Directory Operations:**
- `ensure_directory(path)` - Create directory if needed
- `clean_directory(path, pattern)` - Clean files

**Data Operations:**
- `load_json_file(path)` - Load JSON
- `save_json_file(data, path)` - Save JSON
- `generate_file_hash(path)` - Generate file hash

**Formatting:**
- `format_duration(seconds)` - Format time duration
- `truncate_string(text, max_len)` - Truncate text

**Example:**
```python
from utils.helpers import (
    format_file_size,
    sanitize_filename,
    ensure_directory
)

# Format file size
size = format_file_size(1536000)  # "1.46 MB"

# Sanitize filename
safe_name = sanitize_filename("My Document (2024).pdf")

# Ensure directory exists
ensure_directory("./outputs")
```

---

### 4. **file_handler.py** - File Management
Handle file operations and uploads.

**Class:**
- `FileHandler` - Main file handler

**Key Methods:**
- `save_upload(file_data, filename)` - Save uploaded file
- `save_upload_async(file_data, filename)` - Async save
- `copy_file(source, dest)` - Copy file
- `move_file(source, dest)` - Move file
- `delete_file(path)` - Delete file
- `delete_files(paths)` - Delete multiple files
- `cleanup_temp_files(max_age_hours)` - Clean old files
- `get_output_path(input, format)` - Generate output path
- `read_file_chunks(path)` - Read file in chunks
- `get_file_info(path)` - Get file information

**Example:**
```python
from utils.file_handler import FileHandler

handler = FileHandler()

# Save upload
file_path = handler.save_upload(file_data, "document.pdf")

# Get output path
output_path = handler.get_output_path(
    input_file="input.pdf",
    output_format="docx"
)

# Cleanup old files
handler.cleanup_temp_files(max_age_hours=24)
```

---

### 5. **progress.py** - Progress Tracking
Track conversion progress.

**Classes:**
- `ProgressTracker` - Basic progress tracker
- `CLIProgressBar` - CLI progress bar (tqdm)
- `RichProgressBar` - Rich progress bar
- `BatchProgressTracker` - Batch conversion tracker

**Example:**
```python
from utils.progress import CLIProgressBar, BatchProgressTracker

# CLI progress bar
with CLIProgressBar(total=100, description="Converting") as pbar:
    for i in range(100):
        # Do work
        pbar.update(1)

# Batch tracker
tracker = BatchProgressTracker(total_files=10)
tracker.start_file("file1.pdf")
# ... conversion ...
tracker.complete_file(success=True)
tracker.print_summary()
```

---

### 6. **errors.py** - Error Handling
Custom exceptions for better error handling.

**Exception Classes:**
- `ConverterError` - Base exception
- `FileValidationError` - Validation failed
- `UnsupportedFormatError` - Format not supported
- `ConversionError` - Conversion failed
- `FileSizeError` - File too large
- `FileNotFoundError` - File not found
- `PermissionError` - Permission denied
- `ConfigurationError` - Config error
- `BatchConversionError` - Batch error
- `OCRError` - OCR processing error
- `EncodingError` - Encoding error
- `TimeoutError` - Operation timeout

**Functions:**
- `handle_conversion_error(error, input_file)` - Convert to ConverterError

**Example:**
```python
from utils.errors import (
    ConversionError,
    UnsupportedFormatError,
    handle_conversion_error
)

# Raise custom error
raise ConversionError(
    message="Failed to convert PDF",
    input_file="document.pdf",
    output_format="docx"
)

# Handle generic error
try:
    # conversion code
    pass
except Exception as e:
    error = handle_conversion_error(e, "input.pdf")
    print(error.to_dict())
```

---

## 🔧 Usage Patterns

### Complete Conversion Flow

```python
from utils.validators import validate_file, validate_conversion
from utils.file_handler import FileHandler
from utils.logger import get_logger
from utils.progress import CLIProgressBar
from utils.errors import ConversionError

logger = get_logger(__name__)
handler = FileHandler()

def convert_file(input_file, output_format):
    # Validate file
    is_valid, error = validate_file(input_file)
    if not is_valid:
        raise ConversionError(error)
    
    # Validate conversion
    input_format = get_file_extension(input_file)
    is_valid, error = validate_conversion(input_format, output_format)
    if not is_valid:
        raise ConversionError(error)
    
    # Get output path
    output_path = handler.get_output_path(input_file, output_format)
    
    # Convert with progress
    with CLIProgressBar(total=100, description="Converting") as pbar:
        # Conversion logic here
        pbar.update(100)
    
    logger.info(f"Converted: {input_file} -> {output_path}")
    return output_path
```

---

## 📊 Best Practices

1. **Always validate files** before conversion
2. **Use logging** for debugging and monitoring
3. **Handle errors gracefully** with custom exceptions
4. **Track progress** for better UX
5. **Clean up temporary files** regularly
6. **Use async methods** for better performance

---

## 🔍 Testing

All utilities include error handling and logging. Test with:

```python
# Test validation
from utils.validators import validate_file
is_valid, error = validate_file("test.pdf")
assert is_valid, error

# Test file operations
from utils.file_handler import FileHandler
handler = FileHandler()
info = handler.get_file_info("test.pdf")
print(info)
```

---

**Version:** 1.0.0  
**Last Updated:** 2024
