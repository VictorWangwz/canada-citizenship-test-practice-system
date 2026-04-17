# Migration to Cloudflare D1 - Complete Guide

## Overview

This guide will help you migrate from SQLite (embedded in Docker) to Cloudflare D1 for completely free deployment on Cloudflare Pages.

## ✅ Benefits

- **100% Free**: Unlimited bandwidth, 10 million requests/month
- **Global Edge Network**: Fast worldwide
- **No Server Management**: Serverless
- **Custom Domain**: Free SSL, victorwz.com integration

---

## 📋 Prerequisites

1. Cloudflare account (free)
2. GitHub repository (already done ✅)
3. Node.js and npm installed

---

## 🚀 Step-by-Step Migration

### Step 1: Install Wrangler CLI

```powershell
npm install -g wrangler
```

### Step 2: Login to Cloudflare

```powershell
wrangler login
```

This will open your browser to authorize Wrangler.

### Step 3: Export Database to D1 Format

```powershell
# Run the export script
python export-to-d1.py
```

This creates:
- `migrations/schema.sql` - Database structure
- `migrations/data.sql` - All 211 questions

### Step 4: Create D1 Database

```powershell
cd webapp
wrangler d1 create citizenship-test-db
```

**Important**: Copy the `database_id` from the output!

Example output:
```
✅ Successfully created DB 'citizenship-test-db'
Created your database using D1's new storage backend.

[[d1_databases]]
binding = "DB"
database_name = "citizenship-test-db"
database_id = "abc123-def456-ghi789"  # ← COPY THIS
```

### Step 5: Update wrangler.toml

Edit `webapp/wrangler.toml` and replace `YOUR_DATABASE_ID_HERE` with your actual database_id.

### Step 6: Import Schema

```powershell
wrangler d1 execute citizenship-test-db --file=../migrations/schema.sql
```

### Step 7: Import Data

```powershell
wrangler d1 execute citizenship-test-db --file=../migrations/data.sql
```

This imports all 211 questions into D1.

### Step 8: Verify Import

```powershell
wrangler d1 execute citizenship-test-db --command="SELECT COUNT(*) FROM questions"
```

Should show: `211`

### Step 9: Update API Routes

Rename the D1 versions to replace the old files:

```powershell
# Questions API
Move-Item app/api/questions/route.ts app/api/questions/route.old.ts
Move-Item app/api/questions/route-d1.ts app/api/questions/route.ts

# Submit API
Move-Item app/api/submit/route.ts app/api/submit/route.old.ts
Move-Item app/api/submit/route-d1.ts app/api/submit/route.ts
```

### Step 10: Test Locally

```powershell
# Still in webapp directory
npm run dev
```

Open http://localhost:3001 and test the app works with D1.

### Step 11: Deploy to Cloudflare Pages

#### Option A: Via Cloudflare Dashboard (Easiest)

1. Go to: https://dash.cloudflare.com/
2. Select your account → Pages
3. Click "Create application" → "Connect to Git"
4. Authorize GitHub access
5. Select `canada-citizenship-test` repository
6. Configure build settings:
   ```
   Framework preset: Next.js
   Build command: cd webapp && npm install && npm run build
   Build output directory: webapp/.next
   Root directory: (leave blank)
   Node.js version: 20
   ```
7. Click "Save and Deploy"

#### Option B: Via Wrangler CLI

```powershell
# Build the app
npm run build

# Deploy to Pages
wrangler pages deploy .next --project-name=canada-citizenship-test
```

### Step 12: Add D1 Binding in Cloudflare Dashboard

1. Go to your Cloudflare Pages project
2. Settings → Functions
3. D1 database bindings
4. Variable name: `DB`
5. D1 database: Select `citizenship-test-db`
6. Click "Save"

### Step 13: Configure Custom Domain

1. In Cloudflare Pages → Custom domains
2. Click "Set up a custom domain"
3. Enter: `canada-citizenship-test.victorwz.com`
4. Click "Add"

For path-based routing (`victorwz.com/canada-citizenship-test-practice`), you'll need to set up a Cloudflare Worker (see below).

### Step 14: Commit and Push Changes

```powershell
cd ..   # Back to project root
git add .
git commit -m "Migrate to Cloudflare D1 for serverless deployment"
git push
```

---

## 🔧 Path-Based Routing (Optional)

For `victorwz.com/canada-citizenship-test-practice`:

1. Create a Cloudflare Worker
2. Add this code:

```javascript
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    if (url.pathname.startsWith('/canada-citizenship-test-practice')) {
      // Proxy to Pages deployment
      const newUrl = new URL(request.url);
      newUrl.hostname = 'canada-citizenship-test.pages.dev';
      newUrl.pathname = url.pathname.replace('/canada-citizenship-test-practice', '');
      
      return fetch(newUrl, request);
    }
    
    // Pass through other requests
    return fetch(request);
  }
};
```

3. Deploy Worker to `victorwz.com` route: `victorwz.com/canada-citizenship-test-practice/*`

---

## 📊 Cost Comparison

| Platform | Monthly Cost | Notes |
|----------|--------------|-------|
| **Cloudflare Pages + D1** | **$0** | ✅ This option (free tier: 10M requests, 100K DB reads/day) |
| Railway | ~$5 | Docker-based deployment |
| Fly.io | ~$0-5 | Free tier available but limited |
| Vercel | $0 | Can't use SQLite |

---

## ✅ What You Get

- ✅ **Free hosting** (Cloudflare Pages)
- ✅ **Free database** (D1)
- ✅ **Free CDN** (Cloudflare global network)
- ✅ **Free SSL** certificate
- ✅ **Custom domain** support
- ✅ **Automatic deployments** from GitHub
- ✅ **Unlimited bandwidth**
- ✅ **DDoS protection**

---

## 🆘 Troubleshooting

**"Database not configured" error**:
- Make sure you added D1 binding in Cloudflare Pages settings
- Variable name must be exactly `DB`

**Build fails**:
- Check Node.js version is 20 in Cloudflare Pages settings
- Verify build command: `cd webapp && npm install && npm run build`

**Questions not loading**:
- Verify data import: `wrangler d1 execute citizenship-test-db --command="SELECT COUNT(*) FROM questions"`
- Check D1 binding is correct in wrangler.toml

---

## 🎯 Next Steps After Deployment

1. Test the deployed app
2. Configure custom domain
3. Enable GitHub auto-deployment
4. Monitor usage in Cloudflare dashboard

Your app will be at: `https://canada-citizenship-test.pages.dev`
