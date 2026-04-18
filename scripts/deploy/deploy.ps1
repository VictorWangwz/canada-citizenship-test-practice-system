# Deploy to Cloudflare Pages from local machine using Docker for the build

Write-Host "Building with @cloudflare/next-on-pages inside Docker (Linux)..."
docker run --rm `
  -v "${PWD}\webapp:/app" `
  -w /app `
  node:20 `
  bash -c "npm ci && npx @cloudflare/next-on-pages@1"

if ($LASTEXITCODE -ne 0) {
  Write-Host "Build failed!" -ForegroundColor Red
  exit 1
}

Write-Host "Deploying to Cloudflare Pages..."
wrangler pages deploy webapp/.vercel/output/static `
  --project-name=canada-citizenship-test

Write-Host "Done!" -ForegroundColor Green
