# Docker Verification and Setup Script
# Run this after Docker Desktop is installed

Write-Host "=======================================" -ForegroundColor Cyan
Write-Host "Docker Verification Script" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""

# Check Docker installation
Write-Host "Checking Docker installation..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "SUCCESS: $dockerVersion" -ForegroundColor Green
    } else {
        Write-Host "ERROR: Docker command failed" -ForegroundColor Red
        Write-Host "Make sure Docker Desktop is running (check system tray for whale icon)" -ForegroundColor Yellow
        exit 1
    }
} catch {
    Write-Host "ERROR: Docker is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please run: .\install-docker.ps1" -ForegroundColor Yellow
    exit 1
}

# Check Docker daemon is running
Write-Host ""
Write-Host "Checking if Docker daemon is running..." -ForegroundColor Yellow
try {
    $dockerInfo = docker info 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "SUCCESS: Docker daemon is running" -ForegroundColor Green
    } else {
        Write-Host "ERROR: Docker daemon is not running" -ForegroundColor Red
        Write-Host "Please start Docker Desktop from the Start menu" -ForegroundColor Yellow
        exit 1
    }
} catch {
    Write-Host "ERROR: Cannot connect to Docker daemon" -ForegroundColor Red
    Write-Host "Please start Docker Desktop from the Start menu" -ForegroundColor Yellow
    exit 1
}

# Check Docker Compose
Write-Host ""
Write-Host "Checking Docker Compose..." -ForegroundColor Yellow
try {
    $composeVersion = docker-compose --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "SUCCESS: $composeVersion" -ForegroundColor Green
    } else {
        Write-Host "WARNING: Docker Compose not found" -ForegroundColor Yellow
        Write-Host "Modern Docker Desktop includes Compose V2 as 'docker compose'" -ForegroundColor White
    }
} catch {
    Write-Host "Docker Compose V1 not found (this is OK with modern Docker)" -ForegroundColor Yellow
}

# Test Docker with hello-world
Write-Host ""
Write-Host "Running Docker test (hello-world)..." -ForegroundColor Yellow
try {
    $testOutput = docker run --rm hello-world 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "SUCCESS: Docker is working correctly!" -ForegroundColor Green
    } else {
        Write-Host "ERROR: Docker test failed" -ForegroundColor Red
        Write-Host $testOutput -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "ERROR: Docker test failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=======================================" -ForegroundColor Green
Write-Host "Docker is installed and working!" -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Run: .\build-docker.ps1 (to build the Docker image)" -ForegroundColor White
Write-Host "2. Run: .\run-docker.ps1 (to run the container)" -ForegroundColor White
Write-Host ""
