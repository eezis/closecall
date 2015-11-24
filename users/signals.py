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
from models import UserProfile

# from django.conf import settings
import os.path


@receiver(post_save, sender=UserProfile)
def handle_a_model_save(sender, **kwargs):
    print 'signals: a UserProfile was saved'

    try:
        # https://docs.djangoproject.com/en/dev/ref/signals/#post-save
        # Arguments sent with this signal:
        # sender, instance (The actual instance being saved) created, raw, using, update_fields
        if kwargs.get('created', True):
            userprofile = kwargs.get('instance')
            # if there is not lat & lon then we need to create it, then update the cache
            print userprofile.get_lat_lon()
        else:
            print
    except:
        pass



