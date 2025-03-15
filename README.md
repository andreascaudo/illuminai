# IlluminAI Document Reader

An open-source document reader application with AI-powered document interaction capabilities. IlluminAI allows you to open various document formats and interact with the content using state-of-the-art language models from providers like Anthropic, OpenAI, and more.

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)

## 📋 Features

- **Document Support**: Open and display various document formats (.pdf, .txt, .docx, .rtf, .odt, .md, etc.)
  - Visual PDF rendering with Preview-like experience (when PyMuPDF is installed)
  - Fallback to text-only mode for all document types
- **Interactive AI Analysis**: Select text and right-click to access context-specific AI options:
  - "Explain like I'm 5" - Get simplified explanations of complex text
  - "Summarize this" - Get concise summaries of selected content
  - "Ask a question" - Inquire about specific aspects of the selected text
- **Multiple LLM Providers**: Support for different LLM providers:
  - Anthropic Claude (primary focus)
  - OpenAI GPT models
  - xAI Grok (support planned)
- **Context-Aware Processing**: Intelligent handling of context with adjustable token limits
  - Default 8,000 token limit (user-adjustable)
  - For large documents, smart selection of context around the user selection
- **Clean, Modern UI**: Simple, intuitive interface built with PyQt6
  - Multi-document support with tabs
  - Dark mode support
  - Drag and drop file opening

## 🖼️ Screenshots

*[Screenshots to be added]*

## 🔧 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. Clone this repository:
```bash
git clone https://github.com/yourusername/illuminai.git
cd illuminai
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

> **Note on Dependencies**: 
> - Optional packages like `tiktoken` and `lxml` may require a compiler. The application will work without them using fallback methods.
> - PyMuPDF (for visual PDF rendering) can be challenging to install on some systems. See [PyMuPDF Installation Guide](docs/PYMUPDF_INSTALL.md) for detailed instructions.
> - If you encounter issues with compilation, the core functionality will still work - PDFs will display in text-only mode.

4. Run the application:
```bash
python run.py
```

## Running Tests

To verify that the document handlers are working correctly:

```bash
python -m unittest discover src/tests
```

### Generating Test Documents

To create sample documents in various formats for testing:

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run the test document generator
python scripts/create_test_docs.py
```

This will create sample documents in the `test_documents` directory in multiple formats:
- PDF
- TXT
- DOCX
- RTF
- Markdown

## Configuration

### API Keys

To use the AI features, you'll need to set up API keys:

1. Open the application
2. Go to Settings → Preferences
3. In the "API Keys" tab, enter your API keys for:
   - Anthropic Claude
   - OpenAI GPT
   
> Note: The xAI Grok API is included as a placeholder for future integration.

### Token Limits

You can adjust the maximum token limit in the toolbar. Higher token limits allow for more context but may:
- Increase API costs
- Slow down response times

## 🚀 Usage

### Opening Documents

- Click "Open" in the toolbar or use File → Open from the menu
- Alternatively, drag and drop files directly into the application window
- Supported formats include PDF, TXT, RTF, DOCX, ODT, Markdown, and more

### Using AI Features

1. Select text in the document that you want to analyze
2. Right-click on the selected text to see AI interaction options
3. Choose an option:
   - "Explain like I'm 5" for simplified explanations
   - "Summarize this" for a concise summary
   - "Ask a question..." to ask specific questions about the text
4. View AI response in the panel that appears at the bottom of the document

### Configuring LLM Providers

1. Go to Settings → Preferences
2. Select the "API Keys" tab
3. Enter your API keys for the LLM providers you want to use
4. Select your preferred default provider

## ⚙️ Configuration

### LLM Settings

- **API Keys**: Configure API keys for different LLM providers in Settings → Preferences
- **Token Limits**: Adjust the maximum token limit for context in the toolbar
- **Default Provider**: Set your preferred LLM provider in Settings → Preferences

### UI Settings

- **Font Size**: Customize the font size in Settings → Preferences
- **Dark Mode**: Toggle dark mode for a more comfortable reading experience in low light

## 🔄 API Integration

IlluminAI is designed to work with multiple LLM providers:

- **Anthropic Claude**: Primary focus, uses the claude-3-sonnet model by default
- **OpenAI GPT**: Support for GPT-4 and other models
- **xAI Grok**: Placeholder implementation for future integration when public API becomes available

## 🧩 Architecture

IlluminAI follows a modular architecture to make it easy to extend:

- **Document Handlers**: Pluggable handlers for different document formats
- **LLM Providers**: Modular implementation of different LLM APIs
- **UI Components**: Clean separation of UI elements and business logic

## 🛠️ Development

### Project Structure

```
illuminai/
├── src/
│   ├── document_handlers/  # Document format handlers
│   ├── llm_providers/      # LLM API integrations
│   ├── ui/                 # UI components
│   ├── utils/              # Utility functions
│   └── main.py             # Application entry point
├── requirements.txt        # Dependencies
├── LICENSE                 # MIT License
└── README.md               # Documentation
```

### Adding Support for New Document Types

1. Create a new handler in `src/document_handlers/`
2. Implement the document handler interface
3. Register the handler in `DocumentFactory`

### Adding New LLM Providers

1. Create a new provider in `src/llm_providers/`
2. Implement the `LLMProvider` interface
3. Update the `LLMService` class to include the new provider

## 🔍 Troubleshooting

### Installation Issues

- **Dependency installation fails**: Some packages like `tiktoken` and `lxml` may require a C compiler. The application includes fallback methods that will work without these packages.

- **PyMuPDF installation errors**: If you encounter errors installing PyMuPDF for visual PDF rendering, see our [PyMuPDF Installation Guide](docs/PYMUPDF_INSTALL.md). The application will work without it, using text-only mode for PDFs.

- **Package not found**: If you see an error about a missing package, ensure you've installed all dependencies with `pip install -r requirements.txt`.

### Runtime Issues

- **API Key Issues**: If you see "API key not set" errors, make sure you've entered your API keys in Settings → Preferences → API Keys.

- **Document Loading Fails**: 
  - Verify the document format is supported
  - Check file permissions
  - For PDF files, ensure the PDF is not encrypted or password-protected

- **No Response from AI**: 
  - Check your internet connection
  - Verify API key is valid
  - Try with a shorter text selection (reduce token count)

### Common Errors

- **Import Error**: If you see an import error, make sure you're running the application from the project root with `python run.py`.

- **Token Limit Exceeded**: If the selected text is too long, you'll need to either select a smaller portion or increase the token limit in the toolbar.

- **PyQt6 Import Errors**: If you see errors about missing PyQt6 classes or modules (like `QAction`), check the [PyQt6 Compatibility Guide](docs/COMPATIBILITY.md) for solutions. PyQt6 reorganized many classes compared to PyQt5.

- **Relative Import Errors**: If you encounter errors like "attempted relative import beyond top-level package", check the [Import Structure Guide](docs/IMPORTS.md). Always run the application using the `run.py` script from the project root.

- **PDF Visual Rendering Not Working**: If PDFs are displaying as text only, you may not have PyMuPDF installed correctly. See the [PyMuPDF Installation Guide](docs/PYMUPDF_INSTALL.md) for solutions.

## 📜 License

IlluminAI is released under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## ✨ Conclusion

IlluminAI aims to make document reading more interactive and insightful by leveraging the latest advancements in AI language models. The application is designed with flexibility, extensibility, and ease of use in mind.

Whether you're a student trying to understand complex topics, a professional analyzing documents, or a developer looking to extend the application with new features, IlluminAI provides a solid foundation for AI-powered document interaction.

## 🙏 Acknowledgements

- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) for the UI framework
- [PyPDF2](https://github.com/py-pdf/pypdf) for PDF text extraction
- [PyMuPDF](https://github.com/pymupdf/PyMuPDF) for visual PDF rendering
- [python-docx](https://github.com/python-openxml/python-docx) for DOCX support
- [odfpy](https://github.com/eea/odfpy) for ODT support
- [Anthropic](https://www.anthropic.com/) and [OpenAI](https://openai.com/) for their LLM APIs 