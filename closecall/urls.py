from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
# from django.views.generic.base import RedirectView

from core.views import HomeView, strava_registration, redirect_to_strava_login, CreateUserInput #, MyRegistrationView
from publish.views import NewsView
from users.views import CreateUserProfileView, UpdateUserProfileView, DetailUserProfileView, CheckForUserProfile


from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


# I subclassed the registration.forms class RegistrationForm, so now I need to the the URL to use my form class
from myregistration.forms import MyRegistrationForm
from registration.views import RegistrationView
# url(r'^register/$',RegistrationView.as_view(form_class=MyRegistrationForm), name='registration_register'),


urlpatterns = patterns('',
    url(r"^$", HomeView, name="home"),
    url(r'^about/', TemplateView.as_view(template_name="about.html"), name="about"),
    url(r'^welcome/', TemplateView.as_view(template_name="welcome.html"), name="welcome"),
    url(r'^date-test/', TemplateView.as_view(template_name="date-test.html"), name="date-test"),

    # attempt to override registration so that it has first and last (this probably should have worked, probably need name='registration_register')
    # url(r'^accounts/register/', MyRegistrationView.as_view(), name="register"),

    # I subclassed the registration.forms class RegistrationForm, so now I need to the the URL to use my form class
    # *** didn't work, see note in myregistration.forms ***
    # url(r'^accounts/register/$',RegistrationView.as_view(form_class=MyRegistrationForm), name='registration_register'),
    # The line aboved needed to PRECEDE this next line, so that it's found first
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
    (r'^summernote/', include('django_summernote.urls')),
    # url(r'^strava-registration/(?P<strava_token>\w+)/$', strava_registration, name="strava-registration"),
    url(r'^strava-registration', strava_registration, name="strava-registration"),
    # url(r'^strava-registration/(?P<state>\w+)/$', strava_registration, name="strava-registration"),
    url(r'^get-strava-login', redirect_to_strava_login, name="strava-login"),
    url(r'^login-help-page/', TemplateView.as_view(template_name='loginhelper.html'), name="login-helper"),
    url(r'^faq/', TemplateView.as_view(template_name='faq.html'), name="faq"),
    url(r'^smart-500/', TemplateView.as_view(template_name='smart-500.html'), name="smart-500"),
    url(r'^not-going-to-register/', CreateUserInput.as_view(subject='Non Registration'), name='non-register'),
    url(r'^thank-you-for-your-input/',TemplateView.as_view(template_name='thank_you_for_your_input.html'), name='thank-you-for-input'),


    # url(r'^/static/(?P<path>.*)$', '/Users/eae/code/sites/closecall/static/'),
) # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()

handler500 = "core.views.handler500"
