from django.db import models
from django.contrib.auth.models import User
from geoposition.fields import GeopositionField

# Create your models here.

class Incident(models.Model):
    user = models.ForeignKey(User)
    # location = models.TextField(blank=True)
    address = models.CharField(null=True, blank=True, max_length=200)
    what = models.TextField(blank=True, verbose_name="Describe What Happened")
    date = models.DateField(null=True, blank=True, verbose_name="Date of Incident")
    time = models.TimeField(null=True, blank=True, verbose_name="Approximate Time of Incident")
    vehicle_description = models.CharField(null=True, blank=True, max_length=150, verbose_name="Vehicle Description")
    color = models.CharField(null=True, blank=True, max_length=30)
    make = models.CharField(null=True, blank=True, max_length=50)
    model = models.CharField(null=True, blank=True, max_length=50)
    license_certain = models.CharField(null=True, blank=True, max_length=20, verbose_name="License Plate (use this input field if you are certain of the plate's numbers)")
    license_uncertain = models.CharField(null=True, blank=True, max_length=150, verbose_name="License Plate (use this input field if you are pretty sure, but not 100 percent certain)")
    id_it_by = models.CharField(null=True, blank=True, max_length=250, verbose_name="List any special identifying characteristics of vehicle, if any" )
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    position = GeopositionField(null=True, blank=True)


    class Meta:
        verbose_name = "Incident"
        verbose_name_plural = "Incidents"
        ordering = ['-date']

    def __unicode__(self):
        return self.user.username + " " + self.what[:100]

