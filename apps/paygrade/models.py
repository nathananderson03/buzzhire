from django.db import models
from django.core import validators
from djmoney.models.fields import MoneyField
from decimal import Decimal
from django.conf import settings

class BasePayGradeManager(models.Manager):
    "Model manager for PayGrades."

    def get_pay_grade(self, **kwargs):
        """Returns the appropriate pay grade,
        given some kwargs to filter by.
        """
        # Returns the first matching pay grade
        matches = self.get_matching_pay_grades(**kwargs)
        if matches:
            return matches.first()
        raise self.model().DoesNotExist

    def get_matching_pay_grades(self, years_experience):
        """Returns queryset of matching pay grades for the supplied
        filter terms, ordered by most relevant.
        
        Models subclassing BasePayGrade with extra fields should
        also subclass BasePayGradeManager, and override this method. 
        """
        return self.get_queryset().filter(
                        years_experience__lte=years_experience)


YEARS_EXPERIENCE_CHOICES = (
    (0, 'No preference'),
    (1, '1 year'),
    (3, '3 years'),
    (5, '5 years'),
)


class BasePayGrade(models.Model):
    """A means of specifying minimum rates of pay for different services.
    
    This is an abstract class that should be subclassed by each service.
    """
    years_experience = models.PositiveSmallIntegerField(
                                'Years of experience',
                                choices=YEARS_EXPERIENCE_CHOICES)

    min_client_pay_per_hour = MoneyField('Minimum client cost per hour',
              max_digits=5, decimal_places=2,
              default_currency='GBP',
              default=Decimal(settings.CLIENT_MIN_WAGE),
              validators=[
                validators.MinValueValidator(settings.CLIENT_MIN_WAGE)])

    # Define which fields should be used to filter out the correct
    # pay grade.  Models subclassing BasePayGrade and adding extra fields
    # should extend filter_fields like so:
    #
    #    filter_fields = BasePayGrade.filter_fields + ('my_field',)
    #
    filter_fields = ('years_experience',)

    objects = BasePayGradeManager()

    def __unicode__(self):
        return '%s: %s at %s' % (self.__class__,
                                 self.years_experience,
                                 self.min_client_pay_per_hour)

    class Meta:
        abstract = True
        ordering = ('-years_experience',)
