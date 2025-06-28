# Gunicorn configuration for Close Call Database
# Architecture: Cloudflare -> nginx -> gunicorn -> Django

import multiprocessing
import os

# Server socket
bind = "127.0.0.1:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 60
max_requests = 1000
max_requests_jitter = 50

# Restart workers after this many requests, with up to max_requests_jitter added, to prevent memory leaks
preload_app = True

# Logging
accesslog = "/var/log/gunicorn/ccdb-access.log"
errorlog = "/var/log/gunicorn/ccdb-error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "ccdb-gunicorn"

# Server mechanics
daemon = False
pidfile = "/var/run/gunicorn/ccdb.pid"
user = "www-data"
group = "www-data"
tmp_upload_dir = None

# SSL (not needed with Cloudflare Tunnel)
# keyfile = None
# certfile = None

# Environment
raw_env = [
    f"DJANGO_SETTINGS_MODULE=closecall.settings",
]

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190