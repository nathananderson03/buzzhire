from django.conf import settings


def main(request):
    """"Context processor for adding site wide variables
    to the template contexts.
    """

    return {
        'contact_email': settings.CONTACT_EMAIL,
        'bookings_email': settings.BOOKINGS_EMAIL,
        'facebook_url': settings.FACEBOOK_URL,
        'twitter_url': settings.TWITTER_URL,
    }

