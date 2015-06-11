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
            'first': forms.TextInput({'placeholder': 'use your real first name'}),
            'last': forms.TextInput({'placeholder': 'use your real last name'}),
            'city': forms.TextInput({'placeholder': 'NA if you live in a country lacking cities'}),
            'state': forms.TextInput({'placeholder': 'NY CA CO / Ontario / Victoria / etc'}),
            'zipcode': forms.TextInput({'placeholder': 'provide if you live in a big city'}),
            'country': forms.TextInput({'placeholder': 'United States, United Kingdom, France, etc'}),
        }



