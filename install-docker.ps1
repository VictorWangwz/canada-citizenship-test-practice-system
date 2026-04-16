# Complete Docker Installation and Setup Guide for Windows
# Run each step in order

Write-Host "=======================================" -ForegroundColor Cyan
Write-Host "Docker Installation Guide for Windows" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check Windows Version
Write-Host "Step 1: Checking Windows version..." -ForegroundColor Yellow
$windowsVersion = [System.Environment]::OSVersion.Version
Write-Host "Windows Version: $($windowsVersion.Major).$($windowsVersion.Minor) Build $($windowsVersion.Build)" -ForegroundColor White

if ($windowsVersion.Build -lt 19041) {
    Write-Host "WARNING: Your Windows version might not support Docker Desktop properly." -ForegroundColor Red
    Write-Host "Docker Desktop requires Windows 10 Build 19041 or higher, or Windows 11." -ForegroundColor Yellow
}

# Step 2: Check if WSL 2 is installed
Write-Host ""
Write-Host "Step 2: Checking WSL 2 (Windows Subsystem for Linux)..." -ForegroundColor Yellow
try {
    $wslVersion = wsl --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "WSL is installed:" -ForegroundColor Green
        Write-Host $wslVersion -ForegroundColor White
    } else {
        Write-Host "WSL does not appear to be installed." -ForegroundColor Yellow
    }
} catch {
    Write-Host "WSL is not installed or not accessible." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "If WSL 2 is not installed, you need to install it first:" -ForegroundColor Cyan
Write-Host "1. Open PowerShell as Administrator" -ForegroundColor White
Write-Host "2. Run: wsl --install" -ForegroundColor White
Write-Host "3. Restart your computer" -ForegroundColor White
Write-Host ""

# Step 3: Check if Docker is already installed
Write-Host "Step 3: Checking if Docker is already installed..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Docker is already installed: $dockerVersion" -ForegroundColor Green
        Write-Host ""
        $continue = Read-Host "Do you want to continue anyway? (y/n)"
        if ($continue -ne "y") {
            exit 0
        }
    } else {
        Write-Host "Docker is not installed." -ForegroundColor Yellow
    }
} catch {
    Write-Host "Docker is not installed." -ForegroundColor Yellow
}

# Step 4: Download Docker Desktop
Write-Host ""
Write-Host "Step 4: Docker Desktop Installation" -ForegroundColor Yellow
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To install Docker Desktop:" -ForegroundColor White
Write-Host "1. Go to: https://www.docker.com/products/docker-desktop" -ForegroundColor Cyan
Write-Host "2. Click 'Download for Windows'" -ForegroundColor White
Write-Host "3. Run the installer (Docker Desktop Installer.exe)" -ForegroundColor White
Write-Host "4. Follow the installation wizard" -ForegroundColor White
Write-Host "5. When prompted, ensure WSL 2 backend is selected (recommended)" -ForegroundColor White
Write-Host "6. Restart your computer after installation completes" -ForegroundColor White
Write-Host ""

Write-Host "Alternative: Download directly using this link:" -ForegroundColor Yellow
Write-Host "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe" -ForegroundColor Cyan
Write-Host ""

# Step 5: Provide next steps
Write-Host "Step 5: After Installation" -ForegroundColor Yellow
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "After Docker Desktop is installed and your computer is restarted:" -ForegroundColor White
Write-Host "1. Launch Docker Desktop from the Start menu" -ForegroundColor White
Write-Host "2. Wait for Docker to start (it will show a whale icon in the system tray)" -ForegroundColor White
Write-Host "3. Accept the Docker Subscription Service Agreement if prompted" -ForegroundColor White
Write-Host "4. Run this verification script: .\verify-docker.ps1" -ForegroundColor Cyan
Write-Host ""

Write-Host "Press any key to open the Docker Desktop download page in your browser..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
Start-Process "https://www.docker.com/products/docker-desktop"
