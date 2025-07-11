#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generate data.js file for homepage map clustering - SIMPLE VERSION.
Parses position strings to extract lat/lon values.
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


def parse_position(position_str):
    """Parse position string '(lat, lon)' into lat, lon floats."""
    try:
        if not position_str or position_str == '':
            return None, None
        
        # Remove parentheses and split by comma
        position_str = position_str.strip('()')
        parts = position_str.split(',')
        
        if len(parts) != 2:
            return None, None
            
        lat = float(parts[0].strip())
        lon = float(parts[1].strip())
        
        return lat, lon
    except:
        return None, None


def create_the_file():
    """Generate new data.js file with all user locations."""
    new_data_file = os.path.join(settings.PROJECT_ROOT, 'nginx-root', 'new-data.js')
    
    print(f'Creating new file: {new_data_file}')
    
    # Get all user profiles that have positions
    user_profiles = UserProfile.objects.exclude(
        position__isnull=True
    ).exclude(
        position__exact=''
    ).order_by('id')
    
    total_all = user_profiles.count()
    print(f'Found {total_all} user profiles with position data')
    
    with open(new_data_file, 'w') as fh:
        # Write header first
        fh.write('var data = { "count": ')
        count_position = fh.tell()  # Save position to update count later
        fh.write('0000000')  # Placeholder for count
        fh.write(',\n  "members": [\n')
        
        valid_locations = 0
        first = True
        
        for user in user_profiles:
            try:
                # Parse the position string
                lat, lon = parse_position(user.position)
                
                # Skip invalid coordinates
                if lat is not None and lon is not None and lat != 0.0 and lon != 0.0:
                    if not first:
                        fh.write(',\n')
                    else:
                        first = False
                    
                    fh.write(f'  {{"member": {user.id}, "longitude": {lon}, "latitude": {lat} }}')
                    valid_locations += 1
                    
                    if valid_locations % 1000 == 0:
                        print(f'  Processed {valid_locations} valid locations...')
                
            except Exception as e:
                print(f'Error processing user {user.id}: {e}')
                continue
        
        fh.write('\n ]}\n')
        
        # Go back and update the count
        fh.seek(count_position)
        fh.write(str(valid_locations).rjust(7))
    
    print(f'Generated data for {valid_locations} users with valid locations out of {total_all} total users')
    return new_data_file, valid_locations


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
    print('Starting data.js generation...')
    new_file, count = create_the_file()
    
    if count > 0:
        backup_and_copy_file()
        print(f'Success! Generated data.js with {count} user locations.')
        print('Remember to purge Cloudflare cache!')
    else:
        print('Error: No valid locations found!')


if __name__ == '__main__':
    update_data_file()