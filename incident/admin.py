from django.contrib import admin

from incident.models import Incident

# Register your models here.

class IncidentAdmin(admin.ModelAdmin):
    search_fields = ['user__last_name', 'user__email', 'what',]
    # list_filter = ('user',) <-- this makes an exhaustive list with every user, I so make that a search rather than filter

    fields = (
        ('user', 'address', 'visible'),
        'what',
        ('reviewed', 'accepted', 'closedfirstloop'),
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

admin.site.register(Incident, IncidentAdmin)




