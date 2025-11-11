# Gunicorn configuration for local testing
# Simplified version without special directories

import multiprocessing

# Server socket
bind = "127.0.0.1:8890"
backlog = 512

# Worker processes
workers = 2
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 60
max_requests = 1000
max_requests_jitter = 50

# Restart workers after this many requests to prevent memory leaks
preload_app = True

# Logging (to both console and files for local testing)
# Use both stdout and file logging
accesslog = "-"  # Keep console output
errorlog = "-"   # Keep console output
loglevel = "info"
access_log_format = '[CC] %(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Note: Django's internal logging (configured in settings.py) will write to logs/ directory
# This includes application errors, security events, and custom logging

# Process naming
proc_name = "closecall-local"

# Server mechanics
daemon = False
reload = True

# Environment
raw_env = [
    "DJANGO_SETTINGS_MODULE=closecall.settings",
]