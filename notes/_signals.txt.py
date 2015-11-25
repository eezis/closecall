"""
This is how signals work -- using post_save to update UserMap

1. Make the apps.py, use the ready function to "register" the apps interest in sending and receiving signals

"""


from django.apps import AppConfig

class UserProfileConfig(AppConfig):
    name = 'users' # the name of this app (eg, the app directory)
    verbose_name = 'UserProfile App'

    def ready(self):
        #print 'APP CONFIG READY HAS BEEN RUN!'
        import users.signals


"""
2. Load the AppConfig class via the __init__.py
"""

default_app_config = 'users.apps.UserProfileConfig'


"""
3. create your signals.py (in the same app you registered -- users in this case)

    a. sender=TheModelYouWant
    b. look for the signal you want, and it's "action" (e.g, 'created', 'updated', etc)
    c. write your logic

"""

from django.dispatch import receiver
from django.db.models.signals import post_save
from models import UserProfile

# from django.conf import settings
import os.path


@receiver(post_save, sender=UserProfile)
def handle_a_model_save(sender, **kwargs):
    print 'signals.py:hams: post_save received '
    print '   kwargs', kwargs

    try:
        # https://docs.djangoproject.com/en/dev/ref/signals/#post-save
        # Arguments sent with this signal:
        # sender, instance (The actual instance being saved) created, raw, using, update_fields
        if kwargs.get('created', True):
            print "signals.py:hams: inside 'created true'"
            userprofile = kwargs.get('instance')
            # if there is not lat & lon then we need to create it, then update the cache
            # other wise the update will get created in the middle of file creation.
            # should inspect and verify the file somehow
            try:
                print userprofile.get_lat_lon()
            except:
                print "signals.py:hams: UserProfile.get_lat_lon failed - it excepted"
                pass
            # build the string, then write the file, or just write the .dat and let workflow do it
            # workflow might be best
        else:
            print "signals.py:hams: The kwargs.get('created', True) failed -- so it was probably an update?"
    except:
        print "signals.py:hams: Exception raised by: if kwargs.get('created', True):"
        pass


