from django.contrib.auth.models import User


# Handle user name display
def _get_full_name(self):
    if self.is_freelancer:
        return self.freelancer.get_full_name()
    else:
        return self.email
User.get_full_name = _get_full_name


# Users should display as their full name
User.__unicode__ = User.get_full_name