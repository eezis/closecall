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
            'first': forms.TextInput(attrs={
                'placeholder': 'John',
                'class': 'form-control',
                'aria-required': 'true'
            }),
            'last': forms.TextInput(attrs={
                'placeholder': 'Smith',
                'class': 'form-control',
                'aria-required': 'true'
            }),
            'city': forms.TextInput(attrs={
                'placeholder': 'Denver',
                'class': 'form-control',
                'aria-required': 'true'
            }),
            'state': forms.TextInput(attrs={
                'placeholder': 'Colorado',
                'class': 'form-control',
                'aria-required': 'true'
            }),
            'zipcode': forms.TextInput(attrs={
                'placeholder': '80202',
                'class': 'form-control',
                'aria-required': 'true'
            }),
            'country': forms.TextInput(attrs={
                'placeholder': 'United States',
                'class': 'form-control',
                'aria-required': 'true',
                'autocomplete': 'country-name'
            }),
        }

    def clean(self):
        """
        Validate that city, state, and country are provided for accurate geocoding.
        City-states like Singapore, Monaco, etc. don't need separate city/state values.
        """
        cleaned_data = super().clean()
        city = cleaned_data.get('city')
        state = cleaned_data.get('state')
        country = cleaned_data.get('country')

        errors = []

        # Country is always required
        if not country or country.strip() == '':
            errors.append(ValidationError(
                "Please enter your country. This is required for geocoding your location.",
                code='country_required'
            ))

        # Check if city/state are missing
        city_is_missing = not city or city.strip() == '' or city.strip().upper() == 'NA'
        state_is_missing = not state or state.strip() == '' or state.strip().upper() == 'NA'

        # For non-city-states, require both city and state
        if country:
            is_city_state = any(
                cs.lower() in country.lower()
                for cs in CITY_STATE_COUNTRIES
            )

            if not is_city_state:
                if city_is_missing:
                    errors.append(ValidationError(
                        "Please enter your city. This is needed for accurate incident notifications. "
                        "If you live in a country without cities, please enter 'NA' in the city field.",
                        code='city_required'
                    ))

                if state_is_missing:
                    errors.append(ValidationError(
                        "Please enter your state/province/region. This is needed for accurate incident notifications. "
                        "If you live in a country without states, please enter 'NA' in the state field.",
                        code='state_required'
                    ))

        if errors:
            raise ValidationError(errors)

        return cleaned_data



