"""
detect and cure no position
"""

import sys
try:
    sys.path.append("/Users/eae/code/sites/closecall")
    sys.path.append("/Users/eae/.virtualenvs/closecall/lib/python2.7/site-packages")
    #  no ImportError is thrown!
    sys.path.append("/home/eezis/sites/closecall")
    sys.path.append("/home/eezis/sites/closecall/closecall")
    sys.path.append("/home/eezis/.virtualenvs/closecall/bin/python2.7/site-packages")
except ImportError:
    print "import error -- probably on production machine -- trying that . . ."
    try:
        sys.path.append("/home/eezis/sites/closecall")
        sys.path.append("/home/eezis/sites/closecall/closecall")
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


# THIS SAME CODE IS IN CORE.UTILS.PY, but I am leaving this hear so that it's in one unit for use
# at the server
"""
Gets the geocoded postion of the address, puts it (lat, lon) format
returns ERROR if it was unable to complete the geocode
"""
def get_geocode(address):
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address='
    r = requests.get(url+address)
    goog_resp = r.json()
    if goog_resp['status'] == 'OK':
        # print gresp['results']
        lat = goog_resp['results'][0]['geometry']['location']['lat']
        lon = goog_resp['results'][0]['geometry']['location']['lng']
        position = "({}, {})".format(lat,lon)
        return position
    else:
        return 'ERROR'


def find_np_and_cure():
    np = UserProfile.objects.filter(position=None)
    # if not an empty list . . .
    print np
    if np:
        for n in np:
            if n.zipcode != None:
                address = "{} {} {} {}".format(n.city, n.state, n.zipcode, n.country)
            else:
                address = "{} {} {}".format(n.city, n.state, n.country)

            position = get_geocode(address)
            if position != 'ERROR':
                n.position = position
                n.save()
                print 'Fixed Position for {}'.format(n.user.username)
            else:
                print 'Count not fix position for {} using address: {}'.format(n.user.username, address)
    else:
        print "There were no positions to fix"


def ensure_incidents_have_positin():
    inp = Incident.objects.filter(position=None)
    if inp:
        print "HOUSTON WE HAVE A PROBLEM: At least one incident does not have a position"
        for i in inp:
            print "User {} entered an incident without position information {}".format(i.user.username,i.what[80])
    else:
        print "All Incident Reports have position information"




find_np_and_cure()
ensure_incidents_have_positin()



# p = get_geocode('Boulder, CO')
# print p

# p = get_geocode('Fort Mill, South Carolina')
# print p



