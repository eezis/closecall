from django import forms
from django.contrib.auth.models import User
# from registration.forms import RegistrationForm
# from django.contrib.auth.forms import UserCreationForm

from django.forms import EmailField

class StravaEmailForm(forms.Form):
    """Form to collect email after Strava OAuth authentication"""
    email = forms.EmailField(
        label="Email Address",
        required=True,
        help_text="We'll use this to notify you about incidents in your area",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com',
            'autofocus': True,
        })
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "This email is already registered. Please use a different email or log in with your existing account."
            )
        return email

# class MyRegistrationForm(RegistrationForm):
#     first_name = forms.RegexField(regex=r'^[\w ]+$',
#                                 max_length=40,
#                                 label=("First Name"),
#                                 error_messages={'invalid': ("This value may contain only letters.")})

#     last_name = forms.RegexField(regex=r'^[\w ]+$',
#                                 max_length=40,
#                                 label=("First Name"),
#                                 error_messages={'invalid': ("This value may contain only letters.")})
#     # username = forms.RegexField(regex=r'^[\w.@+-]+$',
#     #                             max_length=30,
#     #                             label=("Username"),
#     #                             error_messages={'invalid': ("This value may contain only letters, numbers and @/./+/-/_ characters.")})
#     # email = forms.EmailField(label=("E-mail"))
#     # password1 = forms.CharField(widget=forms.PasswordInput,
#     #                             label=("Password"))
#     # password2 = forms.CharField(widget=forms.PasswordInput,
#     #                             label=("Password (again)"))

#     # NO EFFECT, THIS IS FOR MODELFORMS AND RegistrationForm is a forms.Form
#     # class Meta:
#     #     model = User
#     #     fields = ["first_name", "last_name", "username", "email", "password1", "password2",]



# # override https://github.com/django/django/blob/master/django/contrib/auth/forms.py#L71
# class EmailRegistrationForm(UserCreationForm):
#     # add an email field
#     email = EmailField(label=("Email address"), required=True, help_text=("Required."))

#     class Meta:
#         model = User
#         fields = ("first_name", "last_name", "username", "email", "password1", "password2")

#     def save(self, commit=True):
#         # print("Now saving")
#         user = super(UserCreationForm, self).save(commit=False)
#         # the next line has been added so that the email is captured and saved
#         user.email = self.cleaned_data["email"]
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user


