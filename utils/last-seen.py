# So, let me remind you that I do this voluntarily. With this site comes lots of things; like death threats from drivers (who can easily find me) and the threat of lawsuits. This site also has costs; opportunity cost, and real costs that come out of my own pocket. So yes, I know WHO you are and WHERE you are. But what I don't know is what you -- or anyone else -- will do with



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

from django.contrib.auth.models import User
from users.models import UserProfile
# from last_seen.model import LastSeen


def Get_User_Activity(the_email):
    U = User.objects.get(email=the_email)
    lastlogin = U.last_login
    print 'lastlogin {}'.format(lastlogin)


# U = User.objects.get(email='joelmullen@hotmail.com')
# U = User.objects.get(email='ernest.ezis@gmail.com')
# U = User.objects.get(username='eae')
U = User.objects.get(email='lgo1018@gmail.com')
print U.username
ll = User.objects.get(username=U.username).last_login
print ll

print U.email
print U.pk
print User.objects.get(username=U.username).last_login
# print User.objects.get(username='Joel Mullen').last_login

# Get_User_Activity("joelmullen@hotmail.com")

