from django.contrib import admin

from incident.models import Incident

# Register your models here.

class IncidentAdmin(admin.ModelAdmin):
    search_fields = ['user__last_name', 'user__email', 'what',]
    # list_filter = ('user',) <-- this makes an exhaustive list with every user, I so make that a search rather than filter
    ordering = ('-created',)

admin.site.register(Incident, IncidentAdmin)




