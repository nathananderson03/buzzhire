from apps.service import services


def service_for_freelancer(freelancer):
    """Returns the service for the supplied freelancer.
    """
    for service in services.values():
        if service.freelancer_model == freelancer.__class__:
            return service
    raise ValueError('Could not get find a service registered for '
                     '%s freelancer.' % freelancer.__class__)
