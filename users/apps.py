from django.apps import AppConfig

class UserProfileConfig(AppConfig):
    name = 'users' # the name of this app (eg, the app directory)
    verbose_name = 'UserProfiles App'

    def ready(self):
        import users.signals