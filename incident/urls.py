from django.conf.urls import patterns, url
from views import CreateIncidentView, ListIncidentView, DetailIncidentView, UpdateIncidentView, DeleteIncidentView

urlpatterns = patterns('',
    url(r'^list/$', ListIncidentView.as_view(), name='users-incident-list'),
    url(r'^create/$', CreateIncidentView.as_view(), name='create-incident'),
    url(r'^detail/(?P<pk>\d+)/$', DetailIncidentView.as_view(), name='incident-detail'),
    url(r'^update/(?P<pk>\d+)/$', UpdateIncidentView.as_view(), name='update-incident'),
    url(r'^delete/(?P<pk>\d+)/$', DeleteIncidentView.as_view(), name='delete-incident'),
    # this is for showing incidents that I wish to expose for a special reason (like link to it from a news story)
    # the linking mecanims fake-2934 = incident.pk is mapped manually (for now) in a dictionary in the view
    url(r'^show/([a-z0-9-]{8})/$', 'incident.views.show_this_incident', name="show-specific-incident"),
    )

