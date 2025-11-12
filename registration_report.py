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
    # Order by user registration date, not profile creation date
    all_profiles = UserProfile.objects.exclude(
        user__username__icontains='test'
    ).select_related('user').order_by('-user__date_joined')

    # Find Strava registrations
    strava_profiles = all_profiles.filter(
        Q(created_with__icontains='strava') | Q(oauth_data__icontains='strava')
    )

    # Find traditional registrations (non-Strava)
    traditional_profiles = all_profiles.exclude(
        Q(created_with__icontains='strava') | Q(oauth_data__icontains='strava')
    )

    # Calculate time periods (using local timezone)
    now = timezone.localtime(timezone.now())
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
    recent_strava = strava_profiles.filter(user__date_joined__gte=one_week_ago).count()
    recent_traditional = traditional_profiles.filter(user__date_joined__gte=one_week_ago).count()
    recent_total = all_profiles.filter(user__date_joined__gte=one_week_ago).count()

    print(f'Last 7 days: {recent_total} total registrations')
    print(f'  • Strava: {recent_strava}')
    print(f'  • Traditional: {recent_traditional}')

    # Last 30 days breakdown
    month_strava = strava_profiles.filter(user__date_joined__gte=one_month_ago).count()
    month_traditional = traditional_profiles.filter(user__date_joined__gte=one_month_ago).count()
    month_total = all_profiles.filter(user__date_joined__gte=one_month_ago).count()

    print(f'\nLast 30 days: {month_total} total registrations')
    print(f'  • Strava: {month_strava}')
    print(f'  • Traditional: {month_traditional}')

    # Last year breakdown
    year_strava = strava_profiles.filter(user__date_joined__gte=one_year_ago).count()
    year_traditional = traditional_profiles.filter(user__date_joined__gte=one_year_ago).count()
    year_total = all_profiles.filter(user__date_joined__gte=one_year_ago).count()

    print(f'\nLast 365 days: {year_total} total registrations')
    print(f'  • Strava: {year_strava}')
    print(f'  • Traditional: {year_traditional}')
    print()

    # Check for users without profiles (orphaned accounts)
    print('⚠️  ORPHANED ACCOUNTS (Users without Profiles)')
    print('-' * 40)

    orphaned_users = User.objects.filter(profile__isnull=True).exclude(
        username__icontains='test'
    )
    total_orphaned = orphaned_users.count()
    orphaned_inactive = orphaned_users.filter(is_active=False).count()
    orphaned_active = orphaned_users.filter(is_active=True).count()

    print(f'Total users without profiles: {total_orphaned:,}')
    print(f'  • Inactive (never verified email): {orphaned_inactive:,}')
    print(f'  • Active (verified but no profile): {orphaned_active:,}')

    # Recent orphaned accounts (last 30 days)
    recent_orphaned = orphaned_users.filter(date_joined__gte=one_month_ago)
    if recent_orphaned.exists():
        print(f'\nRecent orphaned accounts (last 30 days): {recent_orphaned.count()}')
        print('Last 10 orphaned accounts:')
        print('-' * 60)
        for user in recent_orphaned.order_by('-date_joined')[:10]:
            status = '✅ Active' if user.is_active else '❌ Inactive'
            local_date = timezone.localtime(user.date_joined)
            print(f'{local_date.strftime("%Y-%m-%d %H:%M")} - {user.username} - {user.email} - {status}')

    # Breakdown by year
    print('\nOrphaned accounts by year:')
    print('-' * 60)
    from django.db.models.functions import TruncYear
    from django.db.models import Count
    yearly_orphaned = orphaned_users.annotate(
        year=TruncYear('date_joined')
    ).values('year').annotate(
        count=Count('id')
    ).order_by('-year')[:5]

    for item in yearly_orphaned:
        year = item['year'].year if item['year'] else 'Unknown'
        count = item['count']
        print(f'{year}: {count:,} users')

    print()

    print('🚴 STRAVA REGISTRATION DETAILS')
    print('-' * 40)

    if strava_profiles.exists():
        # Most recent Strava registration
        most_recent = strava_profiles.first()
        reg_date = timezone.localtime(most_recent.user.date_joined)
        print(f'Date: {reg_date.strftime("%B %d, %Y at %I:%M %p")}')
        first_name = most_recent.first or most_recent.user.first_name or ''
        last_name = most_recent.last or most_recent.user.last_name or ''
        print(f'User: {first_name} {last_name} ({most_recent.user.username})')
        print(f'Email: {most_recent.user.email}')
        print(f'Location: {most_recent.city or "None"}, {most_recent.state or "None"}, {most_recent.country or "None"}')
        print(f'Created with: {most_recent.created_with}')

        days_ago = (now - reg_date).days
        hours_ago = (now - reg_date).total_seconds() / 3600

        # Check if same calendar day (not just < 24 hours)
        is_today = now.date() == reg_date.date()

        if is_today:
            print(f'Time ago: {hours_ago:.1f} hours')
            print('🎉 NEW REGISTRATION TODAY!')
        elif days_ago < 7:
            if hours_ago < 24:
                print(f'Time ago: {hours_ago:.1f} hours (yesterday)')
            else:
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
        recent_count = strava_profiles.filter(user__date_joined__gte=one_week_ago).count()

        print()
        print(f'Registrations in the last 7 days: {recent_count}')

        if recent_count > 0:
            print('Recent registrations:')
            print('-' * 60)
            for profile in strava_profiles.filter(user__date_joined__gte=one_week_ago)[:10]:
                local_date = timezone.localtime(profile.user.date_joined)
                first_name = profile.first or profile.user.first_name or ''
                last_name = profile.last or profile.user.last_name or ''
                print(f'{local_date.strftime("%Y-%m-%d %H:%M")} - {first_name} {last_name} - {profile.city or "None"}, {profile.state or "None"}')
        else:
            # Show last 5 registrations regardless of date
            print()
            print('Last 5 Strava registrations:')
            print('-' * 60)
            for profile in strava_profiles[:5]:
                local_date = timezone.localtime(profile.user.date_joined)
                first_name = profile.first or profile.user.first_name or ''
                last_name = profile.last or profile.user.last_name or ''
                print(f'{local_date.strftime("%Y-%m-%d")} - {first_name} {last_name} - {profile.city or "None"}, {profile.state or "None"}')
    else:
        print('No Strava registrations found in the database.')

    print()

    print('👤 TRADITIONAL REGISTRATION DETAILS')
    print('-' * 40)

    if traditional_profiles.exists():
        # Most recent traditional registration
        most_recent_trad = traditional_profiles.first()
        reg_date_trad = timezone.localtime(most_recent_trad.user.date_joined)
        print(f'Date: {reg_date_trad.strftime("%B %d, %Y at %I:%M %p")}')
        first_name = most_recent_trad.first or most_recent_trad.user.first_name or ''
        last_name = most_recent_trad.last or most_recent_trad.user.last_name or ''
        print(f'User: {first_name} {last_name} ({most_recent_trad.user.username})')
        print(f'Email: {most_recent_trad.user.email}')
        print(f'Location: {most_recent_trad.city or "None"}, {most_recent_trad.state or "None"}, {most_recent_trad.country or "None"}')
        print(f'Created with: {most_recent_trad.created_with or "Traditional Registration"}')

        days_ago_trad = (now - reg_date_trad).days
        hours_ago_trad = (now - reg_date_trad).total_seconds() / 3600

        # Check if same calendar day (not just < 24 hours)
        is_today = now.date() == reg_date_trad.date()

        if is_today:
            print(f'Time ago: {hours_ago_trad:.1f} hours')
            print('🎉 NEW REGISTRATION TODAY!')
        elif days_ago_trad < 7:
            if hours_ago_trad < 24:
                print(f'Time ago: {hours_ago_trad:.1f} hours (yesterday)')
            else:
                print(f'Days ago: {days_ago_trad}')
            print('✅ Recent registration')

        # Check for recent traditional registrations (last 7 days)
        recent_trad_count = traditional_profiles.filter(user__date_joined__gte=one_week_ago).count()

        print()
        print(f'Traditional registrations in the last 7 days: {recent_trad_count}')

        if recent_trad_count > 0:
            print('Recent traditional registrations:')
            print('-' * 60)
            for profile in traditional_profiles.filter(user__date_joined__gte=one_week_ago)[:10]:
                created_with = profile.created_with or 'Traditional'
                local_date = timezone.localtime(profile.user.date_joined)
                print(f'{local_date.strftime("%Y-%m-%d %H:%M")} - {profile.first or profile.user.first_name} {profile.last or profile.user.last_name} ({profile.user.username}) - {created_with}')

    print()
    print('=' * 70)

if __name__ == '__main__':
    check_strava_registrations()