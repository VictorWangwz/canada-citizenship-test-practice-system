# Cloudflare Deployment Guide

## Important: Database Considerations

Your app currently uses an SQLite database embedded in the Docker image. **Cloudflare Pages doesn't support Docker or file-based databases directly.**

You have two deployment options:

---

## Option 1: Cloudflare Pages with API Route (Recommended for your domain)

Cloudflare Pages can host Next.js apps, but we need to adapt the database approach:

### Step 1: Migrate to Cloudflare D1 (SQLite-compatible database)

1. **Create D1 Database**:
   ```bash
   npx wrangler d1 create citizenship-test-db
   ```

2. **Import your questions**:
   ```bash
   npx wrangler d1 execute citizenship-test-db --file=path/to/schema.sql
   ```

3. **Update Next.js API routes** to use D1 instead of better-sqlite3

### Step 2: Deploy to Cloudflare Pages

1. Push your code to GitHub (we'll do this below)

2. Go to [Cloudflare Dashboard](https://dash.cloudflare.com) → Pages

3. Click "Create application" → "Connect to Git"

4. Select your `canada-citizenship-test` repository

5. Configure build settings:
   ```
   Framework preset: Next.js
   Build command: cd webapp && npm install && npm run build
   Build output directory: webapp/.next
   Root directory: (leave blank)
   ```

6. Add D1 binding in Pages settings

7. Set custom domain: `victorwz.com/canada-citizenship-test-practice`

---

## Option 2: Deploy Docker Image to Container Platform (Easier, keeps current setup)

Since you already have a working Docker image with embedded database, deploy to a container Platform:

### A. Railway (Easiest)

1. Go to [Railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub"
3. Select your repository
4. Railway auto-detects Dockerfile and deploys
5. Set up custom domain: `victorwz.com/canada-citizenship-test-practice`

### B. Fly.io

1. Install flyctl: `powershell -c "irm https://fly.io/install.ps1 | iex"`
2. Run: `fly launch` (in project directory)
3. Deploy: `fly deploy`
4. Set custom domain

### C. DigitalOcean App Platform

1. Connect GitHub repository
2. Select Docker as build method
3. Configure custom domain

---

## Option 3: Cloudflare Workers + External Database

1. Deploy your Docker container to any cloud provider (AWS ECS, Google Cloud Run)
2. Use Cloudflare as CDN/proxy in front of it
3. Configure path routing for `/canada-citizenship-test-practice`

---

## My Recommendation

**For victorwz.com/canada-citizenship-test-practice:**

Use **Railway** or **Fly.io** + **Cloudflare Proxy**:

1. Deploy Docker container to Railway/Fly.io (keeps everything working as-is)
2. Get deployment URL (e.g., `https://your-app.railway.app`)
3. In Cloudflare DNS, create a CNAME or use Workers route to proxy `/canada-citizenship-test-practice` to your deployment
4. This gives you:
   - ✅ Your custom domain
   - ✅ Cloudflare CDN/security
   - ✅ No code changes needed
   - ✅ SQLite database works as-is

---

## Quick Start (Railway Deployment)

1. **Push to GitHub** (we'll do this next)

2. **Deploy to Railway**:
   - Go to https://railway.app
   - Sign in with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select `canada-citizenship-test`
   - Railway detects Dockerfile automatically
   - Click "Deploy"

3. **Configure Domain**:
   - In Railway → Settings → Domain
   - Click "Custom Domain"
   - Add: `citizenship-test.victorwz.com` (subdomain approach)
   - OR use Cloudflare Workers for path-based routing

4. **Cloudflare Path Routing** (for `/canada-citizenship-test-practice`):
   - Create Cloudflare Worker:
   ```javascript
   export default {
     async fetch(request) {
       const url = new URL(request.url);
       if (url.pathname.startsWith('/canada-citizenship-test-practice')) {
         // Proxy to Railway deployment
         const targetUrl = 'https://your-railway-app.railway.app' + 
           url.pathname.replace('/canada-citizenship-test-practice', '');
         return fetch(targetUrl, request);
       }
       // Other routes continue normally
       return fetch(request);
     }
   };
   ```

Would you like me to proceed with Railway deployment, or do you prefer to migrate to Cloudflare D1 for full Cloudflare Pages integration?
