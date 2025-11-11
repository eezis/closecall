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
    """Check and report on all registrations with Strava/traditional breakdown"""

    # Get all user profiles (exclude test users)
    all_profiles = UserProfile.objects.exclude(
        user__username__icontains='test'
    ).order_by('-created')

    # Find Strava registrations
    strava_profiles = all_profiles.filter(
        Q(created_with__icontains='strava') | Q(oauth_data__icontains='strava')
    )

    # Find traditional registrations (non-Strava)
    traditional_profiles = all_profiles.exclude(
        Q(created_with__icontains='strava') | Q(oauth_data__icontains='strava')
    )

    # Calculate time periods
    now = timezone.now()
    one_week_ago = now - timezone.timedelta(days=7)
    one_month_ago = now - timezone.timedelta(days=30)
    one_year_ago = now - timezone.timedelta(days=365)

    print('=' * 70)
    print('CLOSE CALL DATABASE REGISTRATION REPORT')
    print('=' * 70)
    print(f'Report generated: {now.strftime("%B %d, %Y at %I:%M %p")}')
    print()

    print('📊 OVERALL STATISTICS')
    print('-' * 40)
    print(f'Total users in database: {all_profiles.count()}')
    print(f'  • Strava registrations: {strava_profiles.count()} ({strava_profiles.count()*100//all_profiles.count() if all_profiles.count() > 0 else 0}%)')
    print(f'  • Traditional registrations: {traditional_profiles.count()} ({traditional_profiles.count()*100//all_profiles.count() if all_profiles.count() > 0 else 0}%)')
    print()

    print('📈 RECENT ACTIVITY')
    print('-' * 40)

    # Last 7 days breakdown
    recent_strava = strava_profiles.filter(created__gte=one_week_ago).count()
    recent_traditional = traditional_profiles.filter(created__gte=one_week_ago).count()
    recent_total = all_profiles.filter(created__gte=one_week_ago).count()

    print(f'Last 7 days: {recent_total} total registrations')
    print(f'  • Strava: {recent_strava}')
    print(f'  • Traditional: {recent_traditional}')

    # Last 30 days breakdown
    month_strava = strava_profiles.filter(created__gte=one_month_ago).count()
    month_traditional = traditional_profiles.filter(created__gte=one_month_ago).count()
    month_total = all_profiles.filter(created__gte=one_month_ago).count()

    print(f'\nLast 30 days: {month_total} total registrations')
    print(f'  • Strava: {month_strava}')
    print(f'  • Traditional: {month_traditional}')

    # Last year breakdown
    year_strava = strava_profiles.filter(created__gte=one_year_ago).count()
    year_traditional = traditional_profiles.filter(created__gte=one_year_ago).count()
    year_total = all_profiles.filter(created__gte=one_year_ago).count()

    print(f'\nLast 365 days: {year_total} total registrations')
    print(f'  • Strava: {year_strava}')
    print(f'  • Traditional: {year_traditional}')
    print()

    print('🚴 STRAVA REGISTRATION DETAILS')
    print('-' * 40)

    if strava_profiles.exists():
        # Most recent Strava registration
        most_recent = strava_profiles.first()
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