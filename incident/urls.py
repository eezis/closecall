from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from views import CreateIncidentView, ListIncidentView, DetailIncidentView, UpdateIncidentView, DeleteIncidentView, show_all_incidents

urlpatterns = patterns('',
    url(r'^list/$', ListIncidentView.as_view(), name='users-incident-list'),
    url(r'^create/$', CreateIncidentView.as_view(), name='create-incident'),
    url(r'^detail/(?P<pk>\d+)/$', DetailIncidentView.as_view(), name='incident-detail'),
    url(r'^update/(?P<pk>\d+)/$', UpdateIncidentView.as_view(), name='update-incident'),
    url(r'^delete/(?P<pk>\d+)/$', DeleteIncidentView.as_view(), name='delete-incident'),
    # this is for showing incidents that I wish to expose for a special reason (like link to it from a news story)
    # the linking mecanims fake-2934 = incident.pk is mapped manually (for now) in a dictionary in the view
    # url(r'^show/([A-Z0-9-]{13})/$', 'incident.views.show_this_incident', name="show-specific-incident"),
    url(r'^show/([\w|\W|-|0-9]{10,50})/$', 'incident.views.show_this_incident', name="show-specific-incident"),
    # url(r'^show-detail/(?P<pk>\d+)/$', 'incident.views.show_this_incident_for_authed_users', name="show-specific-incident"),
    url(r'^show-detail/(?P<incident_id>\d+)/$', 'incident.views.show_this_incident_for_authed_users', name="show-specific-incident"),
    url(r'^reporting-step-1/$', TemplateView.as_view(template_name="incident/reporting-step-1.html") , name="reporting-1"),
    url(r'^all-incidents/?$', show_all_incidents, name="show-all-incidents"),

    )

