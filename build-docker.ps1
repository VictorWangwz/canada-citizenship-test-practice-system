# Build Docker Image Script
# This creates the Docker image for the citizenship test webapp

Write-Host "=======================================" -ForegroundColor Cyan
Write-Host "Building Docker Image" -ForegroundColor Cyan
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

# Check if database exists
Write-Host ""
Write-Host "Checking database..." -ForegroundColor Yellow
$dbPath = ".\data\questions.db"
if (Test-Path $dbPath) {
    $dbSize = (Get-Item $dbPath).Length / 1KB
    Write-Host "Database found: $dbPath ($([math]::Round($dbSize, 2)) KB)" -ForegroundColor Green
} else {
    Write-Host "WARNING: Database not found at $dbPath" -ForegroundColor Yellow
    Write-Host "The container will fail to start without a database." -ForegroundColor Yellow
    Write-Host "Run these commands first:" -ForegroundColor Cyan
    Write-Host "  uv run python main.py --setup" -ForegroundColor White
    Write-Host "  uv run python main.py --generate-llm --provider openai" -ForegroundColor White
    Write-Host ""
    $continue = Read-Host "Continue anyway? (y/n)"
    if ($continue -ne "y") {
        exit 1
    }
}

# Choose build type
Write-Host ""
Write-Host "Choose build type:" -ForegroundColor Yellow
Write-Host "1. Production (optimized, smaller image, recommended)" -ForegroundColor White
Write-Host "2. Development (includes dev tools, hot reload)" -ForegroundColor White
Write-Host ""
$buildType = Read-Host "Enter choice (1 or 2)"

switch ($buildType) {
    "1" {
        Write-Host ""
        Write-Host "Building production image..." -ForegroundColor Cyan
        Write-Host "This may take 5-10 minutes on first build..." -ForegroundColor Yellow
        Write-Host ""
        
        Set-Location webapp
        docker build -t citizenship-test-webapp:latest -f Dockerfile .
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "SUCCESS: Image built successfully!" -ForegroundColor Green
            Write-Host "Image name: citizenship-test-webapp:latest" -ForegroundColor White
            Write-Host ""
            Write-Host "Next steps:" -ForegroundColor Cyan
            Write-Host "1. Run: cd .. (to go back to project root)" -ForegroundColor White
            Write-Host "2. Run: .\run-docker.ps1 (to start the container)" -ForegroundColor White
        } else {
            Write-Host ""
            Write-Host "ERROR: Build failed!" -ForegroundColor Red
            exit 1
        }
    }
    "2" {
        Write-Host ""
        Write-Host "Building development image..." -ForegroundColor Cyan
        Write-Host ""
        
        Set-Location webapp
        docker build -t citizenship-test-webapp:dev -f Dockerfile.dev .
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "SUCCESS: Development image built successfully!" -ForegroundColor Green
            Write-Host "Image name: citizenship-test-webapp:dev" -ForegroundColor White
            Write-Host ""
            Write-Host "Next steps:" -ForegroundColor Cyan
            Write-Host "1. Run: cd .. (to go back to project root)" -ForegroundColor White
            Write-Host "2. Run: .\run-docker.ps1 (to start the container)" -ForegroundColor White
        } else {
            Write-Host ""
            Write-Host "ERROR: Build failed!" -ForegroundColor Red
            exit 1
        }
    }
    default {
        Write-Host "Invalid choice" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "View images:" -ForegroundColor Yellow
docker images citizenship-test-webapp
