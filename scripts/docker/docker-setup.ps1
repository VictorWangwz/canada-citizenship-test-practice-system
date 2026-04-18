# Docker Setup Script for Canada Citizenship Test Webapp
# Run this from the project root directory

Write-Host "Canada Citizenship Test - Docker Setup" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is installed
Write-Host "Checking Docker installation..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Docker found: $dockerVersion" -ForegroundColor Green
    } else {
        throw "Docker not found"
    }
} catch {
    Write-Host "Docker is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

# Check if database exists
Write-Host ""
Write-Host "Checking database..." -ForegroundColor Yellow
$dbPath = ".\data\questions.db"
if (Test-Path $dbPath) {
    Write-Host "Database found at $dbPath" -ForegroundColor Green
} else {
    Write-Host "Database not found at $dbPath" -ForegroundColor Red
    Write-Host "Please populate the database first:" -ForegroundColor Yellow
    Write-Host "  uv run python main.py --setup" -ForegroundColor Cyan
    Write-Host "  uv run python main.py --generate-llm --provider openai" -ForegroundColor Cyan
    exit 1
}

# Ask user which mode to run
Write-Host ""
Write-Host "Choose deployment mode:" -ForegroundColor Yellow
Write-Host "1. Production (optimized, recommended)" -ForegroundColor White
Write-Host "2. Development (hot reload for code changes)" -ForegroundColor White
Write-Host ""
$mode = Read-Host "Enter choice (1 or 2)"

switch ($mode) {
    "1" {
        Write-Host ""
        Write-Host "Starting production build..." -ForegroundColor Cyan
        docker-compose up --build
    }
    "2" {
        Write-Host ""
        Write-Host "Starting development mode..." -ForegroundColor Cyan
        Set-Location webapp
        docker-compose -f docker-compose.dev.yml up --build
    }
    default {
        Write-Host "Invalid choice. Please run the script again." -ForegroundColor Red
        exit 1
    }
}
