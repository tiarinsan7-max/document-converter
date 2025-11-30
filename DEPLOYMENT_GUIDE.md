# 🚀 Deployment Guide - Universal Document Converter

**Deploy your app in 3 easy ways!**

---

## 📋 Quick Overview

| Method | Time | Cost | Difficulty | Best For |
|--------|------|------|------------|----------|
| **Streamlit Cloud** | 10 min | FREE | ⭐ Easy | Production |
| **Local Network** | 2 min | FREE | ⭐ Easiest | Home/Office |
| **Ngrok** | 5 min | FREE* | ⭐⭐ Easy | Testing/Sharing |

---

## 🎯 RECOMMENDED: Streamlit Cloud (FREE & Easy!)

**Best choice for most users - completely free and professional!**

### Why Streamlit Cloud?

- ✅ **100% FREE** - No credit card needed
- ✅ **Easy Setup** - Deploy in 10 minutes
- ✅ **Professional URL** - `your-app.streamlit.app`
- ✅ **Always Online** - 24/7 availability
- ✅ **HTTPS Included** - Secure by default
- ✅ **Auto Updates** - Push to GitHub = auto deploy

---

## 📦 Method 1: Streamlit Cloud Deployment

### Step 1: Prepare Your Code

Your code is already ready! But let's make sure:

```bash
cd /root/Cline

# Check if you have a git repository
git status

# If not initialized, run:
git init
git add .
git commit -m "Initial commit - Document Converter v1.1.0"
```

### Step 2: Create GitHub Repository

**Option A: Using GitHub Website**

1. Go to https://github.com/
2. Click **"New repository"** (green button)
3. Name it: `document-converter` (or any name)
4. Keep it **Public** (required for free Streamlit Cloud)
5. **Don't** initialize with README (you already have files)
6. Click **"Create repository"**

**Option B: Using GitHub CLI** (if installed)

```bash
gh repo create document-converter --public --source=. --remote=origin
```

### Step 3: Push Your Code to GitHub

```bash
# Add GitHub as remote (replace with YOUR username and repo name)
git remote add origin https://github.com/YOUR_USERNAME/document-converter.git

# Push your code
git branch -M main
git push -u origin main
```

**Example:**
```bash
git remote add origin https://github.com/john/document-converter.git
git branch -M main
git push -u origin main
```

### Step 4: Deploy to Streamlit Cloud

1. **Go to:** https://share.streamlit.io/
2. **Sign in** with your GitHub account
3. Click **"New app"** button
4. **Fill in the form:**
   - **Repository:** Select `YOUR_USERNAME/document-converter`
   - **Branch:** `main`
   - **Main file path:** `streamlit_app/app.py`
5. Click **"Deploy!"**

### Step 5: Wait for Deployment

- Streamlit will install dependencies (2-3 minutes)
- You'll see a build log
- When done, your app will be live!

### Step 6: Access Your App

Your app will be available at:
```
https://YOUR_USERNAME-document-converter.streamlit.app
```

**Share this URL with anyone!** 🎉

---

## 🔄 Updating Your Deployed App

Whenever you make changes:

```bash
# Make your changes to the code
# Then commit and push:
git add .
git commit -m "Updated features"
git push

# Streamlit Cloud will automatically redeploy!
```

---

## 🏠 Method 2: Local Network Access

**Best for:** Using at home/office on multiple devices

### Quick Start

```bash
cd /root/Cline
./start_network.sh
```

This script will:
1. Show your server's IP address
2. Open firewall port 8501
3. Start the app
4. Display the access URL

### Manual Method

```bash
# Step 1: Get your IP address
hostname -I | awk '{print $1}'
# Example output: 192.168.1.100

# Step 2: Start Streamlit
cd /root/Cline
source venv/bin/activate
streamlit run streamlit_app/app.py --server.address 0.0.0.0 --server.port 8501

# Step 3: Open firewall (if needed)
sudo firewall-cmd --permanent --add-port=8501/tcp
sudo firewall-cmd --reload
```

### Access from Other Devices

On any device on the **same WiFi network**:

1. Open browser
2. Go to: `http://YOUR_IP:8501`
3. Example: `http://192.168.1.100:8501`

---

## 🌍 Method 3: Internet Access with Ngrok

**Best for:** Temporary sharing, demos, testing

### Step 1: Install Ngrok

```bash
# Download ngrok
cd ~
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz

# For ARM64 (Raspberry Pi, etc.)
# wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm64.tgz

# Extract
tar xvzf ngrok-v3-stable-linux-*.tgz

# Move to system path
sudo mv ngrok /usr/local/bin/

# Verify
ngrok version
```

### Step 2: Get Ngrok Auth Token

1. Go to https://ngrok.com/
2. Sign up (free account)
3. Go to dashboard: https://dashboard.ngrok.com/
4. Copy your **Authtoken**

### Step 3: Configure Ngrok

```bash
ngrok config add-authtoken YOUR_AUTH_TOKEN_HERE
```

### Step 4: Start Your App

**Terminal 1:**
```bash
cd /root/Cline
source venv/bin/activate
streamlit run streamlit_app/app.py
```

**Terminal 2:**
```bash
ngrok http 8501
```

### Step 5: Share the URL

Ngrok will display:
```
Forwarding  https://abc123.ngrok.io -> http://localhost:8501
```

**Share the `https://abc123.ngrok.io` URL** with anyone!

### Ngrok Features

- ✅ Works from anywhere in the world
- ✅ HTTPS automatically enabled
- ✅ Free tier available
- ⚠️ URL changes each restart (unless paid plan)
- ⚠️ Session timeout on free tier

---

## 🐳 Method 4: Docker Deployment (Advanced)

### Create Dockerfile

```bash
cat > Dockerfile << 'EOF'
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run app
CMD ["streamlit", "run", "streamlit_app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
EOF
```

### Build and Run

```bash
# Build image
docker build -t document-converter .

# Run container
docker run -p 8501:8501 document-converter
```

### Docker Compose

```bash
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./uploads:/app/uploads
      - ./outputs:/app/outputs
    restart: unless-stopped
EOF

# Run with docker-compose
docker-compose up -d
```

---

## ☁️ Method 5: Cloud Platforms

### Heroku

```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login

# Create app
heroku create your-app-name

# Create Procfile
echo "web: streamlit run streamlit_app/app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile

# Deploy
git push heroku main
```

### Railway.app

1. Go to https://railway.app/
2. Sign in with GitHub
3. Click "New Project"
4. Select your repository
5. Railway auto-detects and deploys!

### Render.com

1. Go to https://render.com/
2. Sign in with GitHub
3. Click "New Web Service"
4. Select your repository
5. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run streamlit_app/app.py --server.port=$PORT --server.address=0.0.0.0`

---

## 📊 Deployment Comparison

### Streamlit Cloud
- ✅ **FREE**
- ✅ Easiest setup
- ✅ Auto-deploy from GitHub
- ✅ Professional URL
- ⚠️ Must be public repo (free tier)

### Local Network
- ✅ **FREE**
- ✅ Fastest performance
- ✅ Full control
- ⚠️ Only on same network
- ⚠️ Server must stay on

### Ngrok
- ✅ Quick setup
- ✅ Works anywhere
- ✅ HTTPS included
- ⚠️ URL changes (free tier)
- ⚠️ Session limits (free tier)

### Docker
- ✅ Portable
- ✅ Consistent environment
- ✅ Easy scaling
- ⚠️ Requires Docker knowledge
- ⚠️ More complex setup

### Cloud Platforms
- ✅ Professional hosting
- ✅ Scalable
- ✅ Custom domains
- ⚠️ May have costs
- ⚠️ More configuration

---

## 🎯 Recommended Deployment Path

### For Most Users:

**1. Start with Streamlit Cloud** (FREE & Easy)
- Perfect for production
- Professional URL
- Always online
- No maintenance

**2. Use Local Network for Testing**
- Quick testing
- Fast performance
- No external dependencies

**3. Use Ngrok for Demos**
- Share with clients
- Temporary access
- Quick setup

---

## 🔒 Security Checklist

Before deploying publicly:

- [ ] File size limits enabled (✅ Already done - 100MB)
- [ ] Error handling in place (✅ Already done)
- [ ] Temp file cleanup (✅ Already done)
- [ ] Consider adding authentication (optional)
- [ ] Use HTTPS (✅ Automatic with Streamlit Cloud/Ngrok)
- [ ] Monitor usage
- [ ] Set up backups

---

## 📱 Mobile Access

Once deployed, access from mobile:

### iPhone/iPad:
1. Open Safari
2. Go to your app URL
3. Tap Share → Add to Home Screen

### Android:
1. Open Chrome
2. Go to your app URL
3. Menu → Add to Home screen

---

## 🔧 Troubleshooting

### Streamlit Cloud Issues

**Build fails:**
```bash
# Check requirements.txt is complete
# Make sure all imports are listed
# Verify Python version compatibility
```

**App crashes:**
```bash
# Check logs in Streamlit Cloud dashboard
# Verify file paths are correct
# Check for missing dependencies
```

### Local Network Issues

**Can't access from other devices:**
```bash
# Check firewall
sudo firewall-cmd --list-ports

# Verify app is running
ps aux | grep streamlit

# Check IP address
hostname -I
```

### Ngrok Issues

**Tunnel not starting:**
```bash
# Verify auth token
ngrok config check

# Make sure Streamlit is running first
# Try different port
ngrok http 8502
```

---

## 📚 Additional Resources

### Documentation
- Streamlit Cloud: https://docs.streamlit.io/streamlit-community-cloud
- Ngrok: https://ngrok.com/docs
- Docker: https://docs.docker.com/

### Your Project Files
- `HOSTING_GUIDE.md` - Detailed hosting guide
- `start_network.sh` - Quick network startup script
- `requirements.txt` - All dependencies

---

## ✅ Quick Start Commands

### Deploy to Streamlit Cloud (Recommended)

```bash
# 1. Push to GitHub
git init
git add .
git commit -m "Deploy app"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main

# 2. Go to https://share.streamlit.io/
# 3. Deploy!
```

### Run on Local Network

```bash
cd /root/Cline
./start_network.sh
```

### Run with Ngrok

```bash
# Terminal 1
cd /root/Cline
source venv/bin/activate
streamlit run streamlit_app/app.py

# Terminal 2
ngrok http 8501
```

---

## 🎉 Success!

Once deployed, your app will be accessible:

- **Streamlit Cloud:** `https://your-app.streamlit.app`
- **Local Network:** `http://YOUR_IP:8501`
- **Ngrok:** `https://random.ngrok.io`

**Share the URL and enjoy!** 🚀

---

## 💡 Pro Tips

1. **Start with Streamlit Cloud** - It's free and easiest
2. **Use Local Network for testing** - Fast and simple
3. **Keep your repo updated** - Auto-deploys to Streamlit Cloud
4. **Monitor your app** - Check Streamlit Cloud analytics
5. **Add to mobile home screen** - App-like experience

---

**Need help? Check the troubleshooting section or ask for assistance!**
