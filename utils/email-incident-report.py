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
from django.contrib.auth.models import User


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





subject = "Close Call Database - Incident Reported in your Area"

msg = """
Greetings from the Close Call Database for Cyclists.

Two recent incidents have been reported in your area. The first incident occurred Saturday out by Carter Lake. It was not very serious but was entered into the database to create a record for that driver. The second incident occurred on Tuesday January 27th on Flagstaff. That incident deserves some consideration.

The motorist on Flagstaff exhibited some troubling behavior. In the video you can see the driver make a careless pass, traveling into the oncoming traffic lane in front of a blind corner. Then for some reason, the driver inexplicably pulled over further up the road to confront the cyclist and eventually punched the cyclist in the chest. The cyclist filmed the entire episode. Unfortunately, something seems a bit "off" with this particular driver and we should be wary of him. If anyone has had previous encounters with the driver in question -- he drives an orange subaru, with dents, you will see it in the video -- please email closecalldatabase@gmail.com with the information or file an incident report (even if it was a past encounter).

You can read the account and see the video of the Flagstaff incident here: http://closecalldatabase.com/incident/show-detail/70/

The police are investigating the incident.

You may wish to share this email with other cyclists in your area, particularly if they ride up Flagstaff.


Ride Safely,

Ernest Ezis
Close Call Database

"""


# print 'taking off with U object list for testing'
# user_list = []
# u = UserProfile.objects.get(user__username='eezis')
# print u
# user_list.append(u)



user_list = get_users_close_to_incident(70,60)

print '\n'
print 'sending emails\n'

for u in user_list:
    print "EMAILS ARE OFF TO PREVENT A MISTAKE, INCIDENT ID NEEDS TO BE CHANGED?"
    print u'emailing: {}'.format(u.user.email)
    # send_incident_notification(subject, msg, u.user.email)


# email a copy to me
u = User.objects.get(username='eezis')
send_incident_notification(subject, msg, u.email)

print '\n'
print 'emails have been sent'



