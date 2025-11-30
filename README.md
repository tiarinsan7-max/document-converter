# 📄 Universal Document Converter

A powerful, production-ready document conversion application supporting multiple file formats with CLI, API, and Web interfaces.

## 🚀 Features

### Supported Formats
- **PDF** - Portable Document Format
- **DOCX** - Microsoft Word Documents
- **XLSX** - Microsoft Excel Spreadsheets
- **CSV** - Comma-Separated Values
- **JSON** - JavaScript Object Notation
- **TXT** - Plain Text Files

### Conversion Matrix
All formats can be converted to and from each other:
- PDF ↔ DOCX, XLSX, CSV, JSON, TXT
- DOCX ↔ PDF, XLSX, CSV, JSON, TXT
- XLSX ↔ PDF, DOCX, CSV, JSON, TXT
- CSV ↔ PDF, DOCX, XLSX, JSON, TXT
- JSON ↔ PDF, DOCX, XLSX, CSV, TXT
- TXT ↔ PDF, DOCX, XLSX, CSV, JSON

### Interfaces
1. **CLI** - Command-line interface for automation
2. **REST API** - FastAPI-based API for integration
3. **Streamlit UI** - Interactive web interface
4. **React UI** - Modern web application

### Advanced Features
- ✅ Batch processing
- ✅ Progress tracking
- ✅ Error handling & logging
- ✅ File validation
- ✅ Encoding detection
- ✅ Format preservation
- ✅ OCR support (for scanned PDFs)
- ✅ Async processing
- ✅ Configurable conversion rules

## 📦 Installation

### Prerequisites
- Python 3.9 or higher
- Node.js 16+ (for React UI)
- Tesseract OCR (optional, for OCR features)

### Quick Start

#### Option 1: Automated Setup (Recommended)

**Linux/Mac:**
```bash
./setup.sh
```

**Windows:**
```bash
setup.bat
```

#### Option 2: Manual Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd Cline
```

2. **Create virtual environment**
```bash
python3 -m venv venv

# Activate on Linux/Mac:
source venv/bin/activate

# Activate on Windows:
venv\Scripts\activate
```

3. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

4. **Install Tesseract (Optional - for OCR)**
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# macOS
brew install tesseract

# Windows
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
```

## 🎯 Usage

### CLI Interface

**Basic conversion:**
```bash
python main.py convert input.pdf output.docx
```

**Batch conversion:**
```bash
python main.py batch-convert --input-dir ./documents --output-dir ./converted --format pdf
```

**List supported formats:**
```bash
python main.py list-formats
```

### API Interface

**Start the API server:**
```bash
python -m api.main
# or
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

**API Endpoints:**
- `POST /convert` - Convert single file
- `POST /batch-convert` - Convert multiple files
- `GET /formats` - List supported formats
- `GET /health` - Health check

**Example API call:**
```bash
curl -X POST "http://localhost:8000/convert" \
  -F "file=@document.pdf" \
  -F "output_format=docx"
```

### Streamlit UI

**Start Streamlit app:**
```bash
streamlit run streamlit_app/app.py
```

Access at: `http://localhost:8501`

### React UI

**Setup and start:**
```bash
cd web
npm install
npm start
```

Access at: `http://localhost:3000`

## 📁 Project Structure

```
Cline/
├── converters/          # Conversion modules
│   ├── base_converter.py
│   ├── pdf_converter.py
│   ├── excel_converter.py
│   ├── word_converter.py
│   ├── json_converter.py
│   └── text_converter.py
├── api/                 # FastAPI backend
│   ├── main.py
│   ├── routes.py
│   └── models.py
├── cli/                 # CLI interface
│   └── main.py
├── utils/               # Utilities
│   ├── validators.py
│   ├── logger.py
│   ├── helpers.py
│   └── file_handler.py
├── web/                 # React frontend
│   ├── src/
│   └── package.json
├── streamlit_app/       # Streamlit UI
│   └── app.py
├── Rules/               # Conversion rules
│   └── conversion_rules.json
├── Workflows/           # Automation workflows
│   └── batch_processor.py
├── tests/               # Unit tests
├── config/              # Configuration
├── uploads/             # Temporary uploads
├── outputs/             # Converted files
├── logs/                # Application logs
├── requirements.txt     # Python dependencies
├── main.py             # Main entry point
└── README.md           # This file
```

## ⚙️ Configuration

Configuration files are stored in the `config/` directory and `Rules/` folder.

**config/settings.py** - Application settings
**Rules/conversion_rules.json** - Custom conversion rules

## 🧪 Testing

Run tests:
```bash
pytest tests/ -v
```

Run with coverage:
```bash
pytest tests/ --cov=. --cov-report=html
```

## 📊 Logging

Logs are stored in the `logs/` directory:
- `app.log` - Application logs
- `error.log` - Error logs
- `conversion.log` - Conversion activity logs

## 🔧 Development

### Code Quality

**Format code:**
```bash
black .
```

**Lint code:**
```bash
flake8 .
```

**Type checking:**
```bash
mypy .
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📝 License

MIT License - See LICENSE file for details

## 🆘 Support

For issues and questions:
- Create an issue on GitHub
- Check the documentation
- Review existing issues

## 🎉 Acknowledgments

Built with:
- FastAPI
- Streamlit
- React
- Python-docx
- Pandas
- PyPDF2
- And many other amazing open-source libraries

---

**Version:** 1.0.0  
**Last Updated:** 2024
