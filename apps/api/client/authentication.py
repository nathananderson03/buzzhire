from rest_framework.authentication import SessionAuthentication

class CSRFExemptAuthentication(SessionAuthentication):
    """
    Disables CSRF checks for some of the views. (e.g. registration)
    """

    def enforce_csrf(self, request):
        return