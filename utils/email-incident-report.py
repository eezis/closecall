"""
Given and incident ID, find all the users that are within X miles

1. Change the

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

import datetime
# import requests

from users.models import UserProfile
from incident.models import Incident
from core.utils import distance_between_geocoded_points
from core.views import send_incident_notification
from django.contrib.auth.models import User

INCIDENT_ID = 407
# TWEAK THE INCIDENT_ID CONSTANT UP TOP!

TESTING = True
MAIL_TO_EE = False

Radius = 10
# Radius = 30
# Radius = 40
# Radius = 60

subject = "Close Call Database - Incident Reported in your Area"

msg = """
Greetings from the Close Call Database for Cyclists. You are receiving this message because an incident has been reported by a cyclist in your area.

You can find the details here: http://closecalldatabase.com/incident/show-detail/#INCIDENT_ID#/

Please review this incident and note the vehicle and driver descriptions. If you have had a previous encounter with the vehicle in question, please reply to this email with details.

You may wish to share this email with other cyclists, particularly if they ride in the area where the incident occurred.

Ride Safely,

Ernest Ezis

Close Call Database

@closecalldb
"""

HTML_msg = """
<p>Greetings from the Close Call Database for Cyclists. You are receiving this message because an incident has been reported by a cyclist in your area.</p>

<p>Please review the incident and note the vehicle and driver descriptions. If you have had a previous encounter with the vehicle in question, please reply to this email with details.</p>

<p>You may wish to share this email with other cyclists that ride in the area where the incident occurred.</p>

<p>You can find the details <a href="http://closecalldatabase.com/incident/show-detail/#INCIDENT_ID#/">here</a>.</p>

<p>Ride Safely,</p>

<p><br />
Ernest Ezis<br />
<a href="http://closecalldatabase.com">Close Call Database</a>
<br /><br />
<a href="https://twitter.com/closecalldb" class="twitter-follow-button" data-show-count="false"><img src="http://closecalldatabase.com/static/images/followclosecalldb.png"></a>
<script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+'://platform.twitter.com/widgets.js';fjs.parentNode.insertBefore(js,fjs);}}(document, 'script', 'twitter-wjs');</script>
&nbsp;&nbsp;&nbsp;
<br /> <br />
<a href="https://twitter.com/eezis" class="twitter-follow-button" data-show-count="false"><img src="http://closecalldatabase.com/static/images/followeezis.png"></a>
<script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+'://platform.twitter.com/widgets.js';fjs.parentNode.insertBefore(js,fjs);}}(document, 'script', 'twitter-wjs');</script>
&nbsp;&nbsp;&nbsp;
</p>
"""

msg = msg.replace('#INCIDENT_ID#', str(INCIDENT_ID))
HTML_msg = HTML_msg.replace('#INCIDENT_ID#', str(INCIDENT_ID))

# sets the email_sent field to True
# records the text of the email message that was sent out
def update_incident_model_with_email_facts(incident_id, email_message):
    i = Incident.objects.get(id=incident_id)
    i.email_sent = True
    i.email_text = email_message
    i.email_sent_on = datetime.datetime.now()
    i.save()


def get_users_close_to_incident(incident_id, radius=60):
    # get the incident
    i = Incident.objects.get(id=incident_id)
    if i.email_sent:
        print "\n\r Email Flag is set, has this incident has already been emailed out???\n\r\n\r"
        raise Exception("This incident has already been emailed out???")


    # create a list object to store the users that will get alerts for this incident
    matched_users = []
    # we want to search the full universe of users that agreed to get email alerts
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


# IS THIS EVER CALLED???
def email_the_users(subject, message, user_list):
    print '------------------ in email_the_users  method ----------'
    for u in user_list:
        send_incident_notification(subject, message, u.email)

    if not TESTING:
        email_message = msg
        update_incident_model_with_email_facts(INCIDENT_ID, email_message)




# print 'taking off with U object list for testing'
# user_list = []
# u = UserProfile.objects.get(user__username='eezis')
# print u
# user_list.append(u)




user_list = get_users_close_to_incident(INCIDENT_ID, Radius)

print '\n'
print '{} users in the incident zone'.format(len(user_list))
print 'sending emails\n'


for u in user_list:
    if TESTING:
        print "EMAILS ARE OFF TO PREVENT A MISTAKE, INCIDENT ID NEEDS TO BE CHANGED?"
        print u'emailing: {}'.format(u.user.email)
    else:
        print u'emailing: {}'.format(u.user.email)
        send_incident_notification(subject, msg, u.user.email, htmlmsg=HTML_msg)

# Now update the model
if not TESTING:
    update_incident_model_with_email_facts(INCIDENT_ID, msg)


# email a copy to me
if MAIL_TO_EE:
    print '\n'
    print 'now sending copy to eezis'
    print '\n'
    u = User.objects.get(username='eezis')
    # send_incident_notification(subject, msg, u.email)
    send_incident_notification(subject, msg, u.email, htmlmsg=HTML_msg)

print '\n'
if TESTING:
    print 'emails have ***NOT*** been sent'
else:
    print 'emails have been sent for {}'.format(str(INCIDENT_ID))



