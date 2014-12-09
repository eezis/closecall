from django.db import models
from django.contrib.auth.models import User
from geoposition.fields import GeopositionField

# Create your models here.

class Incident(models.Model):
    user = models.ForeignKey(User)
    # location = models.TextField(blank=True)
    address = models.CharField(null=True, blank=True, max_length=200)
    what = models.TextField(verbose_name='Describe What Happened (be factual, include direction of travel for cyclists and vehicles, note witnesses, etc.)')
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

    # add threat_level should be options: Belligerent, Agressive, Unsure, Probably Accident (but worth recording)
    BELLIGERENT = 'Belligerent'
    THREATENING = 'Threatening'
    AGGRESSIVE  = 'Aggressive'
    CARELESS    = 'Careless'
    STUPID      = 'Thoughtless'

    TA_CHOICES = (
        (BELLIGERENT, 'Belligerent'),
        (THREATENING, 'Threatening'),
        (AGGRESSIVE,  'Aggressive'),
        (CARELESS,    'Careless'),
        (STUPID,      'Just Plain Stupid'),
    )

    tav = "Threat Assessment: In your opinion the motorist/person in question was being . . ."
    threat_assessment = models.CharField(null=True, max_length=50, choices=TA_CHOICES, default=AGGRESSIVE, verbose_name=tav)

    # add danger level
    EXTREMELY_DANGEROUS = 10
    VERY_DANGEROUS = 8
    DANGEROUS = 5
    SOMEWHAT_DANGEROUS = 3
    CONCERNING = 1

    THREAT_CHOICES = (
        (EXTREMELY_DANGEROUS, 'Extremely Dangerous - The action could have caused a fatility'),
        (VERY_DANGEROUS, 'Very Dangerous - The action could have caused serious injury or death'),
        (DANGEROUS, 'Dangerous - the action could have caused serious injury'),
        (SOMEWHAT_DANGEROUS, 'Somewhat Dangerous - the action could have caused moderate injuries'),
        (CONCERNING, 'The action was not very dangerous, but is still a cause for concern'),
    )
    dav = "Danger Assessment: In your opinion, this encounter was . . . "
    danger_assessment = models.IntegerField(null=True, choices=THREAT_CHOICES, default=DANGEROUS, verbose_name=dav)

    def incident_was_dangerous(self):
        return self.danger_assessment >= self.DANGEROUS

    def driver_is_considered_dangerous(self):
        return self.threat_assessment >= self.AGGRESSIVE

    def danger_level(self):
        levels = {
            # 10: 'Extremely Dangerous - The action could have caused a fatility',
            # 8: 'Very Dangerous - The action could have caused serious injury or death',
            # 5: 'Dangerous - the action could have caused serious injury',
            # 3: 'Somewhat Dangerous - the action could have caused moderate injuries',
            # 1: 'The action was not very dangerous, but is still a cause for concern',
            10: 'Extremely Dangerous',
            8: 'Very Dangerous',
            5: 'Dangerous',
            3: 'Somewhat Dangerous',
            1: 'Not Very Dangerous, But Still A Cause For Concern',
        }
        # print levels[8]
        return levels[self.danger_assessment]


    # def get_lat(self):
    #     return self.position.to_string()



    # def get_lon(self):
    #     return str(self.position).split(',')[1]


    """

    possible usage

    extremely_dangerous_incidents = Incident.objects.filter(danger_assessment=Incident.EXTREMELY_DANGEROUS)
    dangerous_incidents = Incident.objects.filter(danger_assessment__gte=Incident.SOMEWHAT_DANGEROUS)
    concerning_incidents = Incident.objects.filter(danger_assessment=Incident.CONCERNING)

    if incident_object.danger_assessment == Incident.EXTREMELY_DANGEROUS:
        # do something with live entry
    """
    class Meta:
        verbose_name = "Incident"
        verbose_name_plural = "Incidents"
        ordering = ['-date']

    def __unicode__(self):
        return self.user.username + " " + self.what[:100]



"""

Accident should be a big menu item, you report an incident or an accident . . .

"""

    # ACCIDENT = 'Accident'
    # INCIDENT = 'Incident'
    # accident_or_incident_choices = ((Accident, 'Accident'),(Incident, 'Incident'),)
    # accident_or_incident = models.CharField(null=True, max_length=20 verbose_name="Are you reporting an accident or an incident?")


    # def is_accident(self):
    #     return self.accident_or_incident in (self.ACCIDENT)

    # def is_incident(self):
    #     return self.accident_or_incident in (self.INCIDENT)







