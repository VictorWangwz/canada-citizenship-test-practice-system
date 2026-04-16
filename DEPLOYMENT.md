# Canada Citizenship Test Practice

Docker deployment configuration for Cloudflare Pages

## Quick Deploy to Cloudflare Pages

### Prerequisites
- Cloudflare account
- Domain configured in Cloudflare
- GitHub repository

### Deployment Steps

1. **Connect GitHub Repository**
   - Go to Cloudflare Dashboard → Pages
   - Click "Create a project"
   - Connect to your GitHub repository
   - Select `canada-citizenship-test` repository

2. **Configure Build Settings**
   ```
   Framework preset: Next.js
   Build command: cd webapp && npm install && npm run build
   Build output directory: webapp/.next
   Root directory: (leave blank or set to /)
   ```

3. **Environment Variables** (Optional)
   - No environment variables needed (database is embedded in Docker image)

4. **Custom Domain**
   - After deployment, go to Custom Domains
   - Add custom domain: `victorwz.com`
   - Add path-based routing for `/canada-citizenship-test-practice`

### Alternative: Docker Deployment on Cloudflare Workers

If using Docker image instead:

1. **Push image to registry**
   ```powershell
   docker tag citizenship-test-webapp:latest your-registry/citizenship-test-webapp:latest
   docker push your-registry/citizenship-test-webapp:latest
   ```

2. **Deploy to Cloudflare Workers for Platforms**
   - Use Workers for deploying containerized applications
   - Configure custom domain and routing

### CI/CD with GitHub Actions

Use `.github/workflows/deploy.yml` (included) for automatic deployment on push to main branch.

### Build Commands

For local development:
```powershell
# Build Docker image
.\build-docker-with-db.ps1

# Run locally
docker run -d -p 3000:3000 citizenship-test-webapp:latest
```

For production deployment:
```powershell
# Build production image
docker build -t citizenship-test-webapp:production -f webapp/Dockerfile .

# Push to registry
docker tag citizenship-test-webapp:production your-registry/citizenship-test:latest
docker push your-registry/citizenship-test:latest
```
