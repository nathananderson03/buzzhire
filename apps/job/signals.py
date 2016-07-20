import django.dispatch


# Signal that is sent when a job is changed
job_request_changed = django.dispatch.Signal(providing_args=['instance',
                                                             'changed_data',
                                                             'silent'])
