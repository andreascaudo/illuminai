# Development Guide for Illuminai

This guide provides options for setting up your development environment for Illuminai.

## Option 1: Development with PostgreSQL (Recommended for Production)

### PostgreSQL Setup

1. Install PostgreSQL on your system:
   ```bash
   # macOS
   brew install postgresql
   
   # Ubuntu/Debian
   sudo apt install postgresql postgresql-contrib
   
   # Windows
   # Download from https://www.postgresql.org/download/windows/
   ```

2. Create a database:
   ```bash
   createdb illuminai
   ```

3. Install the Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Update your .env file to use PostgreSQL:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/illuminai
   ```

### Troubleshooting PostgreSQL Installation

If you have issues with psycopg2-binary installation:

1. Try installing the system dependencies:
   ```bash
   # macOS
   brew install postgresql
   
   # Ubuntu/Debian
   sudo apt-get install libpq-dev python3-dev
   ```

2. Try using the source distribution instead:
   ```bash
   pip uninstall psycopg2-binary
   pip install psycopg2
   ```

## Option 2: Development with SQLite (Easiest Setup)

For a simpler development setup, you can use SQLite which doesn't require a separate database server.

1. Modify your database.py file:
   ```python
   # Get database URL from environment variables or use SQLite by default
   DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./illuminai.db")
   
   # Create engine with SQLite-specific parameters
   connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
   engine = create_engine(DATABASE_URL, connect_args=connect_args)
   ```

2. Update your .env file to use SQLite:
   ```
   DATABASE_URL=sqlite:///./illuminai.db
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Docker Development Setup

Using Docker eliminates the need to install dependencies directly:

1. Make sure Docker and Docker Compose are installed
2. Run the application:
   ```bash
   docker-compose up -d
   ```

This will set up all services including PostgreSQL in containers.

## Database Migrations

After setting up your database:

```bash
alembic upgrade head
```

## Running the Application

```bash
# Backend
cd src/backend
uvicorn main:app --reload

# Frontend
cd src/frontend
npm install
npm run dev
```