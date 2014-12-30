from django import forms
from django.forms import ModelForm
from django.forms.extras.widgets import SelectDateWidget

# from tinymce.widgets import TinyMCE
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

from models import Incident



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
    date = forms.DateField(("%m/%d/%Y",), widget=forms.DateInput(format="%m/%d/%Y", attrs={'class': 'datePicker',}), label='Date of Incident:',)
    time = forms.TimeField(("%H:%M %p",), widget=forms.TimeInput(format="%H:%M %p", attrs={'class': 'timePicker', 'id': 'timePicker',
        'placeholder': '10:45 am'}), label='Approximate Time') #, required=False)
    class Meta:
        model = Incident
        fields = ['position','what', 'date', 'time', 'witnesses', 'threat_assessment', 'danger_assessment', 'color', 'make', 'model', 'vehicle_description',
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
                'placeholder':'Bill E. Witness, bwitness@gmail.com (cyclist); Jane Sawit, 555-555-5555 (motorist); etc',
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
            "license_certain":forms.TextInput(attrs={
                'placeholder':'State/Province license plate number - if certain ( OR 555-55-5555 )',
            }),
            "license_uncertain":forms.TextInput(attrs={
                'placeholder':'State/Province and license plate number - if not completely certain - ( OR 555-55-5555 )',
            }),
            "id_it_by":forms.TextInput(attrs={
                'placeholder':'Dent in front right quarter panel, playboy mud flaps, etc',
            }),

            "address": forms.HiddenInput(),

        }


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





