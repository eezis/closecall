#!/usr/bin/env python
"""
Analyze UserProfile data to understand address and geocoding completeness.

This script identifies:
1. Users with NO address data and position=NULL
2. Users with complete address data but position=NULL (can be fixed by geocoding)
"""

import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'closecall.settings')
django.setup()

from users.models import UserProfile

def analyze_profiles():
    """Analyze all UserProfile records for address and position completeness."""

    print("=" * 80)
    print("USER PROFILE DATA ANALYSIS")
    print("=" * 80)
    print()

    all_profiles = UserProfile.objects.select_related('user').all()
    total_profiles = all_profiles.count()

    print(f"Total UserProfile records: {total_profiles}")
    print()

    # Category 1: NO address data AND position=NULL
    no_address_no_position = []

    # Category 2: HAS address data BUT position=NULL (can be fixed)
    has_address_no_position = []

    # Category 3: HAS position (geocoded successfully)
    with_position = []

    # Category 4: Partial address data AND position=NULL
    partial_address_no_position = []

    for profile in all_profiles:
        # Check address completeness
        has_city = profile.city and profile.city.strip() and profile.city.strip().upper() != 'NA'
        has_state = profile.state and profile.state.strip() and profile.state.strip().upper() != 'NA'
        has_country = profile.country and profile.country.strip() and profile.country.strip().upper() != 'NA'

        has_position_data = bool(profile.position and profile.position.strip())

        # Build profile info
        info = {
            'id': profile.pk,
            'username': profile.user.username,
            'email': profile.user.email,
            'name': f"{profile.first or ''} {profile.last or ''}".strip(),
            'city': profile.city or '',
            'state': profile.state or '',
            'country': profile.country or '',
            'position': profile.position or '',
            'active': profile.user.is_active,
            'date_joined': profile.user.date_joined.strftime('%Y-%m-%d'),
        }

        if has_position_data:
            # Category 3: Has geocoded position
            with_position.append(info)
        elif has_city and has_state and has_country:
            # Category 2: Complete address but no position (can be fixed)
            has_address_no_position.append(info)
        elif not has_city and not has_state and not has_country:
            # Category 1: No address data at all
            no_address_no_position.append(info)
        else:
            # Category 4: Partial address data
            partial_address_no_position.append(info)

    # Print Category 1: NO address, NO position
    print("=" * 80)
    print("CATEGORY 1: NO ADDRESS DATA + NO POSITION")
    print("=" * 80)
    print(f"Count: {len(no_address_no_position)}")
    print()
    if no_address_no_position:
        for p in no_address_no_position:
            print(f"  ID: {p['id']:4d} | User: {p['username']:20s} | Name: {p['name']:30s}")
            print(f"           Active: {p['active']} | Joined: {p['date_joined']} | Email: {p['email']}")
            print()
    else:
        print("  (None found)")
    print()

    # Print Category 2: HAS address, NO position (FIXABLE)
    print("=" * 80)
    print("CATEGORY 2: COMPLETE ADDRESS BUT NO POSITION (FIXABLE)")
    print("=" * 80)
    print(f"Count: {len(has_address_no_position)}")
    print()
    if has_address_no_position:
        for p in has_address_no_position:
            print(f"  ID: {p['id']:4d} | User: {p['username']:20s} | Name: {p['name']:30s}")
            print(f"           Active: {p['active']} | Joined: {p['date_joined']}")
            print(f"           Address: {p['city']}, {p['state']}, {p['country']}")
            print()
    else:
        print("  (None found)")
    print()

    # Print Category 4: PARTIAL address, NO position
    print("=" * 80)
    print("CATEGORY 3: PARTIAL ADDRESS + NO POSITION")
    print("=" * 80)
    print(f"Count: {len(partial_address_no_position)}")
    print()
    if partial_address_no_position:
        for p in partial_address_no_position:
            print(f"  ID: {p['id']:4d} | User: {p['username']:20s} | Name: {p['name']:30s}")
            print(f"           Active: {p['active']} | Joined: {p['date_joined']}")
            print(f"           City: '{p['city']}' | State: '{p['state']}' | Country: '{p['country']}'")
            print()
    else:
        print("  (None found)")
    print()

    # Print summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total profiles:                        {total_profiles:4d}")
    print(f"Profiles WITH geocoded position:       {len(with_position):4d}")
    print(f"Profiles WITHOUT position:             {total_profiles - len(with_position):4d}")
    print()
    print(f"  ├─ No address data (Cat 1):          {len(no_address_no_position):4d}")
    print(f"  ├─ Complete address (Cat 2, fixable): {len(has_address_no_position):4d}")
    print(f"  └─ Partial address (Cat 3):          {len(partial_address_no_position):4d}")
    print()
    print("=" * 80)

    return {
        'total': total_profiles,
        'with_position': len(with_position),
        'no_address_no_position': len(no_address_no_position),
        'has_address_no_position': len(has_address_no_position),
        'partial_address_no_position': len(partial_address_no_position),
    }


if __name__ == '__main__':
    analyze_profiles()
