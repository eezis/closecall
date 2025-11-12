#!/usr/bin/env python
"""
Merge Derek Griffiths' duplicate accounts.

Background:
- 2017: Derek registered (username: "Derek Griffiths")
- Oct 2025: Derek registered again via Strava (username: "Derek Griffiths-59446524")
- Both accounts have same email: derek@coloradorunnermag.com
- Both accounts have incidents and profiles

Strategy:
- Keep: Old account (id=13348, username="Derek Griffiths")
- Merge FROM: New account (id=25450, username="Derek Griffiths-59446524")
- Transfer: 2 incidents from new → old account
- Update: Profile with latest Strava info
- Delete: New account and its profile

Run with: python merge_derek_accounts.py
"""

import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'closecall.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import UserProfile
from incident.models import Incident
from django.db import transaction

def merge_derek_accounts(dry_run=True):
    """Merge Derek's two accounts into one."""

    print("=" * 70)
    print("MERGING DEREK GRIFFITHS DUPLICATE ACCOUNTS")
    print("=" * 70)
    print()

    if dry_run:
        print("🔍 DRY RUN MODE - No changes will be made")
        print()

    try:
        # Get both accounts
        old_account = User.objects.get(id=13348, username="Derek Griffiths")
        new_account = User.objects.get(id=25450, username="Derek Griffiths-59446524")

        print(f"✓ Found old account: {old_account.username} (ID: {old_account.id})")
        print(f"  Email: {old_account.email}")
        print(f"  Date joined: {old_account.date_joined}")
        print(f"  Last login: {old_account.last_login}")
        print()

        print(f"✓ Found new account: {new_account.username} (ID: {new_account.id})")
        print(f"  Email: {new_account.email}")
        print(f"  Date joined: {new_account.date_joined}")
        print(f"  Last login: {new_account.last_login}")
        print()

        # Verify emails match
        if old_account.email != new_account.email:
            print(f"❌ ERROR: Emails don't match!")
            print(f"   Old: {old_account.email}")
            print(f"   New: {new_account.email}")
            return False

        # Get profiles
        try:
            old_profile = old_account.profile
            print(f"✓ Old profile: {old_profile.first} {old_profile.last}")
            print(f"  Location: {old_profile.city}, {old_profile.state}")
            print(f"  Created with: {old_profile.created_with}")
            print()
        except UserProfile.DoesNotExist:
            print("⚠️  Old account has NO profile")
            old_profile = None

        try:
            new_profile = new_account.profile
            print(f"✓ New profile: {new_profile.first} {new_profile.last}")
            print(f"  Location: {new_profile.city}, {new_profile.state}")
            print(f"  Created with: {new_profile.created_with}")
            print()
        except UserProfile.DoesNotExist:
            print("⚠️  New account has NO profile")
            new_profile = None

        # Get incidents
        old_incidents = Incident.objects.filter(user=old_account)
        new_incidents = Incident.objects.filter(user=new_account)

        print(f"Incidents:")
        print(f"  Old account: {old_incidents.count()} incidents")
        for inc in old_incidents:
            what_preview = inc.what[:50] if len(inc.what) > 50 else inc.what
            print(f"    - ID {inc.id}: {what_preview}...")

        print(f"  New account: {new_incidents.count()} incidents")
        for inc in new_incidents:
            what_preview = inc.what[:50] if len(inc.what) > 50 else inc.what
            print(f"    - ID {inc.id}: {what_preview}...")
        print()

        # Perform merge
        print("=" * 70)
        print("MERGE PLAN:")
        print("=" * 70)
        print(f"1. Transfer {new_incidents.count()} incidents from NEW → OLD account")
        print(f"2. Update OLD profile with latest Strava info from NEW profile")
        print(f"3. Update OLD account last_login to most recent")
        print(f"4. Delete NEW profile")
        print(f"5. Delete NEW account")
        print()

        if dry_run:
            print("🔍 DRY RUN - Would execute the above plan")
            print()
            print("To actually perform the merge, run:")
            print("  python merge_derek_accounts.py --execute")
            return True

        # Execute merge in transaction
        with transaction.atomic():
            # Step 1: Transfer incidents
            incident_count = new_incidents.update(user=old_account)
            print(f"✓ Transferred {incident_count} incidents to old account")

            # Step 2: Update old profile with latest Strava info
            if old_profile and new_profile:
                # Keep the older profile but update with newer Strava data
                old_profile.created_with = f"{old_profile.created_with}; Also: {new_profile.created_with}"
                old_profile.oauth_data = new_profile.oauth_data  # Latest OAuth data
                old_profile.save()
                print(f"✓ Updated old profile with latest Strava info")

            # Step 3: Update last_login to most recent
            if new_account.last_login > old_account.last_login:
                old_account.last_login = new_account.last_login
                old_account.save()
                print(f"✓ Updated last_login to {old_account.last_login}")

            # Step 4: Delete new profile
            if new_profile:
                new_profile.delete()
                print(f"✓ Deleted new profile")

            # Step 5: Delete new account
            new_account.delete()
            print(f"✓ Deleted new account")

        print()
        print("=" * 70)
        print("✅ MERGE COMPLETED SUCCESSFULLY")
        print("=" * 70)
        print()

        # Verify final state
        final_account = User.objects.get(id=13348)
        final_incidents = Incident.objects.filter(user=final_account)
        print(f"Final state:")
        print(f"  Account: {final_account.username} ({final_account.email})")
        print(f"  Total incidents: {final_incidents.count()}")
        print(f"  Profile: {final_account.profile.first} {final_account.profile.last}")
        print(f"  Location: {final_account.profile.city}, {final_account.profile.state}")

        return True

    except User.DoesNotExist as e:
        print(f"❌ ERROR: Account not found - {str(e)}")
        return False
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    # Check if --execute flag is provided
    dry_run = '--execute' not in sys.argv

    success = merge_derek_accounts(dry_run=dry_run)
    sys.exit(0 if success else 1)
