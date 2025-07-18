"""
Django settings for cc project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

# Admins get 500 errors
ADMINS = (
    (('Ernest', 'ernest.ezis@gmail.com'), ('CCDB Admi', 'closecalldatabase@gmail.com'),)
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '[REDACTED - MOVED TO ENVIRONMENT VARIABLES]'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
DEV_MODE = False

TEMPLATE_DEBUG = True

# ALLOWED_HOSTS = ['*', '104.131.56.181', '.closecalldatabase.com', '127.0.0.1', 'localhost', 'closecall', ]
# ALLOWED_HOSTS = ['*', ]
# ALLOWED_HOSTS = ['.closecalldatabase.com', '127.0.0.1', ]
ALLOWED_HOSTS = ['.closecalldatabase.com', '127.0.0.1', 'strava.com', '104.131.56.18', '104.131.56.181']

# this is set by the second so 60 * 5 = 5 minutes
# fifteen months - I went from 3 months to 15 on 12/3/15
# because some users have a hard time managing their logins
SESSION_COOKIE_AGE = 60 * 60 * 24 * 30 * 15


GEOPOSITION_MAP_OPTIONS = {
    'minZoom': 3,
    'maxZoom': 15,
}

GEOPOSITION_MARKER_OPTIONS = {
    'cursor': 'move'
}



# https://docs.djangoproject.com/en/1.7/ref/settings/#template-context-processors
# must add manually if you are going to then add your own
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    )

TEMPLATE_CONTEXT_PROCESSORS += (
    'publish.views.AnnouncementView',
)

# Application definition

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # needed for enabling the Site object (used by Django Registration Redux)
    # add this, set SITE_ID = 1
    # migrate (no makemigration needed) https://docs.djangoproject.com/en/1.7/ref/contrib/sites/
    # then use the admin to set it.
    'django.contrib.sites',
    'django.contrib.redirects',
)

SITE_ID = 1

THIRD_PARTY_APPS = (
    'django_extensions',
    'crispy_forms',
    'geoposition',
    'registration', #django-registration-redux 1.1
    'django_summernote',  #editor
    'rest_framework',
)

CRISPY_TEMPLATE_PACK = 'bootstrap3'

# LOCAL_APPS = ('core', incident', 'authentication')
LOCAL_APPS = (
    'core',
    'incident',
    'publish',
    'users',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# This is for Django-Registration-Redux
ACCOUNT_ACTIVATION_DAYS = 14  # One-week activation window; you may, of course, use a different value.
REGISTRATION_AUTO_LOGIN = True  # Automatically log the user in.
LOGIN_REDIRECT_URL = '/'


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
)

ROOT_URLCONF = 'closecall.urls'

WSGI_APPLICATION = 'closecall.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'closecall',
        'USER': 'eaecc',
        'PASSWORD': '[REDACTED - USE ENVIRONMENT VARIABLES]',
        'HOST': '127.0.0.1', # Leave blank for socket connection
        'PORT': '', # default postgres port is 5432 for the curious
        'CONN_MAX_AGE': 300,
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

# STATIC_URL = '/static/'
# EE NOTE 1.23.17 -- I should have left this as '/static/' I had it as http://close...
# so when I added SSL the admin was choking on and prohibiting the deliver of
# the css files from "http"
# STATIC_URL = 'http://closecalldatabase.com/static/'
# STATIC_URL = 'https://closecalldatabase.com/static/'
STATIC_URL = '/static/'  # this is controlled in nginx.conf

# https://docs.djangoproject.com/en/1.7/howto/static-files/#deployment
# STATIC_ROOT = '/home/eezis/sites/static/closecall/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'nginx-root/static/')


# when collectstatic is run at the server
# $ sudo '/home/eezis/.virtualenvs/closecall/bin/python' manage.py collectstatic
# this setting tells it where to look for files that need to be collectd,
# it should automagically collect from the static subdirectories of any .virtualenv applications
# and any applications that you have created . . . but it is not picking up a modification that I made
# so I am trying this explicit declaration.
STATICFILES_DIRS = (
    '/home/eezis/sites/closecall/geoposition/static/',
    '/home/eezis/sites/closecall/static/',
)


# STATICFILES_DIRS =(
#     os.path.join(os.path.dirname(__file__), '../static').replace('\\','/'),
#     os.path.join(os.path.dirname(__file__), '../static').replace('\\','/'),
# )

TEMPLATE_DIRS = (
#     BASE_DIR.join('templates').replace('\\','/'),
    os.path.join(os.path.dirname(__file__), '../templates').replace('\\','/'),
#     # '/templates/',
)




# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'closecalldatabase@gmail.com'
# EMAIL_HOST_PASSWORD = '[REDACTED - MOVED TO ENVIRONMENT VARIABLES]'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_SUBJECT_PREFIX = '[CCDB] '


EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'eezis'
EMAIL_HOST_PASSWORD = '[REDACTED - MOVED TO ENVIRONMENT VARIABLES]'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# current registration emails form sendgrid are:: from: webmaster@localhost
DEFAULT_FROM_EMAIL = 'closecalldatabase@gmail.com'



# https://github.com/summernote/django-summernote
# see link above for more options
SUMMERNOTE_CONFIG = {
    # Change editor size
    'width': '100%',
    # 'height': '480',
    'height': '380',

    # Customize toolbar buttons
    'toolbar': [
        # ['style', ['style']],
        # ['style', ['bold', 'italic', 'underline', 'clear']],

        ['style', ['style']],
        ['font', ['bold', 'italic', 'underline', 'superscript', 'subscript',
                  'strikethrough', 'clear']],
        ['fontname', ['fontname']],
        ['fontsize', ['fontsize']],
        ['para', ['ul', 'ol', 'height']],
        ['insert', ['link']],
    ],


    # Set `upload_to` function for attachments.
    # 'attachment_upload_to': my_custom_upload_to_func(),

    # Set custom storage class for attachments.
    # 'attachment_storage_class': 'my.custom.storage.class.name',

    # Set external media files for SummernoteInplaceWidget.
    # !!! Be sure to put {{ form.media }} in template before initiate summernote.
    'inplacewidget_external_css': (
        '//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css',
        '//netdna.bootstrapcdn.com/font-awesome/4.0.3/css/font-awesome.min.css',
    ),
    'inplacewidget_external_js': (
        # '//code.jquery.com/jquery-1.9.1.min.js',
        '//code.jquery.com/jquery-1.11.2.min.js',
        '//netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js',
    ),
}


# settings.py
# ValueError: Unable to configure handler 'file': [Errno 13] Permission denied: '/home/eezis/sites/closecall/django-errors.log'
# http://stackoverflow.com/questions/18547855/permission-denied-when-writing-log-file
# I ran sudo touch django-errors.log   then I ran chmod 775 django-errors.log    that worked and allowed me to start it up
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'django-errors.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers':['file'],
            'propagate': True,
            'level':'DEBUG',
        },
        'closecall': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }
}


REST_FRAMEWORK = {
    # restrict to admin users
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.IsAdminUser',
        # 'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.AllowAny',
        ),
    # turn on pagination
    # 'PAGE_SIZE': 10
}

# I am using 1.77 so it won't work, need the upgrade > 1.9
# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#         'OPTIONS': {
#             'min_length': 6,
#         }
#     },
# ]

# http://chase-seibert.github.io/blog/2014/01/12/python-unicode-console-output.html
import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)


try:
    from dev_settings import *
except:
    pass
