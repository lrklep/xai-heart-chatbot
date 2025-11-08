# 🚀 Deployment Guide - FastAPI on Render + Streamlit Cloud

## Part 1: Deploy FastAPI Backend to Render

### Step 1: Create Render Account
1. Go to **https://render.com/**
2. Sign up or log in (use GitHub for easy connection)

### Step 2: Create New Web Service
1. Click **"New +"** button in top right
2. Select **"Web Service"**
3. Connect your GitHub repository: **lrklep/xai-heart-chatbot**

### Step 3: Configure Service
Fill in these settings:

- **Name:** `xai-heart-api` (or your choice)
- **Region:** `Oregon (US West)` (free tier available)
- **Branch:** `master`
- **Root Directory:** Leave blank
- **Runtime:** `Python 3`
- **Build Command:** `pip install -r requirements-api.txt`
- **Start Command:** `uvicorn api.api:app --host 0.0.0.0 --port $PORT`
- **Instance Type:** `Free`

### Step 4: Environment Variables
Add this environment variable:
- **Key:** `PYTHON_VERSION`
- **Value:** `3.11.10`

### Step 5: Deploy
1. Click **"Create Web Service"**
2. Wait 3-5 minutes for deployment
3. Once deployed, you'll see a URL like: `https://xai-heart-api.onrender.com`
4. **Copy this URL** - you'll need it for Streamlit!

### Step 6: Test API
Visit: `https://your-render-url.onrender.com/docs`
You should see the FastAPI documentation!

---

## Part 2: Update Streamlit Cloud Configuration

### Step 1: Go to Streamlit Cloud Dashboard
1. Go to **https://share.streamlit.io/**
2. Find your deployed app
3. Click **Settings** (⚙️ icon)

### Step 2: Add Environment Variable
1. Go to **"Secrets"** or **"Advanced settings"**
2. Add environment variable:

```toml
API_URL = "https://your-render-url.onrender.com"
```

Replace `your-render-url` with your actual Render URL (from Step 5 above)

### Step 3: Reboot App
1. Click **"Reboot app"** button
2. Wait for restart (30 seconds)
3. Your app should now connect to the Render API! 🎉

---

## 🔍 Verification Steps

### Check API (Render):
- ✅ Visit: `https://your-render-url.onrender.com/health`
- Should return: `{"status": "healthy"}`

### Check Streamlit:
- ✅ Visit your Streamlit app URL
- ✅ Should NOT show "Cannot connect to API" error
- ✅ Try making a prediction - should work!

---

## 📋 Important Notes

### Render Free Tier:
- ⚠️ **Sleeps after 15 minutes of inactivity**
- ⚠️ **First request after sleep takes 30-60 seconds** (cold start)
- ✅ Unlimited deployments
- ✅ 750 hours/month free

### Keeping API Awake (Optional):
If you want to prevent cold starts, you can:
1. Use a service like **UptimeRobot** (free) to ping your API every 5 minutes
2. Upgrade to Render paid plan ($7/month)

---

## 🆘 Troubleshooting

### "Application failed to start"
- Check logs in Render dashboard
- Verify `requirements-api.txt` installed successfully
- Make sure Python 3.11.10 is set in environment variables

### "Cannot connect to API" in Streamlit
- Verify API_URL environment variable is set correctly in Streamlit
- Check that Render URL is HTTPS (not HTTP)
- Make sure Render service is running (not sleeping)

### "Model file not found"
- Ensure `models/` folder is committed to git
- Check that `.gitignore` doesn't exclude model files
- Verify files exist in GitHub repository

---

## 🎯 Expected URLs

After deployment, you'll have:

1. **API Backend (Render):**
   - `https://xai-heart-api.onrender.com`
   - API Docs: `https://xai-heart-api.onrender.com/docs`
   - Health Check: `https://xai-heart-api.onrender.com/health`

2. **Frontend (Streamlit Cloud):**
   - `https://[your-app-name].streamlit.app`

---

## ✅ Success Checklist

- [ ] Render account created
- [ ] GitHub repo connected to Render
- [ ] Web service created with correct settings
- [ ] PYTHON_VERSION environment variable set
- [ ] Deployment successful (green checkmark)
- [ ] API URL copied from Render
- [ ] API_URL added to Streamlit Cloud secrets
- [ ] Streamlit app rebooted
- [ ] Both services are working together!

---

## 🚀 Next Steps After Deployment

1. **Test thoroughly** - Try all features
2. **Monitor logs** - Check Render and Streamlit dashboards
3. **Share your app** - Get the Streamlit Cloud URL
4. **Optional:** Set up custom domain

---

**Need help?** Check the logs in:
- Render: Dashboard → Logs tab
- Streamlit: App → Manage app → Logs
