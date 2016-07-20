from django.contrib.gis.db import models
from apps.freelancer.models import Freelancer, PublishedFreelancerManager
from apps.core.models import GeoPolymorphicManager
from apps.job.models import JobRequest
from apps.paygrade.models import BasePayGrade, BasePayGradeManager


BAR_SERVICE_TITLE = 'bar staff'

ROLE_MIXOLOGIST = 'MX'
ROLE_BARMAN = 'BM'
ROLE_BARISTA = 'BT'

ROLE_CHOICES = (
    (ROLE_BARMAN, 'Bartender'),
    (ROLE_MIXOLOGIST, 'Mixologist'),
    (ROLE_BARISTA, 'Barista'),
)

class BarJobRequest(JobRequest):
    """A JobRequest that is specifically for bar staff to complete.
    """
    service = BAR_SERVICE_TITLE

    role = models.CharField(max_length=2,
                                     default=ROLE_BARMAN,
                                     choices=ROLE_CHOICES)
    def get_service_description(self):
        return self.get_role_display()


class BarFreelancer(Freelancer):
    "A bar staff is a type of freelancer."

    service = BAR_SERVICE_TITLE

    role = models.CharField(max_length=2,
                                     default=ROLE_BARMAN,
                                     choices=ROLE_CHOICES)

    objects = GeoPolymorphicManager()
    published_objects = PublishedFreelancerManager()

    class Meta:
        verbose_name = 'bartender'
        verbose_name_plural = 'bar staff'


class BarPayGradeManager(BasePayGradeManager):
    "Model manager for BarPayGrades."

    def get_matching_pay_grades(self, role, **kwargs):
        """Returns queryset of matching pay grades for the supplied
        filter terms, ordered by most relevant.
        """
        return super(BarPayGradeManager, self).get_matching_pay_grades(
            **kwargs).filter(role=role)


class BarPayGrade(BasePayGrade):
    "Pay grade model for bar staff."

    role = models.CharField(max_length=2,
                             choices=ROLE_CHOICES)

    filter_fields = BasePayGrade.filter_fields + ('role',)

    objects = BarPayGradeManager()

    class Meta(BasePayGrade.Meta):
        unique_together = ('years_experience', 'role')