# Deployment Guide

This guide explains how to deploy the Illuminai application to a production environment. The application is designed to be deployed using Docker containers for easy setup and management.

## Domain Setup

The application is designed to be deployed to the domain `illuminai.book`. You need to:

1. Register the domain
2. Configure DNS settings to point to your hosting provider
3. Configure SSL/TLS certificates (recommended using Let's Encrypt)

## Production Deployment Options

### Option 1: Docker Compose (Self-hosted)

1. Clone the repository to your server
```bash
git clone https://github.com/yourusername/illuminai.git
cd illuminai
```

2. Create `.env` file from the example
```bash
cp .env.example .env
```

3. Edit the `.env` file with your production settings
```bash
# Generate a strong secret key
SECRET_KEY=your_secure_random_string

# Set strong database password
POSTGRES_PASSWORD=your_strong_db_password

# Configure public URLs
NEXT_PUBLIC_API_URL=https://api.illuminai.book
```

4. Build and start the containers
```bash
docker-compose up -d
```

5. Set up a reverse proxy (Nginx or similar) to handle SSL termination and routing

### Option 2: Cloud Deployment

#### AWS Deployment

1. Set up an AWS account and install the AWS CLI
2. Configure AWS ECS (Elastic Container Service) or Elastic Beanstalk
3. Create an RDS PostgreSQL instance
4. Deploy containers using the provided Dockerfiles
5. Set up AWS Application Load Balancer for routing
6. Configure Route 53 for domain management

#### Vercel + Digital Ocean

1. Deploy the frontend to Vercel:
   - Connect your GitHub repository to Vercel
   - Configure environment variables in Vercel dashboard
   - Set up custom domain for the frontend

2. Deploy the backend to Digital Ocean App Platform:
   - Create a new app in Digital Ocean
   - Connect to your GitHub repository
   - Configure environment variables
   - Set up managed PostgreSQL database
   - Configure domain for API

## Database Migration

When deploying for the first time or updating:

```bash
# Connect to the backend container
docker-compose exec backend bash

# Run migrations
alembic upgrade head
```

## Security Considerations

1. Always use HTTPS in production
2. Set strong, unique passwords for database
3. Keep the SECRET_KEY secure and unique per environment
4. Configure proper CORS settings for production
5. Set up regular database backups
6. Update dependencies regularly

## Scaling Considerations

As user base grows:

1. Consider using AWS S3 or similar for book storage instead of local storage
2. Set up a CDN for serving static assets
3. Implement caching layers (Redis)
4. Consider horizontal scaling of backend services
5. Monitor performance and optimize as needed