#!/bin/bash
# Start script for Close Call Database Gunicorn server

# Exit on any error
set -e

# Change to project directory
cd /home/eae/code/closecall

# Activate virtual environment
source .venv/bin/activate

# Create log directories if they don't exist
sudo mkdir -p /var/log/gunicorn
sudo mkdir -p /var/run/gunicorn
sudo chown www-data:www-data /var/log/gunicorn
sudo chown www-data:www-data /var/run/gunicorn

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run database migrations
echo "Running database migrations..."
python manage.py migrate

# Start Gunicorn
echo "Starting Gunicorn server..."
exec gunicorn closecall.wsgi:application \
    --config gunicorn.conf.py \
    --log-file=- \
    --access-logfile=- \
    --error-logfile=-