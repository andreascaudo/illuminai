# Illuminai

An open-source e-book reading platform that allows users to upload, manage, and read their e-books through an intuitive, Kindle-like interface.

## Features

- Upload e-books (.epub, .pdf, .txt)
- Read books within the app with customizable reading experience
- User account management with secure authentication
- Personal library organization 
- Responsive design for desktop and mobile devices

## Tech Stack

- **Frontend**: React.js with Next.js
- **Backend**: Python with FastAPI
- **Database**: SQLite (with PostgreSQL as an optional alternative)
- **Authentication**: JWT-based authentication
- **File Storage**: Local storage with S3 migration path
- **E-book Rendering**: React-Reader for EPUB, React-PDF for PDF files

## Reading Features

- **EPUB Support**: Full EPUB file rendering with navigation
- **PDF Support**: PDF viewing with page navigation
- **TXT Support**: Plain text reading with formatting
- **Customization**: Font size, line spacing, and theme selection
- **Persistence**: Reading progress is saved automatically
- **Keyboard Shortcuts**: For easy navigation

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

### EPUB Reader Architecture

The EPUB reader implementation:
1. Uses React-Reader component with custom configuration
2. Handles EPUB internal files through the backend API
3. Transforms internal file paths to go through the backend
4. Saves reading location in localStorage for persistence
5. Customizes appearance based on user preferences

### Security Considerations

- JWT authentication protects all book access endpoints
- EPUB internal file endpoint doesn't require authentication to allow proper rendering
- Content-type headers are set correctly for all file types

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
   ```

3. Set up the backend
   ```bash
   cd src/backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
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
- `src/backend/models/book.py` - Book database model and schemas
- `src/backend/utils/auth.py` - Authentication utilities
- `src/backend/database/database.py` - Database configuration

### Frontend

- `src/frontend/pages/read/[id].tsx` - Main book reading page
- `src/frontend/components/EpubReader.tsx` - EPUB reader component
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

## Future Plans

- Mobile apps (iOS and Android) using React Native
- Reading progress synchronization across devices
- Highlights and annotations
- Book collections and tags
- Social features (sharing, recommendations)
- Advanced search within books

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.