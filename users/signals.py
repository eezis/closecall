"""
I wish to update the UserMap in real time. The plan is . . .

1. Use a post_save signal after a UserProfile is created to contact this file
    http://www.koopman.me/2015/01/django-signals-example/
    a. create this file (signals.py)
    b. create apps.py -- use AppConfig to "register" this file

    from django.apps import AppConfig

    class UserProfileConfig(AppConfig):
        name = 'users'
        verbose_name = 'UserProfiles App'

        def ready(self):
            import users.signals

    c. edit __init__.py;

        default_app_config = 'users.apps.UserProfileConfig'

2. Check for a Lat & Lon -- create it not there

3. Write the file to the os independnt /nginx-root/dataloader directory
    -- name it id.dat where the id is just the new id, 5412.dat, etc

4. use workflow to monitor directory and process the new piece of data
    https://github.com/mdipierro/workflow



    - add it to the end of the existing file, use regex to replace the ' }\n ]}' at the end of the file
      with the new data and then \n ]}

      {"member": 5402, "longitude": 24.1051864, "latitude": 56.9496487 }
     ]}

     delete the .dat file that provided the data

5.

FOR THIS TO WORK ADD import receivers.py to the urls.py file.

"""

"""
To use workflow . .

create a file workflow.config using the syntax below
run workflow.py in that folder [..nginix-root/dataloader]

config.py

process_dat: *.dat: python process.py $0

"""


from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.db import transaction
from .models import UserProfile

# from django.conf import settings
import os.path
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_user_profile_on_registration(sender, instance, created, **kwargs):
    """
    Automatically create a UserProfile for users who register through
    traditional django-registration-redux flow (not Strava).
    Strava registration handles profile creation in its own view.

    Uses transaction.on_commit() to avoid race conditions - profile is only
    created after the User transaction is committed to the database.
    This is the Django 5.1+ best practice for signal handlers.
    """
    if created:
        # Use transaction.on_commit() to avoid race conditions
        # This ensures the User is committed to DB before we check for profile
        def create_profile_if_needed():
            try:
                # Refresh from database to get latest state
                user = User.objects.get(pk=instance.pk)

                # Check if profile already exists (Strava flow may have created it)
                if not hasattr(user, 'profile'):
                    UserProfile.objects.create(
                        user=user,
                        first=user.first_name or '',
                        last=user.last_name or '',
                        created_with='Traditional Registration'
                    )
                    logger.info(f"AUTO-CREATED UserProfile for traditional registration: {user.username} ({user.email})")
                else:
                    logger.info(f"Profile already exists for {user.username}, skipping auto-creation")
            except User.DoesNotExist:
                # Transaction was rolled back, user doesn't exist
                logger.warning(f"User {instance.pk} does not exist, transaction may have been rolled back")
            except Exception as e:
                logger.error(f"ERROR auto-creating UserProfile for {instance.username}: {str(e)}")

        transaction.on_commit(create_profile_if_needed)


@receiver(post_save, sender=UserProfile)
def handle_a_model_save(sender, **kwargs):
    print('signals.py:hams: post_save received ')
    print('   kwargs', kwargs)

    try:
        # https://docs.djangoproject.com/en/dev/ref/signals/#post-save
        # Arguments sent with this signal:
        # sender, instance (The actual instance being saved) created, raw, using, update_fields
        if kwargs.get('created', True):
            print("signals.py:hams: inside 'created true'")
            userprofile = kwargs.get('instance')
            # if there is not lat & lon then we need to create it, then update the cache
            # other wise the update will get created in the middle of file creation.
            # should inspect and verify the file somehow
            try:
                print(userprofile.get_lat_lon())
            except:
                print("signals.py:hams: UserProfile.get_lat_lon failed - it excepted\n")
                pass
            # build the string, then write the file, or just write the .dat and let workflow do it
            # workflow might be best
        else:
            print("signals.py:hams: The kwargs.get('created', True) failed -- so it was probably an update, maybe adding a geocode?\n")
    except:
        # I added a try/except around this because it somehow genearated IOError: [Errno 5] Input/output error
        try:
            print("signals.py:hams: Exception raised by: if kwargs.get('created', True):\n")
        except:
            pass
        pass



# NOTE WELL PRINT STATEMENTS ARE ONLY VISIBLE AT THE SERVER IN THE TAB WHERE
# $ gunicorn closecall.wsgi:application --workers=3 --bind 127.0.0.1:8000 --log-file=-
# was run!
# [2015-11-24 13:31:06 +0000] [13353] [INFO] Booting worker with pid: 13353
# signals: a UserProfile was saved
# (37.09024, -95.71289100000001)
# CreateUserProfileView.form_valid :: kjack1111 -- kjackgilchrist@gmail.com
# signals: a UserProfile was saved
# the kwargs.get('created', True) failed -- so it was probably an update?


