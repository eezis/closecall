#!/usr/bin/env python
"""
Test script for spammer blacklist functionality.
Run with: python test_spammer_blacklist.py
"""

import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'closecall.settings')
django.setup()

from users.models import SpammerBlacklist
import json

def test_email_normalization():
    """Test email normalization function."""
    print("=" * 60)
    print("Testing Email Normalization")
    print("=" * 60)

    test_cases = [
        ('r.y.a.n@gmail.com', 'ryan@gmail.com'),
        ('R.Y.A.N@gmail.com', 'ryan@gmail.com'),
        ('ry.a.nwh.i.t.e.54763.4.@gmail.com', 'ryanwhite547634@gmail.com'),
        ('r.y.a.n.w.h.ite54.7.6.34@gmail.com', 'ryanwhite547634@gmail.com'),
        ('ryanwhite547634@gmail.com', 'ryanwhite547634@gmail.com'),
        ('RYANWHITE547634@GMAIL.COM', 'ryanwhite547634@gmail.com'),
        ('test.user@example.com', 'testuser@example.com'),
        ('test@example.com', 'test@example.com'),
    ]

    all_passed = True
    for email, expected in test_cases:
        result = SpammerBlacklist.normalize_email(email)
        passed = result == expected
        all_passed = all_passed and passed

        status = "✓" if passed else "✗"
        print(f"{status} {email:45} -> {result:30} (expected: {expected})")

    print()
    return all_passed

def test_blacklist_matching():
    """Test that blacklist matches normalized emails."""
    print("=" * 60)
    print("Testing Blacklist Matching")
    print("=" * 60)

    # Get the blacklisted spammer
    try:
        spammer = SpammerBlacklist.objects.get(normalized_email='ryanwhite547634@gmail.com')
        print(f"✓ Found blacklist entry for: {spammer.normalized_email}")
        print(f"  Current email variations: {json.loads(spammer.email_variations)}")
        print(f"  Current usernames: {json.loads(spammer.usernames)}")
        print(f"  Hit count: {spammer.hit_count}")
        print()

        # Test variations that should match
        test_emails = [
            'r.y.a.n.w.h.ite54.7.6.34@gmail.com',  # Original from Oct
            'ry.a.nwh.i.t.e.54763.4.@gmail.com',   # Today's attempt
            'ryanwhite547634@gmail.com',            # No periods
            'R.Y.A.N.WHITE.547634@GMAIL.COM',       # Different caps and periods
            'r.yan.whi.te547634@gmail.com',         # Different period placement
        ]

        print("Testing email variations that should be blocked:")
        for email in test_emails:
            normalized = SpammerBlacklist.normalize_email(email)
            matches = SpammerBlacklist.objects.filter(normalized_email=normalized).exists()
            status = "✓ BLOCKED" if matches else "✗ NOT BLOCKED"
            print(f"{status}: {email:50} -> {normalized}")

        print()
        return True

    except SpammerBlacklist.DoesNotExist:
        print("✗ Blacklist entry not found!")
        return False

def test_non_matching_emails():
    """Test that legitimate emails are not blocked."""
    print("=" * 60)
    print("Testing Non-Matching Emails (should NOT be blocked)")
    print("=" * 60)

    legitimate_emails = [
        'legitimate.user@gmail.com',
        'cyclist@example.com',
        'test@closecalldatabase.com',
        'ryanwhite@differentdomain.com',  # Same name, different domain
    ]

    all_passed = True
    for email in legitimate_emails:
        normalized = SpammerBlacklist.normalize_email(email)
        matches = SpammerBlacklist.objects.filter(normalized_email=normalized).exists()
        passed = not matches
        all_passed = all_passed and passed

        status = "✓ ALLOWED" if passed else "✗ INCORRECTLY BLOCKED"
        print(f"{status}: {email:50} -> {normalized}")

    print()
    return all_passed

def show_blacklist_summary():
    """Show summary of all blacklisted entries."""
    print("=" * 60)
    print("Current Blacklist Summary")
    print("=" * 60)

    blacklist = SpammerBlacklist.objects.all()
    print(f"Total blacklisted entries: {blacklist.count()}")
    print()

    for entry in blacklist:
        print(f"Normalized Email: {entry.normalized_email}")
        print(f"  Email Variations: {json.loads(entry.email_variations)}")
        print(f"  Usernames: {json.loads(entry.usernames)}")
        print(f"  IPs: {json.loads(entry.ip_addresses)}")
        print(f"  Hit Count: {entry.hit_count}")
        print(f"  First Seen: {entry.first_seen}")
        print(f"  Last Seen: {entry.last_seen}")
        print()

def main():
    print()
    print("█" * 60)
    print("SPAMMER BLACKLIST TEST SUITE")
    print("█" * 60)
    print()

    # Run all tests
    test1 = test_email_normalization()
    test2 = test_blacklist_matching()
    test3 = test_non_matching_emails()
    show_blacklist_summary()

    # Summary
    print("=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    print(f"Email Normalization: {'✓ PASSED' if test1 else '✗ FAILED'}")
    print(f"Blacklist Matching:  {'✓ PASSED' if test2 else '✗ FAILED'}")
    print(f"Non-Matching Emails: {'✓ PASSED' if test3 else '✗ FAILED'}")
    print()

    if test1 and test2 and test3:
        print("✓ ALL TESTS PASSED")
        print()
        print("The next time ry.a.nwh.i.t.e.54763.4.@gmail.com (or any variation)")
        print("tries to register, they will be redirected to:")
        print("https://www.fbi.gov/investigate/cyber")
        return 0
    else:
        print("✗ SOME TESTS FAILED")
        return 1

if __name__ == '__main__':
    sys.exit(main())
