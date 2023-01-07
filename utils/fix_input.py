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

import re
from incident.models import Incident

INCIDENT_ID = 290


i = Incident.objects.get(id=INCIDENT_ID)

# print i.what




input = """
<p>The&nbsp;<span class="aBn" data-term="goog_2010924288" tabindex="0" style="border-bottom-width: 1px; border-bottom-style: dashed; border-bottom-color: rgb(204, 204, 204); position: relative; top: -2px; z-index: 0;"><span class="aQJ" style="position: relative; top: 2px; z-index: -1;">Wednesday</span></span>&nbsp;Morning Velo's "A Group" rode to Rabbit Mountain&nbsp;<span class="aBn" data-term="goog_2010924289" tabindex="0" style="border-bottom-width: 1px; border-bottom-style: dashed; border-bottom-color: rgb(204, 204, 204); position: relative; top: -2px; z-index: 0;"><span class="aQJ" style="position: relative; top: 2px; z-index: -1;">on Wednesday</span></span>&nbsp;Morning. After reaching the summit the group turned back and headed south toward Rte 66. It was about&nbsp;<span class="aBn" data-term="goog_2010924290" tabindex="0" style="border-bottom-width: 1px; border-bottom-style: dashed; border-bottom-color: rgb(204, 204, 204); position: relative; top: -2px; z-index: 0;"><span class="aQJ" style="position: relative; top: 2px; z-index: -1;">7:15 a.m.</span></span>, there was very little traffic. The group had split in two, with a group up the road and one chasing it. We were not impeding traffic, there was always an open lane on that lightly traveled road.</div><div class="gmail_default" style="color: rgb(34, 34, 34); font-size: 12.8000001907349px; line-height: normal; font-family: verdana, sans-serif;"><br></div><div class="gmail_default" style="color: rgb(34, 34, 34); font-size: 12.8000001907349px; line-height: normal; font-family: verdana, sans-serif;">[insert photo of group]</div><div class="gmail_default" style="color: rgb(34, 34, 34); font-size: 12.8000001907349px; line-height: normal; font-family: verdana, sans-serif;"><br></div><div class="gmail_default" style="color: rgb(34, 34, 34); font-size: 12.8000001907349px; line-height: normal; font-family: verdana, sans-serif;">On two prior occasions, some of us had encountered a dangerous motorist that, rather than passing safely, had chosen to pull to the right, into the should, and then drive by us at very high speeds -- endangering herself and the cyclists.&nbsp; Since we were riding in this area again, one of the riders chose to take a video camera along in case the driver was encountered again.</div><div class="gmail_default" style="color: rgb(34, 34, 34); font-size: 12.8000001907349px; line-height: normal; font-family: verdana, sans-serif;"><br></div><div class="gmail_default" style="color: rgb(34, 34, 34); font-size: 12.8000001907349px; line-height: normal; font-family: verdana, sans-serif;">While we were on the part of the road that gets renamed to Vestal Road, a car approached us from behind, also traveling south. The group was traveling 22 mph, riding two abreast, and the oncoming traffic lane was wide open. The driver had good visibility and could see that the road way was clear. Rather than crossing into the other lane in order to pass us safely on the left hand side -- the legally required lawful pass -- the driver elected to drive off-road, onto the right hand shoulder, at a high rate of speed (est 44mph or more), and sped past the group. When she was clear of the first group, she drove back into the roadway, and passed the group up the road properly by utilizing the oncoming lane. A woman was driving and she appeared to have two small children in the car with her.</div><div class="gmail_default" style="color: rgb(34, 34, 34); font-size: 12.8000001907349px; line-height: normal; font-family: verdana, sans-serif;"><br></div><div class="gmail_default" style="color: rgb(34, 34, 34); font-size: 12.8000001907349px; line-height: normal; font-family: verdana, sans-serif;">The incident was caught on video, and that video was shared with the Boulder County Sheriff's Office that is going to investigate the incident.&nbsp; This report will get updated in the future, with the results of the investigation.</div><div class="gmail_default" style="color: rgb(34, 34, 34); font-size: 12.8000001907349px; line-height: normal; font-family: verdana, sans-serif;"><br></div><div class="gmail_default" style="color: rgb(34, 34, 34); font-size: 12.8000001907349px; line-height: normal; font-family: verdana, sans-serif;">Here is a video of what took place. The sunlight makes the license plate difficult to read, but the listed license plate is the correct one (276 KII, the car is a 1998 Saturn S-Series SL).</div><div class="gmail_default" style="color: rgb(34, 34, 34); font-size: 12.8000001907349px; line-height: normal; font-family: verdana, sans-serif;"><br></div><div class="gmail_default" style="color: rgb(34, 34, 34); font-size: 12.8000001907349px; line-height: normal; font-family: verdana, sans-serif;">[embed the video here]</div><div><br></div>
"""

input = i.what


fixed_input = re.sub('<font.*?>', '', input, flags=re.M|re.S)
fixed_input = re.sub('</font>', '', fixed_input, flags=re.M|re.S)

fixed_input = re.sub('<span style=.*?>', '', fixed_input, flags=re.M|re.S)
fixed_input = re.sub('</span>', '', fixed_input, flags=re.M|re.S)

print fixed_input