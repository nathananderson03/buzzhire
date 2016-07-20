from django.apps import AppConfig


class ServiceConfig(AppConfig):

    name = 'apps.service'
    verbose_name = 'Service'

    def ready(self):

        # Autodiscover services.py files in other apps
        self.module.autodiscover()
