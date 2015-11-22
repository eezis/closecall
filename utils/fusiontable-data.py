# -*- coding: utf-8 -*-

# https://developers.google.com/maps/articles/toomanymarkers
# https://developers.google.com/maps/documentation/javascript/fusiontableslayer
# https://www.google.com/fusiontables/DataSource?docid=1kkG-JAOLZFp85VWIFZ0N75hnF-_xHFnlkWNSGJ1f#rows:id=1
# see the _map_of_members.txt file for directions

"""
Gets the data to paste into data/test.csv that then gets imported into the fusiontable on googledrive
"""

import sys
reload(sys) # just to be sure
sys.setdefaultencoding('utf-8')
import os

# get the OS indendent home direction
home_dir = os.path.expanduser("~")
# print home_dir
sys.path.append(home_dir + "/code/sites/closecall")
sys.path.append(home_dir + "/.virtualenvs/closecall/lib/python2.7/site-packages")

os.environ['DJANGO_SETTINGS_MODULE'] = 'closecall.settings'
import django
django.setup()

from users.models import UserProfile

UPS = UserProfile.objects.all()

print UPS.count()

# for u in UPS:
#     print u'"{}, {}, {}, {}", {}'.format(unicode(u.city), unicode(u.state), unicode(u.country), unicode(u.zipcode), unicode(u.created)).encode('utf-8')

total = UPS.count()
print 'var data = {{ "count": {},'.format(total)
print '  "members": ['

# "longitude": -64.404945, "latitude": -32.202924
total = 5
count = 0
for u in UPS[:50]:
    count += 1
    lat, lon = u.get_lat_lon()
    # print '  {{"{}": {}, "longitude": {}, "latitude": {} }}'.format('member', 'test', lat, lon)
    if count < total:
        print '  {{"{}": {}, "longitude": {}, "latitude": {} }},'.format('member', 'test', lat, lon)
    else:
        print '  {{"{}": {}, "longitude": {}, "latitude": {} }}'.format('member', 'test', lat, lon)


print ' ]}'

# https://googlemaps.github.io/js-marker-clusterer/examples/data.json

# var data = { "count": 10785236,
#  "photos": [{"photo_id": 27932, "photo_title": "Atardecer en Embalse", "photo_url": "http://www.panoramio.com/photo/27932", "photo_file_url": "http://mw2.google.com/mw-panoramio/photos/medium/27932.jpg", "longitude": -64.404945, "latitude": -32.202924, "width": 500, "height": 375, "upload_date": "25 June 2006", "owner_id": 4483, "owner_name": "Miguel Coranti", "owner_url": "http://www.panoramio.com/user/4483"}
# ,
# {"photo_id": 522084, "photo_title": "In Memoriam Antoine de Saint ExupÃ©ry", "photo_url": "http://www.panoramio.com/photo/522084", "photo_file_url": "http://mw2.google.com/mw-panoramio/photos/medium/522084.jpg", "longitude": 17.470493, "latitude": 47.867077, "width": 500, "height": 350, "upload_date": "21 January 2007", "owner_id": 109117, "owner_name": "Busa PÃ©ter", "owner_url": "http://www.panoramio.com/user/109117"}
# ,
# ...
# {"photo_id": 10240311, "photo_title": "two planes", "photo_url": "http://www.panoramio.com/photo/10240311", "photo_file_url": "http://mw2.google.com/mw-panoramio/photos/medium/10240311.jpg", "longitude": 20.306683, "latitude": 49.750107, "width": 332, "height": 500, "upload_date": "15 May 2008", "owner_id": 454219, "owner_name": "Rafal Ociepka", "owner_url": "http://www.panoramio.com/user/454219"}
# ,
# {"photo_id": 7593894, "photo_title": "æ¡‚æž—åèƒœç™¾æ™¯â€”â€”é‡é¾™æ²³", "photo_url": "http://www.panoramio.com/photo/7593894", "photo_file_url": "http://mw2.google.com/mw-panoramio/photos/medium/7593894.jpg", "longitude": 110.424957, "latitude": 24.781747, "width": 500, "height": 375, "upload_date": "04 February 2008", "owner_id": 161470, "owner_name": "John Su", "owner_url": "http://www.panoramio.com/user/161470"}
# ]}
