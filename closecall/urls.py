from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin

from core.views import HomeView

urlpatterns = patterns('',
    url(r"^$", HomeView, name="home"),
    url(r'^about/', TemplateView.as_view(template_name="about.html"), name="about"),
    url(r'^welcome/', TemplateView.as_view(template_name="welcome.html"), name="welcome"),

    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^incident/', include('incident.urls')),
    url(r'^eeadmin/', include(admin.site.urls)),

)
