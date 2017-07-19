import os
# get the OS indendent home direction
home_dir = os.path.expanduser("~")
import sys
# print home_dir
sys.path.append(home_dir + "/code/sites/closecall")
sys.path.append(home_dir + "/sites/closecall")
sys.path.append(home_dir + "/.virtualenvs/closecall/lib/python2.7/site-packages")

os.environ['DJANGO_SETTINGS_MODULE'] = 'closecall.settings'
import django
django.setup()

from incident.models import Incident

PLATE_CHARS = '09'

Incidents = Incident.objects.filter(license_certain__contains=PLATE_CHARS)

for i in Incidents:
    print u"\n{}\t{}\t PLATE: {}\n".format(i.id, i.address, i.license_certain,)

Incidents = Incident.objects.filter(license_uncertain__contains=PLATE_CHARS)

for i in Incidents:
    print u"\n{}\t{}\t{}\n".format(i.id, i.address, i.license_uncertain,)




Incidents = Incident.objects.filter(what__contains='coal')

for i in Incidents:
    # print u"\n\n{}\t{}\n{}\n".format(i.id, i.address, i.what,)
    print i.id
    print i.address
    print i.what

Incidents = Incident.objects.filter(address__contains='Natchez')


count = 0

for i in Incidents:
    count += 1
    print "\n{}\t{}\t{}\t{}\n".format(i.id, count, i.address, i.license_certain, i.license_uncertain,)


# Incidents = Incident.objects.filter(vehicle_description__contains='volvo')
# for i in Incidents:
#     print "\n{}\t{}\t{}\t{}\n{}\n".format(i.id, i.address, i.license_certain, i.license_uncertain, i.vehicle_description)

Incidents = Incident.objects.filter(make__icontains='volvo')
for i in Incidents:
    print "\n{}\t{}\t{}\t{}\n{}\n".format(i.id, i.address, i.license_certain, i.license_uncertain, i.vehicle_description)
