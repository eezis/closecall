
"""
http://blog.doismellburning.co.uk/2012/06/25/django-and-static-files/

The key to understanding how to server static files during production is to
recognize the process flow:

1. Django needs to know where to look for static files (it will gather them from
    many different locations if needed) and,

2. Using "$ python manage.py collectstatic" Django will put all of those files
    into a single directory that you specify


the code that does that magic is specified in the settings.py under
STATICFILES_FINDERS

One entry in there -- 'django.contrib.staticfiles.finders.FileSystemFinder', --
is smart and will scan all the app directories looking for a '/static/' subdir.

The second entry -- 'django.contrib.staticfiles.finders.AppDirectoriesFinder' --
looks where you tell it to look by specifying STATICFILES_DIRS

    import os
    PROJECT_DIR = os.path.dirname(__file__)

    STATICFILES_DIRS = (os.path.join(PROJECT_DIR, 'static'),)



"""

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'amlit.settings'

import django
django.setup()

from django.conf import settings

# STATICFILES_DIRS, STATIC_URL, STATICFILES_FINDERS, STATIC_URL, STATIC_ROOT


def get_static_file_info():
    print "\nWhen you run the 'python manage.py collectstatic' command . . .\n"

    if 'django.contrib.staticfiles.finders.FileSystemFinder' in settings.STATICFILES_FINDERS:
        print "Django will look for static assets in all the $app_name/static/ directories\n"

    if 'django.contrib.staticfiles.finders.AppDirectoriesFinder' in settings.STATICFILES_FINDERS:
        print "Django will also look in the following directories (specified in STATICFILES_DIRS):\n"
        for d in settings.STATICFILES_DIRS:
            print "\t{}".format(d)
    else:
        print "YOU ARE NOT USING 'django.contrib.staticfiles.finders.AppDirectoriesFinder' in your STATICFILES_DIRS"
        print "This means that Django is only looking in the $app_name/static/ directories\n"

    print "\nAfter finding the assets you are asking django to place them here (STATIC_ROOT):\n"
    print "\t {}\n\n".format(settings.STATIC_ROOT)


    print "Which means that your nginx location /static/ alias should be:\n\n\t{}".format(settings.STATIC_ROOT)
    print "\nlike this . . ."
    ngnix_location_config = """
        location /static/ {{
            alias {};
            expires 1d;
        }}
    """
    print ngnix_location_config.format(settings.STATIC_ROOT)


    print "You are telling the browser to find the static files at (STATIC_URL):\n\n \t{}\n".format(settings.STATIC_URL)
    if not settings.STATIC_URL.endswith('/'):
        print "\n***** ERROR Add A Trailing Slash to your STATIC_URL setting ***** \n"

    print "\nif the URL is not correct, update your STATIC_URL entry"

    if settings.STATIC_ROOT in settings.STATICFILES_DIRS:
        print """*** this is wrong, you should not be telling Django to find assets in the very directory
        where you are asking them to be deposited.\n\n
        STATIC_ROOT should be where you want the files to go\n
        STATICFILES_DIRS should contain extra directories that you want to inspect for static assets.
        """

    print "\n\n\n\n\n\n"


get_static_file_info()