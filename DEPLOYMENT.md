# 🚂 Deployment Guide - Railway + Supabase

This guide will walk you through deploying Hello Super to Railway.

## 📋 Pre-Deployment Checklist

Before deploying, ensure you have:

- [x] ✅ All code is complete and tested
- [x] ✅ Supabase project created and configured
- [x] ✅ Database schema run (`scripts/setup_supabase.sql`)
- [x] ✅ Storage bucket created (`task-attachments`)
- [x] ✅ Environment variables ready

## 🚀 Step-by-Step Deployment

### Step 1: Prepare Your Code

1. **Ensure `.env` is in `.gitignore`** (already done ✅)
2. **Review files to commit**:
   ```bash
   git status
   ```
3. **Stage all files**:
   ```bash
   git add .
   ```
4. **Create initial commit**:
   ```bash
   git commit -m "Initial commit: Hello Super demo app"
   ```

### Step 2: Push to GitHub

1. **Create a new repository on GitHub**:
   - Go to https://github.com/new
   - Name it `hello-super` (or your preferred name)
   - Don't initialize with README, .gitignore, or license
   - Click "Create repository"

2. **Add remote and push**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/hello-super.git
   git branch -M main
   git push -u origin main
   ```

   Replace `YOUR_USERNAME` with your GitHub username.

### Step 3: Deploy to Railway

1. **Sign up/Login to Railway**:
   - Go to https://railway.app
   - Sign up with your GitHub account

2. **Create New Project**:
   - Click **"New Project"**
   - Select **"Deploy from GitHub repo"**
   - Authorize Railway to access your GitHub if prompted
   - Select the `hello-super` repository

3. **Railway will auto-detect**:
   - ✅ Python project
   - ✅ Uses `pyproject.toml`
   - ✅ Uses `Procfile` for start command

### Step 4: Configure Environment Variables

In Railway dashboard:

1. Go to your project → **Variables** tab
2. Add these environment variables:

   | Variable | Value | Notes |
   |----------|-------|-------|
   | `SUPABASE_URL` | `https://your-project.supabase.co` | From Supabase Dashboard |
   | `SUPABASE_KEY` | `your-anon-key` | From Supabase Dashboard |
   | `SUPABASE_SERVICE_KEY` | `your-service-role-key` | ⚠️ Keep secret! |
   | `SECRET_KEY` | `generate-new-one` | Generate with: `python3 -c "import secrets; print(secrets.token_hex(32))"` |
   | `DEBUG` | `false` | Production setting |

   **Important**: Generate a NEW `SECRET_KEY` for production (don't use your dev one!)

3. Click **"Deploy"** or Railway will auto-deploy

### Step 5: Wait for Deployment

- Railway will:
  1. Install dependencies (takes ~2-3 minutes)
  2. Build your application
  3. Start the server using the `Procfile`

- Watch the **Deployments** tab for progress
- Check **Logs** if there are any errors

### Step 6: Get Your Public URL

1. Once deployed, click **"Generate Domain"**
2. Railway will create a URL like: `https://hello-super-production.up.railway.app`
3. Copy this URL

### Step 7: Verify Deployment

1. **Health Check**:
   ```
   https://your-url.up.railway.app/health
   ```
   Should return: `{"status": "healthy", "version": "0.1.0"}`

2. **Visit Your App**:
   ```
   https://your-url.up.railway.app
   ```

3. **Test Features**:
   - ✅ Landing page loads
   - ✅ Can register/login
   - ✅ Can create tasks
   - ✅ Can upload files
   - ✅ Real-time updates work

## 🔧 Troubleshooting

### Build Fails

**Error**: "No module named 'uvicorn'"
- **Solution**: Railway should auto-detect Python. Check that `pyproject.toml` has all dependencies.

**Error**: "Port already in use"
- **Solution**: Railway sets `$PORT` automatically. The `Procfile` should use `$PORT`.

### App Crashes on Startup

**Error**: "SUPABASE_URL not found"
- **Solution**: Check all environment variables are set in Railway dashboard.

**Error**: "Database connection failed"
- **Solution**: Verify `SUPABASE_URL` and `SUPABASE_KEY` are correct.

### RLS Policy Errors

**Error**: "Row-level security policy violation"
- **Solution**: Ensure `SUPABASE_SERVICE_KEY` is set (not just `SUPABASE_KEY`).

## 📊 Monitoring

### View Logs

1. Go to Railway dashboard → Your project
2. Click **"Deployments"** → Select a deployment
3. Click **"View Logs"**

### Metrics

Railway provides:
- CPU usage
- Memory usage
- Network traffic
- Request count

## 🔄 Updating Your App

1. **Make changes locally**
2. **Commit and push**:
   ```bash
   git add .
   git commit -m "Your update message"
   git push
   ```
3. **Railway auto-deploys** on push to main branch

## 💰 Cost Estimate

| Service | Free Tier | Paid Tier |
|---------|-----------|-----------|
| **Railway** | $5 credits/month | $20/month + usage |
| **Supabase** | 500MB DB, 1GB storage | $25/month Pro |
| **Total** | **$0** for small demos | ~$45/month for production |

## 🎯 Next Steps

- [ ] Set up custom domain (optional)
- [ ] Configure CORS if needed
- [ ] Set up monitoring/alerts
- [ ] Enable HTTPS (Railway does this automatically)

## 📚 Resources

- [Railway Documentation](https://docs.railway.app)
- [Supabase Documentation](https://supabase.com/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

---

**Congratulations! Your app is now live! 🎉**

