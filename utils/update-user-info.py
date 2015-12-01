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
from django.contrib.auth.models import User

# username = 'Matt Kobzik'
# username = 'Sam Thomas'
username = 'Greg Cantori'


u = User.objects.get(username=username)
print u
print
print u.email
u.email = 'gcantori@gmail.com'
u.save()

u = User.objects.get(username=username)
print
print 'changed'
print
print u
print
print u.email


# # U = UserProfile.objects.get()
# U.email = 'sthomas1990@gmail.com'
# U.save()

# print u.email

