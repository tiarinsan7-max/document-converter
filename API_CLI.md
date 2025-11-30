# API & CLI Documentation

Complete guide for using the REST API and Command-Line Interface.

---

## 📡 REST API

### Starting the API Server

```bash
# Using main.py
python main.py api --port 8000 --reload

# Using uvicorn directly
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

# Production mode
uvicorn api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### API Documentation

Once running, access interactive documentation at:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json

---

## 🔌 API Endpoints

### 1. Convert Single File

**Endpoint:** `POST /api/v1/convert`

**Description:** Convert a single file to target format

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/convert" \
  -F "file=@document.pdf" \
  -F "output_format=docx" \
  -F "quality=high"
```

**Parameters:**
- `file` (required): File to convert
- `output_format` (required): Target format (pdf, docx, xlsx, csv, json, txt)
- `quality` (optional): Conversion quality (low, medium, high) - default: high

**Response:**
```json
{
  "success": true,
  "message": "Conversion completed successfully",
  "input_file": "document.pdf",
  "output_file": "document.docx",
  "output_format": "docx",
  "file_size": 45678,
  "download_url": "/download/document.docx",
  "conversion_time": 2.34
}
```

---

### 2. Batch Convert Files

**Endpoint:** `POST /api/v1/batch-convert`

**Description:** Convert multiple files at once

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/batch-convert" \
  -F "files=@file1.pdf" \
  -F "files=@file2.docx" \
  -F "files=@file3.csv" \
  -F "output_format=pdf" \
  -F "quality=high"
```

**Response:**
```json
{
  "success": true,
  "message": "Batch conversion completed: 2 successful, 1 failed",
  "total_files": 3,
  "successful": 2,
  "failed": 1,
  "results": [
    {
      "filename": "file1.pdf",
      "status": "success",
      "output_file": "file1.docx",
      "download_url": "/download/file1.docx"
    }
  ],
  "total_time": 5.67
}
```

---

### 3. Download Converted File

**Endpoint:** `GET /api/v1/download/{filename}`

**Description:** Download converted file

**Request:**
```bash
curl -O "http://localhost:8000/api/v1/download/document.docx"
```

**Note:** Files are automatically deleted after download.

---

### 4. Get Supported Formats

**Endpoint:** `GET /api/v1/formats`

**Description:** List all supported formats and conversions

**Request:**
```bash
curl "http://localhost:8000/api/v1/formats"
```

**Response:**
```json
{
  "formats": ["csv", "docx", "json", "pdf", "txt", "xlsx"],
  "total": 6,
  "conversions": {
    "pdf": ["csv", "docx", "json", "txt", "xlsx"],
    "docx": ["csv", "json", "pdf", "txt", "xlsx"],
    ...
  }
}
```

---

### 5. Get Format Conversions

**Endpoint:** `GET /api/v1/formats/{format_name}`

**Description:** Get supported conversions for specific format

**Request:**
```bash
curl "http://localhost:8000/api/v1/formats/pdf"
```

**Response:**
```json
{
  "format": "pdf",
  "supported_conversions": ["csv", "docx", "json", "txt", "xlsx"],
  "total": 5
}
```

---

### 6. Health Check

**Endpoint:** `GET /api/v1/health`

**Description:** Check API health and status

**Request:**
```bash
curl "http://localhost:8000/api/v1/health"
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "uptime": 3600.5,
  "supported_formats": 6
}
```

---

### 7. Cleanup Files

**Endpoint:** `DELETE /api/v1/cleanup`

**Description:** Clean up old temporary files

**Request:**
```bash
curl -X DELETE "http://localhost:8000/api/v1/cleanup"
```

---

## 🖥️ Command-Line Interface (CLI)

### Basic Commands

#### 1. Convert Single File

```bash
python main.py convert <input_file> <output_file> [--quality <level>]
```

**Examples:**
```bash
# Convert PDF to DOCX
python main.py convert document.pdf output.docx

# Convert with quality setting
python main.py convert document.pdf output.docx --quality high

# Convert CSV to XLSX
python main.py convert data.csv data.xlsx
```

---

#### 2. Batch Convert

```bash
python main.py batch --input-dir <directory> --output-format <format> [options]
```

**Options:**
- `--input-dir`: Input directory path (required)
- `--output-dir`: Output directory path (default: ./outputs)
- `--output-format`: Target format (required)
- `--quality`: Conversion quality (default: high)
- `--recursive`: Process subdirectories

**Examples:**
```bash
# Convert all files in directory to PDF
python main.py batch --input-dir ./documents --output-format pdf

# Recursive conversion
python main.py batch \
  --input-dir ./docs \
  --output-dir ./converted \
  --output-format docx \
  --recursive

# With quality setting
python main.py batch \
  --input-dir ./files \
  --output-format pdf \
  --quality medium
```

---

#### 3. List Supported Formats

```bash
python main.py formats
```

**Output:**
- Table of supported formats
- Conversion matrix
- Statistics

---

#### 4. Start API Server

```bash
python main.py api [--host <host>] [--port <port>] [--reload]
```

**Examples:**
```bash
# Start on default port
python main.py api

# Custom port with auto-reload
python main.py api --port 8080 --reload

# Production mode
python main.py api --host 0.0.0.0 --port 8000
```

---

#### 5. Start Streamlit UI

```bash
python main.py streamlit [--port <port>]
```

**Example:**
```bash
python main.py streamlit --port 8501
```

---

#### 6. Show Version

```bash
python main.py version
```

---

## 🔄 Batch Processing & Workflows

### Using Batch Processor

```python
from Workflows import BatchProcessor, find_files
from pathlib import Path

# Initialize processor
processor = BatchProcessor(max_workers=4)

# Find files
files = find_files(
    Path('./documents'),
    extensions=['pdf', 'docx'],
    recursive=True
)

# Process batch
results = processor.process_batch(
    input_files=files,
    output_dir=Path('./converted'),
    output_format='pdf',
    quality='high'
)

print(f"Successful: {results['successful']}")
print(f"Failed: {results['failed']}")
```

---

### Using Workflow Scheduler

```python
from Workflows import WorkflowScheduler

scheduler = WorkflowScheduler()

# Create workflow
workflow = scheduler.create_workflow(
    name='daily_pdf_conversion',
    input_dir='./incoming',
    output_dir='./processed',
    output_format='pdf',
    quality='high',
    recursive=True
)

# Run workflow
results = scheduler.run_workflow('daily_pdf_conversion')

# List all workflows
workflows = scheduler.list_workflows()

# Run all enabled workflows
all_results = scheduler.run_all_workflows()
```

---

## 🐍 Python API Usage

### Direct Conversion

```python
from converters import convert_file

# Simple conversion
output = convert_file('input.pdf', 'output.docx')
print(f"Converted to: {output}")

# With quality
output = convert_file(
    'input.pdf',
    'output.docx',
    quality='high'
)
```

---

### Using Factory

```python
from converters import ConverterFactory

factory = ConverterFactory()

# Check support
if factory.supports_conversion('pdf', 'docx'):
    output = factory.convert('input.pdf', 'output.docx')

# Get supported formats
formats = factory.get_supported_formats()
conversions = factory.get_supported_conversions('pdf')
```

---

### Async Batch Processing

```python
import asyncio
from Workflows import BatchProcessor
from pathlib import Path

async def convert_async():
    processor = BatchProcessor()
    
    files = [
        Path('file1.pdf'),
        Path('file2.docx'),
        Path('file3.csv')
    ]
    
    results = await processor.process_batch_async(
        input_files=files,
        output_dir=Path('./outputs'),
        output_format='pdf',
        quality='high'
    )
    
    return results

# Run
results = asyncio.run(convert_async())
```

---

## ⚙️ Configuration

### Environment Variables

Create `.env` file:

```env
# API Settings
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=False

# File Settings
MAX_UPLOAD_SIZE=104857600  # 100MB

# Conversion Settings
DEFAULT_QUALITY=high
ENABLE_OCR=True

# Logging
LOG_LEVEL=INFO

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8501
```

---

### Conversion Rules

Edit `Rules/conversion_rules.json`:

```json
{
  "conversion_rules": {
    "pdf": {
      "quality_settings": {
        "high": {
          "dpi": 300,
          "compression": "low"
        }
      }
    }
  },
  "batch_processing": {
    "max_concurrent": 4,
    "timeout_seconds": 300,
    "retry_attempts": 3
  }
}
```

---

## 🔒 Security

### File Validation

All uploads are validated:
- File size limits
- Extension checking
- MIME type validation
- Content validation

### CORS Configuration

Configure allowed origins in `.env`:
```env
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
```

---

## 📊 Monitoring & Logging

### Log Files

- `logs/app.log` - General application logs
- `logs/error.log` - Error logs
- `logs/conversion.log` - Conversion activity

### Log Levels

Set in `.env`:
```env
LOG_LEVEL=DEBUG  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

---

## 🐛 Error Handling

### API Errors

```json
{
  "success": false,
  "error": "ConversionError",
  "message": "Failed to convert file",
  "details": {
    "input_file": "document.pdf",
    "output_format": "docx"
  }
}
```

### CLI Errors

Errors are displayed with rich formatting:
- ✓ Success (green)
- ✗ Error (red)
- ⚠ Warning (yellow)

---

## 🚀 Performance Tips

1. **Use batch processing** for multiple files
2. **Adjust max_workers** based on CPU cores
3. **Lower quality** for faster conversions
4. **Enable caching** for repeated conversions
5. **Use async** for I/O-bound operations

---

## 📝 Examples

### Complete Workflow Example

```python
from Workflows import WorkflowScheduler
from pathlib import Path

# Create scheduler
scheduler = WorkflowScheduler()

# Create workflow
scheduler.create_workflow(
    name='invoice_processing',
    input_dir='/data/invoices',
    output_dir='/data/processed',
    output_format='pdf',
    quality='high',
    recursive=False
)

# Run workflow
results = scheduler.run_workflow('invoice_processing')

print(f"Processed {results['total_files']} files")
print(f"Success: {results['successful']}")
print(f"Failed: {results['failed']}")
```

---

**Version:** 1.0.0  
**Last Updated:** 2024
