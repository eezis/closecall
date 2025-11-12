#!/usr/bin/env python
"""
Geocode UserProfile records that have complete address data but missing position.

This script:
1. Finds profiles with city, state, country BUT position=NULL
2. Attempts to geocode each one using Google Maps API
3. Saves successful geocodes to the database
4. Reports on successes and failures
"""

import os
import django
import time

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'closecall.settings')
django.setup()

from users.models import UserProfile
from core.utils import get_geocode

def geocode_missing_positions(dry_run=False):
    """
    Geocode all profiles with complete address data but no position.

    Args:
        dry_run: If True, don't save changes to database
    """
    print("=" * 80)
    print("GEOCODING MISSING POSITIONS")
    print("=" * 80)
    print(f"Mode: {'DRY RUN (no changes will be saved)' if dry_run else 'LIVE (changes will be saved)'}")
    print()

    # Find profiles with complete address but no position
    profiles_to_fix = []
    all_profiles = UserProfile.objects.select_related('user').all()

    for profile in all_profiles:
        has_city = profile.city and profile.city.strip() and profile.city.strip().upper() != 'NA'
        has_state = profile.state and profile.state.strip() and profile.state.strip().upper() != 'NA'
        has_country = profile.country and profile.country.strip() and profile.country.strip().upper() != 'NA'
        has_position = bool(profile.position and profile.position.strip())

        if not has_position and has_city and has_state and has_country:
            profiles_to_fix.append(profile)

    print(f"Found {len(profiles_to_fix)} profiles to geocode")
    print()

    if len(profiles_to_fix) == 0:
        print("Nothing to do!")
        return

    successes = []
    failures = []

    for i, profile in enumerate(profiles_to_fix, 1):
        # Build address string
        if profile.zipcode and profile.zipcode.strip():
            address = f"{profile.city}, {profile.state}, {profile.zipcode}, {profile.country}"
        else:
            address = f"{profile.city}, {profile.state}, {profile.country}"

        print(f"[{i}/{len(profiles_to_fix)}] Geocoding: {profile.user.username}")
        print(f"      Address: {address}")

        # Attempt geocoding
        position = get_geocode(address)

        if position and position != 'ERROR':
            print(f"      ✓ SUCCESS: {position}")

            if not dry_run:
                profile.position = position
                profile.save()
                print(f"      ✓ Saved to database")
            else:
                print(f"      (DRY RUN - not saved)")

            successes.append({
                'id': profile.pk,
                'username': profile.user.username,
                'address': address,
                'position': position,
            })
        else:
            print(f"      ✗ FAILED: Could not geocode")
            failures.append({
                'id': profile.pk,
                'username': profile.user.username,
                'address': address,
                'error': 'GEOCODING_FAILED',
            })

        print()

        # Rate limiting - don't hammer Google Maps API
        if i < len(profiles_to_fix):
            time.sleep(0.5)  # 500ms between requests

    # Print summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total profiles attempted:  {len(profiles_to_fix)}")
    print(f"Successful geocodes:       {len(successes)}")
    print(f"Failed geocodes:           {len(failures)}")
    print()

    if failures:
        print("FAILED PROFILES:")
        print("-" * 80)
        for f in failures:
            print(f"  ID {f['id']:4d}: {f['username']:25s} | {f['address']}")
        print()

    if not dry_run:
        print(f"✓ {len(successes)} profiles have been geocoded and saved to the database")
    else:
        print(f"DRY RUN COMPLETE - No changes were made to the database")
        print(f"Run with --live to apply changes")

    print("=" * 80)

    return {
        'total': len(profiles_to_fix),
        'successes': len(successes),
        'failures': len(failures),
    }


if __name__ == '__main__':
    import sys

    # Check for --live flag
    dry_run = '--live' not in sys.argv

    if dry_run:
        print()
        print("⚠️  DRY RUN MODE - No changes will be saved")
        print("    Add --live flag to save changes to database")
        print()
        input("Press ENTER to continue with dry run...")
        print()
    else:
        print()
        print("⚠️  LIVE MODE - Changes WILL be saved to database")
        print()
        response = input("Are you sure you want to continue? (yes/no): ")
        if response.lower() != 'yes':
            print("Aborted.")
            sys.exit(0)
        print()

    geocode_missing_positions(dry_run=dry_run)
