# -*- coding: utf-8 -*-

"""
produce a file in this format, where count = number of records.

var data = { "count": 5300,
  "members": [
  {"member": 3, "longitude": -105.2838511, "latitude": 40.0454736 },
  {"member": 8, "longitude": -105.2838511, "latitude": 40.0454736 },
  {"member": 10, "longitude": -105.2838511, "latitude": 40.0454736 },
  {"member": 12, "longitude": -105.1019275, "latitude": 40.1672068 },
  {"member": 13, "longitude": -105.2077798, "latitude": 40.0005378 },
  {"member": 14, "longitude": -105.2838511, "latitude": 40.0454736 },
  {"member": 15, "longitude": -105.2399774, "latitude": 40.0293099 },
  ...
  {"member": 5454, "longitude": -118.542586, "latitude": 34.3916641 },
  {"member": 5455, "longitude": -77.1398878, "latitude": 38.8485316 }
 ]}


"""


import sys
reload(sys) # just to be sure
sys.setdefaultencoding('utf-8')
import os
import shutil

# get the OS indendent home direction
home_dir = os.path.expanduser("~")
# print home_dir
sys.path.append(home_dir + "/code/sites/closecall")
sys.path.append(home_dir + "/sites/closecall")
sys.path.append(home_dir + "/.virtualenvs/closecall/lib/python2.7/site-packages")

os.environ['DJANGO_SETTINGS_MODULE'] = 'closecall.settings'
import django
django.setup()

from users.models import UserProfile

from django.conf import settings

new_data_file = "{}/nginx-root/new-data.json".format(settings.PROJECT_ROOT)
data_file = "{}/nginx-root/data.json".format(settings.PROJECT_ROOT)


def create_the_file():
    print 'creating the new file: {}'.format(new_data_file)
    UPS = UserProfile.objects.all().order_by('id')
    fh = open(new_data_file, 'w')

    total = UPS.count()

    fh.write('var data = {{ "count": {},\n'.format(total))
    fh.write('  "members": [\n')
    count = 0
    for u in UPS:
        count += 1
        # SO THIS CALL WILL TRIGGER SOME PRINT STATEMENTS IF A NEW POSITION NEEDS TO BE GEOCODED
        # THAT'S A PROBLEM?
        # PROBABLY NOT IF BUILDING A STRING AND WRITING TO A FILE -- like I was testing in ipython
        lat, lon = u.get_lat_lon()
        # print '  {{"{}": {}, "longitude": {}, "latitude": {} }}'.format('member', 'test', lat, lon)
        if count < total:
            fh.write('  {{"{}": {}, "longitude": {}, "latitude": {} }},\n'.format('member', u.id, lon, lat))
        else:
            fh.write('  {{"{}": {}, "longitude": {}, "latitude": {} }}\n'.format('member', u.id, lon, lat))


    fh.write( ' ]}\n')



def copy_the_file():
    print 'copying the file'
    src = new_data_file
    dst = data_file
    shutil.copy(src, dst)




def update_data_file():
    create_the_file()
    copy_the_file()
    print 'done'

update_data_file()


"""
to view it in the console
"""

if 0 == 1:

    # doesn't need to be ordered, but useful during development
    # UPS = UserProfile.objects.all()
    UPS = UserProfile.objects.all().order_by('id')

    print UPS.count()

    total = UPS.count()
    # total = 50

    print 'var data = {{ "count": {},'.format(total)
    print '  "members": ['
    count = 0
    # for u in UPS[:total]:
    for u in UPS:
        count += 1
        # SO THIS CALL WILL TRIGGER SOME PRINT STATEMENTS IF A NEW POSITION NEEDS TO BE GEOCODED
        # THAT'S A PROBLEM?
        # PROBABLY NOT IF BUILDING A STRING AND WRITING TO A FILE -- like I was testing in ipython
        lat, lon = u.get_lat_lon()
        # print '  {{"{}": {}, "longitude": {}, "latitude": {} }}'.format('member', 'test', lat, lon)
        if count < total:
            print '  {{"{}": {}, "longitude": {}, "latitude": {} }},'.format('member', u.id, lon, lat)
        else:
            print '  {{"{}": {}, "longitude": {}, "latitude": {} }}'.format('member', u.id, lon, lat)


    print ' ]}'







def make_big_string(UPS):
    count = 0
    jdata = 'var data = {{ "count": {},\n'.format(UPS.count)
    jdata = jdata + '  "members": ['
    for u in UPS:
        count += 1
        lat, lon = u.get_lat_lon()

    if count < total:
        print '  {{"{}": {}, "longitude": {}, "latitude": {} }},'.format('member', u.id, lon, lat)
    else:
        print '  {{"{}": {}, "longitude": {}, "latitude": {} }}'.format('member', u.id, lon, lat)



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
