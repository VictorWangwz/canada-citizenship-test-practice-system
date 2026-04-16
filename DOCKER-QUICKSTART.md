# 🚢 Docker Quick Start

The easiest way to run the Canadian Citizenship Test webapp.

## Prerequisites

1. **Docker Desktop** - [Download here](https://www.docker.com/products/docker-desktop)
2. **Database populated** - Run the Python scripts first:
   ```powershell
   uv run python main.py --setup
   uv run python main.py --generate-llm --provider openai
   ```

## Run the App

### Method 1: Using the Setup Script (Easiest)

```powershell
.\docker-setup.ps1
```

Choose option 1 for production or option 2 for development mode.

### Method 2: Docker Compose

**Production mode:**
```powershell
docker-compose up --build
```

**Development mode (with hot reload):**
```powershell
cd webapp
docker-compose -f docker-compose.dev.yml up --build
```

### Method 3: Docker CLI

```powershell
# Build the image
cd webapp
docker build -t citizenship-test-webapp .

# Run the container
docker run -p 3000:3000 -v ${PWD}\..\data:/app/data:ro citizenship-test-webapp
```

## Access the App

Open your browser to: **http://localhost:3000**

## Stop the App

Press `Ctrl+C` or in detached mode:
```powershell
docker-compose down
```

## Troubleshooting

**"Database not found"**
- Ensure you've run the Python scripts to populate the database first
- Check that `data/questions.db` exists in the project root

**"Port 3000 already in use"**
- Stop other services using port 3000
- Or change the port in `docker-compose.yml`:
  ```yaml
  ports:
    - "3001:3000"
  ```

## More Information

See [webapp/DOCKER.md](webapp/DOCKER.md) for detailed Docker documentation.
