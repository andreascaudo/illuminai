# Illuminai Architecture

This document outlines the architecture of the Illuminai e-book reader application.

## System Overview

Illuminai is built with a modern stack focused on performance, scalability, and developer experience:

- **Frontend**: React.js with Next.js for SSR and optimized rendering
- **Backend**: Python with FastAPI for a high-performance API
- **Database**: SQLite for local development (PostgreSQL for production)
- **Authentication**: JWT-based token authentication
- **File Storage**: Local file storage (with AWS S3 as a planned alternative)

## Architecture Diagram

```
┌────────────────┐     ┌────────────────┐     ┌────────────────┐
│                │     │                │     │                │
│    Frontend    │◄────┤     Backend    │◄────┤   Database     │
│   (Next.js)    │     │   (FastAPI)    │     │  (SQLite/PG)   │
│                │────►│                │────►│                │
└────────────────┘     └───────┬────────┘     └────────────────┘
                              │
                              ▼
                      ┌────────────────┐
                      │                │
                      │  File Storage  │
                      │                │
                      └────────────────┘
```

## Component Details

### Frontend (Next.js/React)

The frontend is organized using a component-based architecture:

- **Pages**: Main application views (index, login, register, library, read)
- **Components**: Reusable UI elements (Navbar, BookCard, EpubReader, etc.)
- **Context**: Global state management (AuthContext for user authentication)
- **Styles**: Global styles and component-specific styling

Key features:
- Server-side rendering for optimal performance
- API integration with the backend
- Responsive design for all devices
- Book readers for different formats (EPUB, PDF, TXT)

### Backend (FastAPI)

The backend follows a modular API design:

- **Routers**: API endpoints organized by resource (auth, users, books)
- **Models**: Database models and Pydantic schemas for validation
- **Services**: Business logic separated from API controllers
- **Database**: SQLAlchemy ORM for database operations
- **Utils**: Helper functions and middleware

Key features:
- Fast API endpoints with automatic OpenAPI documentation
- JWT authentication
- File upload handling and validation
- Database migrations with Alembic

### Database

The database schema consists of the following main tables:

- **users**: User account information
- **books**: Book metadata and storage paths

Relationships:
- One-to-many relationship between users and books

SQLite is used for development, while PostgreSQL is recommended for production deployments.

### File Storage

For the initial implementation, files are stored locally:

- Books are stored in user-specific directories
- Files are renamed to unique identifiers to prevent collisions
- Future plan: Migrate to AWS S3 or similar cloud storage for scalability

## Authentication Flow

1. User registers or logs in
2. Backend validates credentials and issues a JWT token
3. Frontend stores the token in localStorage
4. Token is included in the Authorization header for API requests
5. Backend validates the token for protected routes

## Data Flow

### Book Upload Process:

1. User selects a file in the upload form
2. Frontend validates file format and size
3. File is sent to the backend with book metadata
4. Backend validates the file, creates a unique filename, and saves it
5. Book metadata is stored in the database with a reference to the file path
6. User is redirected to their library

### Book Reading Process:

1. User selects a book from their library
2. Frontend requests the book metadata and content from the backend
3. Backend verifies user ownership and serves the file
4. Frontend renders the book using the appropriate reader component

## Scalability Considerations

- **Horizontal Scaling**: Backend can be scaled horizontally by deploying multiple instances
- **Database**: Migrate to PostgreSQL for production with more concurrent users
- **File Storage**: Migration path to cloud storage (S3) for unlimited scaling
- **Caching**: Future implementation of Redis for caching frequently accessed data

## Security Considerations

- **Authentication**: JWT tokens with proper expiration
- **Password Storage**: Secure password hashing with bcrypt
- **File Validation**: Strict file type and size validation
- **CORS**: Proper CORS configuration for production
- **Input Validation**: All user input is validated using Pydantic schemas

## Future Extensions

- **Mobile Apps**: React Native iOS and Android applications
- **Reading Progress Sync**: Synchronize reading progress across devices
- **Annotations & Highlights**: Allow users to annotate and highlight text
- **Social Features**: Book sharing and recommendations
- **AI Features**: Book summaries, recommendations, and search enhancement