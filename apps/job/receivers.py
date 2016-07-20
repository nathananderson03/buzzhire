from django.dispatch import receiver
from apps.core.email import send_mail
from apps.core.templatetags.core_tags import summary_for_email
from django.conf import settings
from django.template.loader import render_to_string
from .models import JobRequest
from .signals import job_request_changed
from django_fsm.signals import post_transition
from apps.notification.models import Notification
from apps.notification.sms import send_sms


@receiver(post_transition)
def notifications_on_job_request_opened(sender, instance, name,
                                source, target, **kwargs):
    "Sends notifies when a new job request is opened."
    if isinstance(instance, JobRequest) and name == 'open':

            # First, notify the bookings email address
            subject = 'New job request %s' % instance.reference_number
            send_mail(settings.BOOKINGS_EMAIL,
                      subject,
                      'email/base',
                      {'title': 'New job request',
                       'content': summary_for_email(instance, 'admin')
                    })

            # Next, send a confirmation email to the client
            send_mail(instance.client.user.email,
                  'Thank you for your booking',
                  'email/base',
                  {'title': 'Thank you for your booking',
                   'content': render_to_string(
                            'job/email/includes/jobrequest_created.html',
                            {'object': instance}),
                   'bookings_email': settings.BOOKINGS_EMAIL},
                  from_email=settings.BOOKINGS_FROM_EMAIL)


@receiver(post_transition)
def notify_client_on_job_request_confirmed(sender, instance, name,
                                          source, target, **kwargs):
    """Sends a notification email to the client when a job request
    is confirmed."""
    if isinstance(instance, JobRequest) and \
                                        target == JobRequest.STATUS_CONFIRMED:
            content = render_to_string(
                'job/email/includes/jobrequest_confirmed.html',
                {'object': instance,
                 'base_url': settings.BASE_URL})
            send_mail(instance.client.user.email,
                  'Your job request is now confirmed',
                  'email/base',
                  {'title': 'Your job request is now confirmed',
                   'content': content,
                   'bookings_email': settings.BOOKINGS_EMAIL},
                  from_email=settings.BOOKINGS_FROM_EMAIL)

            # Create notification
            message = 'Your job request for a %s is now confirmed.' \
                                                    % instance.service
            Notification.objects.create(
                    message=message,
                    category='client_job_request_confirmed',
                    related_object=instance,
                    user=instance.client.user)

            send_sms(instance.client.user,
                     render_to_string('job/sms/client_confirmed.txt',
                                      {'job_request': instance}),
                     instance)

@receiver(post_transition)
def notify_client_on_jobrequest_cancelled(sender, instance, name,
                                          source, target, **kwargs):
    """Sends a notification email to the client when a job request
    is cancelled."""
    if isinstance(instance, JobRequest) and \
                                        target == JobRequest.STATUS_CANCELLED:
            content = render_to_string(
                'job/email/includes/jobrequest_cancelled.html',
                {'object': instance,
                 'bookings_email': settings.BOOKINGS_EMAIL
                 })
            send_mail(instance.client.user.email,
                  'Your job request has been cancelled',
                  'email/base',
                  {'title': 'Your job request has been cancelled',
                   'content': content,
                   'bookings_email': settings.BOOKINGS_EMAIL},
                  from_email=settings.BOOKINGS_FROM_EMAIL)

            # Create notification
            message = 'Your job request for a %s has been cancelled.' \
                                                    % instance.service
            Notification.objects.create(
                    message=message,
                    category='client_job_request_cancelled',
                    related_object=instance,
                    user=instance.client.user)


@receiver(job_request_changed)
def notify_client_on_job_request_changed(sender, instance,
                                         changed_data, silent, **kwargs):
    """Notifies the client if their job request is edited by a staff member.
    """
    if not silent:
        content = render_to_string(
            'job/email/includes/jobrequest_changed.html',
            {'object': instance})
        send_mail(instance.client.user.email,
              'Your job request has been changed',
              'email/base',
              {'title':
               'Your job request has been changed',
               'content': content,
               'bookings_email': settings.BOOKINGS_EMAIL},
              from_email=settings.BOOKINGS_FROM_EMAIL)

        # Notification for app
        Notification.objects.create(
                message='Your job request has been changed.',
                category='client_job_request_changed',
                related_object=instance,
                user=instance.client.user)
