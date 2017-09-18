from django.contrib import admin
from django import forms

# Register your models here.
from models import UserProfile, UserBlogProfile

# Register your models here.

class UserProfileAdminCustomization(forms.ModelForm):
    # class Meta:

    # I want to make the Position field in the admin optional to fill in because when some assclown puts
    # 'Denverish, CO' in there, I want to correct the Denver part then use the clustermap-data.py program to
    # fix the geocode rather than doing it by hand (it is a required field in the Model)
    def __init__(self, *args, **kwargs):
        # call the panent constructor
        super(UserProfileAdminCustomization, self).__init__(*args, **kwargs)
        # now a 'fields' property has been created so we can tweak it
        self.fields['position'].required = False


class UserProfileAdmin(admin.ModelAdmin):
    form = UserProfileAdminCustomization

    search_fields = ['first', 'last', 'country', 'city', 'user__email' ]
    list_filter = ('country', 'state',)

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserBlogProfile)
