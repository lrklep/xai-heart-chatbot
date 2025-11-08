# 🚀 GitHub Repository Setup - Quick Guide

## ✅ What We've Done So Far

Your code has been committed to git locally with 9 organized commits:

1. ✅ Initial commit: Configuration files
2. ✅ Add data/heart.csv
3. ✅ Add model training script
4. ✅ Add trained model artifacts
5. ✅ Add FastAPI backend
6. ✅ Added Streamlit interface
7. ✅ Extra pages (Research Summary, Black Box Comparison)
8. ✅ Documentation files
9. ✅ Tests

---

## 📝 Next Steps: Push to GitHub

### Step 1: Create GitHub Repository

1. **Go to:** https://github.com/new

2. **Repository Settings:**
   - **Name:** `xai-heart-disease-chatbot` (or your choice)
   - **Description:** `Heart Disease Risk Assessment System with Explainable AI (SHAP & LIME)`
   - **Visibility:** Public or Private
   - ⚠️ **IMPORTANT:** 
     - ❌ DO NOT check "Add a README file"
     - ❌ DO NOT add .gitignore
     - ❌ DO NOT add license
   - Click **"Create repository"**

### Step 2: Connect and Push

After creating the repo on GitHub, run these commands in PowerShell:

```powershell
# Add the remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/xai-heart-disease-chatbot.git

# Rename branch to main (GitHub's default)
git branch -M main

# Push all commits to GitHub
git push -u origin main
```

**Example (if your username is "abhay123"):**
```powershell
git remote add origin https://github.com/abhay123/xai-heart-disease-chatbot.git
git branch -M main
git push -u origin main
```

### Step 3: Verify

Go to your GitHub repository URL and you should see all your files!

---

## 🔐 Authentication

When you push, GitHub will ask for authentication. You have two options:

### Option A: Personal Access Token (Recommended)
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo` (full control)
4. Generate and copy the token
5. Use the token as your password when prompted

### Option B: GitHub CLI
```powershell
# Install GitHub CLI if not already installed
winget install GitHub.cli

# Authenticate
gh auth login

# Then push normally
git push -u origin main
```

---

## 📊 What Will Be Pushed

Your repository will contain:

```
xai-heart-disease-chatbot/
├── .gitignore
├── README.md
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── api/
│   └── api.py
├── app/
│   ├── streamlit_app.py
│   └── pages/
│       ├── 1_Research_Summary.py
│       └── 2_Black_Box_Comparison.py
├── data/
│   └── heart.csv
├── docs/
│   ├── ARCHITECTURE.md
│   ├── IMPROVEMENTS.md
│   ├── QUICK_REFERENCE.md
│   ├── USER_GUIDE.md
│   └── slides.md
├── models/
│   ├── features.json
│   ├── metrics.json
│   ├── model.joblib
│   ├── preproc.joblib
│   └── shap_explainer.joblib
├── tests/
│   └── smoke_test.py
└── train/
    └── train.py
```

---

## 🎯 Quick Commands Reference

```powershell
# Check current status
git status

# View commit history
git log --oneline

# Add remote (replace with your URL)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Check remotes
git remote -v

# Push to GitHub
git push -u origin main

# Future pushes (after first push)
git push
```

---

## 🆘 Troubleshooting

### "Remote already exists"
```powershell
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
```

### "Authentication failed"
- Use Personal Access Token instead of password
- Or use GitHub CLI: `gh auth login`

### "Branch main does not exist"
```powershell
git branch -M main
```

### "Large files warning"
- Model files are included (normal for ML projects)
- If too large (>100MB), consider using Git LFS:
```powershell
git lfs install
git lfs track "*.joblib"
```

---

## ✅ After Pushing Successfully

1. **Visit your repo:** https://github.com/YOUR_USERNAME/xai-heart-disease-chatbot
2. **Add topics:** Click gear icon → Add topics: `machine-learning`, `explainable-ai`, `streamlit`, `shap`, `lime`, `healthcare`
3. **Edit description** on GitHub
4. **Add GitHub badges** to README (optional)

---

## 🎉 You're Done!

Your code is now:
- ✅ Organized in clean commits
- ✅ Ready to push to GitHub
- ✅ Properly documented
- ✅ Version controlled

Just follow Step 1 and Step 2 above to complete the push!

---

**Need help?** Run these commands to see where you are:
```powershell
git status
git remote -v
git branch
```
