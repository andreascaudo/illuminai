# PyMuPDF Installation Guide

## Overview

PyMuPDF is used for visual PDF rendering in IlluminAI, providing a macOS Preview-like experience. However, it can be challenging to install on some systems because it requires compilation of C/C++ code.

**Important**: IlluminAI will work without PyMuPDF, falling back to text-only mode for PDFs. The visual rendering is an enhancement but not required for core functionality.

## Installation Methods

### Method 1: Standard Installation

Try the standard pip installation first:

```bash
pip install pymupdf==1.23.19
```

### Method 2: Pre-built Wheels (macOS)

If you encounter compilation errors on macOS, try installing pre-built wheels:

```bash
pip install --find-links=https://github.com/pymupdf/PyMuPDF/releases pymupdf
```

### Method 3: Using Homebrew (macOS)

For Homebrew users on macOS:

```bash
brew install mupdf
pip install pymupdf
```

### Method 4: Linux Dependencies

On Ubuntu/Debian Linux, install the required system packages first:

```bash
sudo apt-get install libmupdf-dev
pip install pymupdf
```

On Fedora/RHEL/CentOS:

```bash
sudo dnf install mupdf-devel
pip install pymupdf
```

### Method 5: Windows Installation

On Windows, you might need to install Visual C++ Build Tools first:

1. Install [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. Select "C++ build tools" during installation
3. Then install PyMuPDF:
```bash
pip install pymupdf
```

## Common Error Messages and Solutions

### 1. "Command 'gcc' failed"

This indicates missing compiler tools. Install them with:

**macOS**:
```bash
xcode-select --install
```

**Ubuntu/Debian**:
```bash
sudo apt-get install build-essential
```

### 2. "mupdf.h: No such file or directory"

Missing MuPDF development files:

**macOS**:
```bash
brew install mupdf
```

**Ubuntu/Debian**:
```bash
sudo apt-get install libmupdf-dev
```

### 3. Error in arm64 Architecture (Apple Silicon)

For M1/M2 Macs, try using Rosetta:

```bash
arch -x86_64 pip install pymupdf
```

## Verifying Installation

To verify that PyMuPDF is installed correctly:

```python
python -c "import fitz; print(fitz.__version__)"
```

If this prints a version number without errors, PyMuPDF is installed correctly.

## Fallback Text-Only Mode

If you cannot install PyMuPDF after trying these methods, IlluminAI will still work! 

The application will automatically detect that PyMuPDF is not available and fall back to text-only mode for PDFs. All other functionality will work normally. 