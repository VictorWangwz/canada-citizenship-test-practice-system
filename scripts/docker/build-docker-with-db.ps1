# Build script that includes the database in the Docker image
# Run this from the PROJECT ROOT (not from webapp folder)

Write-Host "=======================================" -ForegroundColor Cyan
Write-Host "Building Docker Image with Database" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the right directory
$currentDir = Split-Path -Leaf (Get-Location)
if ($currentDir -eq "webapp") {
    Write-Host "Please run this from the project root directory, not from webapp" -ForegroundColor Red
    Write-Host "Run: cd .." -ForegroundColor Yellow
    exit 1
}

# Check if database exists
Write-Host "Checking database..." -ForegroundColor Yellow
$dbPath = ".\data\questions.db"
if (Test-Path $dbPath) {
    $dbSize = (Get-Item $dbPath).Length / 1KB
    Write-Host "Database found: $([math]::Round($dbSize, 2)) KB" -ForegroundColor Green
} else {
    Write-Host "ERROR: Database not found at $dbPath" -ForegroundColor Red
    Write-Host "Please populate the database first:" -ForegroundColor Yellow
    Write-Host "  uv run python main.py --setup" -ForegroundColor Cyan
    Write-Host "  uv run python main.py --generate-llm --provider openai" -ForegroundColor Cyan
    exit 1
}

# Build from project root with webapp as context
Write-Host ""
Write-Host "Building Docker image from project root..." -ForegroundColor Cyan
Write-Host "This includes the database in the image" -ForegroundColor Yellow
Write-Host ""

# Build with the project root as context, but Dockerfile in webapp
docker build `
    -t citizenship-test-webapp:latest `
    -f webapp/Dockerfile `
    .

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=======================================" -ForegroundColor Green
    Write-Host "Image built successfully!" -ForegroundColor Green
    Write-Host "=======================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Database is now included in the image" -ForegroundColor Green
    Write-Host "You no longer need to mount the database volume" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To run the container:" -ForegroundColor Cyan
    Write-Host "  docker run -d --name citizenship-test-webapp -p 3000:3000 citizenship-test-webapp:latest" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "ERROR: Build failed!" -ForegroundColor Red
    exit 1
}
