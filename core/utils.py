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
    incidents = Incident.objects.all()
    for i in incidents:
        if i.latitude and i.longitude:
            if distance_between_geocoded_points(u_lat, u_lon, i.latitude, i.longitude) <= miles:
                matched_incidents.append(i)

    return matched_incidents



"""
Gets the geocoded postion of the address, puts it (lat, lon) format
returns ERROR if it was unable to complete the geocode
"""
def get_geocode(address):
    from django.conf import settings
    import urllib.parse
    import os

    # URL encode the address and add API key
    encoded_address = urllib.parse.quote(address)
    # Use the geocoding-specific key (unrestricted) for server-side calls
    api_key = os.getenv('GOOGLE_MAPS_GEOCODING_KEY', settings.GOOGLE_MAPS_API_KEY)
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={encoded_address}&key={api_key}'

    try:
        r = requests.get(url)
        goog_resp = r.json()

        print(f"Geocoding address: {address}")
        print(f"Google response status: {goog_resp.get('status')}")

        if goog_resp['status'] == 'OK':
            # print(gresp['results'])
            lat = goog_resp['results'][0]['geometry']['location']['lat']
            lon = goog_resp['results'][0]['geometry']['location']['lng']
            position = "({}, {})".format(lat,lon)
            print(f"Geocoded successfully: {position}")
            return position
        else:
            error_msg = goog_resp.get('error_message', 'Unknown error')
            print(f"Geocoding failed: {goog_resp['status']} - {error_msg}")
            return 'ERROR'
    except Exception as e:
        print(f"Exception in geocoding: {e}")
        return 'ERROR'
