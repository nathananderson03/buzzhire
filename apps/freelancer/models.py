from decimal import Decimal
from django.contrib.gis.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from polymorphic import PolymorphicModel
from apps.core.models import GeoPolymorphicManager
from django.conf import settings
from datetime import date
from django.core import validators
from multiselectfield import MultiSelectField
from djmoney.models.fields import MoneyField
from moneyed import Money
from django.contrib.humanize.templatetags.humanize import apnumber
from django.template.defaultfilters import pluralize
from apps.core.views import POUND_SIGN
from apps.location.models import Postcode
from apps.core.validators import mobile_validator
import calendar


def _is_freelancer(self):
    """Custom method on User model.
    Returns whether or not the user account is a freelancer account,
    i.e. has a freelancer profile.
    ."""
    return Freelancer.objects.filter(user=self).exists()
User.is_freelancer = property(_is_freelancer)


def _freelancer(self):
    """Custom method on User model.
    Returns the Freelancer for the user.  If it doesn't, raises
    Freelancer.DoesNotExist.
    """
    return self.freelancer_set.get()
User.freelancer = property(_freelancer)


def client_to_freelancer_rate(client_rate):
    """Given a client rate as a moneyed.Money object,
    return the freelancer rate, also as a Money object.
    """
    freelancer_rate = client_rate * (1 - (Decimal(settings.COMMISSION_PERCENT)
                                       / 100))

    # Round freelancer rate to nearest 25p
    # TB the "%.2f" conversion ensures it's to two decimal places
    ROUNDING = float(settings.COMMISSION_ROUND_PENCE) / 100
    freelancer_rate.amount = Decimal(
        "%.2f" % (round(float(freelancer_rate.amount) / ROUNDING) * ROUNDING))
    return freelancer_rate

# FREELANCER_MIN_WAGE = client_to_freelancer_rate(Money(settings.CLIENT_MIN_WAGE,
#                       'GBP')).amount
FREELANCER_MIN_WAGE = 6


class PublishedFreelancerManager(GeoPolymorphicManager):
    """Manager for published freelancers.
    Note that models inheriting Freelancer should redeclare it:
    
        class SpecialFreelancer(Freelancer):
            objects = models.Manager()
            published_objects = PublishedFreelancerManager()
    """
    def get_queryset(self):
        queryset = super(PublishedFreelancerManager, self).get_queryset()
        return queryset.filter(published=True)


class Freelancer(PolymorphicModel):
    "A freelancer is a person offering a professional service."

    service = None  # Needed for API

    published = models.BooleanField(default=False,
        help_text='Whether or not the freelancer is matched with jobs.')

    # A link to a user account.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, unique=True)

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    mobile = models.CharField(max_length=13,
          validators=[mobile_validator],
          help_text='Your mobile phone number will be visible to clients on '
            'whose jobs you are booked.')

    photo = models.ImageField(upload_to='freelancer/photos/%Y/%m/%d',
                              blank=True)

    FLUENCY_BASIC = 'BA'
    FLUENCY_CONVERSATIONAL = 'CO'
    FLUENCY_FLUENT = 'FL'
    FLUENCY_NATIVE = 'NA'
    FLUENCY_CHOICES = (
        (FLUENCY_BASIC, 'Basic'),
        (FLUENCY_CONVERSATIONAL, 'Conversational'),
        (FLUENCY_FLUENT, 'Fluent'),
        (FLUENCY_NATIVE, 'Native'),
    )
    english_fluency = models.CharField(max_length=2, choices=FLUENCY_CHOICES)
    eligible_to_work = models.BooleanField('I am eligible to work in the UK.',
                                           default=False)

    # TODO - Legacy field, remove once migrated
    PHONE_TYPE_ANDROID = 'AN'
    PHONE_TYPE_IPHONE = 'IP'
    PHONE_TYPE_WINDOWS = 'WI'
    PHONE_TYPE_OTHER = 'OT'
    PHONE_TYPE_NON_SMARTPHONE = 'NS'
    PHONE_TYPE_CHOICES = (
        (PHONE_TYPE_ANDROID, 'Android'),
        (PHONE_TYPE_IPHONE, 'iPhone'),
        (PHONE_TYPE_WINDOWS, 'Windows'),
        (PHONE_TYPE_OTHER, 'Other smartphone'),
        (PHONE_TYPE_NON_SMARTPHONE, 'Non smartphone'),
    )
    phone_type_old = models.CharField(max_length=2, choices=PHONE_TYPE_CHOICES,
                                  blank=True)

    # TODO - remove days_available and hours_available
    DAYS_OF_WEEK_CHOICES = [(calendar.day_abbr[i].lower(),
                               calendar.day_name[i]) for i in range(7)]
    days_available = MultiSelectField(
                'Which days of the week are you available to work?',
                choices=DAYS_OF_WEEK_CHOICES,
                blank=True)

    HOURS_AVAILABLE_MORNINGS = 'MO'
    HOURS_AVAILABLE_AFTERNOONS = 'AF'
    HOURS_AVAILABLE_EVENINGS = 'EV'
    HOURS_AVAILABLE_NIGHT = 'NI'
    HOURS_AVAILABLE_CHOICES = (
        (HOURS_AVAILABLE_MORNINGS, 'Mornings'),
        (HOURS_AVAILABLE_AFTERNOONS, 'Afternoons'),
        (HOURS_AVAILABLE_EVENINGS, 'Evenings'),
        (HOURS_AVAILABLE_NIGHT, 'Night'),
    )
    # Mornings, Afternoons, Evenings, Night, Flexible
    hours_available = MultiSelectField(
                            'What are your preferred working hours?',
                            choices=HOURS_AVAILABLE_CHOICES,
                            blank=True)


    minimum_pay_per_hour = MoneyField(max_digits=5, decimal_places=2,
              default_currency='GBP', default=Decimal(FREELANCER_MIN_WAGE),
              help_text='The minimum pay per hour you will accept.',
              validators=[validators.MinValueValidator(FREELANCER_MIN_WAGE)])

    postcode = models.ForeignKey(Postcode, blank=True, null=True)

    DISTANCE_CHOICES = [(i, "%s mile%s" % (str(apnumber(i)).capitalize(),
                                           pluralize(i))) \
                                        for i in (1, 2, 5, 10, 20, 50)]
    travel_distance = models.PositiveSmallIntegerField(
        choices=DISTANCE_CHOICES, default=5,
        help_text='The maximum distance you are prepared to travel to a job.')

    # The integer stored in experience denotes that they have
    # AT LEAST that number of years experience.
    YEARS_EXPERIENCE_LESS_ONE = 0
    YEARS_EXPERIENCE_ONE = 1
    YEARS_EXPERIENCE_THREE = 3
    YEARS_EXPERIENCE_FIVE = 5
    YEARS_EXPERIENCE_CHOICES = (
        (YEARS_EXPERIENCE_LESS_ONE, 'Less than 1 year'),
        (YEARS_EXPERIENCE_ONE, '1 - 3 years'),
        (YEARS_EXPERIENCE_THREE, '3 - 5 years'),
        (YEARS_EXPERIENCE_FIVE, 'More than 5 years'),
    )
    years_experience = models.PositiveSmallIntegerField(
                                default=YEARS_EXPERIENCE_ONE,
                                choices=YEARS_EXPERIENCE_CHOICES)

    objects = GeoPolymorphicManager()
    published_objects = PublishedFreelancerManager()

    # stores information on the last application_date
    last_applied = models.DateField(auto_now_add=True)


    def save(self, *args, **kwargs):
        if self.published == True:
            self.last_applied = date.today()
        super(Freelancer, self).save(*args, **kwargs)


    @property
    def reference_number(self):
        "Returns a reference number for this freelancer."
        return 'FR%s' % str(self.pk).zfill(7)

    @property
    def is_active(self):
        delta = date.today() - self.last_applied

        return (self.published and (delta.days <= 14))


    def get_full_name(self):
        "Returns the full name of the freelancer."
        return '%s %s' % (self.first_name,
                          self.last_name)

    def get_absolute_url(self):
        return reverse('freelancer_detail', args=(self.pk,))

    def __unicode__(self):
        return self.get_full_name()

    class Meta:
        ordering = 'last_name',
