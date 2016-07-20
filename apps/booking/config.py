from django.apps import AppConfig


class BookingConfig(AppConfig):

    name = 'apps.booking'
    verbose_name = 'Booking'

    def ready(self):

        # import signal handlers
        from . import receivers
