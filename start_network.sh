#!/bin/bash

# Universal Document Converter - Network Startup Script
# This script starts the Streamlit app accessible from other devices

echo "🚀 Starting Universal Document Converter..."
echo ""

# Get server IP address
SERVER_IP=$(hostname -I | awk '{print $1}')

if [ -z "$SERVER_IP" ]; then
    echo "❌ Could not determine server IP address"
    exit 1
fi

echo "📡 Server IP Address: $SERVER_IP"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if Streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit not installed!"
    echo "Please run: pip install -r requirements.txt"
    exit 1
fi

# Check firewall (optional)
echo "🔒 Checking firewall..."
if command -v firewall-cmd &> /dev/null; then
    if ! sudo firewall-cmd --query-port=8501/tcp &> /dev/null; then
        echo "⚠️  Port 8501 not open in firewall"
        echo "Opening port 8501..."
        sudo firewall-cmd --permanent --add-port=8501/tcp
        sudo firewall-cmd --reload
        echo "✅ Port 8501 opened"
    else
        echo "✅ Port 8501 already open"
    fi
elif command -v ufw &> /dev/null; then
    if ! sudo ufw status | grep -q "8501.*ALLOW" &> /dev/null; then
        echo "⚠️  Port 8501 not open in firewall"
        echo "Opening port 8501..."
        sudo ufw allow 8501/tcp
        echo "✅ Port 8501 opened"
    else
        echo "✅ Port 8501 already open"
    fi
else
    echo "ℹ️  No firewall detected or firewall check skipped"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Starting Streamlit on network..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📱 Access from other devices on your network:"
echo ""
echo "   🌐 http://$SERVER_IP:8501"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 Tips:"
echo "   • Make sure devices are on the same WiFi network"
echo "   • On mobile: Open browser and enter the URL above"
echo "   • Press Ctrl+C to stop the server"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Start Streamlit
streamlit run streamlit_app/app.py --server.address 0.0.0.0 --server.port 8501
