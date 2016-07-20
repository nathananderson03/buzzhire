from django.contrib.auth import logout

class StrictAuthenticationMiddleware(object):
    """Logs out users who are inactive."""
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated() and not request.user.is_active:
                logout(request)
