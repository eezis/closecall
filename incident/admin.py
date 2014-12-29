from django.contrib import admin

from incident.models import Incident

# Register your models here.

class IncidentAdmin(admin.ModelAdmin):
    # search_fields = ['first', 'last', 'country',]
    list_filter = ('user',)
    ordering = ('-created',)

admin.site.register(Incident, IncidentAdmin)




