from django.contrib import admin
from django import forms
from django.db import models

from incident.models import Incident


# field customizations

class IncidentAdminCustomization(forms.ModelForm):
    class Meta:
        # model = not needed it seems
        widgets = {
            'vehicle_description': forms.TextInput(attrs=
                {
                    'size': 140,
                    'placeholder': 'White Ford Ranger Pickup (this field will be published, please provide a good description)',
                },
            ),
            'id_it_by': forms.TextInput(attrs=
                {
                    'size': 140,
                    'placeholder': 'Dent in right quarter panel, playboy mud flaps, etc',
                    'label': 'Identifying Characteristics'
                },

            ),
        }

# admin

class IncidentAdmin(admin.ModelAdmin):
    form = IncidentAdminCustomization

    search_fields = ['user__last_name', 'user__email', 'address', 'what', 'license_certain', 'license_uncertain',]
    # list_filter = ('user',) <-- this makes an exhaustive list with every user, I so make that a search rather than filter
    list_display = ('id', 'user', 'date', 'address', 'position', 'reviewed', 'license_certain', 'license_uncertain')
    fields = (
        ('user', 'address'),
        'what',
        ('reviewed', 'accepted', 'visible', 'closedfirstloop'),
        # ('date', 'time', 'timestr'),
        'date',
        # 'time',
        'timestr',
        ('color', 'make', 'model'),
        'vehicle_description',
        ('license_certain', 'license_uncertain'),
        'id_it_by',
        ('latitude', 'longitude'),
        'position',
        'witnesses',
        'internal_note',
        ('reported', 'cited'),
        'cited_note',
        'warned',
        'warned_note',
        'email_sent',
        'email_text',
        'email_sent_on',
        'pending',
        'pending_note',
        'threat_assessment',
        'danger_assessment',
        )

    ordering = ('-created',)

    # formfield_overrides = {
    #     models.TextField: {'widget': forms.TextInput(attrs={'size': '60'})},
    # }

admin.site.register(Incident, IncidentAdmin)




