#!/usr/bin/env python
"""
Script to add existing spammers to the blacklist.
Run with: python add_spammer_to_blacklist.py
"""

import os
import sys
import django
import json
from datetime import datetime

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'closecall.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import SpammerBlacklist

def add_spammer(username, reason="spam_registration"):
    """Add a user to the spammer blacklist."""
    try:
        user = User.objects.get(username=username)
        email = user.email

        # Normalize email
        normalized = SpammerBlacklist.normalize_email(email)

        # Check if already blacklisted
        if SpammerBlacklist.objects.filter(normalized_email=normalized).exists():
            print(f"❌ {email} (normalized: {normalized}) is already blacklisted")
            return False

        # Create blacklist entry
        spammer = SpammerBlacklist.objects.create(
            normalized_email=normalized,
            email_variations=json.dumps([email]),
            ip_addresses=json.dumps([]),  # IP will be captured on next attempt
            usernames=json.dumps([username]),
            reason=reason,
            hit_count=1
        )

        print(f"✓ Added {email} to blacklist")
        print(f"  Normalized: {normalized}")
        print(f"  Username: {username}")
        print(f"  Reason: {reason}")
        print(f"  User status: {'Active' if user.is_active else 'Inactive (never activated)'}")

        return True

    except User.DoesNotExist:
        print(f"❌ User '{username}' not found")
        return False
    except Exception as e:
        print(f"❌ Error adding spammer: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("Adding Known Spammers to Blacklist")
    print("=" * 60)
    print()

    # Add the known spammer
    spammers = [
        'Matthewwaync',  # r.y.a.n.w.h.ite54.7.6.34@gmail.com
    ]

    for username in spammers:
        add_spammer(username)
        print()

    print("=" * 60)
    print("Summary of Blacklist:")
    print("=" * 60)

    # Show all blacklisted entries
    blacklist = SpammerBlacklist.objects.all()
    for entry in blacklist:
        print(f"\nNormalized Email: {entry.normalized_email}")
        print(f"  Email Variations: {json.loads(entry.email_variations)}")
        print(f"  Usernames: {json.loads(entry.usernames)}")
        print(f"  Hit Count: {entry.hit_count}")
        print(f"  First Seen: {entry.first_seen}")
        print(f"  Last Seen: {entry.last_seen}")
        print(f"  Reason: {entry.reason}")

if __name__ == '__main__':
    main()
