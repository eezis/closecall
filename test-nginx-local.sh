#!/bin/bash
# Test nginx configuration locally

set -e

echo "🌐 Testing Nginx Local Configuration"
echo "=================================="

# Check if nginx is installed
if ! command -v nginx &> /dev/null; then
    echo "❌ nginx is not installed. Install with: sudo apt install nginx"
    exit 1
fi

# Test the site configuration
echo "1️⃣ Testing closecall-local site configuration..."
sudo nginx -t -c /dev/stdin <<EOF
events {
    worker_connections 1024;
}
http {
    include /etc/nginx/mime.types;
    include $(pwd)/nginx/sites-available/closecall-local;
}
EOF

if [ $? -eq 0 ]; then
    echo "✅ Nginx configuration syntax is valid"
else
    echo "❌ Nginx configuration has syntax errors"
    exit 1
fi

echo ""
echo "2️⃣ To enable the site for testing:"
echo "   sudo cp nginx/sites-available/closecall-local /etc/nginx/sites-available/"
echo "   sudo ln -sf /etc/nginx/sites-available/closecall-local /etc/nginx/sites-enabled/"
echo "   sudo nginx -t && sudo systemctl reload nginx"
echo ""
echo "3️⃣ Test URLs (after nginx is configured):"
echo "   - Main site: http://localhost"
echo "   - Health check: http://localhost/health"
echo "   - Static files: http://localhost/static/"
echo ""
echo "4️⃣ Logs to monitor:"
echo "   - Access: sudo tail -f /var/log/nginx/closecall-local.access.log"
echo "   - Errors: sudo tail -f /var/log/nginx/closecall-local.error.log"