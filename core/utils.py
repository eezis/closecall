from math import sin, cos, sqrt, atan2, radians
import requests

# import as:: from core.utils import distance_between_geocoded_points

def distance_between_geocoded_points(lat1, lon1, lat2, lon2, units='miles'):

    # all trig functions in python use radians, so convert them here
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    RK = 6373.0 #radius of earth in kilometers
    RM = 3959.0 #radius of earth in miles

    if units == 'miles':
        R = RM
    elif units == 'kilometers':
        R = RK
    else:
        raise Exception("Was expecting 'miles' or 'kilometers' for final function arg, got " + units + " instead.")

    dlon = lon2 - lon1
    dlat = lat2 - lat1

#     print(dlon, dlat)

    a = (sin(dlat/2))**2 + cos(lat1) * cos(lat2) * (sin(dlon/2))**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c
    return distance

"""
Find the original code in the "Distance Between Two Points" ipython notebook


the_moat_km = distance_between_geocoded_points(40.066677,-105.288754,41.7004784,-72.5797328, 'kilometers')
the_moat_miles = distance_between_geocoded_points(40.066677,-105.288754,41.7004784,-72.5797328,)

print(the_moat_miles, the_moat_km)

"""



# ********** NOTE *****************/
#
# This is here for convenience, there is a userprofile.method, same name, differen args
#
# ********** NOTE *****************/

from incident.models import Incident
from django.contrib.auth.models import User

# should be modified to handle last X months.

def get_user_incidents(the_username, miles=60):
    """
    takes a username -- Oliver-Ezis -- and returns a list of incidents within X miles of the city center that
    the user provided
    """
    matched_incidents = []
    user = User.objects.get(username=the_username)
    u_lat = user.position.get_lat()
    u_lon = user.position.get_lon()
    incidences = Incident.objects.all()
    for i in inicidences:
        if distance_between_geocoded_points(u_lat, u_lon, i.position.latitude, i.position.longitude) <= miles:
            matched_incidents.append(i)

    return matched_incidents



"""
Gets the geocoded postion of the address, puts it (lat, lon) format
returns ERROR if it was unable to complete the geocode
"""
def get_geocode(address):
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address='
    r = requests.get(url+address)
    goog_resp = r.json()
    if goog_resp['status'] == 'OK':
        # print(gresp['results'])
        lat = goog_resp['results'][0]['geometry']['location']['lat']
        lon = goog_resp['results'][0]['geometry']['location']['lng']
        position = "({}, {})".format(lat,lon)
        return position
    else:
        return 'ERROR'
