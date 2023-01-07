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

for u in UPS:
    print u'"{}, {}, {}, {}", {}'.format(unicode(u.city), unicode(u.state), unicode(u.country), unicode(u.zipcode), unicode(u.created)).encode('utf-8')

