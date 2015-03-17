# https://developers.google.com/maps/articles/toomanymarkers
# https://developers.google.com/maps/documentation/javascript/fusiontableslayer

"""
Gets the data to paste into data/test.csv that then gets imported into the fusiontable on googledrive
"""

import sys
try:
    sys.path.append("/Users/eae/code/sites/closecall")
    sys.path.append("/Users/eae/.virtualenvs/closecall/lib/python2.7/site-packages")
    sys.path.append("/home/eezis/sites/closecall")
    sys.path.append("/home/eezis/.virtualenvs/closecall/bin/python2.7/site-packages")
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

from users.models import UserProfile

UPS = UserProfile.objects.all()

for u in UPS:
    print u'"{}, {}, {}, {}", {}'.format(unicode(u.city), unicode(u.state), unicode(u.country), unicode(u.zipcode), unicode(u.created)).encode('utf-8')

