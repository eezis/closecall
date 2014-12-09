from django.db import models
from django.contrib.auth.models import User
from core.models import BaseFields

# for finding incidents close to the user
from incident.models import Incident
from core.utils import distance_between_geocoded_points

# null controls the DB, blank=True controls the form (e.g., not a required field)

class UserProfile(BaseFields):
    user = models.OneToOneField(User, related_name='profile')
    first = models.CharField(null=True, max_length=50)
    last = models.CharField(null=True, max_length=50)
    city = models.CharField(null=True, max_length=120)
    state = models.CharField(null=True,  max_length=50)
    country = models.CharField(null=True, max_length=80)
    zipcode = models.CharField(null=True, max_length=30, verbose_name="Zip/Postal Code")
    # does the user want email notifications when new incidents are reported in their area?
    email_incidents = models.BooleanField(default=True, verbose_name="Email Me When Incidents Are Reported In My Area")
    # probably need position in order to do lookups (find incidents within 100 miles)
    position = models.CharField(null=True, blank=True, max_length=80)
    # sms_incidents = models.BooleanField(deault=True, verbose_name="Receive")
    # sms would require phone numbers

    def __unicode__(self):
        return self.first + ' ' + self.last + ' :: ' + self.user.username

    def format_position(self):
        # UserProfile position is stored in a CharField, it looks like this
        # self.position = '(40.0149856, -105.27054559999999)'
        return self.position.strip('()').split(',')

    def get_lat_lon(self):
        geoposition = self.format_position()
        # pluck the parts, and return them as floats.
        lat = float(geoposition[0])
        lon = float(geoposition[1].strip())
        return lat, lon

    def get_lat_as_string(self):
        return self.format_position()[0]

    def get_lon_as_string(self):
        return self.format_position()[1].strip()

    def get_lat(self):
        return float(self.format_position()[0])

    def get_lon(self):
        return float(self.format_position()[1].strip())

    def get_user_incidents(self, miles=60):
        """
        returns a list of incidents within X miles of the user's location, where the location is the geocoded center of the
        city, ST compbination they provided. I could pinpoint that down further to zipcode

        USAGE: as tested in http://localhost:8888/notebooks/Distance%20Between%20Points.ipynb

        from users.models import UserProfile

        up = UserProfile.objects.get(user__username='Oliver-Ezis')
        matches = up.get_user_incidents(35)
        for m in matches:
            print m.what[:50], m.address

        """
        matched_incidents = []
        # u_lat = self.get_lat()
        # u_lon = self.get_lon()
        u_lat, u_lon = self.get_lat_lon()
        incidents = Incident.objects.all()
        for i in incidents:
            if distance_between_geocoded_points(u_lat, u_lon, i.position.latitude, i.position.longitude) <= miles:
                matched_incidents.append(i)

        return matched_incidents




# could add a text field that allowed multiple zipcode entries so that they could get
# notified in multiple jurisdictions