from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
from django.views.generic.base import RedirectView

from core.views import HomeView
from publish.views import NewsView

urlpatterns = patterns('',
    url(r"^$", HomeView, name="home"),
    url(r'^accounts/profile/', RedirectView.as_view(url='/')),
    url(r'^about/', TemplateView.as_view(template_name="about.html"), name="about"),
    url(r'^welcome/', TemplateView.as_view(template_name="welcome.html"), name="welcome"),

    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^incident/', include('incident.urls')),
    # url(r'^news/', TemplateView.as_view(template_name="publish/news.html"), name="news"),
    url(r'^news/', NewsView.as_view(), name="news"),

    url(r'^eeadmin/', include(admin.site.urls)),
)
