from __future__ import unicode_literals

from django import forms
from django.utils.translation import gettext_lazy as _
from registration.forms import RegistrationForm
from registration.users import UserModel


""" THIS DOESN'T WORK, THROWS NOT IMPLEMENTED enable the URLS entry to test further """


# class MyRegistrationForm(RegistrationForm):
#     # username = forms.RegexField(regex=r'^[\w.@+-]+$', max_length=30, label=_("Username"), error_messages={'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")})
#     username = forms.RegexField(regex=r'^[\w.@+ -]+$',
#                                 max_length=30,
#                                 label=_("Username "),
#                                 widget=forms.TextInput(attrs={'placeholder': 'Bob Hope or Bob-Hope-Jr, etc.'}),
#                                 error_messages={'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")})



"""
I sublcassed this and it was never called, I couldn't figure it out.
The trick was to use the prameter option of .as_view to specify which form to use in the URL entries
RegistrationView.as_view(form_class=MyRegistrationForm)

So it loads like this, and my entry needs to proceed the "include" for the registration app in the virtualenv

from myregistration.forms import MyRegistrationForm
from registration.views import RegistrationView

url(r'^accounts/register/$',RegistrationView.as_view(form_class=MyRegistrationForm), name='registration_register'),
url(r'^accounts/', include('registration.backends.default.urls')),



"""

class MyRegistrationForm(RegistrationForm):
    """
    Form for registering a new user account.
    Validates that the requested username is not already in use, and
    requires the password to be entered twice to catch typos.
    Subclasses should feel free to add any additional validation they
    need, but should avoid defining a ``save()`` method -- the actual
    saving of collected user data is delegated to the active
    registration backend.
    """
    required_css_class = 'required'

# I wanted to accept spaces
    username = forms.RegexField(
        regex=r'^[\w.@+ -]+$',
        max_length=30,
        label=_("Username"),
        error_messages={'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")},
    )
    email = forms.EmailField(label=_("E-mail"))
    email_confirm = forms.EmailField(
        required=False,
        label=_("Email"),
        widget=forms.EmailInput(
            attrs={
                'autocomplete': 'off',
                'tabindex': '-1',
                'aria-hidden': 'true',
                'class': 'hp-email-field',
            }
        ),
        help_text=_("Please leave this field blank."),
    )
    password1 = forms.CharField(widget=forms.PasswordInput,
                                label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label=_("Password (again)"))

    def __init__(self, *args, **kwargs):
        self.honeypot_hit = False
        super().__init__(*args, **kwargs)

    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.
        """
        existing = UserModel().objects.filter(username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError(_("A user with that username already exists."))
        else:
            return self.cleaned_data['username']

    def clean_email_confirm(self):
        """
        Honeypot field: any value indicates automated spam.
        """
        value = (self.cleaned_data.get('email_confirm') or '').strip()
        if value:
            self.honeypot_hit = True
        return ''

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data
