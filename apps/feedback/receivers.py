from django.dispatch import receiver
from apps.core.email import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from apps.job.models import JobRequest
from django_fsm.signals import post_transition
from apps.notification.models import Notification


@receiver(post_transition)
def prompt_client_and_drivers_for_feedback(sender, instance, name,
                                          source, target, **kwargs):
    """Emails the client and the drivers for feedback, when a job request
    is finished."""
    if isinstance(instance, JobRequest) and \
                                    target == JobRequest.STATUS_COMPLETE:

        # Email client
        content = render_to_string(
            'feedback/email/includes/feedback_prompt.html',
            {'object': instance,
             'client': instance.client})

        send_mail(instance.client.user.email,
              'Tell us how it went',
              'email/base',
              {'title': 'Tell us how it went',
               'content': content,
               'bookings_email': settings.BOOKINGS_EMAIL},
               from_email=settings.BOOKINGS_FROM_EMAIL)

        # Notification for app
        Notification.objects.create(
            message='Tell us how it went.',
            category='client_feedback_request',
            related_object=instance,
            user=instance.client.user)

        # Email freelancers
        content = render_to_string(
            'feedback/email/includes/feedback_prompt.html',
            {'object': instance})
        recipients = [booking.freelancer.user.email \
                                    for booking in instance.bookings.all()]

        send_mail(recipients,
              'Tell us how it went',
              'email/base',
              {'title': 'Tell us how it went',
               'content': content,
               'bookings_email': settings.BOOKINGS_EMAIL},
               from_email=settings.BOOKINGS_FROM_EMAIL)

         # Notify freelancers for app
         # For now, we don't notify them (because they can't do it from the app)
#         for booking in instance.bookings.all():
#             Notification.objects.create(
#                 message='Tell us how it went.',
#                 category='freelancer_feedback_request',
#                 related_object=instance,
#                 user=booking.freelancer.user)
