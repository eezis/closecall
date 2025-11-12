#!/usr/bin/env python
"""
Send email notifications for an incident to users in the area.

Usage:
    python send_incident_emails.py INCIDENT_ID [--radius MILES] [--test] [--test-email EMAIL]

Examples:
    # Test mode - shows who would get emails but doesn't send
    python send_incident_emails.py 1234 --test

    # Test mode - send only to yourself
    python send_incident_emails.py 1234 --test-email ernest.ezis@gmail.com

    # Send to all users within 60 miles (default)
    python send_incident_emails.py 1234

    # Send to all users within 30 miles
    python send_incident_emails.py 1234 --radius 30
"""

import os
import sys
import argparse
import django

# Setup Django environment
home_dir = os.path.expanduser("~")
sys.path.insert(0, os.path.join(home_dir, "code", "closecall"))
os.environ['DJANGO_SETTINGS_MODULE'] = 'closecall.settings'
django.setup()

import datetime
import logging
from django.conf import settings
from users.models import UserProfile
from incident.models import Incident
from core.utils import distance_between_geocoded_points
from core.views import send_incident_notification

# Get the geolocation logger for tracking users with missing/invalid location data
geolocation_logger = logging.getLogger('geolocation')


def get_users_close_to_incident(incident_id, radius=60):
    """
    Find all users within radius miles of the incident who want email notifications.
    Returns list of UserProfile objects and the incident.
    """
    try:
        incident = Incident.objects.get(id=incident_id)
    except Incident.DoesNotExist:
        print(f"❌ Error: Incident #{incident_id} not found!")
        sys.exit(1)

    if incident.email_sent:
        print(f"⚠️  WARNING: Email flag is already set for incident #{incident_id}!")
        print(f"   Email was sent on: {incident.email_sent_on}")
        response = input("   Do you want to send again anyway? (yes/no): ")
        if response.lower() != 'yes':
            print("Aborted.")
            sys.exit(0)

    # Find users who want email notifications
    matched_users = []
    user_profiles = UserProfile.objects.filter(email_incidents=True)

    print(f"\nSearching {user_profiles.count()} users with email notifications enabled...")

    for profile in user_profiles:
        try:
            u_lat, u_lon = profile.get_lat_lon()
            distance = distance_between_geocoded_points(u_lat, u_lon, incident.latitude, incident.longitude)

            if distance <= radius:
                matched_users.append(profile)
                print(f"  ✓ {profile.first} {profile.last} ({profile.user.email}) - {distance:.1f} miles")
        except Exception as e:
            # Log to geolocation-missing.log for tracking users with invalid/missing location data
            geolocation_logger.warning(
                f"SKIPPED user {profile.user.username} (ID: {profile.user.id}, email: {profile.user.email}) "
                f"for incident #{incident_id}: {str(e)} | "
                f"Profile data: city='{profile.city}', state='{profile.state}', "
                f"country='{profile.country}', position='{profile.position}'"
            )
            print(f"  ⚠️  Skipped {profile.user.username}: {e}")

    return matched_users, incident


def update_incident_email_tracking(incident_id, email_message):
    """Mark incident as emailed with timestamp and message text."""
    incident = Incident.objects.get(id=incident_id)
    incident.email_sent = True
    incident.email_text = email_message
    incident.email_sent_on = datetime.datetime.now()
    incident.save()
    print(f"✓ Updated incident #{incident_id} with email tracking info")


def send_emails(incident_id, user_list, test_mode=False, test_email=None):
    """Send incident notification emails to users."""

    # Email templates
    subject = "Close Call Database - Incident Reported in your Area"

    text_msg = """
Greetings from the Close Call Database for Cyclists. You are receiving this message because an incident has been reported by a cyclist in your area.

You can find the details here: https://closecalldatabase.com/incident/show-detail/#INCIDENT_ID#/

Please review this incident and note the vehicle and driver descriptions. If you have had a previous encounter with the vehicle in question, please reply to this email with details.

You may wish to share this email with other cyclists, particularly if they ride in the area where the incident occurred.

Ride Safely,

Ernest Ezis

Close Call Database

@closecalldb
"""

    html_msg = """
<p>Greetings from the Close Call Database for Cyclists. You are receiving this message because an incident has been reported by a cyclist in your area.</p>

<p>Please review the incident and note the vehicle and driver descriptions. If you have had a previous encounter with the vehicle in question, please reply to this email with details.</p>

<p>You may wish to share this email with other cyclists that ride in the area where the incident occurred.</p>

<p>You can find the details <a href="https://closecalldatabase.com/incident/show-detail/#INCIDENT_ID#/">here</a>.</p>

<p>Ride Safely,</p>

<p><br />
Ernest Ezis<br />
<a href="https://closecalldatabase.com">Close Call Database</a>
<br /><br />
<a href="https://twitter.com/closecalldb" class="twitter-follow-button" data-show-count="false"><img src="https://closecalldatabase.com/static/images/followclosecalldb.png"></a>
&nbsp;&nbsp;&nbsp;
<br /> <br />
<a href="https://twitter.com/eezis" class="twitter-follow-button" data-show-count="false"><img src="https://closecalldatabase.com/static/images/followeezis.png"></a>
&nbsp;&nbsp;&nbsp;
</p>
"""

    # Replace incident ID
    text_msg = text_msg.replace('#INCIDENT_ID#', str(incident_id))
    html_msg = html_msg.replace('#INCIDENT_ID#', str(incident_id))

    # Test mode with specific email
    if test_email:
        print(f"\n📧 TEST MODE: Sending to {test_email} only\n")
        try:
            send_incident_notification(subject, text_msg, test_email, htmlmsg=html_msg)
            print(f"✓ Test email sent to {test_email}")
            return 1
        except Exception as e:
            print(f"❌ Failed to send test email: {e}")
            return 0

    # Test mode - don't actually send
    if test_mode:
        print(f"\n📧 TEST MODE: Would send emails to {len(user_list)} users")
        print("   (No emails will actually be sent)")
        print("\nTo send for real, run without --test flag")
        return 0

    # Actually send emails
    print(f"\n📧 Sending emails to {len(user_list)} users...")
    sent_count = 0
    failed_count = 0

    for profile in user_list:
        try:
            send_incident_notification(subject, text_msg, profile.user.email, htmlmsg=html_msg)
            print(f"  ✓ Sent to {profile.user.email}")
            sent_count += 1
        except Exception as e:
            print(f"  ❌ Failed to send to {profile.user.email}: {e}")
            failed_count += 1

    print(f"\n✓ Sent {sent_count} emails")
    if failed_count > 0:
        print(f"⚠️  {failed_count} emails failed")

    # Update incident tracking
    if sent_count > 0:
        update_incident_email_tracking(incident_id, text_msg)

    return sent_count


def main():
    parser = argparse.ArgumentParser(
        description='Send incident notification emails to users in the area',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('incident_id', type=int, help='Incident ID to send notifications for')
    parser.add_argument('--radius', type=int, default=60, help='Radius in miles (default: 60)')
    parser.add_argument('--test', action='store_true', help='Test mode - show users but don\'t send')
    parser.add_argument('--test-email', type=str, help='Send test email to this address only')

    args = parser.parse_args()

    print("=" * 70)
    print("CLOSE CALL DATABASE - INCIDENT EMAIL NOTIFICATION")
    print("=" * 70)
    print(f"Incident ID: {args.incident_id}")
    print(f"Search radius: {args.radius} miles")
    print(f"Email sender: {settings.DEFAULT_FROM_EMAIL}")

    if args.test:
        print("Mode: TEST (no emails will be sent)")
    elif args.test_email:
        print(f"Mode: TEST (send only to {args.test_email})")
    else:
        print("Mode: PRODUCTION (emails will be sent)")

    print("=" * 70)

    # Get users in the area
    user_list, incident = get_users_close_to_incident(args.incident_id, args.radius)

    print(f"\n✓ Found {len(user_list)} users within {args.radius} miles")

    if len(user_list) == 0:
        print("\n⚠️  No users found in this area. Nothing to send.")
        sys.exit(0)

    # Confirm before sending
    if not args.test and not args.test_email:
        print("\n" + "⚠️ " * 20)
        response = input(f"\nReady to send {len(user_list)} emails. Continue? (yes/no): ")
        if response.lower() != 'yes':
            print("Aborted.")
            sys.exit(0)

    # Send emails
    sent_count = send_emails(args.incident_id, user_list, args.test, args.test_email)

    print("\n" + "=" * 70)
    if args.test:
        print("TEST COMPLETE - No emails were sent")
    elif args.test_email:
        print(f"TEST COMPLETE - Sent {sent_count} test email")
    else:
        print(f"COMPLETE - Sent {sent_count} emails for incident #{args.incident_id}")
    print("=" * 70)


if __name__ == '__main__':
    main()
