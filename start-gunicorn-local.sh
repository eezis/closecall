#!/bin/bash
# Start Gunicorn for local testing (simplified version)

set -e

# Change to project directory
cd /home/eae/code/closecall

# Activate virtual environment
echo "📦 Activating virtual environment..."
source .venv/bin/activate

# Collect static files
echo "📂 Collecting static files..."
python manage.py collectstatic --noinput

# Check for migrations
echo "🗄️ Checking database migrations..."
python manage.py migrate --check || {
    echo "⚠️ Pending migrations detected. Run: python manage.py migrate"
}

# Start Gunicorn for local testing
echo "🚀 Starting Gunicorn server for local testing..."
echo "   Server will be available at: http://127.0.0.1:8000"
echo "   Press Ctrl+C to stop"
echo ""

exec gunicorn closecall.wsgi:application \
    --config gunicorn-local.conf.py