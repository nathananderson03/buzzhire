from twilio.rest import TwilioRestClient
import logging
from django.conf import settings


logger = logging.getLogger('project')

def get_international_phone_number(user):
    """Returns the phone number of the user in international format,
    or None if they have no phone number.
    """
    if user.is_freelancer:
        local_phone = user.freelancer.mobile
    elif user.is_client:
        local_phone = user.client.mobile
    else:
        return None

    return local_to_international_phone_number(local_phone)

def local_to_international_phone_number(local_phone):
    """Converts a local-style phone number (in the form 07xxx xxx xxx)
    to international ('+447xxxxxxxxx').
    """
    return '+447%s' % local_phone[2:].replace(' ', '')


def send_sms(user, message, related_object=None):
    """Send an SMS with the message, to the user.
    
    Currently, this fails silently (though it logs the error).
    
    Optionally, includes a link to a related object.
    """
    logger.debug('Attempting to send sms: %s' % message)

    phone_number = get_international_phone_number(user)
    if not phone_number:
        logger.debug('Could not get a phone number for user id %d.' % user.id)
        return

    if related_object:
        message += ' See more: %s%s' % (settings.BASE_URL,
                                        related_object.get_absolute_url())
    # Add signature
    message += ' The BuzzHire Team'

    try:
        client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID,
                                  settings.TWILIO_TOKEN)
        client.messages.create(
            to=phone_number,
            from_=settings.TWILIO_PHONE_NUMBER,
            body=message,
        )
    except Exception as e:
        logger.debug('Sending of SMS failed: user id %d, message "%s".' % (
                                    user.id, message))
        logger.exception(e)
    else:
        logger.debug('SMS sent.')
