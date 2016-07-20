from django.apps import AppConfig


class FreelancerConfig(AppConfig):

    name = 'apps.freelancer'
    verbose_name = 'Freelancer'

    def ready(self):

        # import signal handlers
        from . import receivers
