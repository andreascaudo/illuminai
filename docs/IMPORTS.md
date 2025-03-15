# Python Import Structure Guide

## Overview

IlluminAI uses absolute imports throughout the codebase. This document explains the import structure and how to avoid common import errors.

## Import Structure

All imports in the codebase should use absolute imports starting with the `src` package:

```python
# Correct
from src.document_handlers.document_factory import DocumentFactory
from src.ui.document_view import DocumentView
from src.utils.token_counter import count_tokens

# Incorrect (using relative imports)
from ..document_handlers.document_factory import DocumentFactory
from .document_view import DocumentView
```

## Common Import Errors

### "attempted relative import beyond top-level package"

This error occurs when Python tries to perform a relative import (using `..` notation) but can't determine the parent package correctly.

**Cause:**
- Using relative imports like `from ..document_handlers import DocumentFactory`
- Not having proper package initialization with `__init__.py` files
- Running a module directly instead of as part of a package

**Solution:**
1. Change relative imports to absolute imports (as shown above)
2. Always run the application using the provided `run.py` script
3. Don't run individual modules directly with `python src/main.py`

### "ModuleNotFoundError: No module named 'src'"

This error typically means Python can't find the `src` package.

**Cause:**
- Running the script from the wrong directory
- Missing proper package initialization

**Solution:**
1. Make sure you're running commands from the project root directory
2. Use the provided `run.py` script which adds the `src` directory to the Python path
3. Ensure all directories have `__init__.py` files

## Best Practices

1. **Always use absolute imports** - This avoids the complexity of relative imports
2. **Run the application using run.py** - This script properly sets up the Python path
3. **Keep proper `__init__.py` files** - Ensure all package directories have these files
4. **Run from the project root** - Always execute commands from the illuminai/ directory 