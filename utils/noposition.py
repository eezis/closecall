"""
detect and cure no position
"""

import sys
try:
    sys.path.append("/Users/eae/code/sites/closecall")
    sys.path.append("/Users/eae/.virtualenvs/closecall/lib/python2.7/site-packages")
except ImportError:
    print "import error -- probably on production machine -- trying that . . ."
    try:
        sys.path.append("/home/eezis/sites/closecall")
        sys.path.append("/home/eezis/.virtualenvs/closecall/bin/python2.7/site-packages")
        print "import complete"
    except:
        "Can't import that virtualenv, is the path correct?"

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'closecall.settings'
import django
django.setup()

import requests

from users.models import UserProfile
url = 'https://maps.googleapis.com/maps/api/geocode/json?address='

def get_geocode(address):
    r = requests.get(url+address)
    goog_resp = r.json()
    if goog_resp['status'] == 'OK':
        # print gresp['results']
        lat = goog_resp['results'][0]['geometry']['location']['lat']
        lon = goog_resp['results'][0]['geometry']['location']['lng']
        position = "({}, {})".format(lat,lon)
        return position
    else:
        return 'error'


def find_np_and_cure():
    np = UserProfile.objects.filter(position=None)
    # if not an empty list . . .
    if not np:
        if np.zipcode != '':
            address = "{} {} {} {}".format(np.city, np.state, np.zipcode, np.country)
        else:
            address = "{} {} {}".format(np.city, np.state, np.country)

        position = get_geocode(address)
        if position != 'error':
            np.position = position
            np.save()
            print 'Fixed Position for {}'.fomat(np.user.username)
        else:
            print 'Count not fix position for {} using address: {}'.format(np.user.username, address)
    else:
        print "There were no positions to fix"


find_np_and_cure()

# p = get_geocode('Boulder, CO')
# print p

# p = get_geocode('Fort Mill, South Carolina')
# print p



