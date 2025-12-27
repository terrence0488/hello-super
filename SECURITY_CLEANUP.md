# 🔒 Security Cleanup Guide

## ⚠️ IMPORTANT: You've exposed sensitive data

If you pushed a DB password or other secrets to GitHub, follow these steps immediately.

## Step 1: Delete GitHub Repository

1. Go to your GitHub repository: `https://github.com/YOUR_USERNAME/hello-super`
2. Click **Settings** (top right of the repo page)
3. Scroll down to **Danger Zone**
4. Click **Delete this repository**
5. Type the repository name to confirm
6. Click **I understand the consequences, delete this repository**

**Note**: Even after deletion, the data may exist in GitHub's backups for up to 90 days. If this is critical, contact GitHub support.

## Step 2: Rotate Your Credentials

**IMMEDIATELY change these in Supabase:**

1. Go to Supabase Dashboard → **Settings** → **API**
2. **Regenerate** your keys:
   - Service Role Key (most important!)
   - Anon Key (optional, but recommended)
3. Update your local `.env` file with new keys

## Step 3: Clean Local Git History

Run these commands in your terminal:

```bash
cd /Users/terrence/Development/hello-super

# Remove the entire git history
rm -rf .git

# Verify no .env file is present
ls -la | grep .env

# If .env exists, make sure it's not tracked
# (it should already be in .gitignore)
```

## Step 4: Verify .gitignore

Make sure these are in `.gitignore`:

```
.env
.env.local
.env.*.local
*.env
```

## Step 5: Start Fresh

```bash
# Initialize new git repo
git init

# Add all files (except .env which is ignored)
git add .

# Create initial commit
git commit -m "Initial commit - clean start"

# Create new GitHub repo (don't push yet!)
# Go to github.com/new and create a new repository
# Then:
git remote add origin https://github.com/YOUR_USERNAME/hello-super.git
git branch -M main
git push -u origin main
```

## Step 6: Verify Before Pushing

**Before pushing, double-check:**

```bash
# See what will be committed
git status

# Verify .env is NOT listed
git ls-files | grep .env
# Should return nothing!

# If .env shows up, remove it:
git rm --cached .env
```

## 🔐 Best Practices Going Forward

1. **Never commit `.env` files**
2. **Use `.env.example`** for templates (already done ✅)
3. **Rotate keys immediately** if exposed
4. **Use GitHub Secrets** for CI/CD (if you add CI later)
5. **Review commits** before pushing sensitive data

## 🆘 If You Need Help

- GitHub Support: https://support.github.com
- Supabase Support: https://supabase.com/support

---

**Remember**: Even deleted repos can be recovered from backups. Always rotate credentials immediately!

