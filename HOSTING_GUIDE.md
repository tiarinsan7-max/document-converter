# 🌐 Hosting Guide - Universal Document Converter

**Make your app accessible from any device!**

---

## 📋 Table of Contents

1. [Local Network Access](#local-network-access) - Access from devices on same WiFi
2. [Internet Access (Ngrok)](#internet-access-ngrok) - Access from anywhere
3. [Cloud Hosting](#cloud-hosting) - Permanent hosting
4. [Security Considerations](#security-considerations)

---

## 🏠 Option 1: Local Network Access (Easiest)

**Best for:** Accessing from devices on the same WiFi network (home/office)

### Step 1: Find Your Server's IP Address

```bash
# Get your IP address
hostname -I | awk '{print $1}'
# or
ip addr show | grep "inet " | grep -v 127.0.0.1
```

**Example output:** `192.168.1.100`

### Step 2: Start Streamlit with Network Access

```bash
cd /root/Cline
source venv/bin/activate
streamlit run streamlit_app/app.py --server.address 0.0.0.0 --server.port 8501
```

### Step 3: Access from Other Devices

On any device on the same network, open a browser and go to:

```
http://YOUR_SERVER_IP:8501
```

**Example:** `http://192.168.1.100:8501`

### Troubleshooting Local Network Access

#### Issue: Can't connect from other devices

**Solution 1: Check Firewall**
```bash
# Allow port 8501 through firewall
sudo firewall-cmd --permanent --add-port=8501/tcp
sudo firewall-cmd --reload

# Or for UFW
sudo ufw allow 8501/tcp
```

**Solution 2: Verify Streamlit is listening on 0.0.0.0**
```bash
# Check if Streamlit is running
netstat -tuln | grep 8501
# Should show: 0.0.0.0:8501
```

**Solution 3: Test connectivity**
```bash
# From another device, ping the server
ping YOUR_SERVER_IP
```

---

## 🌍 Option 2: Internet Access with Ngrok (Quick & Easy)

**Best for:** Temporary access from anywhere, testing, demos

### Step 1: Install Ngrok

```bash
# Download ngrok
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm64.tgz

# Extract
tar xvzf ngrok-v3-stable-linux-arm64.tgz

# Move to /usr/local/bin
sudo mv ngrok /usr/local/bin/

# Verify installation
ngrok version
```

### Step 2: Sign Up for Ngrok (Free)

1. Go to https://ngrok.com/
2. Sign up for a free account
3. Get your auth token from the dashboard

### Step 3: Configure Ngrok

```bash
# Add your auth token
ngrok config add-authtoken YOUR_AUTH_TOKEN
```

### Step 4: Start Streamlit

```bash
# Terminal 1: Start Streamlit
cd /root/Cline
source venv/bin/activate
streamlit run streamlit_app/app.py
```

### Step 5: Start Ngrok Tunnel

```bash
# Terminal 2: Start ngrok
ngrok http 8501
```

### Step 6: Access Your App

Ngrok will display URLs like:
```
Forwarding  https://abc123.ngrok.io -> http://localhost:8501
```

**Share this URL** with anyone! They can access your app from anywhere.

### Ngrok Features

- ✅ Free tier available
- ✅ HTTPS automatically
- ✅ Works from anywhere
- ✅ No firewall configuration needed
- ⚠️ URL changes each time (unless paid plan)
- ⚠️ Session timeout on free tier

---

## ☁️ Option 3: Cloud Hosting (Permanent)

**Best for:** Production use, permanent access, professional deployment

### Option 3A: Streamlit Community Cloud (FREE!)

**Easiest cloud option - completely free!**

#### Step 1: Prepare Your Repository

```bash
# Make sure you have a git repository
cd /root/Cline
git init
git add .
git commit -m "Initial commit"
```

#### Step 2: Push to GitHub

```bash
# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

#### Step 3: Deploy to Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set main file path: `streamlit_app/app.py`
6. Click "Deploy"

**Your app will be live at:** `https://YOUR_APP_NAME.streamlit.app`

#### Requirements for Streamlit Cloud

Create a `requirements.txt` in your repo root (you already have this!):
```
streamlit==1.51.0
PyPDF2==3.0.1
python-docx==1.2.0
openpyxl==3.1.5
pandas==2.3.3
# ... other dependencies
```

---

### Option 3B: Heroku (Free Tier Available)

#### Step 1: Install Heroku CLI

```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login
```

#### Step 2: Create Heroku App

```bash
cd /root/Cline
heroku create your-app-name
```

#### Step 3: Create Procfile

```bash
cat > Procfile << 'EOF'
web: streamlit run streamlit_app/app.py --server.port=$PORT --server.address=0.0.0.0
EOF
```

#### Step 4: Create setup.sh

```bash
cat > setup.sh << 'EOF'
mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
EOF
```

#### Step 5: Deploy

```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

**Your app will be at:** `https://your-app-name.herokuapp.com`

---

### Option 3C: DigitalOcean / AWS / Google Cloud

For more control, deploy on a VPS:

#### Quick Setup Script

```bash
# Install dependencies
sudo apt update
sudo apt install -y python3-pip nginx

# Setup app
cd /root/Cline
source venv/bin/activate
pip install -r requirements.txt

# Create systemd service
sudo cat > /etc/systemd/system/streamlit.service << 'EOF'
[Unit]
Description=Streamlit Document Converter
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/Cline
Environment="PATH=/root/Cline/venv/bin"
ExecStart=/root/Cline/venv/bin/streamlit run streamlit_app/app.py --server.port 8501 --server.address 0.0.0.0

[Install]
WantedBy=multi-user.target
EOF

# Start service
sudo systemctl daemon-reload
sudo systemctl enable streamlit
sudo systemctl start streamlit
```

#### Setup Nginx Reverse Proxy

```bash
sudo cat > /etc/nginx/sites-available/streamlit << 'EOF'
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/streamlit /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🔒 Security Considerations

### For Local Network Access

✅ **Safe** - Only accessible on your local network
⚠️ **Consider:** Password protection if needed

### For Internet Access

⚠️ **Important Security Measures:**

#### 1. Add Authentication

Create `.streamlit/config.toml`:

```toml
[server]
headless = true
port = 8501

[browser]
gatherUsageStats = false

# Add password protection
[server]
enableCORS = false
enableXsrfProtection = true
```

#### 2. Use HTTPS

- Ngrok provides HTTPS automatically
- For cloud hosting, use SSL certificates
- Use Let's Encrypt for free SSL

#### 3. Add Rate Limiting

Create a simple rate limiter in your app:

```python
import streamlit as st
from datetime import datetime, timedelta

# Add to app.py
if 'last_request' not in st.session_state:
    st.session_state.last_request = {}

def rate_limit(max_requests=10, window_minutes=1):
    now = datetime.now()
    user_ip = st.context.headers.get("X-Forwarded-For", "unknown")
    
    if user_ip in st.session_state.last_request:
        requests = st.session_state.last_request[user_ip]
        recent = [r for r in requests if now - r < timedelta(minutes=window_minutes)]
        
        if len(recent) >= max_requests:
            st.error("Too many requests. Please wait.")
            st.stop()
        
        st.session_state.last_request[user_ip] = recent + [now]
    else:
        st.session_state.last_request[user_ip] = [now]
```

#### 4. File Size Limits

Already implemented! (100MB max)

#### 5. Virus Scanning (Optional)

```bash
# Install ClamAV
sudo apt install clamav clamav-daemon

# Update virus definitions
sudo freshclam

# Scan uploaded files
clamscan --infected --remove uploaded_file
```

---

## 🚀 Quick Start Commands

### Local Network (Recommended for Home Use)

```bash
# Get your IP
hostname -I | awk '{print $1}'

# Start app
cd /root/Cline
source venv/bin/activate
streamlit run streamlit_app/app.py --server.address 0.0.0.0 --server.port 8501

# Access from other devices:
# http://YOUR_IP:8501
```

### Internet Access with Ngrok (Recommended for Testing)

```bash
# Terminal 1: Start Streamlit
cd /root/Cline
source venv/bin/activate
streamlit run streamlit_app/app.py

# Terminal 2: Start Ngrok
ngrok http 8501

# Share the ngrok URL!
```

### Streamlit Cloud (Recommended for Production)

```bash
# Push to GitHub
git init
git add .
git commit -m "Deploy app"
git remote add origin YOUR_GITHUB_REPO
git push -u origin main

# Then deploy at: https://share.streamlit.io/
```

---

## 📱 Access from Mobile Devices

Once hosted, access from:

- **iPhone/iPad:** Open Safari, go to your URL
- **Android:** Open Chrome, go to your URL
- **Tablet:** Any browser, go to your URL

**Tip:** Add to home screen for app-like experience!

---

## 🔧 Troubleshooting

### Can't access from other devices

1. **Check firewall:**
   ```bash
   sudo firewall-cmd --list-ports
   ```

2. **Verify Streamlit is running:**
   ```bash
   ps aux | grep streamlit
   ```

3. **Check port is open:**
   ```bash
   netstat -tuln | grep 8501
   ```

4. **Test from server itself:**
   ```bash
   curl http://localhost:8501
   ```

### Ngrok not working

1. **Check auth token:**
   ```bash
   ngrok config check
   ```

2. **Verify Streamlit is running first**

3. **Try different port:**
   ```bash
   ngrok http 8502
   ```

### Cloud deployment fails

1. **Check requirements.txt** is complete
2. **Verify Python version** compatibility
3. **Check logs** in cloud platform
4. **Ensure all dependencies** are listed

---

## 💡 Recommendations

### For Personal Use (Home/Office)
✅ **Use Local Network Access**
- Simple setup
- Fast performance
- No external dependencies
- Free

### For Sharing/Testing
✅ **Use Ngrok**
- Quick setup
- Works from anywhere
- Free tier available
- HTTPS included

### For Production
✅ **Use Streamlit Cloud**
- Free hosting
- Easy deployment
- Automatic HTTPS
- GitHub integration

---

## 📊 Comparison

| Method | Setup Time | Cost | Access | Best For |
|--------|-----------|------|--------|----------|
| Local Network | 2 min | Free | Same WiFi | Home use |
| Ngrok | 5 min | Free* | Anywhere | Testing |
| Streamlit Cloud | 10 min | Free | Anywhere | Production |
| Heroku | 15 min | Free* | Anywhere | Production |
| VPS | 30 min | $5-20/mo | Anywhere | Full control |

*Free tier with limitations

---

## ✅ Next Steps

1. **Choose your hosting method** based on your needs
2. **Follow the setup instructions** for that method
3. **Test access** from another device
4. **Share the URL** with users
5. **Monitor usage** and performance

---

**Need help? Check the troubleshooting section or ask for assistance!**
