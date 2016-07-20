from django.apps import AppConfig


class ReminderConfig(AppConfig):

    name = 'apps.reminder'
    verbose_name = 'Reminder'

    def ready(self):

        # import signal handlers
        from . import receivers

