from django.db import models
from django.contrib.auth.models import User
from core.models import BaseFields

from django.core.mail import send_mail

# for finding incidents close to the user
from incident.models import Incident
from core.utils import distance_between_geocoded_points, get_geocode

# null controls the DB, blank=True controls the form (e.g., not a required field)

class UserProfile(BaseFields):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    first = models.CharField(null=True, max_length=50)
    last = models.CharField(null=True, max_length=50)
    city = models.CharField(null=True, max_length=120, verbose_name="City  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[ NA if Not Applicable ]")
    state = models.CharField(null=True, max_length=50, verbose_name="State/Province/Region  &nbsp;&nbsp;&nbsp;&nbsp;[ NA if Not Applicable ]")
    country = models.CharField(null=True, max_length=80)
    zipcode = models.CharField(null=True, blank=True, max_length=30, verbose_name="Zip/Postal Code")
    # does the user want email notifications when new incidents are reported in their area?
    email_incidents = models.BooleanField(default=True, verbose_name="Email Me When Incidents Are Reported In My Area")
    #
    # email_articles = models.BooleanField(default=True, verbose_name="Email Me When Important ")
    # need position in order to do lookups (find incidents within 100 miles)
    position = models.CharField(null=True, max_length=80)
    # sms_incidents = models.BooleanField(deault=True, verbose_name="Receive")
    # sms would require phone numbers

    # was the account created with custom login, or did they use strava or something else
    # strave=34330 (where the number = their strava_id)
    created_with = models.CharField(null=True, blank=True, max_length=250)
    oauth_data = models.TextField(null=True, blank=True)
    can_blog = models.BooleanField(default=False)


    class meta:
        ordering = ['-created',]

    def __unicode__(self):
        return unicode(self.first) + ' ' + unicode(self.last) + ' :: ' + unicode(self.user.username) + ' ==> ' + unicode(self.user.email) + \
            ' -- ' + self.created.strftime('%Y-%m-%d %H:%M') + ' --  ' + unicode(self.city) + ', ' + unicode(self.state)

    def try_to_geocode(self):
        print('TRY_TO_GEOCODE_CALLED: trying to geocode!')
        send_mail('POSITION FIX', 'Fixing Position for: ' + self.user.username, 'closecalldatabase@gmail.com',
            ['ernest.ezis@gmail.com',], fail_silently=False)
        if self.zipcode != None:
            address = u"{} {} {} {}".format(self.city, self.state, self.zipcode, self.country)
        else:
            address = u"{} {} {}".format(self.city, self.state, self.country)
        pos = get_geocode(address)
        if pos != 'ERROR':
            print(pos)
            return pos
        else:
            return None


    def save(self, *args, **kwargs):
        self.city = self.city
        self.state = self.state
        self.country = self.country
        # AttributeError: NoneType object has no attribute strip
        self.zipcode = self.zipcode

        super(UserProfile, self).save(*args, **kwargs)

    def format_position(self):
        # UserProfile position is stored in a CharField, it looks like this
        # self.position = '(40.0149856, -105.27054559999999)'

        if self.position is None:
            print('FORMAT_POSITION: fixing missing geocode')
            self.position = self.try_to_geocode()
            if self.position:
                print('FORMAT_POSITION: saving missing geocode {}'.format(self.position))
                self.save()


        if self.position is None:
            s = "UserProfile " + str(self.pk) + " for " + self.user.username + " has no position information!"
            raise Exception(s)
            print(s)
            send_mail('CCDB-ERROR :: Profile Lacks Position!', s, 'closecalldatabase@gmail.com',
                ['closecalldatabase@gmail.com', 'ernest.ezis@gmail.com',], fail_silently=False)

            # *** FIX THIS ***
            # message . . . don't seem to have accurate position information for you
            # send to a page where they can update / confirm

        else:
        # pos = self.position
        # return pos.strip('()').split(',')
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
            print(m.what[:50], m.address)

        """
        matched_incidents = []
        # u_lat = self.get_lat()
        # u_lon = self.get_lon()
        u_lat, u_lon = self.get_lat_lon()
        # incidents = Incident.objects.all()
        incidents = Incident.objects.filter(visible=True)
        for i in incidents:
            if distance_between_geocoded_points(u_lat, u_lon, i.position.latitude, i.position.longitude) <= miles:
                matched_incidents.append(i)

        return matched_incidents


class UserBlogProfile(models.Model):
    up = models.OneToOneField(UserProfile, related_name="blogprofile", on_delete=models.CASCADE)
    byline = models.CharField(null=True, max_length=150, verbose_name="Byline (how your name should appear)")
    about_the_author = models.TextField(null=True, blank=True, verbose_name="If you want an 'About The Author' section")

    def __unicode__(self):
        return self.byline




# could add a text field that allowed multiple zipcode entries so that they could get
# notified in multiple jurisdictions