#!/usr/bin/env bash
set -e

PORT=8501
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo "========================================================"
echo "  NovaCart DBMS Prototype - Live Tunnel Launcher"
echo "========================================================"

# Check if Streamlit is running on port 8501
if ! lsof -i :$PORT > /dev/null 2>&1; then
    echo "Starting Streamlit server on port $PORT..."
    /opt/anaconda3/bin/streamlit run app.py --server.port $PORT --server.headless true --server.enableCORS false --server.enableXsrfProtection false > /dev/null 2>&1 &
    sleep 3
else
    echo "Streamlit is already running on port $PORT."
fi

echo "Starting public Cloudflare Tunnel..."
echo "Anyone on any device or network can access this link:"
echo ""
cloudflared tunnel --protocol http2 --url http://localhost:$PORT
