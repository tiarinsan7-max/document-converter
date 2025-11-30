# Installation Guide

Complete installation instructions for Universal Document Converter.

---

## 🔧 System Requirements

### Minimum Requirements
- **Python:** 3.9 or higher
- **RAM:** 2 GB
- **Disk Space:** 500 MB
- **OS:** Linux, macOS, or Windows

### Optional Requirements
- **Node.js:** 16+ (for React UI)
- **Tesseract OCR:** For OCR features

---

## 📦 Installation Methods

### Method 1: Automated Setup (Recommended)

#### Linux/Mac

```bash
# Make setup script executable (if not already)
chmod +x setup.sh

# Run setup
./setup.sh
```

#### Windows

```bash
# Run setup script
setup.bat
```

The automated setup will:
1. ✅ Check Python installation
2. ✅ Create virtual environment
3. ✅ Upgrade pip
4. ✅ Install all dependencies
5. ✅ Display next steps

---

### Method 2: Manual Setup

#### Step 1: Create Virtual Environment

**Why virtual environment?**
- Isolates project dependencies
- Prevents conflicts with system packages
- Required on Debian/Ubuntu systems

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Verify activation:**
```bash
which python  # Linux/Mac
where python  # Windows
# Should show path inside venv directory
```

#### Step 2: Upgrade pip

```bash
pip install --upgrade pip
```

#### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- FastAPI & Uvicorn (API server)
- Streamlit (Web UI)
- Document processing libraries
- Utility libraries

**Installation time:** ~2-5 minutes depending on internet speed

---

## 🔍 Troubleshooting Installation

### Issue: "externally-managed-environment" Error

**Problem:**
```
error: externally-managed-environment
```

**Solution:**
You MUST use a virtual environment on Debian/Ubuntu systems:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Why this happens:**
- Modern Debian/Ubuntu protect system Python
- Prevents breaking system packages
- Virtual environments are the correct solution

---

### Issue: "python3: command not found"

**Solution:**

**Debian/Ubuntu:**
```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip
```

**macOS:**
```bash
brew install python3
```

**Windows:**
Download from: https://www.python.org/downloads/

---

### Issue: "No module named 'venv'"

**Solution:**

**Debian/Ubuntu:**
```bash
sudo apt install python3-venv
```

**Then retry:**
```bash
python3 -m venv venv
```

---

### Issue: pip install fails with permission error

**Solution:**
Make sure virtual environment is activated:
```bash
# Check if activated (should show venv path)
which python

# If not activated:
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

---

### Issue: "Failed building wheel for [package]"

**Solution:**

**Install build dependencies:**

**Debian/Ubuntu:**
```bash
sudo apt install python3-dev build-essential
```

**macOS:**
```bash
xcode-select --install
```

**Windows:**
Install Visual C++ Build Tools from Microsoft

---

## 🎯 Verify Installation

### Test 1: Check Python Version

```bash
python --version
# Should show Python 3.9 or higher
```

### Test 2: Check Installed Packages

```bash
pip list
# Should show fastapi, streamlit, pandas, etc.
```

### Test 3: Run Help Command

```bash
python main.py --help
# Should display available commands
```

### Test 4: List Formats

```bash
python main.py formats
# Should display supported formats table
```

---

## 🌐 Optional: Install Tesseract OCR

### Linux (Debian/Ubuntu)

```bash
sudo apt update
sudo apt install tesseract-ocr
```

### macOS

```bash
brew install tesseract
```

### Windows

1. Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run installer
3. Add to PATH or set in .env:
   ```
   TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
   ```

### Verify Tesseract

```bash
tesseract --version
```

---

## 🎨 Optional: Install React UI Dependencies

### Prerequisites

Install Node.js from: https://nodejs.org/

### Install React Dependencies

```bash
cd web
npm install
```

### Verify React Setup

```bash
npm start
# Should open browser at http://localhost:3000
```

---

## 📝 Post-Installation Setup

### 1. Create .env File

```bash
cp .env.example .env
```

### 2. Edit Configuration (Optional)

```bash
nano .env  # or use your preferred editor
```

### 3. Test Conversion

```bash
# Create a test file
echo "Hello World" > test.txt

# Convert it
python main.py convert test.txt test.pdf

# Check output
ls -lh test.pdf
```

---

## 🚀 Quick Start After Installation

### Activate Virtual Environment

**Every time you open a new terminal:**

```bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

**You'll see `(venv)` in your prompt when activated**

### Run Commands

```bash
# Convert a file
python main.py convert input.pdf output.docx

# Start API server
python main.py api

# Start Streamlit UI
python main.py streamlit

# View formats
python main.py formats
```

---

## 🔄 Updating Dependencies

### Update All Packages

```bash
pip install --upgrade -r requirements.txt
```

### Update Specific Package

```bash
pip install --upgrade fastapi
```

### Check Outdated Packages

```bash
pip list --outdated
```

---

## 🗑️ Uninstallation

### Remove Virtual Environment

```bash
# Deactivate first
deactivate

# Remove venv directory
rm -rf venv  # Linux/Mac
rmdir /s venv  # Windows
```

### Remove Project

```bash
cd ..
rm -rf Cline  # Linux/Mac
rmdir /s Cline  # Windows
```

---

## 📊 Installation Checklist

- [ ] Python 3.9+ installed
- [ ] Virtual environment created
- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] .env file created
- [ ] Test conversion successful
- [ ] (Optional) Tesseract installed
- [ ] (Optional) Node.js installed
- [ ] (Optional) React dependencies installed

---

## 🆘 Getting Help

If you encounter issues:

1. **Check this guide** - Most issues are covered above
2. **Check logs** - Look in `logs/` directory
3. **Verify Python version** - Must be 3.9+
4. **Ensure venv is activated** - Look for `(venv)` in prompt
5. **Try clean install** - Remove venv and reinstall

---

## 💡 Tips

### Tip 1: Always Activate Virtual Environment

Add to your shell profile for convenience:

**~/.bashrc or ~/.zshrc:**
```bash
alias activate-converter='cd ~/Documents/Cline && source venv/bin/activate'
```

### Tip 2: Use Setup Script

The setup script handles everything automatically:
```bash
./setup.sh  # Linux/Mac
setup.bat   # Windows
```

### Tip 3: Keep Dependencies Updated

Periodically update:
```bash
pip install --upgrade -r requirements.txt
```

---

**Installation complete! Ready to convert documents!** 🎉

For usage instructions, see:
- **QUICKSTART.md** - Quick start guide
- **README.md** - Project overview
- **API_CLI.md** - API and CLI reference
