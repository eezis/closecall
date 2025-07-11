#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generate data.js file for homepage map clustering - FAST VERSION.
Only uses existing geocoded locations, doesn't try to geocode new ones.
"""

import os
import sys
import shutil
import django

# Add project to path and setup Django
sys.path.insert(0, '/home/eae/code/closecall')
os.environ['DJANGO_SETTINGS_MODULE'] = 'closecall.settings'
django.setup()

from users.models import UserProfile
from django.conf import settings


def create_the_file():
    """Generate new data.js file with existing user locations only."""
    new_data_file = os.path.join(settings.PROJECT_ROOT, 'nginx-root', 'new-data.js')
    
    print(f'Creating new file: {new_data_file}')
    
    # Get all user profiles that have positions already
    user_profiles = UserProfile.objects.exclude(
        position__isnull=True
    ).exclude(
        position__exact=''
    ).order_by('id')
    
    total = user_profiles.count()
    
    print(f'Found {total} user profiles with positions')
    
    with open(new_data_file, 'w') as fh:
        fh.write(f'var data = {{ "count": {total},\n')
        fh.write('  "members": [\n')
        
        count = 0
        valid_locations = 0
        
        for idx, user in enumerate(user_profiles):
            count += 1
            try:
                # Use the position field directly if it has lat/lon
                if hasattr(user, 'position') and user.position:
                    # position is a GeopositionField with latitude and longitude attributes
                    lat = user.position.latitude
                    lon = user.position.longitude
                    
                    # Skip invalid coordinates
                    if lat and lon and lat != 0.0 and lon != 0.0:
                        valid_locations += 1
                        
                        # Format the member data
                        if idx < total - 1:
                            fh.write(f'  {{"member": {user.id}, "longitude": {lon}, "latitude": {lat} }},\n')
                        else:
                            fh.write(f'  {{"member": {user.id}, "longitude": {lon}, "latitude": {lat} }}\n')
                
            except Exception as e:
                print(f'Error processing user {user.id}: {e}')
                continue
        
        fh.write(' ]}\n')
    
    print(f'Generated data for {valid_locations} users with valid locations')
    return new_data_file


def backup_and_copy_file():
    """Backup existing data.js and copy new file."""
    data_file = os.path.join(settings.PROJECT_ROOT, 'nginx-root', 'data.js')
    new_data_file = os.path.join(settings.PROJECT_ROOT, 'nginx-root', 'new-data.js')
    
    # Copy new file
    print(f'Copying new file to {data_file}')
    shutil.copy(new_data_file, data_file)
    
    # Set permissions
    os.chmod(data_file, 0o644)
    
    # Remove temporary file
    os.remove(new_data_file)


def update_data_file():
    """Main function to update the data.js file."""
    print('Starting FAST data.js generation (no geocoding)...')
    create_the_file()
    backup_and_copy_file()
    print('Done! Remember to purge Cloudflare cache if needed.')


if __name__ == '__main__':
    # Check how many users have positions
    total_users = UserProfile.objects.count()
    users_with_position = UserProfile.objects.exclude(position__isnull=True).exclude(position__exact='').count()
    
    print(f'\nTotal users in database: {total_users}')
    print(f'Users with existing positions: {users_with_position}')
    
    update_data_file()