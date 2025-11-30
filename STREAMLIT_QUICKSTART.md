# 🚀 Streamlit Quick Start Guide

## ✅ Status: READY TO RUN!

Streamlit is fully installed and working. Follow these simple steps to launch your app.

---

## 🎯 Quick Start (3 Steps)

### Step 1: Navigate to Project
```bash
cd /root/Cline
```

### Step 2: Activate Virtual Environment
```bash
source venv/bin/activate
```

### Step 3: Run Streamlit
```bash
streamlit run streamlit_app/app.py
```

**That's it!** Your browser should automatically open to the app.

---

## 🌐 Accessing the App

After running the command, you'll see output like:

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

Open the **Local URL** in your browser.

---

## 🛑 Stopping the App

Press `Ctrl + C` in the terminal to stop the Streamlit server.

---

## 🔧 Common Commands

### Run on Different Port
```bash
streamlit run streamlit_app/app.py --server.port 8080
```

### Run Without Auto-Opening Browser
```bash
streamlit run streamlit_app/app.py --server.headless true
```

### Check Streamlit Version
```bash
streamlit --version
```

### View Installed Packages
```bash
pip list
```

---

## 📱 What You'll See

Your app has **3 main sections**:

1. **Single File Conversion**
   - Upload a file
   - Choose output format
   - Convert & download

2. **Batch Conversion**
   - Upload multiple files
   - Convert all at once
   - Download each result

3. **About**
   - App information
   - Supported formats
   - Documentation

Plus a **Workflows** page (in sidebar) for automation!

---

## ⚡ Pro Tips

1. **Keep Terminal Open:** Don't close the terminal while using the app
2. **Auto-Reload:** Streamlit auto-reloads when you edit code
3. **Clear Cache:** Use the menu (☰) → "Clear cache" if needed
4. **Settings:** Access settings via menu (☰) → "Settings"

---

## 🐛 Troubleshooting

### Port Already in Use?
```bash
# Use a different port
streamlit run streamlit_app/app.py --server.port 8502
```

### Virtual Environment Not Activated?
```bash
# You'll see (venv) in your prompt when activated
source venv/bin/activate
```

### Module Not Found Error?
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

---

## 📚 Next Steps

Once the app is running, try:
- ✅ Converting a PDF to DOCX
- ✅ Batch converting multiple files
- ✅ Creating a workflow
- ✅ Exploring different quality settings

---

## 🎉 Enjoy Your App!

Everything is set up and ready to go. Have fun converting documents! 🚀
