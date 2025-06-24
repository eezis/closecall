from django import forms
from django.forms import ModelForm
# SelectDateWidget was moved from django.forms.extras to django.forms.widgets in Django 1.9+
# from django.forms.widgets import SelectDateWidget  # Not currently used

# from tinymce.widgets import TinyMCE
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django.core.exceptions import ValidationError

from .models import Incident

what_verbose_str = """
Now describe what happened. Be factual, include direction of travel for cyclists and vehicles. Here is an example: <p style="font-size:0.90em;margin-top:10px;margin-left:24px;
    margin-right:30px;">

    I was traveling southbound on Westminster Road, two other cyclists were riding immediately behind me. The driver of a white pickup truck, also traveling south,
    started to honk his horn at us . . . your specifics details . . . </p>
    <p style="font-size:0.90em;margin-top:10px;margin-left:24px;margin-right:30px;">There was very little traffic on the road at the time of the encounter. The lighting was good,
    all cyclists were inside the bike lane. </p>

    <p style="font-size:0.90em;margin-top:10px;margin-left:24px;margin-right:30px;"><i>
    <span style="color:red">If you know the identity and home address of the driver, please do not include that information
    in this report. You can email me that information (closecalldatabase@gmail.com) and I will include it in the non-public notes.</span></i>
    </p>

    <p style="font-size:0.90em;margin-top:10px;margin-left:24px;margin-right:30px;">
    <i>
    If you have <span style="color:red">VIDEO</span> do not enter it in this narrative section. Enter that information in the video section that follows.
    </i>
    </p>


Tell your story with enough context so that it can be understood by cyclists that were not there and may be unfamiliar with the location.
"""

video_verbose_str = """
<p><span style="color:red">VIDEO Section</span></p>
<p>If you have uploaded a video to <strong>youtube</strong>, then you should paste or type the URL into this field. If you have a video but have not uploaded it to youtube yet, then leave this field blank for now. Finish this form and submit it. Then come back and update your report with the URL after you have uploaded it.</p>
<p>If your video is at <strong>Vimeo</strong> or <strong>Facebook</strong> you can email the URL to me (wait for the email will arrive after you create your report). If you have a <span style="color:red">PICTURE</span> or two to accompany your report please email those as well (please resize them first).</p>
"""


class CreateIncidentForm(ModelForm):
    what_pholder ="""A good incident report will be factual and include date, time, and direction of travel of cyclists and motorists.

On November 11, 2014 at approximately 10:45 a.m., I was riding in a group of seven cyclists traveling east on Nelson Road. \
We heard a vehicle, also traveling east, approach from behind. As it got closer, we heard the driver rev the engine.

As the vehicle, a white pickup truck, passed by, someone threw a beer bottle out of the passenger side window. The bottle just \
missed striking one of the riders. We believe the license plate number was 163-JDK.
"""
    # this next line is for simple text input, so all the CRLFS get washed out, etc.
    # what = forms.CharField(widget = forms.Textarea(attrs={'placeholder': what_pholder, }), label='Describe What Happened (a detailed description about the incident)')
    # trying TinyMCE: http://django-tinymce.readthedocs.org/en/latest/usage.html#using-the-widget
    # content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    # what = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30, 'placeholder': what_pholder,}), label='Describe What Happened (a detailed description about the incident)')
    # what = forms.CharField(widget=TinyMCE(attrs={'placeholder': what_pholder,}), label='Describe What Happened (a detailed description about the incident)')
    # what = forms.CharField(widget=SummernoteWidget(attrs={'placeholder': what_pholder,}), label='Describe What Happened (a detailed description about the incident)')

    # "A good incident report should include \n Number of people in the party \n direction you were travelling in",}))
    date = forms.DateField(input_formats=["%m/%d/%Y"], widget=forms.DateInput(format="%m/%d/%Y", attrs={'class': 'datePicker',}), label='Date of Incident:')
    # time = forms.TimeField(("%H:%M %p",), widget=forms.TimeInput(format="%H:%M %p", attrs={'class': 'timePicker', 'id': 'timePicker',
    #     'placeholder': '10:45 am'}), label='Approximate Time') #, required=False)
    timestr = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '10:45 am'}), label='Approximate Time') #, required=False)

    class Meta:
        model = Incident
        labels = {
            "what": what_verbose_str,
            "license_certain" : "License Plate (use this input field if you are certain of the plate's numbers)",
            "license_uncertain" : "License Plate (use this input field if you are pretty sure, but not 100 percent certain)",
            'id_it_by' : 'List any special identifying characteristics of vehicle and passengers that you observed',
            'threat_assessment' : 'Threat Assessment: In your opinion the motorist/person in question was being . . .',
            'danger_assessment' : 'Danger Assessment: In your opinion, this encounter was . . .',
            'youtube_url' : video_verbose_str,
            'position': 'Address where the incident occurred',
        }
        # fields = ['position','what', 'date', 'time', 'witnesses', 'threat_assessment', 'danger_assessment', 'color', 'make', 'model', 'vehicle_description',
        # 'license_certain', 'license_uncertain', 'id_it_by', 'address', ]
        fields = ['position','what', 'date', 'timestr', 'youtube_url', 'witnesses', 'threat_assessment', 'danger_assessment', 'color', 'make', 'model', 'vehicle_description',
        'license_certain', 'license_uncertain', 'id_it_by', 'address', ]

        widgets={
            "what": SummernoteInplaceWidget(),

            # doesn't seem to have support for placeholder text?
            # "what": SummernoteInplaceWidget(attrs={
            #     'placeholder': 'test',
            #     }),

            "vehicle_description":forms.TextInput(attrs={
                'placeholder': 'White Pickup Truck | Black BMW coupe | etc',
            }),
            "witnesses":forms.TextInput(attrs={
                'placeholder':'[Your Name First] Bill E. Witness, bwitness@gmail.com (cyclist); Jane Sawit, 555-555-5555 (motorist); etc',
            }),
            "color":forms.TextInput(attrs={
                'placeholder':'the color of the vehicle in question',
            }),
            "make":forms.TextInput(attrs={
                'placeholder':'Ford | BMW | etc',
            }),
            "model":forms.TextInput(attrs={
                'placeholder':'Explorer | Tahoe | etc',
            }),
            "vehicle_description":forms.TextInput(attrs={
                'placeholder':'White Ford Ranger Pickup Truck (this will be the published description when people read your report)',
            }),
            "license_certain":forms.TextInput(attrs={
                'placeholder':'State/Province license plate number - if certain ( OR: 555-5555 )',
            }),
            "license_uncertain":forms.TextInput(attrs={
                'placeholder':'State/Province and license plate number - if not completely certain - ( OR: 555-5555 )',
            }),
            "id_it_by":forms.TextInput(attrs={
                'placeholder':'Dent in front right quarter panel, playboy mud flaps, etc',
            }),
            "youtube_url":forms.TextInput(attrs={
                'placeholder': 'youtube videos only -- if your video is at Vimeo or Facebook, wait for the email that confirms your report, then send it to me when you reply.',
            }),
            "address": forms.HiddenInput(attrs={
                'class': 'textinput',
                }),

        }

    def __init__(self, *args, **kwargs):
        super(CreateIncidentForm, self).__init__(*args, **kwargs)
        self.fields['vehicle_description'].required = True

    def clean(self):
        super(CreateIncidentForm, self).clean()
        cleaned_data = self.cleaned_data
        address = cleaned_data.get("address")
        if address == '1514-1542 Pleasant St, Boulder, CO 80302, USA':
            raise ValidationError("Please enter the 'Address where the incident occurred' -- see the field above the map and read the directions, in green, right above this message.")


"""
I want to be able to review and score the forms from the site
"""

class AdminScoreForm(ModelForm):

    class Meta:
        model = Incident
        fields = ('reviewed', 'accepted', 'visible', 'show_video', 'ee_show_video', 'utility', 'utility_comment',
            'video_offensive_votes')

# class FormFromSomeModel(forms.ModelForm):
#     class Meta:
#         model = SomeModel
#         widgets = {
#             'foo': SummernoteWidget(),
#             'bar': SummernoteInplaceWidget(),
#         }

        # exclude = ("published", )
        # widgets = {
        #     "date": SelectDateWidget(),
        #     "time": SelectDateWidget(),
        # }

        # # The 'datepicker' ties to the jqueryui script at the bottom of incident_form
        # widgets = {
        #     # 'date': forms.DateInput(attrs={'class':'datepicker'}),
        #     'date': forms.DateInput(attrs={'class':'datepicker', 'size': 10, 'id': 'datepicker', }),
        # }





