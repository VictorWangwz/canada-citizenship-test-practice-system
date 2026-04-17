# 🚀 Deployment Quick Start Guide

## ✅ What's Been Done

1. **Git Repository Initialized** ✅
   - Initial commit created with all files
   - 50 files committed (12,317 lines)
   - Database included (328 KB with 211 questions)

2. **Files Committed**:
   - ✅ Next.js webapp with government-styled UI
   - ✅ Docker configuration (Dockerfile, docker-compose.yml)
   - ✅ Deployment scripts (PowerShell)
   - ✅ CI/CD workflow (GitHub Actions)
   - ✅ Documentation (README, deployment guides)
   - ✅ SQLite database with questions

3. **Files Excluded** (via .gitignore):
   - ❌ Virtual environments (.venv)
   - ❌ Python cache files
   - ❌ Environment variables (.env)
   - ❌ Test/debug files
   - ❌ IDE settings (.vscode)
   - ❌ Temporary data files

---

## 📋 Next Steps

### Step 1: Push to GitHub (IN PROGRESS)

The script `github-push.ps1` is currently running. Complete these steps:

1. **Create GitHub Repository**:
   - Go to: https://github.com/new
   - Name: `canada-citizenship-test`
   - Description: `Canadian Citizenship Test Practice App with Next.js and Docker`
   - Visibility: Public (recommended) or Private
   - **Important**: Do NOT initialize with README
   - Click "Create repository"

2. **Enter your GitHub username** in the terminal

3. **Script will**:
   - Add GitHub remote
   - Rename branch to `main`
   - Push all code to GitHub

### Step 2: Deploy to Production

Choose ONE of these deployment options:

#### Option A: Railway (Recommended - Easiest)

**Why**: Works with Docker immediately, no code changes needed

1. Go to https://railway.app
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select `canada-citizenship-test`
5. Railway auto-detects Dockerfile and deploys
6. Done! You get a URL like: `https://canada-citizenship-test.up.railway.app`

**Custom Domain Setup**:
```
Railway Dashboard → Settings → Domain → Add Custom Domain
Enter: canada-citizenship-test-practice.victorwz.com
```

Then in Cloudflare DNS:
```
Type: CNAME
Name: canada-citizenship-test-practice
Target: <railway-provided-domain>
```

#### Option B: Cloudflare Pages (Requires Migration)

**Why**: Best integration with victorwz.com, but needs database migration

**Trade-off**: Need to migrate from SQLite to Cloudflare D1

See `CLOUDFLARE-SETUP.md` for detailed steps.

#### Option C: Fly.io

1. Install flyctl: `irm https://fly.io/install.ps1 | iex`
2. Run: `fly launch`
3. Deploy: `fly deploy`

---

## 🌐 Custom Domain Setup

### For victorwz.com/canada-citizenship-test-practice

**Option 1: Subdomain (Simpler)**
```
URL: https://canada-citizenship-test.victorwz.com
```

In Cloudflare DNS:
- Type: CNAME
- Name: canada-citizenship-test
- Target: your-deployment.railway.app (or fly.io url)

**Option 2: Path-based (Advanced)**
```
URL: https://victorwz.com/canada-citizenship-test-practice
```

Requires Cloudflare Worker for routing:
```javascript
// Route /canada-citizenship-test-practice/* to your deployment
export default {
  async fetch(request) {
    const url = new URL(request.url);
    if (url.pathname.startsWith('/canada-citizenship-test-practice')) {
      return fetch('https://your-app.railway.app' + url.pathname);
    }
  }
};
```

---

## 🔄 Automated Deployment

GitHub Actions workflow is already configured!

**File**: `.github/workflows/deploy.yml`

**Setup**:
1. Go to GitHub repo → Settings → Secrets
2. Add these secrets:
   - `CLOUDFLARE_API_TOKEN` (if using Cloudflare Pages)
   - `CLOUDFLARE_ACCOUNT_ID` (if using Cloudflare Pages)

**How it works**:
- Push to `main` branch → Automatically deploys
- No manual steps needed

---

## 📊 Deployment Comparison

| Platform | Ease | Docker Support | Custom Domain | Free Tier | Best For |
|----------|------|----------------|---------------|-----------|----------|
| **Railway** | ⭐⭐⭐⭐⭐ | ✅ Yes | ✅ Yes | ⚠️ $5/month | Your use case |
| **Fly.io** | ⭐⭐⭐⭐ | ✅ Yes | ✅ Yes | ✅ Yes (limited) | Production apps |
| **Cloudflare Pages** | ⭐⭐⭐ | ❌ No | ✅ Yes | ✅ Yes | Static/JAMstack |
| **Vercel** | ⭐⭐⭐⭐⭐ | ❌ No | ✅ Yes | ✅ Yes | Next.js apps* |

\* Vercel doesn't support SQLite in serverless environment

---

## 🎯 My Recommendation for You

1. **Push to GitHub** (using the running script)
2. **Deploy to Railway**:
   - Easiest setup (2 clicks)
   - Works with your Docker image as-is
   - Good for small apps (~$5/month)
   - Simple custom domain setup

3. **Add Custom Domain**:
   - Use subdomain: `canada-citizenship-test.victorwz.com`
   - Or set up Cloudflare Worker for path routing

Total time: ~15 minutes

---

## 📝 Commands Reference

```powershell
# Check git status
git status

# View commit history
git log --oneline

# Push to GitHub (manual)
git push -u origin main

# Build Docker image
.\build-docker-with-db.ps1

# Run Docker container locally
docker run -d -p 3000:3000 citizenship-test-webapp:latest

# Stop container
docker stop citizenship-test-webapp
```

---

## 🆘 Troubleshooting

**"Repository not found" when pushing**:
- Make sure you created the GitHub repository first
- Repository name must be exactly: `canada-citizenship-test`

**"Authentication failed"**:
- GitHub might ask for credentials
- Use Personal Access Token instead of password
- Create token at: https://github.com/settings/tokens

**"Database not found" in deployment**:
- Ensure database is committed: `git ls-files data/questions.db`
- Dockerfile correctly copies database - verified ✅

**Domain not working**:
- DNS changes take 5-60 minutes to propagate
- Check CNAME record is correct
- Try `nslookup your-domain.victorwz.com`

---

## 🎉 Success Checklist

- [ ] GitHub repository created
- [ ] Code pushed to GitHub
- [ ] Deployment platform chosen
- [ ] App deployed successfully
- [ ] Custom domain configured
- [ ] DNS propagated
- [ ] App accessible at victorwz.com/*

---

Need help? Check:
- `CLOUDFLARE-SETUP.md` - Detailed Cloudflare guide
- `DEPLOYMENT.md` - General deployment info
- `DOCKER.md` - Docker documentation
