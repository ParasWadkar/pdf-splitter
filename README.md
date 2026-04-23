# 📄 PDF-Splitter

Split each page of a PDF into 4 equal parts (2×2 grid) and export as a new PDF.

## 🚀 Features
- ✅ Fast and lightweight
- ✅ Preserves original quality (vector-based)
- ✅ Simple CLI usage
- ✅ **NEW: GUI for batch processing multiple PDFs**
- ✅ Process multiple PDFs at once
- ✅ Choose output directory

## 📦 Installation

```bash
git clone https://github.com/ParasWadkar/pdf-splitter.git
cd pdf-splitter
pip install -r requirements.txt
```

## 🎯 Usage

### Option 1: GUI (Recommended for Multiple Files)

```bash
python gui.py
```

**Features:**
- 📁 Browse and select multiple PDF files
- 🎨 User-friendly interface
- 📊 Progress tracking
- 📂 Choose custom output directory
- ⚡ Process multiple PDFs at once
- 🚫 Cancel processing anytime

**Steps:**
1. Click "📁 Browse & Select PDFs"
2. Select one or more PDF files
3. (Optional) Click "📂 Choose Output Folder" to specify where to save results
4. Click "⚙️ Process All PDFs"
5. Wait for completion - each PDF will be saved as `filename_split.pdf`

### Option 2: Command Line

```bash
python main.py input.pdf output.pdf
```

**Example:**
```bash
python main.py document.pdf document_split.pdf
```

**What it does:**
- Reads `document.pdf`
- Splits each page into 4 quadrants
- Saves as `document_split.pdf`