# 🚀 Quick Start Guide

Get started with Universal Document Converter in 5 minutes!

---

## 📦 Installation

### 1. Install Python Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Install Tesseract (Optional - for OCR)

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

**Windows:**
Download from: https://github.com/UB-Mannheim/tesseract/wiki

---

## ⚡ Quick Examples

### Convert a Single File (CLI)

```bash
python main.py convert document.pdf output.docx
```

### Batch Convert Directory

```bash
python main.py batch --input-dir ./documents --output-format pdf
```

### Start API Server

```bash
python main.py api --port 8000
```

Then visit: http://localhost:8000/docs

### Start Streamlit UI

```bash
python main.py streamlit
```

Then visit: http://localhost:8501

---

## 🎯 Common Use Cases

### 1. PDF to Word

```bash
python main.py convert report.pdf report.docx
```

### 2. Excel to PDF

```bash
python main.py convert data.xlsx data.pdf
```

### 3. CSV to Excel

```bash
python main.py convert data.csv data.xlsx
```

### 4. Batch Convert All PDFs to DOCX

```bash
python main.py batch \
  --input-dir ./pdfs \
  --output-dir ./word-docs \
  --output-format docx
```

---

## 🔌 API Usage

### Convert via API

```bash
curl -X POST "http://localhost:8000/api/v1/convert" \
  -F "file=@document.pdf" \
  -F "output_format=docx" \
  -F "quality=high"
```

### Download Result

```bash
curl -O "http://localhost:8000/api/v1/download/document.docx"
```

---

## 🐍 Python Code

### Simple Conversion

```python
from converters import convert_file

# Convert file
output = convert_file('input.pdf', 'output.docx')
print(f"Converted to: {output}")
```

### Batch Processing

```python
from Workflows import batch_convert_directory

# Batch convert
results = batch_convert_directory(
    input_dir='./documents',
    output_dir='./converted',
    output_format='pdf',
    quality='high'
)

print(f"Successful: {results['successful']}")
```

---

## 📋 Supported Conversions

| From | To |
|------|-----|
| PDF | DOCX, XLSX, CSV, JSON, TXT |
| DOCX | PDF, XLSX, CSV, JSON, TXT |
| XLSX | PDF, DOCX, CSV, JSON, TXT |
| CSV | PDF, DOCX, XLSX, JSON, TXT |
| JSON | PDF, DOCX, XLSX, CSV, TXT |
| TXT | PDF, DOCX, XLSX, CSV, JSON |

**Total:** 30 conversion pairs

---

## ⚙️ Configuration

### Create .env File

```bash
cp .env.example .env
```

### Edit Settings

```env
# API Settings
API_PORT=8000

# Conversion Quality
DEFAULT_QUALITY=high

# File Size Limit (100MB)
MAX_UPLOAD_SIZE=104857600
```

---

## 🎨 Quality Settings

- **low** - Fast, smaller files, lower quality
- **medium** - Balanced speed and quality
- **high** - Best quality, larger files (default)

**Example:**
```bash
python main.py convert input.pdf output.docx --quality high
```

---

## 📊 View Supported Formats

```bash
python main.py formats
```

Output:
```
┌──────────┬────────────┬─────────────────────────────┐
│ Format   │ Extension  │ Description                 │
├──────────┼────────────┼─────────────────────────────┤
│ PDF      │ .pdf       │ Portable Document Format    │
│ DOCX     │ .docx      │ Microsoft Word Document     │
│ XLSX     │ .xlsx      │ Microsoft Excel Spreadsheet │
│ CSV      │ .csv       │ Comma-Separated Values      │
│ JSON     │ .json      │ JavaScript Object Notation  │
│ TXT      │ .txt       │ Plain Text File             │
└──────────┴────────────┴─────────────────────────────┘
```

---

## 🔍 Troubleshooting

### Issue: "Module not found"
**Solution:** Make sure you activated the virtual environment and installed dependencies:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Issue: "File too large"
**Solution:** Increase MAX_UPLOAD_SIZE in .env:
```env
MAX_UPLOAD_SIZE=209715200  # 200MB
```

### Issue: "Conversion failed"
**Solution:** Check logs in `logs/error.log` for details

### Issue: "Port already in use"
**Solution:** Use a different port:
```bash
python main.py api --port 8080
```

---

## 📚 Next Steps

1. **Read Full Documentation:**
   - [README.md](README.md) - Project overview
   - [API_CLI.md](API_CLI.md) - Complete API & CLI guide
   - [converters/CONVERTERS.md](converters/CONVERTERS.md) - Converter details
   - [utils/UTILITIES.md](utils/UTILITIES.md) - Utilities guide

2. **Explore Examples:**
   - Check `tests/` directory for examples
   - Try different conversion combinations
   - Experiment with quality settings

3. **Customize:**
   - Edit `Rules/conversion_rules.json` for custom settings
   - Create workflows in `Workflows/`
   - Modify API endpoints in `api/routes.py`

4. **Deploy:**
   - Use Docker for containerization
   - Deploy API to cloud (AWS, GCP, Azure)
   - Set up automated workflows

---

## 🆘 Getting Help

- **Check Logs:** `logs/app.log`, `logs/error.log`
- **API Docs:** http://localhost:8000/docs
- **GitHub Issues:** Create an issue for bugs
- **Documentation:** Read the full docs

---

## ✅ Checklist

- [ ] Python 3.9+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Tesseract installed (optional)
- [ ] .env file configured
- [ ] First conversion successful
- [ ] API server running
- [ ] Streamlit UI accessible

---

**🎉 You're ready to start converting documents!**

**Quick Command Reference:**
```bash
# Convert file
python main.py convert input.pdf output.docx

# Batch convert
python main.py batch --input-dir ./docs --output-format pdf

# Start API
python main.py api

# Start UI
python main.py streamlit

# List formats
python main.py formats
```

---

**Version:** 1.0.0  
**Last Updated:** 2024
