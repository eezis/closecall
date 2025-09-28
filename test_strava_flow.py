#!/usr/bin/env python
"""Test script to simulate Strava OAuth flow"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'closecall.settings')
sys.path.insert(0, '/home/eezis/code/closecall')
django.setup()

from django.test import Client
from django.contrib.sessions.backends.db import SessionStore

# Create a test client with proper host
client = Client(HTTP_HOST='localhost')

# Simulate Strava athlete data (without email)
strava_athlete_data = {
    'id': 999999999,
    'username': 'testuser',
    'resource_state': 2,
    'firstname': 'Test',
    'lastname': 'User',
    'bio': '',
    'city': 'Boulder',
    'state': 'Colorado',
    'country': 'United States',
    'sex': 'M',
    'premium': False,
    'summit': False,
    'created_at': '2025-01-01T00:00:00Z',
    'updated_at': '2025-09-28T00:00:00Z',
    'badge_type_id': 0,
    'weight': 70.0,
    'profile_medium': 'https://via.placeholder.com/150',
    'profile': 'https://via.placeholder.com/300',
    'friend': None,
    'follower': None
}

# Create a session and store the Strava data
session = SessionStore()
session['strava_athlete'] = strava_athlete_data
session.create()
session_key = session.session_key

print(f"Created session with key: {session_key}")
print(f"Session contains Strava athlete: {strava_athlete_data['firstname']} {strava_athlete_data['lastname']}")

# Now test accessing the email collection page with this session
client.cookies['sessionid'] = session_key
response = client.get('/strava-complete-registration')

print(f"\nResponse status: {response.status_code}")
print(f"Response URL: {response.url if hasattr(response, 'url') else 'N/A'}")

if response.status_code == 200:
    print("✓ Email collection page loaded successfully")

    # Check if the template contains expected elements
    content = response.content.decode('utf-8')
    if 'Strava Connected Successfully' in content:
        print("✓ Strava success banner found")
    if 'Test User' in content:
        print("✓ User name displayed correctly")
    if 'Boulder' in content and 'Colorado' in content:
        print("✓ Location displayed correctly")
    if 'email' in content.lower():
        print("✓ Email form present")

    # Test form submission with an email
    print("\nTesting email submission...")
    response = client.post('/strava-complete-registration', {
        'email': 'testuser@example.com'
    })

    if response.status_code == 302:
        print(f"✓ Form submitted, redirected to: {response.url}")
    else:
        print(f"Form submission status: {response.status_code}")
        if response.status_code == 200:
            # Check for errors
            if 'error' in response.content.decode('utf-8').lower():
                print("Form errors present")

elif response.status_code == 302:
    print(f"Redirected to: {response.url}")
    print("Session might have expired or data not found")
else:
    print(f"Unexpected status code: {response.status_code}")

print("\n✓ Test complete")