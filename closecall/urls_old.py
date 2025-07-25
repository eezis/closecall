from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
# from django.views.generic.base import RedirectView

from core.views import HomeView, strava_registration, redirect_to_strava_login, redirect_to_strava_via_login_page, CreateUserInput, \
show_user_map, SupportView #, MyRegistrationView
from publish.views import NewsView, news_preview
from users.views import CreateUserProfileView, UpdateUserProfileView, DetailUserProfileView, CheckForUserProfile

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# I subclassed the registration.forms class RegistrationForm, so now I need to the the URL to use my form class
from myregistration.forms import MyRegistrationForm
from registration.views import RegistrationView
# url(r'^register/$',RegistrationView.as_view(form_class=MyRegistrationForm), name='registration_register'),

from incident.views import show_sample_report

#djangorestframework
from api import views
from api.views import IncidentViewSet
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'api/v1/974fcb20-9458-48ae-b373-09de4885309a/incidents', views.IncidentViewSet)

urlpatterns = patterns('',
    url(r"^$", HomeView, name="home"),
    url(r'^about/', TemplateView.as_view(template_name="about.html"), name="about"),
    url(r'^welcome/', TemplateView.as_view(template_name="welcome.html"), name="welcome"),
    url(r'^resources/', TemplateView.as_view(template_name="resources.html"), name="resources"),
    url(r'^date-test/', TemplateView.as_view(template_name="date-test.html"), name="date-test"),

    url(r'^incident/show/CO-141108-001/', show_sample_report, name="show-sample-report"),

    # attempt to override registration so that it has first and last (this probably should have worked, probably need name='registration_register')
    # url(r'^accounts/register/', MyRegistrationView.as_view(), name="register"),

    # I subclassed the registration.forms class RegistrationForm, so now I need to the the URL to use my form class
    # *** didn't work, see note in myregistration.forms ***
    # url(r'^accounts/register/$',RegistrationView.as_view(form_class=MyRegistrationForm), name='registration_register'),
    # The line above needed to PRECEDE this next line, so that it's found first
    url(r'^accounts/', include('registration.backends.default.urls')),
    # simple skips the email verification
    # url(r'^accounts/', include('registration.backends.simple.urls')),

    url(r'^create-user-profile/$', CreateUserProfileView.as_view(), name='create-user-profile'),
    url(r'^user-profile-detail/(?P<pk>\d+)/$', DetailUserProfileView.as_view(), name='user-profile-detail'),
    url(r'^update-user-profile/(?P<pk>\d+)/$', UpdateUserProfileView.as_view(), name='update-user-profile'),
    # no parameter is given (catches the edge case where someone logs in, but they don't have a UserProfile created
    # which means something was broken in the registration process flow
    url(r'^user-profile-detail/$', CheckForUserProfile, name='check-profile-detail'),

    url(r'^incident/', include('incident.urls', namespace='incident')),
    url(r'^blog/', include('publish.urls')),
    url(r'^news/', NewsView.as_view(), name="news"),
    # url(r'^support/?$', SupportView, name="support"),


    url(r'^preview-news/(?P<news_id>\d+)/$', news_preview, name="preview-news"),
    url(r'^eeadmin/', include(admin.site.urls)),
    (r'^summernote/', include('django_summernote.urls')),
    # url(r'^strava-registration/(?P<strava_token>\w+)/$', strava_registration, name="strava-registration"),
    url(r'^strava-registration', strava_registration, name="strava-registration"),
    # url(r'^strava-registration/(?P<state>\w+)/$', strava_registration, name="strava-registration"),
    url(r'^get-strava-login', redirect_to_strava_login, name="strava-login"),
    url(r'^get-strava-login-from-login', redirect_to_strava_via_login_page, name="strava-login"),
    url(r'^login-help-page/', TemplateView.as_view(template_name='loginhelper.html'), name="login-helper"),
    url(r'^faq/?$', TemplateView.as_view(template_name='faq.html'), name="faq"),
    url(r'^support/?$', TemplateView.as_view(template_name='support-ccdb.html'), name="support-ccdb"),
    url(r'^smart-500/', TemplateView.as_view(template_name='smart-500.html'), name="smart-500"),
    url(r'^not-going-to-register/', CreateUserInput.as_view(subject='Non Registration'), name='non-register'),
    url(r'^thank-you-for-your-input/',TemplateView.as_view(template_name='thank_you_for_your_input.html'), name='thank-you-for-input'),
    url(r'^articles/$','publish.views.list_articles', name="list-articles"),
    url(r'^articles/(?P<slug>.*)/$','publish.views.show_article', name="show-article"),
    # write the following view, pattern it on preview-news above
    #url(r'^preview-articles/(?P<slug>.*)/$', article_preview, name="preview-article"),
    url(r'^privacy/',TemplateView.as_view(template_name='privacy.html'), name='privacy-policy'),
    url(r'^write-an-article/', CreateUserInput.as_view(subject='Write An Article'), name='write-article'),
    url(r'^resource-referral/', CreateUserInput.as_view(subject='Resource Referral'), name='resource-referral'),
    url(r'^contact-r/', CreateUserInput.as_view(subject='General Inquiry - Registered User'), name='contact-general-registered'),
    url(r'^contact-u/', CreateUserInput.as_view(subject='General Inquiry UNREGISTERED User'), name='contact-general-unregistered'),
    url(r'^usermap/?$', show_user_map, name="home-user-map"),
    # url(r'^clustered-user-map/?$', TemplateView.as_view(template_name='user-new-map.html'), name="home-new-user-map"),
    # url(r'^clustered-user-map/?$', TemplateView.as_view(template_name='user-new-map.html'), name="home-user-map"),
    # show all incidents is in the incident.url

    # over to djangorest framework
    url(r'^', include(router.urls)),
    # url(r'^api/', include('api.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^ajax-test/?$', TemplateView.as_view(template_name='test/ajax-test.html'), name="ajax-test"),

    # url(r'^/static/(?P<path>.*)$', '/Users/eae/code/sites/closecall/static/'),
) # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += [
    url(r'^robots\.txt$', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
]

handler500 = "core.views.handler500"
handler404 = "core.views.handler404"
