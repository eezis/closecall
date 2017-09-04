from django.db import models
from django.contrib.auth.models import User
from geoposition.fields import GeopositionField
from geoposition import Geoposition
from utils import get_youtube_embed_str

# Create your models here.

class Incident(models.Model):
    user = models.ForeignKey(User)
    # location = models.TextField(blank=True)
    address = models.CharField(null=True, max_length=200)
    # what = models.TextField(verbose_name='Describe What Happened (be factual, include direction of travel for cyclists and vehicles. Example: I was traveling southbound on Westminster Road, two other cyclists were riding immediately behind me. A white pickup, also traveling south . . .<br> test)')
    what = models.TextField(verbose_name="What Happened")
    date = models.DateField(null=True, blank=True, verbose_name="Date of Incident")
    time = models.TimeField(null=True, blank=True, verbose_name="Approximate Time of Incident")
    # create a proxy string to ensure proper migration of TimeField to a String Version
    timestr = models.CharField(null=True, blank=True, max_length=50, verbose_name="Approximate Time of Incident")
    vehicle_description = models.CharField(null=True, blank=True, max_length=150, verbose_name="Vehicle Description -- please fill this out!")
    color = models.CharField(null=True, blank=True, max_length=30)
    make = models.CharField(null=True, blank=True, max_length=50)
    model = models.CharField(null=True, blank=True, max_length=50)
    license_certain = models.CharField(null=True, blank=True, max_length=20, verbose_name="License Plate - CERTAIN")
    license_uncertain = models.CharField(null=True, blank=True, max_length=150, verbose_name="License Plate - UNCERTAIN")
    # this went into production with incident ID 548 -- it is a convenience field
    # and would not be reliable unless the first 500 entries were rechecked and
    # this field was updated
    # licnese_confirmd = models.BooleanField(default=False)
    id_it_by = models.CharField(null=True, blank=True, max_length=250, verbose_name="Identifying Characteristics" )
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    # this will initialize the first drawing of the map

    # THIS FIELD WILL NOT MIGRATE
    # ValueError: Cannot serialize: Geoposition(40.008682,-105.272883)
    # There are some values Django cannot serialize into migration files.
    # For more, see https://docs.djangoproject.com/en/dev/topics/migrations/#migration-serializing

    # To fix change and migrate this model, you must UNCOMMENT the
    # position = GeopositionField(null=True) line found below
    # AND COMMENT the production line that sets the default
    # position = GeopositionField(default=Geoposition(40.008682, -105.272883))
    # do the makemigration and migrate, then reverse the comments to reset to original
    # state (the next line commented, the trailing line -- setting default to 40.00.., -105.. --uncommented)
    # position = GeopositionField(null=True)
    position = GeopositionField(default=Geoposition(40.008682, -105.272883))
    # I am adding these to support the API, should have added them at the outset, 12/4/15
    # override save method, set them there
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    witnesses = models.CharField(null=True, blank=True, max_length=255, verbose_name="Your Name and Names of other Witnesses ( this field is not published )")
    # sadly had to add this because some folks are having trouble writing
    # a useful and literate report -- I can turn it off from the admin
    visible = models.BooleanField(default=True)
    reported = models.BooleanField(default=False) # Reported/Flagged Set visible to False if a user says this is spam or false or abusive, etc.
    cited = models.BooleanField(default=False)
    cited_note = models.TextField(null=True, blank=True)

    warned = models.BooleanField(default=False)
    warned_note = models.TextField(null=True, blank=True)

    reviewed = models.BooleanField(default=False)  # added to help me keep track of workflow
    accepted = models.BooleanField(default=True)   # if not accepted, waiting for more info

    email_sent = models.BooleanField(default=False)
    email_text = models.TextField(null=True, blank=True)
    email_sent_on = models.DateTimeField(null=True, blank=True)

    internal_note = models.TextField(null=True, blank=True)

    reviewed = models.BooleanField(default=False)
    accepted = models.BooleanField(default=True)
    # reviewed, clarified if needed, emails sent if merited
    closedfirstloop = models.BooleanField(default=False)

    pending = models.BooleanField(default=False)
    pending_note = models.TextField(null=True, blank=True)

    # added by EE on 8/21/17, modified 9/4/2017
    youtube_url = models.CharField(null=True, blank=True, max_length=180)
    vimeo_url = models.CharField(null=True, blank=True, max_length=180)
    facebook_url = models.CharField(null=True, blank=True, max_length=180)
    video_embed_string = models.TextField(blank=True)
    # allow users to vote offensive -- if someone posts porn or something . . .
    video_offensive_votes = models.IntegerField(default=0)
    # make the video invisible if too many find it offensive
    show_video = models.BooleanField(default=True)
    # allows EE to override input from sensitrons
    ee_show_video = models.BooleanField(default=False)

    utility = models.DecimalField(null=True, default=0.00, max_digits=4, decimal_places=2)
    # brief reason/descriptino
    utility_comment = models.CharField(null=True, blank=True, max_length=255, verbose_name="Utility Comment")
    # e.g. "California, can't use the video" "No plate, unsure of model of truck" "Unclear language, cannot visualize what happened"
    utility_defect = models.CharField(null=True, blank=True, max_length=255, verbose_name="Utility Defect")
    # Driver fault :: 1 - 10 . . . 10 is driver completely utterly inexcusably wrong
    driver_fault = models.IntegerField(blank=True, null=True)
    # Might not use but added
    has_video = models.BooleanField(default=False)
    has_pic = models.BooleanField(default=False)




    # Commercially Licensed Driver

    # speedlimit
    # youtube
    # police_were_contacted? Why/Why not?
    # police notes?


    # add threat_level should be options: Belligerent, Agressive, Unsure, Probably Accident (but worth recording)
    BELLIGERENT = 'Belligerent'
    THREATENING = 'Threatening'
    AGGRESSIVE  = 'Aggressive'
    CARELESS    = 'Careless'
    STUPID      = 'Thoughtless'

    TA_CHOICES = (
        (BELLIGERENT, 'Belligerent - the driver was malicious and undertook deliberate actions that purposefully put lives at risk'),
        (THREATENING, 'Threatening - the driver create a dangerous situation and delivered a measured threat (close, but not too close)'),
        (AGGRESSIVE,  'Aggressive - the driver was trying to scare, harass or intimidate (yelled, honked, etc)'),
        (CARELESS,    'Careless - the driver caused a problem but it wasn''t deliberately hostile and may have been accidental'),
        (STUPID,      'Just Plain Stupid'),
    )

    tav = "Threat Assessment"
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
    dav = "Danger Assessment"
    danger_assessment = models.IntegerField(null=True, choices=THREAT_CHOICES, default=DANGEROUS, verbose_name=dav)


    def save(self, *args, **kwargs):
        try:
            # position is of type GEO Position, so might have to cast this?
            self.latitude = self.position.latitude
            self.longitude = self.position.longitude
            if self.youtube_url:
                video_embed_string = get_youtube_embed_str(self.youtube_url)
                print "EMBED: {}".format(video_embed_string)
        except:
            pass

        super(Incident, self).save(*args, **kwargs)


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


    # In [97]: I.position.longitude
    # Out[97]: Decimal('-105.1886354914489')

    def get_lat(self):
        return str(self.position.latitude)


    def get_lon(self):
        return str(self.position.longitude)


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







