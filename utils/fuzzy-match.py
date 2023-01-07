import sys
sys.path.append("/Users/eae/code/sites/closecall")
sys.path.append("/Users/eae/.virtualenvs/closecall/lib/python2.7/site-packages")
sys.path.append("/home/eezis/sites/closecall")
sys.path.append("/home/eezis/sites/closecall/closecall")
sys.path.append("/home/eezis/.virtualenvs/closecall/bin/python2.7/site-packages")

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'closecall.settings'
import django
django.setup()

# import requests

from users.models import UserProfile
from incident.models import Incident

I = Incident.objects.all()

for i in I:
    print i.license_certain, i.license_uncertain