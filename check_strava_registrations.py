#!/usr/bin/env python
"""
Check for recent Strava registrations in the Close Call Database.
Run this script periodically to monitor if the Strava OAuth fix is working.

Usage: python check_strava_registrations.py
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'closecall.settings')
sys.path.insert(0, '/home/eezis/code/closecall')
django.setup()

from users.models import UserProfile
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone

def check_strava_registrations():
    """Check and report on Strava registrations"""

    # Find real Strava registrations (exclude test users)
    strava_profiles = UserProfile.objects.filter(
        Q(created_with__icontains='strava') | Q(oauth_data__icontains='strava')
    ).exclude(
        user__username__icontains='test'
    ).order_by('-created')

    print('=' * 70)
    print('STRAVA REGISTRATION REPORT')
    print('=' * 70)
    print(f'Report generated: {timezone.now().strftime("%B %d, %Y at %I:%M %p")}')
    print(f'Total Strava registrations in database: {strava_profiles.count()}')
    print()

    if strava_profiles.exists():
        # Most recent real registration
        most_recent = strava_profiles.first()
        print('*** MOST RECENT SUCCESSFUL STRAVA REGISTRATION ***')
        print(f'Date: {most_recent.created.strftime("%B %d, %Y at %I:%M %p")}')
        print(f'User: {most_recent.first} {most_recent.last} ({most_recent.user.username})')
        print(f'Email: {most_recent.user.email}')
        print(f'Location: {most_recent.city}, {most_recent.state}, {most_recent.country}')
        print(f'Created with: {most_recent.created_with}')

        days_ago = (timezone.now() - most_recent.created).days
        hours_ago = (timezone.now() - most_recent.created).total_seconds() / 3600

        if days_ago == 0:
            print(f'Time ago: {hours_ago:.1f} hours')
            print('🎉 NEW REGISTRATION TODAY!')
        elif days_ago < 7:
            print(f'Days ago: {days_ago}')
            print('✅ Recent registration - Strava OAuth is working!')
        elif days_ago < 30:
            print(f'Days ago: {days_ago}')
            print('📊 Registration within the last month')
        elif days_ago < 365:
            months = days_ago / 30.44
            print(f'Months ago: {months:.1f}')
        else:
            years = days_ago / 365.25
            print(f'Years ago: {years:.1f}')
            print('⚠️  No recent registrations - might need attention')

        # Check for recent registrations (last 7 days)
        one_week_ago = timezone.now() - timezone.timedelta(days=7)
        recent_count = strava_profiles.filter(created__gte=one_week_ago).count()

        print()
        print(f'Registrations in the last 7 days: {recent_count}')

        if recent_count > 0:
            print('Recent registrations:')
            print('-' * 60)
            for profile in strava_profiles.filter(created__gte=one_week_ago)[:10]:
                print(f'{profile.created.strftime("%Y-%m-%d %H:%M")} - {profile.first} {profile.last} - {profile.city}, {profile.state}')
        else:
            # Show last 5 registrations regardless of date
            print()
            print('Last 5 Strava registrations:')
            print('-' * 60)
            for profile in strava_profiles[:5]:
                print(f'{profile.created.strftime("%Y-%m-%d")} - {profile.first} {profile.last} - {profile.city}, {profile.state}')
    else:
        print('No Strava registrations found in the database.')

    print()
    print('=' * 70)

if __name__ == '__main__':
    check_strava_registrations()