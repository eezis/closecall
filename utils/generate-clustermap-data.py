#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generate data.js file for homepage map clustering.
Creates a JavaScript file with member locations for map display.
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
    """Generate new data.js file with all user locations."""
    new_data_file = os.path.join(settings.PROJECT_ROOT, 'nginx-root', 'new-data.js')
    
    print(f'Creating new file: {new_data_file}')
    
    # Get all user profiles with locations
    user_profiles = UserProfile.objects.all().order_by('id')
    total = user_profiles.count()
    
    print(f'Found {total} user profiles')
    
    with open(new_data_file, 'w') as fh:
        fh.write(f'var data = {{ "count": {total},\n')
        fh.write('  "members": [\n')
        
        count = 0
        valid_locations = 0
        
        for user in user_profiles:
            count += 1
            try:
                # Get latitude and longitude
                lat, lon = user.get_lat_lon()
                
                # Skip users without valid coordinates
                if lat and lon and lat != 0.0 and lon != 0.0:
                    valid_locations += 1
                    
                    # Format the member data
                    if count < total:
                        fh.write(f'  {{"member": {user.id}, "longitude": {lon}, "latitude": {lat} }},\n')
                    else:
                        fh.write(f'  {{"member": {user.id}, "longitude": {lon}, "latitude": {lat} }}\n')
            except Exception as e:
                print(f'Error getting location for user {user.id}: {e}')
                continue
        
        fh.write(' ]}\n')
    
    print(f'Generated data for {valid_locations} users with valid locations out of {total} total users')
    return new_data_file


def backup_and_copy_file():
    """Backup existing data.js and copy new file."""
    data_file = os.path.join(settings.PROJECT_ROOT, 'nginx-root', 'data.js')
    new_data_file = os.path.join(settings.PROJECT_ROOT, 'nginx-root', 'new-data.js')
    
    # Backup existing file
    if os.path.exists(data_file):
        backup_file = os.path.join(settings.PROJECT_ROOT, 'nginx-root', 'data-backup.js')
        print(f'Backing up existing data.js to {backup_file}')
        shutil.copy(data_file, backup_file)
    
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
    create_the_file()
    backup_and_copy_file()
    print('Done! Remember to purge Cloudflare cache if needed.')


if __name__ == '__main__':
    # First, let's check how many users we have
    from users.models import UserProfile
    total_users = UserProfile.objects.count()
    print(f'\nTotal users in database: {total_users}')
    
    # Check for command line argument to skip confirmation
    if len(sys.argv) > 1 and sys.argv[1] == '--yes':
        update_data_file()
    else:
        # Ask for confirmation before proceeding
        try:
            response = input('\nDo you want to generate a new data.js file? (yes/no): ')
            if response.lower() == 'yes':
                update_data_file()
            else:
                print('Aborted.')
        except EOFError:
            print('\nNo input provided. Use --yes to run without confirmation.')
            print('Example: python generate-clustermap-data.py --yes')