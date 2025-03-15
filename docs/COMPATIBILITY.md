# PyQt6 Compatibility Guide

## Introduction

IlluminAI uses PyQt6 for its user interface. PyQt6 has some significant differences from PyQt5, including module reorganization. This guide outlines common compatibility issues and their solutions.

## Common Issues

### 1. QAction Import Error

**Problem**: 
```python
ImportError: cannot import name 'QAction' from 'PyQt6.QtWidgets'
```

**Solution**:
In PyQt6, `QAction` was moved from `QtWidgets` to `QtGui`. Change your imports to:

```python
# Incorrect
from PyQt6.QtWidgets import QAction  # This will fail

# Correct
from PyQt6.QtGui import QAction  # Use this instead
```

### 2. Signal/Slot Syntax Changes

**Problem**: The old PyQt5 signal/slot connection syntax may not work correctly in PyQt6.

**Solution**: Use the new-style syntax:

```python
# Old style (may not work reliably in PyQt6)
self.connect(button, SIGNAL('clicked()'), self.handle_click)

# New style (preferred)
button.clicked.connect(self.handle_click)
```

### 3. QApplication exec_() Method

**Problem**: The `exec_()` method has been renamed.

**Solution**: Use `exec()` instead of `exec_()`:

```python
# PyQt5 style
app.exec_()  # This won't work in PyQt6

# PyQt6 style
app.exec()  # Use this instead
```

### 4. Qt Namespace Constants

**Problem**: Some Qt namespace constants have been reorganized.

**Solution**: The constants are now properly placed in enums within the Qt namespace:

```python
# PyQt5 style
Qt.Key_A  # Simple constants still work this way

# For enum-based constants in PyQt6, use the full path
Qt.AlignmentFlag.AlignCenter  # Instead of Qt.AlignCenter
Qt.WindowType.Dialog  # Instead of Qt.Dialog
```

## Version Compatibility

IlluminAI is designed to work with PyQt6 version 6.5.0 or higher. We recommend using the latest stable release for the best experience.

If you encounter compatibility issues, make sure you're using a supported version:

```bash
pip install "PyQt6>=6.5.0"
```

## Troubleshooting

If you encounter other PyQt6-related issues, please check:

1. That your PyQt6 installation is complete with all required modules
2. That you're not mixing PyQt5 and PyQt6 imports
3. That you're using the correct module paths for PyQt6 classes 