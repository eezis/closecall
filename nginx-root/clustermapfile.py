# -*- coding: utf-8 -*-

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

def get_jsondata_as_string():
    UPS = UserProfile.objects.all()
    total = UPS.count()
    jdata ='var data = {{ "count": {},\n'.format(total)
    jdata = jdata + '  "members": [\n'

    count = 0
    for u in UPS:
        count += 1
        lat, lon = u.get_lat_lon()
        if count < total:
            jdata = jdata + '  {{"{}": {}, "longitude": {}, "latitude": {} }},\n'.format('member', count, lon, lat)
        else:
            jdata = jdata + '  {{"{}": {}, "longitude": {}, "latitude": {} }}\n'.format('member', count, lon, lat)

    return jdata + ']}\n'


print get_jsondata_as_string()

print
