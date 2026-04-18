# GitHub Setup and Push Script
# This script helps you create a GitHub repository and push your code

Write-Host "=======================================" -ForegroundColor Cyan
Write-Host "GitHub Repository Setup" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is configured
Write-Host "Checking git configuration..." -ForegroundColor Yellow
$gitUser = git config user.name
$gitEmail = git config user.email

if ($gitUser -and $gitEmail) {
    Write-Host "Git user: $gitUser <$gitEmail>" -ForegroundColor Green
} else {
    Write-Host "Git is not configured!" -ForegroundColor Red
    exit 1
}

# Check current branch
$branch = git branch --show-current
Write-Host "Current branch: $branch" -ForegroundColor Green

# Instructions for creating GitHub repository
Write-Host ""
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host "Step 1: Create GitHub Repository" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Go to: https://github.com/new" -ForegroundColor White
Write-Host "2. Repository name: canada-citizenship-test" -ForegroundColor Yellow
Write-Host "3. Description: Canadian Citizenship Test Practice App with Next.js and Docker" -ForegroundColor White
Write-Host "4. Visibility: Public (or Private if you prefer)" -ForegroundColor White
Write-Host "5. Do NOT initialize with README, .gitignore, or license" -ForegroundColor Red
Write-Host "6. Click 'Create repository'" -ForegroundColor White
Write-Host ""

$openGitHub = Read-Host "Open GitHub in browser to create repository? (y/n)"
if ($openGitHub -eq "y") {
    Start-Process "https://github.com/new"
}

Write-Host ""
Write-Host "After creating the repository, enter your GitHub username"
$githubUsername = Read-Host "GitHub username"

if (!$githubUsername) {
    Write-Host "Username is required!" -ForegroundColor Red
    exit 1
}

# Construct remote URL
$remoteUrl = "https://github.com/$githubUsername/canada-citizenship-test.git"

Write-Host ""
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host "Step 2: Add GitHub Remote" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Remote URL: $remoteUrl" -ForegroundColor Yellow

# Check if remote already exists
$existingRemote = git remote get-url origin 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "Remote 'origin' already exists: $existingRemote" -ForegroundColor Yellow
    $updateRemote = Read-Host "Update remote URL? (y/n)"
    if ($updateRemote -eq "y") {
        git remote set-url origin $remoteUrl
        Write-Host "Remote URL updated!" -ForegroundColor Green
    }
} else {
    git remote add origin $remoteUrl
    Write-Host "Remote 'origin' added!" -ForegroundColor Green
}

Write-Host ""
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host "Step 3: Push to GitHub" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "About to push to: $remoteUrl" -ForegroundColor Yellow
Write-Host "Branch: $branch" -ForegroundColor Yellow
Write-Host ""

$confirmPush = Read-Host "Push to GitHub now? (y/n)"
if ($confirmPush -eq "y") {
    Write-Host ""
    Write-Host "Pushing to GitHub..." -ForegroundColor Cyan
    
    # Rename master to main if needed
    if ($branch -eq "master") {
        Write-Host "Renaming branch from 'master' to 'main'..." -ForegroundColor Yellow
        git branch -M main
        $branch = "main"
    }
    
    # Push to GitHub
    git push -u origin $branch
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "=======================================" -ForegroundColor Green
        Write-Host "Successfully pushed to GitHub!" -ForegroundColor Green
        Write-Host "=======================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "Repository URL: https://github.com/$githubUsername/canada-citizenship-test" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Next steps:" -ForegroundColor Yellow
        Write-Host "1. Review CLOUDFLARE-SETUP.md for deployment options" -ForegroundColor White
        Write-Host "2. Set up GitHub Secrets for CI/CD (if using Cloudflare Pages)" -ForegroundColor White
        Write-Host "3. Choose deployment platform (Railway, Fly.io, or Cloudflare)" -ForegroundColor White
        Write-Host ""
        
        $openRepo = Read-Host "Open repository in browser? (y/n)"
        if ($openRepo -eq "y") {
            Start-Process "https://github.com/$githubUsername/canada-citizenship-test"
        }
    } else {
        Write-Host ""
        Write-Host "Push failed! This might be due to:" -ForegroundColor Red
        Write-Host "1. Repository doesn't exist on GitHub" -ForegroundColor Yellow
        Write-Host "2. Authentication required (you may need to enter GitHub credentials)" -ForegroundColor Yellow
        Write-Host "3. Network issues" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "To push manually, run:" -ForegroundColor Cyan
        Write-Host "  git push -u origin $branch" -ForegroundColor White
    }
} else {
    Write-Host ""
    Write-Host "Push cancelled. To push later, run:" -ForegroundColor Yellow
    Write-Host "  git push -u origin $branch" -ForegroundColor White
}
