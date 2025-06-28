#!/bin/bash
# Test all endpoints to verify the application is working

echo "🔍 Testing Application Endpoints"
echo "==============================="

# Function to test URL
test_url() {
    local url=$1
    local expected_status=${2:-200}
    local description=$3
    
    echo -n "Testing $description ($url)... "
    
    response=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null)
    
    if [ "$response" = "$expected_status" ]; then
        echo "✅ OK ($response)"
    else
        echo "❌ FAILED (got $response, expected $expected_status)"
    fi
}

# Test if gunicorn is running
if ! pgrep -f "gunicorn.*closecall" > /dev/null; then
    echo "⚠️ Gunicorn not running. Start with: ./start-gunicorn-local.sh"
    echo "   Testing with Django development server if available..."
fi

echo ""
echo "🧪 Testing Direct Application (port 8000):"
test_url "http://127.0.0.1:8000" 200 "Home page"
test_url "http://127.0.0.1:8000/admin/" 302 "Admin (should redirect to login)"
test_url "http://127.0.0.1:8000/static/favicon.ico" 200 "Static files"

echo ""
echo "🌐 Testing Through Nginx (port 80) - if configured:"
test_url "http://localhost" 200 "Home page via nginx"
test_url "http://localhost/health" 200 "Health check"
test_url "http://localhost/static/favicon.ico" 200 "Static files via nginx"

echo ""
echo "📊 System Status:"
echo "Gunicorn processes: $(pgrep -f "gunicorn.*closecall" | wc -l)"
echo "Nginx status: $(systemctl is-active nginx 2>/dev/null || echo 'not running')"

echo ""
echo "🎯 Quick Test Commands:"
echo "curl -I http://127.0.0.1:8000                    # Test app directly"
echo "curl -I http://localhost                         # Test via nginx"
echo "curl http://localhost/health                     # Health check"