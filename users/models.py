from django.db import models
from django.contrib.auth.models import User
from core.models import BaseFields

class UserProfile(BaseFields):
    user = models.OneToOneField(User, related_name='profile')
    first = models.CharField(null=True, max_length=50)
    last = models.CharField(null=True, max_length=50)
    city = models.CharField(null=True, max_length=120)
    state = models.CharField(null=True, blank=True, max_length=50)
    country = models.CharField(null=True, max_length=80)
    zipcode = models.CharField(null=True, blank=True, max_length=30, verbose_name="Zip/Postal Code")
    # does the user want email notifications when new incidents are reported in their area?
    email_incidents = models.BooleanField(default=True, verbose_name="Email Me When Incidents Are Reported In My Area")
    # sms_incidents = models.BooleanField(deault=True, verbose_name="Receive")
    # sms would require phone numbers

    def __unicode__(self):
        return self.first + ' ' + self.last + ' :: ' + self.user.username


# could add a text field that allowed multiple zipcode entries so that they could get
# notified in multiple jurisdictions