# Cloudflare D1 Migration Complete! 🎉

## ✅ What's Done

1. **D1 Database Created**: `citizenship-test-db` with 652 questions imported
2. **Next.js App Updated**: Now uses D1 instead of SQLite file
3. **GitHub Actions**: Automated deployment workflow created
4. **Domain Ready**: Can be deployed to `victorwz.com/canada-citizenship-test-practice`

## 🚀 Deployment Options

### Option 1: Deploy via GitHub Actions (Recommended)

#### Step 1: Get Cloudflare Credentials

1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com)
2. Get your **Account ID**:
   - Click on "Workers & Pages"
   - Copy your Account ID from the right sidebar
3. Create an **API Token**:
   - Go to "My Profile" → "API Tokens"
   - Click "Create Token"
   - Use template: "Edit Cloudflare Workers"
   - Add permissions: "Cloudflare Pages - Edit"
   - Create token and copy it

#### Step 2: Add Secrets to GitHub

1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions
3. Add two secrets:
   - `CLOUDFLARE_API_TOKEN`: Your API token from step 1
   - `CLOUDFLARE_ACCOUNT_ID`: Your account ID from step 1

#### Step 3: Commit and Push

```powershell
git add .
git commit -m "Migrate to Cloudflare D1"
git push
```

The GitHub Action will:
- Build the Next.js app
- Convert it for Cloudflare Pages
- Deploy automatically to Cloudflare
- Your app will be live at: `https://canada-citizenship-test.pages.dev`

### Option 2: Deploy Manually via Cloudflare Dashboard

1. **Build for Cloudflare** (requires Linux/WSL):
   ```bash
   cd webapp
   npm install
   npm run build
   npx @cloudflare/next-on-pages
   ```

2. **Deploy via Wrangler**:
   ```bash
   wrangler pages deploy .vercel/output/static --project-name=canada-citizenship-test
   ```

3. **Or use Cloudflare Dashboard**:
   - Go to Workers & Pages → Create application → Pages
   - Connect your GitHub repository
   - Configure build:
     - Framework: Next.js
     - Build command: `cd webapp && npm install && npm run build && npx @cloudflare/next-on-pages`
     - Build output directory: `webapp/.vercel/output/static`
     - Root directory: `/`
   - Add environment binding:
     - Variable type: D1 database
     - Variable name: `DB`
     - Database: Select `citizenship-test-db`
   - Deploy!

## 🌐 Custom Domain Setup

Once deployed, configure your custom domain:

### For Subdomain (Easiest): `canada-citizenship-test.victorwz.com`

1. In Cloudflare Pages project → Custom domains
2. Add: `canada-citizenship-test.victorwz.com`
3. DNS record created automatically
4. Done! ✅

### For Path-Based: `victorwz.com/canada-citizenship-test-practice`

Requires a Cloudflare Worker:

1. Create Worker in Cloudflare Dashboard
2. Add this code:
   ```javascript
   export default {
     async fetch(request, env) {
       const url = new URL(request.url);
       
       // Proxy requests to your Pages deployment
       if (url.pathname.startsWith('/canada-citizenship-test-practice')) {
         const newUrl = new URL(request.url);
         newUrl.hostname = 'canada-citizenship-test.pages.dev';
         newUrl.pathname = newUrl.pathname.replace('/canada-citizenship-test-practice', '');
         
         return fetch(newUrl, request);
       }
       
       // Pass through other requests
       return fetch(request);
     }
   };
   ```
3. Add route: `victorwz.com/canada-citizenship-test-practice/*`

## 📊 Database Status

- **Database**: `citizenship-test-db` (d13edbd5-9fdd-4900-bdcb-da763be0a0bc)
- **Questions**: 652 imported successfully
- **Size**: 0.34 MB
- **Location**: Cloudflare D1 (global replicated)

## 🧪 Test Locally (Linux/WSL Required)

```bash
cd webapp
npm install
npm run build
npx @cloudflare/next-on-pages

# Test with wrangler
npx wrangler pages dev .vercel/output/static --d1 DB=citizenship-test-db
```

## 💰 Cost

**Everything is FREE! 🎉**
- D1 Database: Free tier (5GB storage, 5M reads/day)
- Cloudflare Pages: Free tier (500 builds/month, unlimited requests)
- Custom domain: Already owned (victorwz.com)

## 📝 Changes Made

### Files Modified:
- `webapp/package.json`: Updated dependencies and scripts
- `webapp/lib/database-d1.ts`: D1 database utility (already existed)
- `webapp/app/api/questions/route.ts`: Updated to use D1
- `webapp/app/api/submit/route.ts`: Updated to use D1
- `webapp/next.config.js`: Removed standalone output
- `webapp/wrangler.toml`: Added D1 binding
- `wrangler.toml`: Root config for D1
- `.github/workflows/cloudflare-deploy.yml`: GitHub Actions deployment

### Files Created:
- `migrations/schema.sql`: Database schema
- `migrations/data.sql`: 652 questions data
- `webapp/env.d.ts`: TypeScript types for Cloudflare

## ⚠️ Important Notes

1. **Windows Limitation**: The build process (`@cloudflare/next-on-pages`) works best on Linux/macOS. That's why we use GitHub Actions (Ubuntu) for deployment.

2. **Edge Runtime**: API routes now use `export const runtime = 'edge'` for Cloudflare compatibility.

3. **No Local Development Changes**: Your local Docker setup still works as before. The D1 migration only affects Cloudflare deployment.

## 🎯 Next Steps

1. Add GitHub secrets (CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID)
2. Push code to GitHub
3. Watch GitHub Actions deploy automatically
4. Configure custom domain
5. Test your live app!

## 🆘 Need Help?

- Cloudflare Pages docs: https://developers.cloudflare.com/pages
- D1 Database docs: https://developers.cloudflare.com/d1
- Next.js on Cloudflare: https://developers.cloudflare.com/pages/framework-guides/nextjs

---

**Status**: ✅ Ready to deploy!
