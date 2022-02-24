from django.apps import AppConfig


class UserRegistrationConfig(AppConfig):
    name = 'user_registration'

    def ready(self):
        from . import signals

