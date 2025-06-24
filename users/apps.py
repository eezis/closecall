from django.apps import AppConfig

class UserProfileConfig(AppConfig):
    name = 'users' # the name of this app (eg, the app directory)
    verbose_name = 'UserProfile App'

    def ready(self):
        print('APP CONFIG READY HAS BEEN RUN!')
        import users.signals
