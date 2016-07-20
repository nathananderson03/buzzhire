import time
from huey.djhuey import db_task
from .models import Invitation
from .signals import invitation_created
from apps.job import service_from_class

import logging

logger = logging.getLogger('project')

@db_task()
def invite_matching_freelancers(job_request):
    """Invites all suitable freelancers for the supplied job request.

    This can be called on a job request that has previously had invitations
    sent out.  In that case, it will simply skip inviting anyone who has
    already been invited.
    """
    service = service_from_class(job_request.__class__)
    matcher = service.job_matching_form.job_matcher(job_request)
    freelancers = matcher.get_results(ignore_availability=True)
    invited_count = 0
    for freelancer in freelancers:
        try:
            invitation, created = Invitation.objects.get_or_create(
                                                   freelancer=freelancer,
                                                   jobrequest=job_request)
            if created:
                # Only issue the invitation signal if we created an invitation;
                # in case the user had already been invited
                invited_count += 1
                invitation_created.send(sender=invite_matching_freelancers,
                                    invitation=invitation)

        except Exception as e:
            logger.error('[%s] Failed to invite freelancer %d for job request %d: %s' % (time.ctime(), freelancer.pk, job_request.pk, str(e)))

    print('[%s] Invited %d of %d matching freelancers for %s.' \
                                                        % (time.ctime(),
                                                        invited_count,
                                                        freelancers.count(),
                                                        str(job_request)))
