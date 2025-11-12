# had to do this in order to have a hidden position field
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError

from .models import UserProfile

# City-states and small countries that don't have cities (or city is same as country)
CITY_STATE_COUNTRIES = [
    'Singapore',
    'Monaco',
    'San Marino',
    'Vatican City',
    'Vatican',
]

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
            'zipcode': forms.TextInput({'placeholder': 'Needed for accurate notifications'}),
            'country': forms.TextInput({'placeholder': 'United States, United Kingdom, France, etc'}),
        }

    def clean(self):
        """
        Validate that city is provided for countries that have cities.
        City-states like Singapore, Monaco, etc. don't need a city value.
        """
        cleaned_data = super().clean()
        city = cleaned_data.get('city')
        country = cleaned_data.get('country')

        # Check if city is missing or just whitespace or "NA"
        city_is_missing = not city or city.strip() == '' or city.strip().upper() == 'NA'

        if city_is_missing and country:
            # Check if country is a city-state where city is not applicable
            is_city_state = any(
                cs.lower() in country.lower()
                for cs in CITY_STATE_COUNTRIES
            )

            if not is_city_state:
                raise ValidationError(
                    "Please enter your city. This is needed for accurate incident notifications. "
                    "If you live in a country without cities, please enter 'NA' in the city field."
                )

        return cleaned_data



