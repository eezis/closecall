#!/bin/bash
# Test script for local nginx + gunicorn setup

set -e

echo "🧪 Testing Close Call Database Local Setup"
echo "========================================"

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: Please run this script from the Django project root"
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source .venv/bin/activate

# Test 1: Django check
echo "1️⃣ Testing Django configuration..."
python manage.py check --deploy
if [ $? -eq 0 ]; then
    echo "✅ Django configuration OK"
else
    echo "❌ Django configuration has issues"
    exit 1
fi

# Test 2: Database connectivity
echo "2️⃣ Testing database connectivity..."
python manage.py migrate --check
if [ $? -eq 0 ]; then
    echo "✅ Database connectivity OK"
else
    echo "❌ Database connectivity issues"
    exit 1
fi

# Test 3: Collect static files
echo "3️⃣ Collecting static files..."
python manage.py collectstatic --noinput --clear
if [ $? -eq 0 ]; then
    echo "✅ Static files collected"
else
    echo "❌ Static file collection failed"
    exit 1
fi

# Test 4: Test gunicorn configuration
echo "4️⃣ Testing gunicorn configuration..."
gunicorn --check-config --config gunicorn.conf.py closecall.wsgi:application
if [ $? -eq 0 ]; then
    echo "✅ Gunicorn configuration OK"
else
    echo "❌ Gunicorn configuration has issues"
    exit 1
fi

echo ""
echo "🎉 All tests passed! Ready to start services."
echo ""
echo "To test the full stack:"
echo "1. Start gunicorn: ./start-gunicorn-local.sh"
echo "2. In another terminal, test nginx config: sudo nginx -t"
echo "3. If nginx config is OK, copy and enable the local site"
echo ""
echo "URLs to test:"
echo "- Django direct: http://127.0.0.1:8000"
echo "- Through nginx: http://localhost (if nginx is configured)"
echo "- Health check: http://localhost/health"