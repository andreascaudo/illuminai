# IlluminAI Document Reader - Project Summary

## Overview

IlluminAI is an open-source document reader application with AI-powered document interaction capabilities. It allows users to open various document formats and interact with the content using state-of-the-art language models.

## Key Features Implemented

1. **Document Support**
   - PDF files using pdfplumber
   - Plain text files (.txt)
   - Microsoft Word documents (.docx)
   - Rich Text Format (.rtf)
   - OpenDocument Text (.odt)
   - Markdown files (.md)

2. **UI Components**
   - Clean PyQt6-based user interface
   - Multi-document tabbed interface
   - Context menu for AI interactions
   - Settings dialog for API keys and preferences
   - Drag and drop support for documents
   - Dark mode support

3. **LLM Integration**
   - Support for multiple providers (Anthropic, OpenAI, xAI)
   - Context-aware LLM processing with token limits
   - AI interaction options:
     - "Explain like I'm 5"
     - "Summarize this"
     - "Ask a question..." (with custom input)

4. **Advanced Features**
   - Tokenization utilities for accurate token counting
   - Background processing of LLM requests
   - Smart context selection for large documents
   - Persistent settings (token limits, UI preferences, etc.)

## Architecture

The application follows a modular architecture that makes it easy to extend:

- `src/main.py` - Application entry point
- `src/ui/` - UI components using PyQt6
- `src/document_handlers/` - Document format handlers
- `src/llm_providers/` - LLM API integrations
- `src/utils/` - Utility functions for token counting

## Running the Application

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python run.py
   ```

3. Configure your API keys in the Settings menu

## Recent Improvements

Recent updates to the application include:

1. **Dependency Flexibility**
   - Added fallback methods for token counting without requiring tiktoken
   - Created a custom RTF implementation without external dependencies
   - Provided graceful degradation for optional packages

2. **Simplified Code Structure**
   - Unified document handler interface across all formats
   - Enhanced document factory to improve code organization
   - Added comprehensive error handling in the run script

3. **Better Testing**
   - Added unit tests for document handlers
   - Provided test document samples
   - Improved codebase maintainability

4. **Documentation**
   - Added detailed troubleshooting guides
   - Expanded installation instructions
   - Provided clearer usage examples

## Future Improvements

Potential improvements for future development:

1. **Additional Document Formats**
   - EPUB support
   - HTML support
   - More Microsoft Office formats (.pptx, .xlsx)

2. **Enhanced AI Features**
   - Document-wide analysis
   - Comparison between multiple documents
   - Custom AI prompt templates

3. **UI Enhancements**
   - Document thumbnail previews
   - Search within documents
   - Annotation and highlighting features

4. **Performance Optimization**
   - Caching of document content
   - Optimized token counting for very large documents

5. **Cross-Platform Support**
   - Package for Windows, macOS, and Linux
   - Mobile version 