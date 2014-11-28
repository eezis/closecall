from django.db import models
from django.contrib.auth.models import User
from geoposition.fields import GeopositionField

# Create your models here.

class Incident(models.Model):
    user = models.ForeignKey(User)
    # location = models.TextField(blank=True)
    address = models.CharField(null=True, blank=True, max_length=200)
    what = models.TextField(blank=True, help_text="Describe the where, what, and when of the incident",
        verbose_name="Describe What Happened")
    date = models.DateField(null=True, blank=True, verbose_name="Date of Incident")
    time = models.TimeField(null=True, blank=True, verbose_name="Approximate Time of Incident")
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    position = GeopositionField(null=True, blank=True)


    class Meta:
        verbose_name = "Incident"
        verbose_name_plural = "Incidents"
        ordering = ['created']

    def __unicode__(self):
        return self.user.username + " " + self.what[:100]

