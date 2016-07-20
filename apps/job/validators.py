from django.core.exceptions import ValidationError
from datetime import date, datetime, timedelta
from django.conf import settings


def validate_start_date_and_time(start_date, start_time):
    """Validates the start date and time for a job request.
    We abstract this into a separate function so the form and the api
    serializers can both use it.
    """
    if start_date < date.today():
        raise ValidationError({'date': 'Your job must be in the future.'})
    elif start_date == date.today():
        # If it's today, make sure are giving enough notice
        allowed_time = (datetime.now() + \
                timedelta(hours=settings.JOB_REQUEST_MINIMUM_HOURS_NOTICE)
                ).time()
        if start_time < allowed_time:
             raise ValidationError({'start_time':
                'Your job must be at least %s hours from now.' \
                % settings.JOB_REQUEST_MINIMUM_HOURS_NOTICE})
