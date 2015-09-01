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

# input = """
# <p><font face="Arial">I commute northbound down South 5th Street each morning into downtown Austin, TX from Ben White/Manchaca area.</font></p><p><font face="Arial"><span style="font-size: 1.2em; line-height: 1.42857143;">On the morning of Tuesday August 25th at 9am I encountered an intentionally aggressive driver in a brand new Black Audi A7 driver by a blonde female wearing yoga pants.</span><br></font></p><p><font face="Arial"><span style="font-size: 1.2em; line-height: 1.42857143;">While approaching a stop sign at the intersection of Mary and 5th Street she sped up to pass me prior to the stop sign and squeezed out the gap between her car and the curb only to find herself behind a line of 3 cars. I passed on the right, stopped at the stop sign and proceeded down South 5th.</span><br></font></p><p><span style="font-size: 1.2em; line-height: 1.42857143;"><font face="Arial">As I approached the speed bump and center island, she once again tried to speed up to get around me to only run out of space, she braked to get past the island and then floored it past me with only an inch between her bumper and my rear tire. I shook my fist in the air and decided to chase her down knowing that she would hit a red light at Barton Springs Road.</font></span></p><p><span style="font-size: 1.2em; line-height: 1.42857143;"><font face="Arial"><br></font></span></p><p><font face="Arial"><span style="font-size: 1.2em; line-height: 1.42857143;">I&nbsp;</span><span style="font-size: 20.1599998474121px; line-height: 28.7999992370605px;">caught</span><span style="font-size: 1.2em; line-height: 1.42857143;">&nbsp;up to her at the red light, pulled next to her and asked her to roll down her window, she refused so I&nbsp;tapped her glass, she rolled down the window and started to berate me "Don't touch my f*$%cking car" "You ran a stop sign" "F*&amp;%ck you...." etc etc etc</span></font></p><p><span style="font-family: Arial; font-size: 1.2em; line-height: 1.42857143;">I shared with her that the law in Austin is to provide bicycles 5 feet of passing space between a car a bicycle for safety reasons and told her that I will be recording her license plate down and reporting it for other cyclists in Austin to be on the lookout.</span><br></p><p><span style="font-family: Arial; font-size: 1.2em; line-height: 1.42857143;"><br></span></p><p><span style="font-family: Arial; font-size: 1.2em; line-height: 1.42857143;">She flipped me off and we both went our&nbsp;</span><span style="font-family: Arial; font-size: 20.1599998474121px; line-height: 28.7999992370605px;">separate</span><span style="font-family: Arial; font-size: 1.2em; line-height: 1.42857143;">&nbsp;way.</span><br></p><p><span style="font-family: Arial; font-size: 1.2em; line-height: 1.42857143;"><br></span></p><p><span style="font-family: Arial; font-size: 1.2em; line-height: 1.42857143;">Car: Audi A7</span></p><p><span style="font-size: 1.2em; line-height: 1.42857143;"><font face="Arial">Color: Black</font></span></p><p></p><p><span style="font-size: 1.2em; line-height: 1.42857143;"><font face="Arial">License Plate: FTD 7542</font></span></p><p><span style="margin: 0px; padding: 0px; border: 0px none; font-size: 12px; font-family: Arial, sans-serif; vertical-align: baseline; color: rgb(46, 46, 46); line-height: 18px;">VIN:&nbsp;</span><strong style="margin: 0px; padding: 0px; color: rgb(46, 46, 46); font-family: Arial, sans-serif; font-size: 12px; line-height: 18px;">WAU2GAFC5EN026970</strong><br></p><p><span style="font-size: 1.2em; line-height: 1.42857143;"><font face="Arial">Driver: Attractive blonde female with a fiery attitude towards cyclists.</font></span></p><br><br><p></p>
# """

input = i.what


fixed_input = re.sub('<font.*?>', '', input, flags=re.M|re.S)
fixed_input = re.sub('</font>', '', fixed_input, flags=re.M|re.S)

fixed_input = re.sub('<span style=.*?>', '', fixed_input, flags=re.M|re.S)
fixed_input = re.sub('</span>', '', fixed_input, flags=re.M|re.S)

print fixed_input