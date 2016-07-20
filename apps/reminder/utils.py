from apps.core.email import send_mail
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from django.template.loader import render_to_string
from apps.job.models import JobRequest
from apps.notification.models import Notification
from apps.notification.sms import send_sms
import logging

logger = logging.getLogger('project')

class ScheduledReminderSet(object):
    """A set of reminders that should be scheduled for a job request.
    
    This is a serializable object that can be passed to a task queue, 
    and handles checking that the reminders should still be sent, and the
    sending.
    
    For use with tasks.send_reminders().
    
    """

    def __init__(self, job_request, title, scheduled_datetime,
                 sms_template_name=None):
        self.title = title
        self.job_request_id = job_request.id
        self.start_datetime_when_scheduled = job_request.start_datetime
        self.scheduled_datetime = scheduled_datetime
        self.sms_template_name = sms_template_name

    def __getstate__(self):
        "Method to allow serialization."
        return {
            'title': self.title,
            'job_request_id': self.job_request_id,
            'start_datetime_when_scheduled':
                                        self.start_datetime_when_scheduled,
            'scheduled_datetime': self.scheduled_datetime,
            'sms_template_name': self.sms_template_name,
        }

    def __setstate__(self, dict):
        "Method to allow serialization."
        self.title = dict['title']
        self.job_request_id = dict['job_request_id']
        self.start_datetime_when_scheduled = \
                                        dict['start_datetime_when_scheduled']
        self.scheduled_datetime = dict['scheduled_datetime']
        self.sms_template_name = dict.get('sms_template_name', None)

    @property
    def job_request(self):
        "Returns the job request."
        if not getattr(self, '_job_request', None):
            self._job_request = JobRequest.objects.get(id=self.job_request_id)
        return self._job_request

    def get_job_request_display(self):
        """Robustly returns a display of the job request.
        Will not raise exception if the JobRequest cannot be found."""
        try:
            return str(self.job_request)
        except JobRequest.DoesNotExist:
            return 'missing job request id %s' % self.job_request_id

    def is_still_valid(self):
        """Returns whether it is still valid to send the reminders.
        """
        # Only remind if the status is confirmed (so we don't remind
        # for cancelled jobs)
        if self.job_request.status != JobRequest.STATUS_CONFIRMED:
            logger.debug('Not sending reminder for %s, scheduled at %s, '
                        'because it was not confirmed.' % (self.job_request,
                                                   self.scheduled_datetime))
            return False

        # Test to check the start_datetime hasn't changed; if it has,
        # new reminders will have been scheduled
        # TODO - there is a slight problem with this logic - if the job
        # request is changed and then changed back, multiple reminders
        # will be sent out
        if self.start_datetime_when_scheduled != \
                                            self.job_request.start_datetime:
            logger.debug('Not sending reminder for %s, scheduled at %s, '
                        'because the start_datetime has been changed.' % (
                                                   self.job_request,
                                                   self.scheduled_datetime))
            return False

        # Don't send the reminder if the scheduled time is more than 3 minutes
        # in the past.  This is to prevent a flurry of old reminders being sent
        # out if the queue went down for any reason.
        if self.scheduled_datetime < (timezone.now() - timedelta(minutes=3)):
            logger.debug('Not sending reminder for %s, scheduled at %s, '
                        'because it was stale.' % (self.job_request,
                                                   self.scheduled_datetime))
            return False

        # Otherwise, we're all good
        return True

    def send_to_recipient(self, recipient, recipient_type):
        "Sends reminders to a single recipient."
        content = render_to_string(
            'reminder/email/includes/jobrequest_reminder_%s.html' \
                                                        % recipient_type,
            {'object': self.job_request,
             'base_url': settings.BASE_URL})

        send_mail(recipient.user.email,
              self.title,
              'email/base',
              {'title': self.title,
               'content': content,
               'bookings_email': settings.BOOKINGS_EMAIL},
              from_email=settings.BOOKINGS_FROM_EMAIL)

        Notification.objects.create(
                message=self.title,
                category='%s_reminder' % recipient_type,
                related_object=self.job_request,
                user=recipient.user)

        # Only send reminders to freelancers
        if recipient_type == 'freelancer':
            if self.sms_template_name:
                send_sms(recipient.user, self.get_sms_message(),
                         self.job_request)


    def send(self):
        """Sends out reminders to freelancers and client
        from the supplied reminder set.
        """
        self.send_to_recipient(self.job_request.client, 'client')
        for booking in self.job_request.bookings.all():
            self.send_to_recipient(booking.freelancer, 'freelancer')

    def get_sms_message(self):
        "Returns the text for the sms message."
        return render_to_string(self.sms_template_name,
                                {'job_request': self.job_request})
