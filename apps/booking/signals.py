import django.dispatch


# Signal that is sent when a job is booked
booking_created = django.dispatch.Signal(providing_args=['booking'])

# Signal that is sent when a freelancer is invited
invitation_created = django.dispatch.Signal(providing_args=['invitation'])

# Signal that is sent when a job is applied for
invitation_applied = django.dispatch.Signal(providing_args=['invitation'])

# Signal that is sent when a freelancer's application is declined by an admin
invitation_declined = django.dispatch.Signal(providing_args=['invitation'])
