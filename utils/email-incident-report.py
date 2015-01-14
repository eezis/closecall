"""
Given and incident ID, find all the users that are within X miles
"""

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
from core.utils import distance_between_geocoded_points
from core.views import send_incident_notification


def get_users_close_to_incident(incident_id, radius=60):
    # get the incident
    i = Incident.objects.get(id=incident_id)
    # create a list object to store the matches
    matched_users = []
    # we want to search the full universe of users
    U = UserProfile.objects.filter(email_incidents=True)
    for u in U:
        # get user's lat and lon
        u_lat, u_lon = u.get_lat_lon()
        # if the user is within the given radius of the incident, add them to the list of  matched users
        if distance_between_geocoded_points(u_lat, u_lon, i.position.latitude, i.position.longitude) <= radius:
            u_str = u"{} {} {} {}".format(u.first, u.last, u.user.username, u.user.email)
            print u'{} {} {} {}'.format(u.first, u.last, u.user.username, u.user.email).encode('utf-8')
            # note send the fill userprofile object back
            matched_users.append(u)

    return matched_users


def email_the_users(subject, message, user_list):
    for u in user_list:
        send_incident_notification(subject, message, u.email)




# users = get_users_close_to_incident(64,60)

# for u in users:
#     print unicode(u.user.email).encode('utf-8')





subject = "Close Call - Incident Reported in your Area"

msg = """
Hello,

I am sorry to report that a fellow cyclist in your area filed an Incident Report
involving an aggressive driver. The incident occurred at 272 2nd Street, Troy, NY
on Tuesday January 13th and was reported to the database today. The report includes
a video.

http://closecalldatabase.com/incident/show-detail/56/

The cyclist involved did file a police report.

You may wish to share this email with other cyclists in your area.

Ride Safely,


Ernest Ezis

Close Call Database

"""


# print 'taking off with U object list for testing'
# user_list = []
# u = UserProfile.objects.get(user__username='eezis')
# print u
# user_list.append(u)



user_list = get_users_close_to_incident(56,60)

print '\n'
print 'sending emails\n'

for u in user_list:
    print u'{}'.format(u.user.email)
    # print "EMAILS ARE OFF TO PREVENT A MISTAKE, INCIDENT ID NEEDS TO BE CHANGED?"
    send_incident_notification(subject, msg, u.user.email)
    # email a copy to me
    u = Users.objects.get(username='eezis')
    send_incident_notification(subject, msg, u.user.email)

print '\n'
print 'emails have been sent'



