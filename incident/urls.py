from django.urls import path, re_path
from django.views.generic import TemplateView
from .views import (
    CreateIncidentView, ListIncidentView, DetailIncidentView, 
    UpdateIncidentView, DeleteIncidentView, show_all_incidents,
    show_this_incident, show_this_incident_for_authed_users, admin_score
)

app_name = 'incident'

urlpatterns = [
    path('list/', ListIncidentView.as_view(), name='users-incident-list'),
    path('create/', CreateIncidentView.as_view(), name='create-incident'),
    re_path(r'^detail/(?P<pk>\d+)/$', DetailIncidentView.as_view(), name='incident-detail'),
    re_path(r'^update/(?P<pk>\d+)/$', UpdateIncidentView.as_view(), name='update-incident'),
    re_path(r'^delete/(?P<pk>\d+)/$', DeleteIncidentView.as_view(), name='delete-incident'),
    
    # For showing incidents that are exposed for special reasons (like news story links)
    # The linking mechanism fake-2934 = incident.pk is mapped manually in a dictionary in the view
    re_path(r'^show/(?P<ee_fake_key>[\w|\W|-|0-9]{10,50})/?$', show_this_incident, name="show-specific-incident"),
    re_path(r'^show-detail/(?P<incident_id>\d+)/$', show_this_incident_for_authed_users, name="show-specific-incident"),
    
    path('reporting-step-1/', TemplateView.as_view(template_name="incident/reporting-step-1.html"), name="reporting-1"),
    re_path(r'^all-incidents/?$', show_all_incidents, name="show-all-incidents"),
    re_path(r'^score/(?P<pk>\d+)/$', admin_score, name='admin-scoring'),
]