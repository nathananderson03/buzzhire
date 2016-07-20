import time
from huey.djhuey import crontab, db_periodic_task, db_task
from .models import JobRequest


@db_periodic_task(crontab(minute='*/15'))
def complete_job_requests():
    """This task gets autodiscovered by the huey task queue.
    Every fifteen minutes, checks any open job requests to see if
    they need moving over to being complete.
    """
    count = 0
    for job_request in JobRequest.objects.need_completing():
        job_request.complete()
        job_request.save()
        count += 1
    print('[%s] Automatically completed %d job requests.' % (time.ctime(),
                                                             count))

