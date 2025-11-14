from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# View imports
from core.views import (
    HomeView, strava_registration, redirect_to_strava_login,
    redirect_to_strava_via_login_page, strava_complete_registration,
    CreateUserInput, show_user_map, SupportView
)
from publish.views import NewsView, news_preview, list_articles, show_article
from users.views import (
    CreateUserProfileView, UpdateUserProfileView, 
    DetailUserProfileView, CheckForUserProfile
)
from myregistration.forms import MyRegistrationForm
from myregistration.views import CloseCallRegistrationView
from incident.views import show_sample_report

# API imports
from api import views
from rest_framework import routers

# Create DRF router
router = routers.DefaultRouter()
router.register(r'api/v1/974fcb20-9458-48ae-b373-09de4885309a/incidents', views.IncidentViewSet)

urlpatterns = [
    # Home and basic pages
    path('', HomeView, name="home"),
    path('about/', TemplateView.as_view(template_name="about.html"), name="about"),
    path('welcome/', TemplateView.as_view(template_name="welcome.html"), name="welcome"),
    path('resources/', TemplateView.as_view(template_name="resources.html"), name="resources"),
    path('date-test/', TemplateView.as_view(template_name="date-test.html"), name="date-test"),

    # Sample incident report
    path('incident/show/CO-141108-001/', show_sample_report, name="show-sample-report"),

    # User authentication and profiles
    path('accounts/register/', CloseCallRegistrationView.as_view(form_class=MyRegistrationForm), name='registration_register'),
    path('accounts/', include('registration.backends.default.urls')),
    path('create-user-profile/', CreateUserProfileView.as_view(), name='create-user-profile'),
    re_path(r'^user-profile-detail/(?P<pk>\d+)/$', DetailUserProfileView.as_view(), name='user-profile-detail'),
    re_path(r'^update-user-profile/(?P<pk>\d+)/$', UpdateUserProfileView.as_view(), name='update-user-profile'),
    path('user-profile-detail/', CheckForUserProfile, name='check-profile-detail'),

    # App includes
    path('incident/', include('incident.urls', namespace='incident')),
    path('blog/', include('publish.urls')),
    path('news/', NewsView.as_view(), name="news"),

    # News and blog
    re_path(r'^preview-news/(?P<news_id>\d+)/$', news_preview, name="preview-news"),
    path('articles/', list_articles, name="list-articles"),
    re_path(r'^articles/(?P<slug>.*)/$', show_article, name="show-article"),

    # Admin and editor
    path('eeadmin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),

    # Strava integration
    path('strava-registration', strava_registration, name="strava-registration"),
    path('strava-complete-registration', strava_complete_registration, name="strava-complete-registration"),
    path('get-strava-login', redirect_to_strava_login, name="strava-login"),
    path('get-strava-login-from-login', redirect_to_strava_via_login_page, name="strava-login"),

    # Static pages
    path('login-help-page/', TemplateView.as_view(template_name='loginhelper.html'), name="login-helper"),
    re_path(r'^faq/?$', TemplateView.as_view(template_name='faq.html'), name="faq"),
    re_path(r'^support/?$', SupportView, name="support-ccdb"),
    path('smart-500/', TemplateView.as_view(template_name='smart-500.html'), name="smart-500"),
    path('privacy/', TemplateView.as_view(template_name='privacy.html'), name='privacy-policy'),

    # User input forms
    path('not-going-to-register/', CreateUserInput.as_view(subject='Non Registration'), name='non-register'),
    path('thank-you-for-your-input/', TemplateView.as_view(template_name='thank_you_for_your_input.html'), name='thank-you-for-input'),
    path('write-an-article/', CreateUserInput.as_view(subject='Write An Article'), name='write-article'),
    path('resource-referral/', CreateUserInput.as_view(subject='Resource Referral'), name='resource-referral'),
    path('contact-r/', CreateUserInput.as_view(subject='General Inquiry - Registered User'), name='contact-general-registered'),
    path('contact-u/', CreateUserInput.as_view(subject='General Inquiry UNREGISTERED User'), name='contact-general-unregistered'),

    # Maps
    re_path(r'^usermap/?$', show_user_map, name="home-user-map"),

    # API
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Testing
    re_path(r'^ajax-test/?$', TemplateView.as_view(template_name='test/ajax-test.html'), name="ajax-test"),

    # Robots.txt and ads.txt
    re_path(r'^robots\.txt$', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
    re_path(r'^ads\.txt$', TemplateView.as_view(template_name="ads.txt", content_type='text/plain')),
]

# Add static file serving
urlpatterns += staticfiles_urlpatterns()

# Error handlers
handler500 = "core.views.handler500"
handler404 = "core.views.handler404"
