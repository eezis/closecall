#!/usr/bin/env python
"""
View spammer-to-fbi.log in a readable format.
Run with: python view_fbi_redirects.py
"""

import os
import sys
import re
from pathlib import Path
from datetime import datetime

# Django setup for path resolution
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'closecall.settings')
import django
django.setup()

from django.conf import settings

def parse_log_entry(line):
    """Parse a log entry and extract components."""
    # Example log format:
    # INFO 2025-11-12 08:46:43,378 spammer.fbi test_fbi_logger test_fbi_logger 54 REDIRECTED TO FBI: ry.a.nwh.i.t.e.54763.4.@gmail.com | Normalized: ryanwhite547634@gmail.com | IP: 173.239.254.78 | Username: Matthewwaync | Total attempts: 999 (TEST ENTRY)

    if 'REDIRECTED TO FBI:' not in line:
        return None

    try:
        # Extract timestamp
        timestamp_match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
        timestamp = timestamp_match.group(1) if timestamp_match else "Unknown"

        # Extract email
        email_match = re.search(r'REDIRECTED TO FBI: ([^|]+)\|', line)
        email = email_match.group(1).strip() if email_match else "Unknown"

        # Extract normalized email
        normalized_match = re.search(r'Normalized: ([^|]+)\|', line)
        normalized = normalized_match.group(1).strip() if normalized_match else "Unknown"

        # Extract IP
        ip_match = re.search(r'IP: ([^|]+)\|', line)
        ip = ip_match.group(1).strip() if ip_match else "Unknown"

        # Extract username
        username_match = re.search(r'Username: ([^|]+)\|', line)
        username = username_match.group(1).strip() if username_match else "Unknown"

        # Extract attempt count
        attempts_match = re.search(r'Total attempts: (\d+)', line)
        attempts = attempts_match.group(1) if attempts_match else "Unknown"

        return {
            'timestamp': timestamp,
            'email': email,
            'normalized': normalized,
            'ip': ip,
            'username': username,
            'attempts': attempts
        }
    except Exception as e:
        return None

def view_fbi_log():
    """Display the FBI redirect log in a nice format."""
    log_path = settings.BASE_DIR / 'logs' / 'spammer-to-fbi.log'

    print()
    print("█" * 70)
    print("SPAMMER FBI REDIRECT LOG")
    print("█" * 70)
    print()

    if not log_path.exists():
        print(f"✗ Log file not found: {log_path}")
        print()
        print("No spammers have been redirected yet.")
        print("The log file will be created when the first spammer is caught.")
        return

    with open(log_path, 'r') as f:
        lines = f.readlines()

    if not lines:
        print("Log file exists but is empty.")
        return

    print(f"Log file: {log_path}")
    print(f"Total entries: {len(lines)}")
    print()
    print("=" * 70)

    entries = []
    for line in lines:
        entry = parse_log_entry(line)
        if entry:
            entries.append(entry)

    if not entries:
        print("No valid redirect entries found.")
        return

    # Display entries
    for i, entry in enumerate(entries, 1):
        print(f"\n[{i}] {entry['timestamp']}")
        print(f"    Email:      {entry['email']}")
        print(f"    Normalized: {entry['normalized']}")
        print(f"    IP:         {entry['ip']}")
        print(f"    Username:   {entry['username']}")
        print(f"    Attempts:   {entry['attempts']}")

    print()
    print("=" * 70)
    print(f"Total spammer redirects to FBI: {len(entries)}")
    print("=" * 70)
    print()

if __name__ == '__main__':
    view_fbi_log()
