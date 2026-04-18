# Run Docker Container Script
# This starts the citizenship test webapp in a Docker container

Write-Host "=======================================" -ForegroundColor Cyan
Write-Host "Running Docker Container" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""

# Verify Docker is running
Write-Host "Verifying Docker is running..." -ForegroundColor Yellow
try {
    docker info | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Docker is not running" -ForegroundColor Red
        Write-Host "Please start Docker Desktop" -ForegroundColor Yellow
        exit 1
    }
    Write-Host "Docker is running" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Cannot connect to Docker" -ForegroundColor Red
    exit 1
}

# Check if image exists
Write-Host ""
Write-Host "Checking for Docker images..." -ForegroundColor Yellow
$prodImage = docker images -q citizenship-test-webapp:latest
$devImage = docker images -q citizenship-test-webapp:dev

if (!$prodImage -and !$devImage) {
    Write-Host "ERROR: No Docker image found" -ForegroundColor Red
    Write-Host "Please run: .\build-docker.ps1 first" -ForegroundColor Yellow
    exit 1
}

# Select image to run
$imageToRun = "citizenship-test-webapp:latest"
if ($prodImage -and $devImage) {
    Write-Host "Multiple images found. Which one to run?" -ForegroundColor Yellow
    Write-Host "1. Production (latest)" -ForegroundColor White
    Write-Host "2. Development (dev)" -ForegroundColor White
    $choice = Read-Host "Enter choice (1 or 2)"
    if ($choice -eq "2") {
        $imageToRun = "citizenship-test-webapp:dev"
    }
} elseif ($devImage) {
    $imageToRun = "citizenship-test-webapp:dev"
}

Write-Host "Using image: $imageToRun" -ForegroundColor Green

# Check if database exists
Write-Host ""
Write-Host "Checking database..." -ForegroundColor Yellow
$dbPath = ".\data\questions.db"
if (Test-Path $dbPath) {
    $absoluteDbPath = (Resolve-Path $dbPath).Path
    Write-Host "Database found: $absoluteDbPath" -ForegroundColor Green
} else {
    Write-Host "ERROR: Database not found at $dbPath" -ForegroundColor Red
    Write-Host "Please populate the database first:" -ForegroundColor Yellow
    Write-Host "  uv run python main.py --setup" -ForegroundColor White
    Write-Host "  uv run python main.py --generate-llm --provider openai" -ForegroundColor White
    exit 1
}

# Check if port 3000 is available
Write-Host ""
Write-Host "Checking if port 3000 is available..." -ForegroundColor Yellow
$portInUse = Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue
if ($portInUse) {
    Write-Host "WARNING: Port 3000 is already in use" -ForegroundColor Yellow
    $port = Read-Host "Enter alternate port (e.g., 3001, 3002)"
    if (!$port) {
        $port = "3001"
    }
} else {
    $port = "3000"
    Write-Host "Port 3000 is available" -ForegroundColor Green
}

# Stop any existing container
Write-Host ""
Write-Host "Checking for existing containers..." -ForegroundColor Yellow
$existingContainer = docker ps -a -q -f name=citizenship-test-webapp
if ($existingContainer) {
    Write-Host "Stopping and removing existing container..." -ForegroundColor Yellow
    docker stop citizenship-test-webapp 2>&1 | Out-Null
    docker rm citizenship-test-webapp 2>&1 | Out-Null
}

# Run the container
Write-Host ""
Write-Host "Starting container..." -ForegroundColor Cyan
Write-Host "Container name: citizenship-test-webapp" -ForegroundColor White
Write-Host "Port: $port" -ForegroundColor White
Write-Host "Database: $absoluteDbPath (read-only)" -ForegroundColor White
Write-Host ""

# Get the current directory for volume mounting
$currentDir = (Get-Location).Path
$dataPath = Join-Path $currentDir "data"

# Run container
docker run -d `
    --name citizenship-test-webapp `
    -p "${port}:3000" `
    -v "${dataPath}:/app/data:ro" `
    $imageToRun

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=======================================" -ForegroundColor Green
    Write-Host "Container started successfully!" -ForegroundColor Green
    Write-Host "=======================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Access the app at: http://localhost:${port}" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Useful commands:" -ForegroundColor Yellow
    Write-Host "  View logs:    docker logs -f citizenship-test-webapp" -ForegroundColor White
    Write-Host "  Stop:         docker stop citizenship-test-webapp" -ForegroundColor White
    Write-Host "  Start:        docker start citizenship-test-webapp" -ForegroundColor White
    Write-Host "  Remove:       docker rm -f citizenship-test-webapp" -ForegroundColor White
    Write-Host ""
    
    # Wait a moment then show logs
    Write-Host "Waiting for container to initialize..." -ForegroundColor Yellow
    Start-Sleep -Seconds 3
    Write-Host ""
    Write-Host "Container logs:" -ForegroundColor Yellow
    Write-Host "---" -ForegroundColor Gray
    docker logs citizenship-test-webapp
    Write-Host "---" -ForegroundColor Gray
    Write-Host ""
    
    # Try to open browser
    $openBrowser = Read-Host "Open browser to http://localhost:${port}? (y/n)"
    if ($openBrowser -eq "y") {
        Start-Process "http://localhost:${port}"
    }
} else {
    Write-Host ""
    Write-Host "ERROR: Failed to start container!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Checking for error details..." -ForegroundColor Yellow
    docker logs citizenship-test-webapp 2>&1
}
