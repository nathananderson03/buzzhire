from django.contrib.gis.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from apps.core.models import GeoPolymorphicManager
from apps.freelancer.models import Freelancer, PublishedFreelancerManager
from django.core.urlresolvers import reverse
from apps.job.models import JobRequest, JobRequestQuerySet
from apps.paygrade.models import BasePayGrade, BasePayGradeManager


DRIVER_SERVICE_TITLE = 'delivery driver'

def _is_driver(self):
    """Custom method on User model.
    Returns whether or not the user account is a driver account,
    i.e. has a driver profile.
    ."""
    return Driver.objects.filter(user=self).exists()
User.is_driver = property(_is_driver)


def _driver(self):
    """Custom method on User model.
    Returns the Freelancer for the user.  If it doesn't, raises
    Freelancer.DoesNotExist.
    """
    return Driver.objects.get(user=self)
User.driver = property(_driver)


class VehicleType(models.Model):
    """A type of vehicle that the driver may drive.
    """
    title = models.CharField(max_length=30)
    equivalent_to = models.ForeignKey('driver.VehicleType',
            help_text="Another vehicle type this should be treated as "
                "equivalent to in certain circumstances, such as "
                "in job requests.", blank=True, null=True,
            related_name='equivalent_children')
    delivery_box_applicable = models.BooleanField(blank=True,
                  default=False,
                  help_text='Whether or not delivery boxes are relevant '
                    'to this type of vehicle.')

    objects = models.Manager()

    def __unicode__(self):
        return self.title

    # TODO validation to prevent nested equivalence
    class Meta:
        ordering = ('title',)


class FlexibleVehicleTypeManager(models.Manager):
    """Manager for flexible vehicle types; excludes any vehicle types
    that have an equivalent_to parent.
    """
    def get_queryset(self):
        queryset = super(FlexibleVehicleTypeManager, self).get_queryset()
        return queryset.filter(equivalent_to=None)


class FlexibleVehicleType(VehicleType):
    """Proxy model for vehicle types when we're more flexible about
    the vehicle.

    For example, in job requests, certain vehicle types are as good as another:
    it doesn't matter whether you have a scooter or a motorcycle.

    Our way of handling this is to choose one VehicleType in the database
    to be the main one, and link the others via the equivalent_to field.
    The equivalent_to field should only be used in one direction

    This should only be used in circumstances where collate_under is
    relevant; for example, DriverJobRequests link to vehicle types and
    want to take account of collation, while DriverVehicleTypes don't.
    """
    objects = FlexibleVehicleTypeManager()

    def __unicode__(self):
        """Incorporates any vehicle types
        that are equivalent to this one.
        For example, Motorcycle would be displayed as 'Motorcycle / scooter'.
        """
        children = self.equivalent_children.all()
        if children:
            children_text = '/'.join([str(i).lower() for i in children])
            return "%s / %s" % (self.title, children_text)
        return self.title

    def as_queryset(self):
        """Returns a queryset of all the valid VehicleType equivalents
        to this FlexibleVehicleType.
        """
        pks = list(self.equivalent_children.values_list('pk', flat=True))
        pks.append(self.pk)
        return VehicleType.objects.filter(pk__in=pks)

    class Meta:
        proxy = True


class Driver(Freelancer):
    "A driver is a freelancer whose service is driving."

    service = DRIVER_SERVICE_TITLE

    VEHICLE_TYPE_MOTORCYCLE = 'MC'
    VEHICLE_TYPE_BICYCLE = 'BI'
    VEHICLE_TYPE_CAR = 'CA'
    VEHICLE_TYPE_VAN = 'VA'
    VEHICLE_TYPE_CHOICES = (
        (VEHICLE_TYPE_BICYCLE, 'Bicycle'),
        (VEHICLE_TYPE_MOTORCYCLE, 'Motorcycle/scooter'),
        (VEHICLE_TYPE_CAR, 'Car'),
        (VEHICLE_TYPE_VAN, 'Van'),
    )
    # To delete
    vehicle_types_old = MultiSelectField(choices=VEHICLE_TYPE_CHOICES,
                                         blank=True)

    vehicle_types = models.ManyToManyField(VehicleType,
             verbose_name='Vehicles',
             through='DriverVehicleType',
             blank=True,
             related_name='drivers',
             help_text='Which vehicles you are able and licensed to drive. '
                    'You do not need to provide the vehicle for the booking.')

    # TODO - remove
    motorcycle_licence = models.BooleanField('I have a CBT/full motorcycle license.',
                                             default=False)

    # The integer stored in driving experience denotes that they have
    # AT LEAST that number of years driving experience.
    DRIVING_EXPERIENCE_LESS_ONE = 0
    DRIVING_EXPERIENCE_ONE = 1
    DRIVING_EXPERIENCE_THREE = 3
    DRIVING_EXPERIENCE_FIVE = 5
    DRIVING_EXPERIENCE_CHOICES = (
        (DRIVING_EXPERIENCE_LESS_ONE, 'Less than 1 year'),
        (DRIVING_EXPERIENCE_ONE, '1 - 3 years'),
        (DRIVING_EXPERIENCE_THREE, '3 - 5 years'),
        (DRIVING_EXPERIENCE_FIVE, 'More than 5 years'),
    )
    # Legacy field - to be deleted once has migrated
    driving_experience_old = models.CharField(blank=True,
                                            max_length=3,
                                            choices=DRIVING_EXPERIENCE_CHOICES)
    # Legacy field - to be deleted
    driving_experience_old_2 = models.PositiveSmallIntegerField(default=1,
                                        choices=DRIVING_EXPERIENCE_CHOICES,
                                        blank=True, null=True)

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
    phone_type = models.CharField(max_length=2, choices=PHONE_TYPE_CHOICES,
                                  blank=True)

    objects = GeoPolymorphicManager()
    published_objects = PublishedFreelancerManager()

    def get_absolute_url(self):
        return reverse('freelancer_detail', args=(self.pk,))

    @classmethod
    def driver_from_freelancer(self, freelancer):
        "Returns the driver instance, given the freelancer instance."
        return Driver.objects.get(pk=freelancer.pk)


class DriverVehicleTypeQuerySet(models.QuerySet):
    "Custom queryset for DriverVehicleTypes."

    def owned(self):
        """Filter by driver vehicles that the driver can provide for a booking.
        """
        return self.filter(own_vehicle=True)


class DriverVehicleType(models.Model):
    """'Through' model for storing information for a driver about
    a particular vehicle.
    """

    driver = models.ForeignKey(Driver)
    vehicle_type = models.ForeignKey(VehicleType,
        help_text='Note: you may only create one vehicle of each type.')

    own_vehicle = models.BooleanField(
                            'I can provide this vehicle on a job.',
                            default=False)
    # We store deliver box sizes as integers so we can do simple
    # greater than / less than searches
    DELIVERY_BOX_NONE = 0
    DELIVERY_BOX_STANDARD = 2
    DELIVERY_BOX_PIZZA = 4
    DELIVERY_BOX_CHOICES = (
        (DELIVERY_BOX_NONE, 'None'),
        (DELIVERY_BOX_STANDARD, 'Standard'),
        (DELIVERY_BOX_PIZZA, 'Pizza'),
    )
    delivery_box = models.PositiveSmallIntegerField(
                'Minimum delivery box size', choices=DELIVERY_BOX_CHOICES,
                default=DELIVERY_BOX_NONE,
                help_text='What size delivery box does your vehicle have? '
                    '(Scooters, motorcycles and bicycles only.)')

    objects = DriverVehicleTypeQuerySet.as_manager()

    def __unicode__(self):
        return unicode(self.vehicle_type)

    class Meta:
        unique_together = ('driver', 'vehicle_type')
        ordering = ('vehicle_type__title',)
        verbose_name = 'driver vehicle'


class DriverJobRequest(JobRequest):
    """A JobRequest that is specifically for drivers to complete.
    """
    service = DRIVER_SERVICE_TITLE

    # To delete
    vehicle_types_old = models.ManyToManyField(VehicleType,
           related_name='jobrequests_old', blank=True, null=True)

    vehicle_type = models.ForeignKey(FlexibleVehicleType,
           related_name='jobrequests',
           blank=True, null=True,
           help_text="Which type of vehicle would be appropriate for the job. ")

    minimum_delivery_box = models.PositiveSmallIntegerField(
            choices=DriverVehicleType.DELIVERY_BOX_CHOICES,
            default=DriverVehicleType.DELIVERY_BOX_NONE,
            help_text='For scooters, motorcycles and bicycles, '
                        'the minimum delivery box size.')

    # Legacy field - to be deleted
    driving_experience_old = models.PositiveSmallIntegerField(
                                'Minimum driving experience',
                                choices=Driver.DRIVING_EXPERIENCE_CHOICES,
                                default=Driver.DRIVING_EXPERIENCE_LESS_ONE)

    own_vehicle = models.BooleanField(
                            'The driver must supply their own vehicle.',
                            default=True)

    PHONE_REQUIREMENT_NOT_REQUIRED = 'NR'
    PHONE_REQUIREMENT_ANY = 'AY'
    PHONE_REQUIREMENT_ANDROID = 'AN'
    PHONE_REQUIREMENT_IPHONE = 'IP'
    PHONE_REQUIREMENT_WINDOWS = 'WI'
    PHONE_REQUIREMENT_CHOICES = (
        (PHONE_REQUIREMENT_NOT_REQUIRED, 'No smart phone needed'),
        (PHONE_REQUIREMENT_ANY, 'Any smart phone'),
        (PHONE_REQUIREMENT_ANDROID, 'Android'),
        (PHONE_REQUIREMENT_IPHONE, 'iPhone'),
        (PHONE_REQUIREMENT_WINDOWS, 'Windows'),
    )
    phone_requirement = models.CharField(max_length=2,
            choices=PHONE_REQUIREMENT_CHOICES,
            default=PHONE_REQUIREMENT_NOT_REQUIRED,
            help_text='Whether the driver needs a smart phone to do '
                'this job (for example, if you need them to run an app).')


    def get_vehicle_type_display(self):
        "Returns the vehicle type, or 'Any' if there is none."
        if self.vehicle_type:
            return self.vehicle_type
        return 'Any'

    @property
    def delivery_box_applicable(self):
        "Returns whether or not the minimum delivery box is applicable."
        return self.own_vehicle and self.vehicle_type.delivery_box_applicable

    def get_service_description(self):
        if self.vehicle_type:
            return "%s delivery" % self.vehicle_type
        else:
            return 'delivery'

class DriverPayGradeManager(BasePayGradeManager):
    "Model manager for DriverPayGrades."

    def get_matching_pay_grades(self, vehicle_type, **kwargs):
        """Returns queryset of matching pay grades for the supplied
        filter terms, ordered by most relevant.
        """
        return super(DriverPayGradeManager, self).get_matching_pay_grades(
            **kwargs).filter(vehicle_type=vehicle_type)


class DriverPayGrade(BasePayGrade):
    "Pay grade model for drivers."

    vehicle_type = models.ForeignKey(FlexibleVehicleType,
           blank=True, null=True,
           help_text='Leave blank to specify drivers with no vehicle.')

    filter_fields = BasePayGrade.filter_fields + ('vehicle_type',)

    objects = DriverPayGradeManager()

    class Meta(BasePayGrade.Meta):
        unique_together = ('years_experience', 'vehicle_type')
