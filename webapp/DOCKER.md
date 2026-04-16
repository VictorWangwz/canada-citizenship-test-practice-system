# Docker Deployment Guide

This guide explains how to run the Canadian Citizenship Test webapp using Docker.

## Prerequisites

- Docker Desktop for Windows (or Docker Engine + Docker Compose)
- Questions database populated at `../data/questions.db`

## Quick Start

### Option 1: Production Build

Build and run the production-ready container:

```powershell
# From the project root directory
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

The app will be available at http://localhost:3000

### Option 2: Development Mode with Hot Reload

For development with live code changes:

```powershell
# From the webapp directory
cd webapp
docker-compose -f docker-compose.dev.yml up --build
```

## Docker Commands

### Build the image
```powershell
cd webapp
docker build -t citizenship-test-webapp .
```

### Run the container
```powershell
docker run -p 3000:3000 -v c:\Users\wangz\project\canada-citizenship-test\data:/app/data:ro citizenship-test-webapp
```

### Using Docker Compose (Recommended)
```powershell
# Start services
docker-compose up

# Start in background
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f webapp

# Rebuild and restart
docker-compose up --build
```

## File Structure

```
webapp/
├── Dockerfile              # Production multi-stage build
├── Dockerfile.dev          # Development with hot reload
├── .dockerignore          # Files to exclude from build
└── docker-compose.dev.yml # Development compose file

project-root/
└── docker-compose.yml      # Production compose file
```

## Important Notes

### Database Access

The Docker container mounts the `data` directory as **read-only** (`ro`). This means:
- ✅ The webapp can read questions from `questions.db`
- ❌ The webapp cannot modify the database
- ✅ You populate the database using Python scripts on the host machine

To populate/update the database:
```powershell
# Run these on your host machine (not in Docker)
uv run python main.py --setup
uv run python main.py --generate-llm --provider openai
```

### Multi-Stage Build

The production Dockerfile uses a multi-stage build:
1. **deps**: Installs dependencies
2. **builder**: Builds the Next.js app
3. **runner**: Creates minimal runtime image (~150MB)

### Next.js Standalone Output

The production build uses Next.js standalone output mode, which:
- Creates a self-contained deployment
- Reduces image size significantly
- Includes only necessary dependencies

## Environment Variables

You can customize the database path:

```yaml
# In docker-compose.yml
environment:
  - DB_PATH=/app/data/questions.db
```

## Troubleshooting

### Database not found error

**Problem**: `Error: unable to open database file`

**Solution**: Ensure the database exists and the path is correct:
```powershell
# Check if database exists
Test-Path c:\Users\wangz\project\canada-citizenship-test\data\questions.db

# If not, create it
uv run python main.py --setup
```

### Port already in use

**Problem**: `Error: bind: address already in use`

**Solution**: Either stop the conflicting service or change the port:
```yaml
# In docker-compose.yml
ports:
  - "3001:3000"  # Use port 3001 instead
```

### Changes not reflecting

**Problem**: Code changes don't appear in the container

**Solution**: 
- For production: Rebuild the image `docker-compose up --build`
- For development: Use the dev compose file with volume mounts

## Health Check

The production container includes a health check that:
- Runs every 30 seconds
- Checks if the app responds on port 3000
- Marks container as unhealthy after 3 failed attempts

View health status:
```powershell
docker ps
# Look for "healthy" or "unhealthy" in STATUS column
```

## Performance

### Production Image Size
- Base Node.js Alpine: ~180MB
- Final app image: ~200MB
- Multi-stage build removes dev dependencies

### Resource Usage
- Memory: ~150-200MB
- CPU: Minimal (mostly idle)

## Security

- Runs as non-root user (`nextjs`)
- Database mounted read-only
- No sensitive environment variables needed
- Alpine Linux base for smaller attack surface

## CI/CD Integration

Example GitHub Actions workflow:

```yaml
name: Build Docker Image

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build image
        run: |
          cd webapp
          docker build -t citizenship-test-webapp .
```

## Production Deployment

For production deployment to cloud platforms:

### Docker Hub
```powershell
docker tag citizenship-test-webapp username/citizenship-test-webapp:latest
docker push username/citizenship-test-webapp:latest
```

### AWS ECS / Azure Container Instances / Google Cloud Run
Use the `Dockerfile` with your platform's deployment tools.

### Kubernetes
Create deployments and services based on the Docker image.

## Cleaning Up

Remove containers and images:
```powershell
# Stop and remove containers
docker-compose down

# Remove image
docker rmi citizenship-test-webapp

# Remove dangling images
docker image prune
```
