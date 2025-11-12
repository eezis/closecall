#!/usr/bin/env python
"""
Mark UserProfiles as completed if they have address data.

This is a one-time script to properly classify existing profiles:
- profile_completed=True if they have city, state, country
- profile_completed=False if they're empty auto-created profiles
"""

import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'closecall.settings')
django.setup()

from users.models import UserProfile

def mark_completed_profiles():
    """Mark profiles with address data as completed."""

    print("=" * 80)
    print("MARKING COMPLETED PROFILES")
    print("=" * 80)
    print()

    all_profiles = UserProfile.objects.all()
    total = all_profiles.count()

    print(f"Total profiles: {total}")
    print()

    completed_count = 0
    incomplete_count = 0

    for profile in all_profiles:
        # Check if profile has complete address data
        has_city = profile.city and profile.city.strip() and profile.city.strip().upper() != 'NA'
        has_state = profile.state and profile.state.strip() and profile.state.strip().upper() != 'NA'
        has_country = profile.country and profile.country.strip() and profile.country.strip().upper() != 'NA'

        if has_city and has_state and has_country:
            # Profile has complete address - mark as completed
            if not profile.profile_completed:
                profile.profile_completed = True
                profile.save(update_fields=['profile_completed'])
                completed_count += 1
        else:
            # Profile is incomplete - ensure it's marked as not completed
            if profile.profile_completed:
                profile.profile_completed = False
                profile.save(update_fields=['profile_completed'])
                incomplete_count += 1

    print("=" * 80)
    print("RESULTS")
    print("=" * 80)
    print(f"Marked as COMPLETED:   {completed_count}")
    print(f"Marked as INCOMPLETE:  {incomplete_count}")
    print()

    # Show final counts
    completed = UserProfile.objects.filter(profile_completed=True).count()
    incomplete = UserProfile.objects.filter(profile_completed=False).count()

    print("FINAL COUNTS:")
    print(f"  Completed profiles:   {completed}")
    print(f"  Incomplete profiles:  {incomplete}")
    print(f"  Total:                {completed + incomplete}")
    print("=" * 80)


if __name__ == '__main__':
    mark_completed_profiles()
