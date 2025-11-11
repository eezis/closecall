#!/usr/bin/env python
"""
Test the new logging configuration
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'closecall.settings')
sys.path.insert(0, '/home/eezis/code/closecall')
django.setup()

import logging

# Get different loggers
django_logger = logging.getLogger('django')
strava_logger = logging.getLogger('core.strava')
incidents_logger = logging.getLogger('incident')
users_logger = logging.getLogger('users')
security_logger = logging.getLogger('django.security')

print("Testing new logging configuration...")
print("=" * 60)

# Test each logger
django_logger.info("Test message to django.log")
strava_logger.info("Test message to strava.log")
strava_logger.debug("Debug level test for Strava logger")
incidents_logger.info("Test message to incidents.log")
users_logger.info("Test message to users.log")
security_logger.warning("Test security warning to security.log")

# Test error logging
try:
    raise ValueError("Test error for error logging")
except ValueError as e:
    django_logger.error(f"Test error logged: {e}")

print("\nLog messages have been written to the following files:")
print("  - logs/django.log")
print("  - logs/strava.log")
print("  - logs/incidents.log")
print("  - logs/users.log")
print("  - logs/security.log")
print("  - logs/errors.log (for ERROR level messages)")

print("\nChecking log files...")
print("-" * 60)

import os
logs_dir = '/home/eezis/code/closecall/logs'
if os.path.exists(logs_dir):
    for file in os.listdir(logs_dir):
        if file.endswith('.log'):
            filepath = os.path.join(logs_dir, file)
            size = os.path.getsize(filepath)
            print(f"  {file}: {size:,} bytes")
else:
    print("Logs directory not found!")

print("=" * 60)
print("Logging test complete!")