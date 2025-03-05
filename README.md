# Illuminai

An open-source e-book reading platform that allows users to upload, manage, and read their e-books through an intuitive, Kindle-like interface.

## Features

- Upload e-books (.epub, .pdf, .txt)
- Read books within the app
- User account management
- Personal library organization
- Responsive design for various devices

## Tech Stack

- **Frontend**: React.js with Next.js
- **Backend**: Python with FastAPI
- **Database**: SQLite (with PostgreSQL as an optional alternative)
- **Authentication**: JWT-based authentication
- **File Storage**: Local storage with S3 migration path

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

## Future Plans

- Mobile apps (iOS and Android) using React Native
- Reading progress synchronization across devices
- Highlights and annotations
- Book collections and tags
- Social features (sharing, recommendations)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.