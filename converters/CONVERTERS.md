# Converters Module Documentation

Complete documentation for all document converters.

## 📁 Module Overview

### Converter Classes

1. **BaseConverter** - Abstract base class
2. **PDFConverter** - PDF to other formats
3. **ToPDFConverter** - Other formats to PDF
4. **ExcelConverter** - CSV/XLSX conversions
5. **FromExcelConverter** - To CSV/XLSX conversions
6. **WordConverter** - DOCX to other formats
7. **ToWordConverter** - Other formats to DOCX
8. **JSONConverter** - JSON conversions
9. **ToJSONConverter** - To JSON conversions
10. **ConverterFactory** - Routing and management

---

## 🔄 Supported Conversions

### Complete Conversion Matrix

| From/To | PDF | DOCX | XLSX | CSV | JSON | TXT |
|---------|-----|------|------|-----|------|-----|
| **PDF** | - | ✅ | ✅ | ✅ | ✅ | ✅ |
| **DOCX** | ✅ | - | ✅ | ✅ | ✅ | ✅ |
| **XLSX** | ✅ | ✅ | - | ✅ | ✅ | ✅ |
| **CSV** | ✅ | ✅ | ✅ | - | ✅ | ✅ |
| **JSON** | ✅ | ✅ | ✅ | ✅ | - | ✅ |
| **TXT** | ✅ | ✅ | ✅ | ✅ | ✅ | - |

**Total Conversions:** 30 conversion pairs

---

## 📚 Converter Details

### 1. BaseConverter

Abstract base class for all converters.

**Key Methods:**
- `convert(input_file, output_file, **kwargs)` - Abstract conversion method
- `convert_with_validation(...)` - Conversion with validation
- `supports_conversion(input_fmt, output_fmt)` - Check support
- `get_supported_conversions()` - Get supported conversions

**Features:**
- Automatic validation
- Error handling
- Logging
- Quality settings integration
- Output directory creation

---

### 2. PDFConverter

Convert PDF to other formats.

**Supported Conversions:**
- PDF → TXT (text extraction)
- PDF → DOCX (with tables)
- PDF → CSV (table extraction)
- PDF → XLSX (multi-sheet tables)
- PDF → JSON (structured data)

**Features:**
- Text extraction with pdfplumber
- Table detection and extraction
- Page-by-page processing
- Metadata extraction
- Multi-page support

**Example:**
```python
from converters import PDFConverter

converter = PDFConverter()
output = converter.convert_with_validation(
    'document.pdf',
    'output.docx',
    quality='high'
)
```

---

### 3. ToPDFConverter

Convert other formats to PDF.

**Supported Conversions:**
- TXT → PDF
- CSV → PDF (as table)
- XLSX → PDF (multi-sheet)
- JSON → PDF (formatted)
- DOCX → PDF

**Features:**
- ReportLab for PDF generation
- Table formatting
- Multi-sheet support
- Styled output
- Page breaks

**Example:**
```python
from converters.pdf_converter import ToPDFConverter

converter = ToPDFConverter()
output = converter.convert('data.csv', 'output.pdf')
```

---

### 4. ExcelConverter

Convert between CSV, XLSX, and other formats.

**Supported Conversions:**
- CSV ↔ XLSX
- CSV/XLSX → JSON
- CSV/XLSX → TXT
- CSV/XLSX → DOCX

**Features:**
- Pandas-based processing
- Auto-column width adjustment
- Multi-sheet support (XLSX)
- Table formatting in DOCX
- Encoding detection

**Example:**
```python
from converters import ExcelConverter

converter = ExcelConverter()
output = converter.convert('data.csv', 'output.xlsx')
```

---

### 5. FromExcelConverter

Convert to CSV/XLSX from other formats.

**Supported Conversions:**
- JSON → CSV/XLSX
- TXT → CSV/XLSX
- DOCX → CSV/XLSX (tables)

**Features:**
- JSON structure detection
- Multi-sheet creation
- Table extraction from DOCX
- Delimiter detection

---

### 6. WordConverter

Convert DOCX to other formats.

**Supported Conversions:**
- DOCX → TXT
- DOCX → JSON

**Features:**
- Paragraph extraction
- Table extraction
- Style preservation
- Structured JSON output

**Example:**
```python
from converters import WordConverter

converter = WordConverter()
output = converter.convert('document.docx', 'output.txt')
```

---

### 7. ToWordConverter

Convert to DOCX from other formats.

**Supported Conversions:**
- TXT → DOCX
- JSON → DOCX

**Features:**
- Heading detection
- Paragraph formatting
- Table creation from JSON
- Style application

---

### 8. JSONConverter & ToJSONConverter

Handle JSON conversions.

**Supported Conversions:**
- JSON → TXT
- TXT → JSON

**Features:**
- Pretty printing
- Structure preservation
- Automatic parsing
- Fallback formatting

---

### 9. ConverterFactory

Central routing and management.

**Key Methods:**
- `get_converter(input_fmt, output_fmt)` - Get converter
- `convert(input_file, output_file)` - Convert file
- `supports_conversion(input_fmt, output_fmt)` - Check support
- `get_supported_formats()` - List all formats
- `get_supported_conversions(input_fmt)` - List conversions
- `get_all_conversions()` - Get conversion map

**Example:**
```python
from converters import ConverterFactory

factory = ConverterFactory()

# Check support
if factory.supports_conversion('pdf', 'docx'):
    # Convert
    output = factory.convert('input.pdf', 'output.docx', quality='high')

# Get supported formats
formats = factory.get_supported_formats()
print(formats)  # ['csv', 'docx', 'json', 'pdf', 'txt', 'xlsx']

# Get conversions for PDF
conversions = factory.get_supported_conversions('pdf')
print(conversions)  # ['csv', 'docx', 'json', 'txt', 'xlsx']
```

---

## 🎯 Usage Examples

### Basic Conversion

```python
from converters import convert_file

# Simple conversion
output = convert_file('input.pdf', 'output.docx')
print(f"Converted to: {output}")
```

### With Quality Settings

```python
from converters import convert_file

output = convert_file(
    'input.pdf',
    'output.docx',
    quality='high'  # 'low', 'medium', 'high'
)
```

### Check Supported Formats

```python
from converters import get_supported_formats, get_supported_conversions

# All formats
formats = get_supported_formats()
print(f"Supported formats: {formats}")

# Conversions for specific format
conversions = get_supported_conversions('pdf')
print(f"PDF can convert to: {conversions}")
```

### Using Specific Converter

```python
from converters import PDFConverter

converter = PDFConverter()

# Convert with validation
output = converter.convert_with_validation(
    input_file='document.pdf',
    output_file='output.txt',
    quality='high'
)
```

### Batch Conversion

```python
from converters import ConverterFactory
from pathlib import Path

factory = ConverterFactory()
input_dir = Path('documents')
output_dir = Path('converted')

for pdf_file in input_dir.glob('*.pdf'):
    output_file = output_dir / f"{pdf_file.stem}.docx"
    try:
        factory.convert(pdf_file, output_file)
        print(f"✓ Converted: {pdf_file.name}")
    except Exception as e:
        print(f"✗ Failed: {pdf_file.name} - {e}")
```

---

## ⚙️ Quality Settings

Quality settings are loaded from `Rules/conversion_rules.json`:

### PDF Quality
- **Low:** 72 DPI, high compression
- **Medium:** 150 DPI, medium compression
- **High:** 300 DPI, low compression

### DOCX Settings
- Preserve formatting
- Preserve styles
- Preserve tables
- Preserve images

### XLSX Settings
- Preserve formulas
- Preserve formatting
- Max rows/columns

---

## 🔧 Advanced Features

### Custom Conversion Options

```python
from converters import PDFConverter

converter = PDFConverter()

# PDF to DOCX with options
output = converter.convert(
    'input.pdf',
    'output.docx',
    preserve_images=True,
    preserve_tables=True,
    ocr_enabled=True
)
```

### Error Handling

```python
from converters import convert_file
from utils.errors import ConversionError, UnsupportedFormatError

try:
    output = convert_file('input.pdf', 'output.docx')
except UnsupportedFormatError as e:
    print(f"Format not supported: {e}")
except ConversionError as e:
    print(f"Conversion failed: {e}")
    print(f"Error details: {e.to_dict()}")
```

---

## 📊 Performance Tips

1. **Use appropriate quality settings** - Lower quality = faster conversion
2. **Batch processing** - Use ConverterFactory for multiple files
3. **Large files** - Consider chunking or streaming
4. **Memory** - Close files properly, use context managers
5. **Logging** - Monitor conversion progress

---

## 🐛 Troubleshooting

### Common Issues

**Issue:** PDF to DOCX loses formatting
- **Solution:** Use high quality setting, check source PDF

**Issue:** CSV to XLSX encoding errors
- **Solution:** Specify encoding in conversion rules

**Issue:** Large file conversion fails
- **Solution:** Increase timeout in batch settings

**Issue:** Table extraction from PDF incomplete
- **Solution:** PDF may be image-based, enable OCR

---

## 🔄 Extending Converters

### Adding New Format

1. Create new converter class extending `BaseConverter`
2. Implement `convert()` method
3. Set `supported_input_formats` and `supported_output_formats`
4. Add to `ConverterFactory`

**Example:**
```python
from converters.base_converter import BaseConverter

class MarkdownConverter(BaseConverter):
    def __init__(self):
        super().__init__()
        self.supported_input_formats = ['md']
        self.supported_output_formats = ['html', 'pdf']
    
    def convert(self, input_file, output_file, **kwargs):
        # Implementation
        pass
```

---

**Version:** 1.0.0  
**Last Updated:** 2024
