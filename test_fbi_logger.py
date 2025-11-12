#!/usr/bin/env python
"""
Test script to verify spammer-to-fbi.log is working correctly.
This simulates what happens when a blacklisted spammer tries to register.
Run with: python test_fbi_logger.py
"""

import os
import sys
import django
import json
from pathlib import Path

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'closecall.settings')
django.setup()

import logging
from users.models import SpammerBlacklist

# Get the spammer FBI logger
spammer_fbi_logger = logging.getLogger('spammer.fbi')

def test_fbi_logger():
    """Test that the spammer-to-fbi.log logger works."""
    print("=" * 60)
    print("Testing spammer-to-fbi.log Logger")
    print("=" * 60)
    print()

    # Check if log directory exists
    from django.conf import settings
    log_dir = settings.BASE_DIR / 'logs'
    fbi_log_path = log_dir / 'spammer-to-fbi.log'

    print(f"Log directory: {log_dir}")
    print(f"FBI log file:  {fbi_log_path}")
    print()

    # Simulate a spammer redirect
    test_email = "ry.a.nwh.i.t.e.54763.4.@gmail.com"
    normalized = SpammerBlacklist.normalize_email(test_email)
    test_ip = "173.239.254.78"
    test_username = "Matthewwaync"

    print(f"Simulating redirect for:")
    print(f"  Email:      {test_email}")
    print(f"  Normalized: {normalized}")
    print(f"  IP:         {test_ip}")
    print(f"  Username:   {test_username}")
    print()

    # Log a test entry
    spammer_fbi_logger.info(
        f"REDIRECTED TO FBI: {test_email} | Normalized: {normalized} | "
        f"IP: {test_ip} | Username: {test_username} | "
        f"Total attempts: 999 (TEST ENTRY)"
    )

    print("✓ Test log entry written")
    print()

    # Check if file was created
    if fbi_log_path.exists():
        print(f"✓ Log file exists: {fbi_log_path}")

        # Show the last few lines
        print()
        print("=" * 60)
        print("Recent entries in spammer-to-fbi.log:")
        print("=" * 60)

        with open(fbi_log_path, 'r') as f:
            lines = f.readlines()
            # Show last 5 lines or all if fewer
            recent_lines = lines[-5:] if len(lines) > 5 else lines
            for line in recent_lines:
                print(line.rstrip())

        print()
        print(f"Total entries in log: {len(lines)}")

    else:
        print(f"✗ Log file not found at {fbi_log_path}")
        print("  This may be normal if this is the first time running.")
        print("  The file will be created on the next spammer redirect.")

    print()
    print("=" * 60)
    print("Test Complete")
    print("=" * 60)
    print()
    print("The spammer-to-fbi.log will record:")
    print("  - Email address (with periods)")
    print("  - Normalized email")
    print("  - IP address")
    print("  - Username")
    print("  - Total attempts")
    print("  - Date and time (automatically added by logger)")

if __name__ == '__main__':
    test_fbi_logger()
