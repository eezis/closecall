#!/bin/bash

echo "Restarting Close Call Database services..."
echo ""

# --- Stop CCDB Services ---
echo "Stopping CCDB services..."

# Kill gunicorn for closecall
echo "  Stopping Close Call Gunicorn..."
pkill -f "gunicorn.*closecall"

# Kill nginx with our config
echo "  Stopping Close Call Nginx..."
pkill -f "nginx.*nginx-local-test.conf"

# Clean up nginx pid file if it exists
if [ -f /home/eezis/code/closecall/nginx/nginx.pid ]; then
    echo "  Cleaning up nginx pid file..."
    rm /home/eezis/code/closecall/nginx/nginx.pid
fi

echo "  Waiting 2 seconds for processes to terminate..."
sleep 2

# Force kill if still running
GUNICORN_REMAINING=$(ps aux | grep "gunicorn.*closecall" | grep -v grep)
if [ -n "$GUNICORN_REMAINING" ]; then
    echo "  Force killing remaining Gunicorn processes..."
    pkill -9 -f "gunicorn.*closecall"
    sleep 1
fi

NGINX_REMAINING=$(ps aux | grep "nginx.*nginx-local-test.conf" | grep -v grep)
if [ -n "$NGINX_REMAINING" ]; then
    echo "  Force killing remaining Nginx processes..."
    pkill -9 -f "nginx.*nginx-local-test.conf"
    sleep 1
fi

echo "✓ CCDB services stopped."
echo ""

# --- Start CCDB Services ---
echo "Starting CCDB services..."

cd /home/eezis/code/closecall || { echo "✗ Failed to cd into closecall directory"; exit 1; }

# Activate virtual environment
source .venv/bin/activate || { echo "✗ Failed to activate closecall venv"; exit 1; }

# Start Gunicorn for Close Call Database
echo "  Starting Close Call Gunicorn (port 8890)..."
gunicorn closecall.wsgi:application --config gunicorn-local.conf.py &
GUNICORN_PID=$!
echo "  Close Call Gunicorn started with PID $GUNICORN_PID."

# Start Nginx for Close Call Database
echo "  Starting Close Call Nginx (port 8888)..."
nginx -c /home/eezis/code/closecall/nginx/nginx-local-test.conf &
NGINX_PID=$!
echo "  Close Call Nginx started with PID $NGINX_PID."

deactivate

# Wait for services to initialize
echo ""
echo "Waiting for services to initialize..."
sleep 3

# --- Check if services started successfully ---
echo ""
echo "Checking service status:"
if lsof -i:8890 >/dev/null 2>&1; then
    echo "✓ Gunicorn is running on port 8890"
else
    echo "✗ Gunicorn failed to start on port 8890"
fi

if lsof -i:8888 >/dev/null 2>&1; then
    echo "✓ Nginx is running on port 8888"
else
    echo "✗ Nginx failed to start on port 8888"
fi

echo ""
echo "✓ Close Call Database restart complete!"
echo ""
echo "Access the site at: http://localhost:8888"
