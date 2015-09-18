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

from users.models import UserProfile

username = 'Matt Kobzik'

U = UserProfile.objects.get()

print u.email