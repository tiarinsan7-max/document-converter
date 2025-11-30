# 📋 Workflow Form - Quick Reference Card

## ✅ Simple Fill-In Template

Copy and paste these values into your Streamlit Workflow form:

---

## 🎯 OPTION 1: Basic PDF Converter

```
┌─────────────────────────────────────────────┐
│ Workflow Name:      my_pdf_converter       │
│ Input Directory:    /root/Cline/uploads    │
│ Output Format:      pdf                    │
│ Output Directory:   /root/Cline/outputs    │
│ Quality:            high                   │
│ Subdirectories:     ☐ (unchecked)          │
└─────────────────────────────────────────────┘
```

**What it does:** Converts all files in `uploads/` to PDF format

---

## 🎯 OPTION 2: Word to PDF

```
┌─────────────────────────────────────────────┐
│ Workflow Name:      word_to_pdf            │
│ Input Directory:    /root/Cline/uploads    │
│ Output Format:      pdf                    │
│ Output Directory:   /root/Cline/outputs    │
│ Quality:            high                   │
│ Subdirectories:     ☐ (unchecked)          │
└─────────────────────────────────────────────┘
```

**What it does:** Converts Word documents to PDF

---

## 🎯 OPTION 3: Excel to CSV

```
┌─────────────────────────────────────────────┐
│ Workflow Name:      excel_to_csv           │
│ Input Directory:    /root/Cline/uploads    │
│ Output Format:      csv                    │
│ Output Directory:   /root/Cline/outputs    │
│ Quality:            medium                 │
│ Subdirectories:     ☐ (unchecked)          │
└─────────────────────────────────────────────┘
```

**What it does:** Converts Excel files to CSV format

---

## 🎯 OPTION 4: PDF to Word

```
┌─────────────────────────────────────────────┐
│ Workflow Name:      pdf_to_word            │
│ Input Directory:    /root/Cline/uploads    │
│ Output Format:      docx                   │
│ Output Directory:   /root/Cline/outputs    │
│ Quality:            high                   │
│ Subdirectories:     ☐ (unchecked)          │
└─────────────────────────────────────────────┘
```

**What it does:** Converts PDF files to Word documents

---

## 📝 Field Descriptions (Quick)

| Field | What to Put | Example |
|-------|-------------|---------|
| **Workflow Name** | A unique name (no spaces) | `my_converter` |
| **Input Directory** | Where your files are | `/root/Cline/uploads` |
| **Output Format** | What format you want | `pdf`, `docx`, `csv`, etc. |
| **Output Directory** | Where to save results | `/root/Cline/outputs` |
| **Quality** | How good the conversion | `high` (recommended) |
| **Subdirectories** | Include subfolders? | Usually unchecked |

---

## 🚀 How to Use

1. **Choose** one of the options above (or customize it)
2. **Copy** the values
3. **Paste** into the Streamlit form
4. **Click** "Create Workflow"
5. **Go to** "Run Workflows" tab
6. **Click** the ▶️ button to run it

---

## 💡 Your Directories Are Ready!

✅ Input directory exists: `/root/Cline/uploads`  
✅ Output directory exists: `/root/Cline/outputs`

Just add files to `uploads/` and run your workflow!

---

## 🎯 Recommended First Workflow

**Start with this:**
```
Workflow Name:      test_workflow
Input Directory:    /root/Cline/uploads
Output Format:      pdf
Output Directory:   /root/Cline/outputs
Quality:            high
Subdirectories:     ☐
```

Then:
1. Add a test file to `/root/Cline/uploads/`
2. Run the workflow
3. Check `/root/Cline/outputs/` for the result

---

## ✅ That's It!

Pick an option, fill in the form, and start converting! 🚀
