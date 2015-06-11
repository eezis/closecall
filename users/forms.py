# had to do this in order to have a hidden position field
from django import forms
from django.forms import ModelForm

from models import UserProfile

class UserProfileForm(ModelForm):

    class Meta:
        model = UserProfile
        fields = ['first', 'last', 'city', 'state', 'zipcode', 'country', 'email_incidents', 'position', ]

        # need position to be a hidden field so that it can be updated by Google Geocoder
        widgets={
            'position': forms.HiddenInput(),
            'First': forms.TextInput({'placeholder': 'use your real first name'}),
            'Last': forms.TextInput({'placeholder': 'use your real last name'}),
        }



