# Complete Docker Workflow - All-in-One Script
# This script guides you through the entire Docker setup process

param(
    [switch]$SkipInstallCheck
)

Write-Host "=======================================" -ForegroundColor Cyan
Write-Host "Docker Complete Setup Wizard" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "This wizard will guide you through:" -ForegroundColor White
Write-Host "  1. Docker installation verification" -ForegroundColor White
Write-Host "  2. Building the Docker image" -ForegroundColor White
Write-Host "  3. Running the container" -ForegroundColor White
Write-Host ""

# Step 1: Check Docker
if (!$SkipInstallCheck) {
    Write-Host "Step 1: Checking Docker installation..." -ForegroundColor Yellow
    Write-Host ""
    
    try {
        docker --version | Out-Null
        if ($LASTEXITCODE -eq 0) {
            docker info | Out-Null
            if ($LASTEXITCODE -eq 0) {
                Write-Host "Docker is installed and running!" -ForegroundColor Green
            } else {
                Write-Host "Docker is installed but not running" -ForegroundColor Yellow
                Write-Host "Please start Docker Desktop and run this script again" -ForegroundColor Cyan
                exit 1
            }
        } else {
            throw "Docker not found"
        }
    } catch {
        Write-Host "Docker is not installed!" -ForegroundColor Red
        Write-Host ""
        Write-Host "To install Docker:" -ForegroundColor Yellow
        Write-Host "  1. Run: .\install-docker.ps1" -ForegroundColor Cyan
        Write-Host "  2. Follow the installation instructions" -ForegroundColor White
        Write-Host "  3. Restart your computer" -ForegroundColor White
        Write-Host "  4. Run this script again" -ForegroundColor White
        Write-Host ""
        $installNow = Read-Host "Open installation guide now? (y/n)"
        if ($installNow -eq "y") {
            .\install-docker.ps1
        }
        exit 1
    }
}

Write-Host ""
Write-Host "---" -ForegroundColor Gray

# Step 2: Check database
Write-Host ""
Write-Host "Step 2: Checking database..." -ForegroundColor Yellow
Write-Host ""

$dbPath = ".\data\questions.db"
if (Test-Path $dbPath) {
    $dbSize = (Get-Item $dbPath).Length / 1KB
    Write-Host "Database found: $([math]::Round($dbSize, 2)) KB" -ForegroundColor Green
} else {
    Write-Host "Database not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "You need to populate the database first:" -ForegroundColor Yellow
    Write-Host "  uv run python main.py --setup" -ForegroundColor Cyan
    Write-Host "  uv run python main.py --generate-llm --provider openai" -ForegroundColor Cyan
    Write-Host ""
    exit 1
}

Write-Host ""
Write-Host "---" -ForegroundColor Gray

# Step 3: Build image
Write-Host ""
Write-Host "Step 3: Building Docker image..." -ForegroundColor Yellow
Write-Host ""

$prodImage = docker images -q citizenship-test-webapp:latest

if ($prodImage) {
    Write-Host "Docker image already exists" -ForegroundColor Green
    $rebuild = Read-Host "Rebuild the image? (y/n)"
    if ($rebuild -ne "y") {
        Write-Host "Skipping build..." -ForegroundColor Yellow
    } else {
        Write-Host ""
        Write-Host "Rebuilding image..." -ForegroundColor Cyan
        .\build-docker.ps1
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Build failed!" -ForegroundColor Red
            exit 1
        }
    }
} else {
    Write-Host "Building Docker image (this may take 5-10 minutes)..." -ForegroundColor Cyan
    Write-Host ""
    
    Set-Location webapp
    docker build -t citizenship-test-webapp:latest -f Dockerfile .
    Set-Location ..
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "Build failed!" -ForegroundColor Red
        exit 1
    }
    
    Write-Host ""
    Write-Host "Image built successfully!" -ForegroundColor Green
}

Write-Host ""
Write-Host "---" -ForegroundColor Gray

# Step 4: Run container
Write-Host ""
Write-Host "Step 4: Running Docker container..." -ForegroundColor Yellow
Write-Host ""

$runNow = Read-Host "Start the container now? (y/n)"
if ($runNow -eq "y") {
    Write-Host ""
    .\run-docker.ps1
} else {
    Write-Host ""
    Write-Host "Container not started." -ForegroundColor Yellow
    Write-Host "To start it later, run: .\run-docker.ps1" -ForegroundColor Cyan
}
