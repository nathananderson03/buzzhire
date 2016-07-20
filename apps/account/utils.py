def user_display(user):
    """Returns the text to display for the user.
    Used by django-allauth, see settings.ACCOUNT_USER_DISPLAY.
    """
    return user.get_full_name()