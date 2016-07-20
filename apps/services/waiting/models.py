from django.contrib.gis.db import models
from apps.freelancer.models import Freelancer, PublishedFreelancerManager
from apps.job.models import JobRequest
from apps.core.models import GeoPolymorphicManager
from apps.paygrade.models import BasePayGrade


WAITING_SERVICE_TITLE = 'waiters'


class WaitingJobRequest(JobRequest):
    """A JobRequest that is specifically for waiting staff to complete.
    """
    service = WAITING_SERVICE_TITLE


class WaitingFreelancer(Freelancer):
    "A waiting staff is a type of freelancer."

    service = WAITING_SERVICE_TITLE

    objects = GeoPolymorphicManager()
    published_objects = PublishedFreelancerManager()


    class Meta:
        verbose_name = 'waiter'


class WaitingPayGrade(BasePayGrade):
    "Pay grade model for waiting staff."

    pass
