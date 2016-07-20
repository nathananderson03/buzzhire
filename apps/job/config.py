from django.apps import AppConfig


class JobConfig(AppConfig):

    name = 'apps.job'
    verbose_name = 'Job'

    def ready(self):

        # import signal handlers
        from . import receivers

