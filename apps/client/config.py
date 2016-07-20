from django.apps import AppConfig


class ClientConfig(AppConfig):

    name = 'apps.client'
    verbose_name = 'Client'

    def ready(self):

        # import signal handlers
        from . import receivers
