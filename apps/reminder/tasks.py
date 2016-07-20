import time
from huey.djhuey import db_task
from . import utils


@db_task()
def send_reminders(reminder_set):
    """Huey task for sending out job request reminders.
    
    Accepts a ScheduledReminderSet. 
    """
    print('[%s] send_reminders() called for %s.' % (time.ctime(),
                                    reminder_set.get_job_request_display()))

    if reminder_set.is_still_valid():
        try:
            reminder_set.send()
        except Exception as e:
            print('[%s] Failed to send reminders for %s.' % (time.ctime(),
                                        reminder_set.get_job_request_display()))
            print('Exception: %s' % e)
            # Reraise exception so it gets caught by other logging
            raise
        else:
            print('[%s] Sent reminders for %s.' % (time.ctime(),
                                        reminder_set.get_job_request_display()))
    else:
        print('[%s] Skipped sending reminders for %s.' % (time.ctime(),
                                    reminder_set.get_job_request_display()))
