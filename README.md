# Illuminai

An open-source e-book reading platform that allows users to upload, manage, and read their e-books through an intuitive, Kindle-like interface. Now featuring AI-powered reading assistance with LLM integration.

## Features

- Upload e-books (.epub, .pdf, .txt)
- Read books within the app with customizable reading experience
- User account management with secure authentication
- Personal library organization 
- Responsive design for desktop and mobile devices
- **AI-powered reading assistance** using large language models (LLMs)

## Tech Stack

- **Frontend**: React.js with Next.js
- **Backend**: Python with FastAPI
- **Database**: SQLite (with PostgreSQL as an optional alternative)
- **Authentication**: JWT-based authentication
- **File Storage**: Local storage with S3 migration path
- **E-book Rendering**: React-Reader for EPUB, React-PDF for PDF files
- **AI Integration**: OpenAI and Anthropic API integrations
- **Text Processing**: Tokenization and chunking for efficient LLM context management

## Reading Features

- **EPUB Support**: Full EPUB file rendering with navigation
- **PDF Support**: PDF viewing with page navigation
- **TXT Support**: Plain text reading with formatting
- **Customization**: Font size, line spacing, and theme selection
- **Persistence**: Reading progress is saved automatically
- **Keyboard Shortcuts**: For easy navigation

## LLM Features

- **Text Selection**: Select any text in your e-book to ask questions about it
- **Smart Context**: Automatically extracts the right amount of context around your selection
- **Book Processing**: Books are processed into manageable chunks for efficient LLM interaction
- **API Key Management**: Securely store and manage your LLM provider API keys
- **Multiple Providers**: Support for OpenAI (GPT-4, GPT-3.5) and Anthropic (Claude) models
- **Token Optimization**: Intelligently manages context size to optimize token usage

## Implementation Details

### Backend Endpoints

- **/api/auth**: Authentication endpoints (register, login, refresh)
- **/api/books**: Book management and content serving
  - GET `/api/books`: List user's books
  - GET `/api/books/{id}`: Get book details
  - GET `/api/books/{id}/content`: Get book content (with format-specific handling)
  - GET `/api/books/{id}/{file_path}`: Access EPUB internal files
  - POST `/api/books/upload`: Upload new book
  - PUT `/api/books/{id}`: Update book metadata
  - DELETE `/api/books/{id}`: Delete book
- **/api/api-keys**: LLM API key management
  - GET `/api/api-keys`: List user's API keys
  - POST `/api/api-keys`: Add a new API key
  - PUT `/api/api-keys/{id}`: Update an API key
  - DELETE `/api/api-keys/{id}`: Delete an API key
- **/api/books/llm**: LLM integration for books
  - POST `/api/books/llm/{book_id}/process`: Process a book for LLM use
  - GET `/api/books/llm/{book_id}/chunks`: Get book chunks
  - POST `/api/books/llm/{book_id}/ask`: Ask a question about book content
  - GET `/api/books/llm/{book_id}/interactions`: Get past LLM interactions

### EPUB Reader Architecture

The EPUB reader implementation:
1. Uses React-Reader component with custom configuration
2. Handles EPUB internal files through the backend API
3. Transforms internal file paths to go through the backend
4. Saves reading location in localStorage for persistence
5. Customizes appearance based on user preferences

### EPUB Reader Architecture

The EPUB reader implementation:
1. Uses React-Reader component with custom configuration
2. Handles EPUB internal files through the backend API
3. Transforms internal file paths to go through the backend
4. Saves reading location in localStorage for persistence
5. Customizes appearance based on user preferences

### LLM Integration Architecture

The LLM integration follows these key principles:
1. **Smart Chunking**: Books are processed into semantic chunks during upload
2. **Selective Context**: Only relevant portions around the user's selection are sent to the LLM
3. **Secure API Key Handling**: User API keys are encrypted before storage
4. **Provider Abstraction**: Common interface for different LLM providers
5. **Efficient Token Usage**: Context size is optimized to reduce token consumption

### Security Considerations

- JWT authentication protects all book access endpoints
- EPUB internal file endpoint doesn't require authentication to allow proper rendering
- Content-type headers are set correctly for all file types
- API keys are encrypted using Fernet symmetric encryption before storage
- Background processing for book chunking to handle large files safely

## Getting Started

### Prerequisites

- Node.js (v16+)
- Python (v3.9-3.13)
- Docker (optional, for containerization)

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/illuminai.git
   cd illuminai
   ```

2. Set up environment variables
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   # Add ENCRYPTION_KEY for API key encryption
   ```

3. Set up the backend
   ```bash
   cd src/backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   # Note: Required packages include cryptography, tiktoken, openai, anthropic
   ```

4. Run database migrations
   ```bash
   alembic upgrade head
   ```

5. Set up the frontend
   ```bash
   cd src/frontend
   npm install
   ```

6. Start the development servers
   ```bash
   # Backend (from src/backend directory)
   uvicorn main:app --reload

   # Frontend (from src/frontend directory)
   npm run dev
   ```

7. Access the application
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   
### Setting Up LLM Features

1. Register for API keys from supported providers:
   - [OpenAI API](https://platform.openai.com)
   - [Anthropic API](https://console.anthropic.com)

2. Add your API keys in the application:
   - Navigate to the API Keys page
   - Add your provider keys (they will be encrypted)
   - Set your preferred provider as default

3. Using the LLM features:
   - Open any book in the reader
   - Select text you want to ask about
   - Click "Ask AI" or use Ctrl/Cmd+Q shortcut
   - Type your question and adjust context settings if needed

## Docker Deployment

To run using Docker Compose:

```bash
docker-compose up -d
```

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details.

## Architecture

For detailed information about the application architecture, see the [Architecture Documentation](docs/architecture.md).

## Deployment

For deployment to the illuminai.book domain, see the [Deployment Documentation](docs/deployment.md).

## Key Files

### Backend

- `src/backend/routers/books.py` - Book management and content serving endpoints
- `src/backend/routers/book_llm.py` - LLM integration endpoints for books
- `src/backend/routers/api_keys.py` - API key management endpoints
- `src/backend/models/book.py` - Book and chunk models and schemas
- `src/backend/models/user.py` - User and API key models and schemas
- `src/backend/utils/auth.py` - Authentication utilities
- `src/backend/utils/encryption.py` - API key encryption utilities
- `src/backend/utils/book_chunker.py` - Book text chunking utilities
- `src/backend/utils/llm_service.py` - LLM provider integration
- `src/backend/database/database.py` - Database configuration

### Frontend

- `src/frontend/pages/read/[id].tsx` - Main book reading page with LLM integration
- `src/frontend/components/EpubReader.tsx` - EPUB reader component
- `src/frontend/components/LLMQuestionPanel.tsx` - LLM question interface
- `src/frontend/pages/api-keys.tsx` - API key management page
- `src/frontend/pages/library/index.tsx` - Book library page
- `src/frontend/components/BookUpload.tsx` - Book upload component

## Debugging Common Issues

### EPUB Reading Issues

- **404 Not Found for EPUB internal files**: Check the backend endpoint that serves internal EPUB files
- **EPUB not loading**: Verify the book file is valid and EPUB resolver function is working
- **Navigation not working**: Check event handling in the reader component
- **Styling issues**: Check font size and theme application in the reader

### PDF Reading Issues

- **PDF not rendering**: Check PDF.js worker URL in configuration
- **Navigation broken**: Verify page number state and handlers

### LLM Integration Issues

- **API Key errors**: Check if the key is correct and the provider is supported
- **Book processing fails**: Ensure the book file is valid and properly formatted
- **Missing context**: Verify the chunk retrieval logic is working correctly
- **No response from LLM**: Check network connectivity and API rate limits
- **Context too large**: Adjust the context size or chunk size settings

## Future Plans

- Further LLM enhancements:
  - Memory of past interactions within a reading session
  - Book summaries and chapter outlines
  - Character and plot tracking
  - Learning mode with concept explanations
  - Multiple language support
- Mobile apps (iOS and Android) using React Native
- Reading progress synchronization across devices
- Highlights and annotations with LLM-powered insights
- Book collections and tags with AI-suggested organization
- Social features (sharing, recommendations)
- Advanced search within books

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.