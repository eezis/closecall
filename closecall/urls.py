from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
# from django.views.generic.base import RedirectView

from core.views import HomeView #, MyRegistrationView
from publish.views import NewsView
from users.views import CreateUserProfileView, UpdateUserProfileView, DetailUserProfileView, CheckForUserProfile


from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = patterns('',
    url(r"^$", HomeView, name="home"),
    url(r'^about/', TemplateView.as_view(template_name="about.html"), name="about"),
    url(r'^welcome/', TemplateView.as_view(template_name="welcome.html"), name="welcome"),
    url(r'^date-test/', TemplateView.as_view(template_name="date-test.html"), name="date-test"),

    # attempt to override registration so that it has first and last
    # url(r'^accounts/register/', MyRegistrationView.as_view(), name="register"),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^create-user-profile/$', CreateUserProfileView.as_view(), name='create-user-profile'),
    url(r'^user-profile-detail/(?P<pk>\d+)/$', DetailUserProfileView.as_view(), name='user-profile-detail'),
    url(r'^update-user-profile/(?P<pk>\d+)/$', UpdateUserProfileView.as_view(), name='update-user-profile'),
    # no parameter is given (catches the edge case where someone logs in, but they don't have a UserProfile created
    # which means something was broken in the registration process flow
    url(r'^user-profile-detail/$', CheckForUserProfile, name='check-profile-detail'),


    url(r'^incident/', include('incident.urls')),
    url(r'^news/', NewsView.as_view(), name="news"),
    url(r'^eeadmin/', include(admin.site.urls)),
    # url(r'^/static/(?P<path>.*)$', '/Users/eae/code/sites/closecall/static/'),
) # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()