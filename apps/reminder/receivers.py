from datetime import timedelta
from django.dispatch import receiver
from apps.core.email import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from apps.job.models import JobRequest
from django_fsm.signals import post_transition
from apps.notification.models import Notification
from .tasks import send_reminders
from .utils import ScheduledReminderSet
from apps.job.signals import job_request_changed


def enqueue_reminders(job_request):
    "Enqueues reminders for clients and freelancers."
    # Schedule two sets of reminders
    infos = (
        # Reminders an hour before
        ScheduledReminderSet(job_request,
                 'Your job starts in one hour',
                 job_request.start_datetime - timedelta(hours=1),
                 'reminder/sms/one_hour_reminder.txt'),

        # Reminders 10 minutes before
        ScheduledReminderSet(job_request,
                 'Your job starts in ten minutes',
                 job_request.start_datetime - timedelta(minutes=10),
                 'reminder/sms/ten_minutes_reminder.txt'),
    )

    for info in infos:
        send_reminders.schedule(args=(info,),
                               eta=info.scheduled_datetime)


@receiver(post_transition)
def enqueue_reminders_on_job_request_confirmed(sender, instance, name,
                                          source, target, **kwargs):
    """Enqueues reminders for clients and freelancers,
    once the job request is confirmed."""
    if isinstance(instance, JobRequest) and \
                                        target == JobRequest.STATUS_CONFIRMED:
        enqueue_reminders(instance)


@receiver(job_request_changed)
def enqueue_reminders_on_job_request_changed(sender, instance,
                                         changed_data, silent, **kwargs):
    # If the datetime has changed, queue the reminders up again
    if any(i in ('date', 'start_time') for i in changed_data):
        # Only for confirmed jobs
        if instance.status == JobRequest.STATUS_CONFIRMED:
            enqueue_reminders(instance)
