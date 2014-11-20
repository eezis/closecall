from django.conf.urls import patterns, url
from views import CreateIncidentView, ListIncidentView, DetailIncidentView, UpdateIncidentView, DeleteIncidentView

urlpatterns = patterns('',
    url(r'^list/$', ListIncidentView.as_view(), name='users-incident-list'),
    url(r'^create/$', CreateIncidentView.as_view(), name='create-incident'),
    url(r'^detail/(?P<pk>\d+)/$', DetailIncidentView.as_view(), name='incident-detail'),
    url(r'^update/(?P<pk>\d+)/$', UpdateIncidentView.as_view(), name='update-incident'),
    url(r'^delete/(?P<pk>\d+)/$', DeleteIncidentView.as_view(), name='delete-incident'),
    )
