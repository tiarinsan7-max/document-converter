# 📋 Workflows Guide - How to Fill In the Form

## What is a Workflow?

A **workflow** is an automated batch conversion task that:
- Monitors a specific input directory
- Converts all files in that directory to a chosen format
- Saves the converted files to an output directory
- Can be run on-demand or scheduled

---

## 📝 Form Fields Explained

### **1. Workflow Name** (Required)
**What to enter:** A unique name to identify this workflow

**Examples:**
- `daily_pdf_conversion`
- `excel_to_csv_reports`
- `word_to_pdf_documents`
- `my_batch_converter`

**Tips:**
- Use descriptive names
- No spaces (use underscores or hyphens)
- Keep it short and memorable

---

### **2. Input Directory** (Required)
**What to enter:** The folder path where your source files are located

**Examples:**
```
/root/Cline/uploads
/home/user/Documents/to_convert
/tmp/input_files
./uploads
```

**Tips:**
- Use absolute paths (starting with `/`) or relative paths (starting with `./`)
- Make sure the directory exists
- The workflow will process all compatible files in this folder

**For your project, you could use:**
```
/root/Cline/uploads
```

---

### **3. Output Format** (Required)
**What to select:** The format you want to convert files TO

**Options:**
- `pdf` - Portable Document Format
- `docx` - Microsoft Word Document
- `xlsx` - Microsoft Excel Spreadsheet
- `csv` - Comma-Separated Values
- `json` - JavaScript Object Notation
- `txt` - Plain Text File

**Example Use Cases:**
- Convert all Word docs to PDF → Select `pdf`
- Convert Excel files to CSV → Select `csv`
- Convert PDFs to Word → Select `docx`

---

### **4. Output Directory** (Required)
**What to enter:** The folder path where converted files will be saved

**Examples:**
```
/root/Cline/outputs
/home/user/Documents/converted
/tmp/output_files
./outputs
```

**Tips:**
- Use a different directory from input (to avoid confusion)
- Make sure you have write permissions
- The directory will be created if it doesn't exist

**For your project, you could use:**
```
/root/Cline/outputs
```

---

### **5. Quality** (Optional)
**What to select:** Conversion quality level

**Options:**
- `low` - Fast conversion, smaller files, lower quality
- `medium` - Balanced speed and quality
- `high` - Best quality, larger files, slower (recommended)

**Default:** `high`

**When to use each:**
- **Low:** Quick previews, testing
- **Medium:** General use, good balance
- **High:** Final documents, important files

---

### **6. Process subdirectories** (Optional)
**What to check:** Whether to include files in subfolders

**Options:**
- ☐ Unchecked (default) - Only process files in the main input directory
- ☑ Checked - Process files in the input directory AND all subdirectories

**Example:**
If your input directory is `/root/Cline/uploads` and it contains:
```
uploads/
├── file1.pdf
├── file2.docx
└── subfolder/
    └── file3.xlsx
```

- **Unchecked:** Only converts `file1.pdf` and `file2.docx`
- **Checked:** Converts all three files (including `file3.xlsx` in subfolder)

---

## 🎯 Complete Example

Here's a complete example workflow setup:

### Example 1: Convert PDFs to Word Documents
```
Workflow Name:      pdf_to_word_converter
Input Directory:    /root/Cline/uploads
Output Format:      docx
Output Directory:   /root/Cline/outputs
Quality:            high
Subdirectories:     ☐ (unchecked)
```

### Example 2: Convert Excel Files to CSV
```
Workflow Name:      excel_to_csv_batch
Input Directory:    /root/Cline/uploads
Output Format:      csv
Output Directory:   /root/Cline/outputs
Quality:            medium
Subdirectories:     ☑ (checked)
```

### Example 3: Convert Everything to PDF
```
Workflow Name:      all_to_pdf
Input Directory:    /root/Cline/uploads
Output Format:      pdf
Output Directory:   /root/Cline/outputs
Quality:            high
Subdirectories:     ☑ (checked)
```

---

## 🚀 Quick Start for Your Project

### Step 1: Create Test Directories
```bash
cd /root/Cline
mkdir -p uploads outputs
```

### Step 2: Add Some Test Files
```bash
# Copy or move some files to the uploads directory
cp /path/to/your/file.pdf uploads/
```

### Step 3: Fill in the Workflow Form

**Recommended Settings:**
```
Workflow Name:      test_workflow
Input Directory:    /root/Cline/uploads
Output Format:      pdf (or whatever you need)
Output Directory:   /root/Cline/outputs
Quality:            high
Subdirectories:     ☐ (start unchecked for testing)
```

### Step 4: Create and Run
1. Click "Create Workflow"
2. Go to "Run Workflows" tab
3. Click "▶️ Run test_workflow"
4. Check the `/root/Cline/outputs` directory for converted files

---

## 💡 Pro Tips

1. **Start Simple:** Create a test workflow with just a few files first
2. **Use Existing Directories:** Your project already has `uploads/` and `outputs/` directories
3. **Descriptive Names:** Use names that describe what the workflow does
4. **Test First:** Run the workflow manually before scheduling it
5. **Check Permissions:** Make sure you can read from input and write to output directories

---

## 🐛 Common Issues

### "Directory not found"
**Solution:** Create the directories first:
```bash
mkdir -p /root/Cline/uploads /root/Cline/outputs
```

### "No files to convert"
**Solution:** Make sure there are compatible files in the input directory

### "Permission denied"
**Solution:** Check that you have read/write permissions:
```bash
ls -la /root/Cline/uploads
ls -la /root/Cline/outputs
```

---

## 📚 What Happens When You Run a Workflow?

1. **Scans** the input directory for compatible files
2. **Identifies** the format of each file
3. **Converts** each file to the specified output format
4. **Saves** converted files to the output directory
5. **Reports** success/failure for each file

---

## ✅ Ready to Create Your First Workflow!

Use the examples above and fill in the form with your specific needs. Start with a simple test workflow to get familiar with the process.

**Need help?** Check the examples above or start with the "Quick Start" section!
