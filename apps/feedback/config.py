from django.apps import AppConfig


class FeedbackConfig(AppConfig):

    name = 'apps.feedback'
    verbose_name = 'Feedback'

    def ready(self):

        # import signal handlers
        from . import receivers
