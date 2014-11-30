from django.db import models
from django.contrib.auth.models import User
from core.models import BaseFields

class UserProfile(BaseFields):
    user = models.OneToOneField(User, related_name='profile')
    first = models.CharField(null=True, blank=True, max_length=50)
    last = models.CharField(null=True, blank=True, max_length=50)
    city = models.CharField(null=True, blank=True, max_length=120)
    state = models.CharField(null=True, blank=True, max_length=50)
    country = models.CharField(null=True, blank=True, max_length=50)
    zipcode = models.CharField(null=True, blank=True, max_length=30)
    email_incidents = models.BooleanField(default=True, verbose_name="Send Email When Incidents Occur In Your Area")
    # sms_incidents = models.BooleanField(deault=True, verbose_name="Receive")
    # sms would require phone numbers



# could add a text field that allowed multiple zipcode entries so that they could get
# notified in multiple jurisdictions