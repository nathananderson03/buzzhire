from django.db import models
from django.utils import timezone
from django import forms
from django.db.models import Count, F
from datetime import date, time
import calendar
from apps.freelancer.models import Freelancer
from apps.job.models import JobRequest
from .signals import invitation_applied


class BookingOrInvitationQuerySet(models.QuerySet):
    "Custom queryset for Bookings and Invitations."

    def future(self):
        """Filter by job requests that are in the future (i.e. started
        today or later.
        TODO - we may need to improve this so it takes into account duration.
        """
        return self.filter(jobrequest__end_datetime__gte=timezone.now())

    def past(self):
        """Filter by job requests that are in the past (i.e. started
        yesterday or before."""
        return self.exclude(jobrequest__end_datetime__gte=timezone.now())

    def complete(self):
        """Filter by job requests that have been completed.
        """
        return self.filter(jobrequest__status=JobRequest.STATUS_COMPLETE)

    def for_freelancer(self, freelancer):
        "Filters by job requests that a freelancer has been allocated to."
        return self.filter(freelancer=freelancer)

    def for_client(self, client):
        "Filters by job requests created by the supplied client."
        return self.filter(jobrequest__client=client)

    def published(self):
        """Filter by job requests are for freelancers who are published.
        """
        return self.filter(freelancer__published=True)


class InvitationQuerySet(BookingOrInvitationQuerySet):
    "Queryset for invitations."

    def can_be_applied_to_by_freelancer(self, freelancer):
        """Returns all invitations that the supplied freelancer
        can apply to.
        """
        # Filter by freelancer
        queryset = self.filter(freelancer=freelancer)

        # Exclude invitations for past job requests
        queryset = queryset.future()

        # Filter by invitations they haven't already applied to
        queryset = queryset.filter(date_applied__isnull=True)

        # Filter by job requests that are open
        queryset = queryset.filter(jobrequest__status=JobRequest.STATUS_OPEN)

        # Filter by job requests that they aren't already booked on
        already_booked_on = Booking.objects.for_freelancer(
                            freelancer).values_list('jobrequest_id', flat=True)
        queryset = queryset.exclude(jobrequest_id__in=already_booked_on)

        return queryset

    def applied_to_by_freelancer(self, freelancer):
        """Returns all invitations that the supplied freelancer
        has applied to.  Excludes any applications that have been accepted. 
        """
        # Filter by freelancer
        queryset = self.filter(freelancer=freelancer)

        # Filter by whether the invitation has been applied to
        queryset = queryset.filter(date_applied__isnull=False)

        # Filter by job requests that they aren't already booked on
        already_booked_on = Booking.objects.for_freelancer(
                            freelancer).values_list('jobrequest_id', flat=True)
        queryset = queryset.exclude(jobrequest_id__in=already_booked_on)

        return queryset

    def undeclined_applications(self):
        """Returns all the applications that have not been declined.
        To use with a job request:
        
            job_request.invitations.undeclined_applications()
        """
        return self.filter(date_applied__isnull=False,
                           date_declined__isnull=True)

class JobInvalidStatus(Exception):
    "Exception raised when a job has the wrong status for a particular action."
    pass

class JobInPast(Exception):
    "Exception raised when a job is in the past."
    pass


class JobFullyBooked(Exception):
    "Exception raised when a job is fully booked."
    pass

class JobAlreadyAppliedToByFreelancer(Exception):
    "Exception raised when the freelancer has already applied to the job."
    pass

class JobAlreadyBookedByFreelancer(Exception):
    "Exception raised when the freelancer has already been booked on the job."
    pass


class Invitation(models.Model):
    """An invitation to a particular freelancer to book
    a particular job request.  They can be created by admins, or automatically,
    and they essentially give permission to freelancers to book themselves
    onto a job request.
    """
    freelancer = models.ForeignKey(Freelancer, related_name='invitations')
    jobrequest = models.ForeignKey(JobRequest, related_name='invitations')
    date_created = models.DateTimeField(auto_now_add=True)
    date_applied = models.DateTimeField(blank=True, null=True,
                help_text='When the freelancer applied to the job.')
    date_declined = models.DateTimeField(blank=True, null=True,
                help_text='When the freelancer was declined for the job.')
    # TODO date_accepted should be deleted, as it is now the same as when
    # the creation date of the booking
    date_accepted = models.DateTimeField(blank=True, null=True)
    manual = models.BooleanField(default=True,
                help_text='Whether this invitation was created manually.')

    def __unicode__(self):
        return self.reference_number

    def get_absolute_url(self):
        # We define this for notifications that use these as the related object
        # Just link through to the job request
        return self.jobrequest.get_absolute_url()

    @property
    def reference_number(self):
        "Returns a reference number for this invitation."
        return 'IN%s' % str(self.pk).zfill(7)

    class Meta:
        # A single freelancer can't be invited twice for the same job
        unique_together = (("freelancer", "jobrequest"),)
        ordering = ['date_applied']

    def can_be_applied_to(self):
        "Whether or not the invitation can be applied to."
        try:
            self.validate_can_be_applied_to()
        except:
            return False
        return True

    def validate_can_be_applied_to(self):
        """Validates whether the invitation can be applied to.
        
        Raises JobInPast or JobAlreadyBookedByFreelancer on failure.
        """
        # Check that the job request is still open
        if self.jobrequest.status != JobRequest.STATUS_OPEN:
            raise JobInvalidStatus()

        # Check that the job request is not in the past
        if self.jobrequest.end_datetime < timezone.now():
            raise JobInPast()

        # Check that the job request hasn't been applied to by
        # this freelancer already
        if self.date_applied:
            raise JobAlreadyAppliedToByFreelancer()

        # Check that they're not already booked
        if self.is_accepted():
            raise JobAlreadyBookedByFreelancer()

    def validate_can_be_declined(self):
        """Validates whether the invitation can be declined.
        
        Raises JobAlreadyBookedByFreelancer on failure.
        """
        # Check that they're not already booked
        if self.is_accepted():
            raise JobAlreadyBookedByFreelancer()

    def mark_as_applied(self):
        """Marks the invitation as applied."""
        self.date_applied = timezone.now()
        self.save()
        # Dispatch signal
        invitation_applied.send(sender=self.__class__, invitation=self)

    def is_accepted(self):
        """Whether or not the invitation has been accepted."""
        return self.jobrequest.bookings.for_freelancer(
                                                    self.freelancer).exists()

    def can_be_accepted(self):
        """Whether or not the invitation can be accepted,
        i.e. if it has been applied to, and hasn't already
        been accepted/declined.
        """
        return bool(self.date_applied) and not bool(self.date_declined) \
            and not self.is_accepted()

    def decline(self):
        """Mark the invitation as declined.
        """
        self.date_declined = timezone.now()
        self.save()

    objects = InvitationQuerySet.as_manager()


class Booking(models.Model):
    """A Booking is an allocation of a single freelancer to a JobRequest.
    JobRequests can potentially have multiple Bookings.
    """
    freelancer = models.ForeignKey(Freelancer, related_name='bookings')
    jobrequest = models.ForeignKey(JobRequest, related_name='bookings')
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.reference_number

    @property
    def reference_number(self):
        "Returns a reference number for this booking."
        return 'BK%s' % str(self.pk).zfill(7)

    class Meta:
        # A single freelancer can't be booked in twice for the same job
        unique_together = (("freelancer", "jobrequest"),)

    objects = BookingOrInvitationQuerySet.as_manager()



class Availability(models.Model):
    """A model for storing the general availability
    of a particular freelancer."""
    freelancer = models.OneToOneField(Freelancer)

    # Defines the shift times in the form: (name, start hour, end hour)
    SHIFT_TIMES = (
        ('early_morning', 2, 7),
        ('morning', 7, 12),
        ('afternoon', 12, 17),
        ('evening', 17, 22),
        ('night', 22, 2),
    )
    # Specify the two dimensions for the fields, to help with processing
    SHIFTS = [i[0] for i in SHIFT_TIMES]
    DAYS = [day.lower() for day in calendar.day_name]

    AVAILABILITY_CHOICES = ((True, 'Available'), (False, 'Not available'))
    FIELD_KWARGS = {
        'choices': AVAILABILITY_CHOICES,
        'default': True,
    }
    # Define all the shifts for the week as separate fields
    # Obviously this isn't very DRY, but it's simple to read and will
    # perform better than having them in separate tables
    monday_early_morning = models.BooleanField(help_text='2am - 7am',
                                               **FIELD_KWARGS)
    monday_morning = models.BooleanField(help_text='7am - 12pm',
                                         **FIELD_KWARGS)
    monday_afternoon = models.BooleanField(help_text='12pm - 5pm',
                                           **FIELD_KWARGS)
    monday_evening = models.BooleanField(help_text='5pm - 10pm',
                                         **FIELD_KWARGS)
    monday_night = models.BooleanField(help_text='10pm - 2am',
                                       **FIELD_KWARGS)

    tuesday_early_morning = models.BooleanField(**FIELD_KWARGS)
    tuesday_morning = models.BooleanField(**FIELD_KWARGS)
    tuesday_afternoon = models.BooleanField(**FIELD_KWARGS)
    tuesday_evening = models.BooleanField(**FIELD_KWARGS)
    tuesday_night = models.BooleanField(**FIELD_KWARGS)

    wednesday_early_morning = models.BooleanField(**FIELD_KWARGS)
    wednesday_morning = models.BooleanField(**FIELD_KWARGS)
    wednesday_afternoon = models.BooleanField(**FIELD_KWARGS)
    wednesday_evening = models.BooleanField(**FIELD_KWARGS)
    wednesday_night = models.BooleanField(**FIELD_KWARGS)

    thursday_early_morning = models.BooleanField(**FIELD_KWARGS)
    thursday_morning = models.BooleanField(**FIELD_KWARGS)
    thursday_afternoon = models.BooleanField(**FIELD_KWARGS)
    thursday_evening = models.BooleanField(**FIELD_KWARGS)
    thursday_night = models.BooleanField(**FIELD_KWARGS)

    friday_early_morning = models.BooleanField(**FIELD_KWARGS)
    friday_morning = models.BooleanField(**FIELD_KWARGS)
    friday_afternoon = models.BooleanField(**FIELD_KWARGS)
    friday_evening = models.BooleanField(**FIELD_KWARGS)
    friday_night = models.BooleanField(**FIELD_KWARGS)

    saturday_early_morning = models.BooleanField(**FIELD_KWARGS)
    saturday_morning = models.BooleanField(**FIELD_KWARGS)
    saturday_afternoon = models.BooleanField(**FIELD_KWARGS)
    saturday_evening = models.BooleanField(**FIELD_KWARGS)
    saturday_night = models.BooleanField(**FIELD_KWARGS)

    sunday_early_morning = models.BooleanField(**FIELD_KWARGS)
    sunday_morning = models.BooleanField(**FIELD_KWARGS)
    sunday_afternoon = models.BooleanField(**FIELD_KWARGS)
    sunday_evening = models.BooleanField(**FIELD_KWARGS)
    sunday_night = models.BooleanField(**FIELD_KWARGS)

    @classmethod
    def shift_from_time(cls, given_time):
        "Returns a shift, based on a given time."
        for shift, start_hour, end_hour in cls.SHIFT_TIMES:
            if start_hour < end_hour:
                # If the start hour is before the end hour, just see
                # if the time is between them
                if given_time >= time(start_hour) \
                                               and given_time < time(end_hour):
                    return shift
            else:
                # For the shift time that spans midnight, it's a different test
                if given_time >= time(start_hour) \
                                        or given_time < time(end_hour):
                    return shift
        raise ValueError('Could not find shift for time %s.' % given_time)

    class Meta:
        verbose_name_plural = "Availability"



def _is_full(self):
    "Returns whether or not the job request is fully booked."
    return self.bookings.count() >= self.number_of_freelancers
JobRequest.is_full = property(_is_full)

def _number_of_invited_freelancers(self):
    """ Returns the number of invited freelancers for specific job request.
    """
    return self.invitations.count()
JobRequest.number_of_invited_freelancers = property(_number_of_invited_freelancers)

def _number_of_applied_freelancers(self):
    """ Returns the number of applied freelancers for specific job request.
    """
    undeclined_applications = self.invitations.undeclined_applications()
    return undeclined_applications.count()
JobRequest.number_of_applied_freelancers = property(_number_of_applied_freelancers)


def _has_freelancers_waiting_acceptance(self):
    """ Returns whether or not job request has any applied freelancers
    waiting to be accepted.
    """
    undeclined_applications = self.invitations.undeclined_applications()
    booked_freelancers = self.bookings.get_queryset()
    return booked_freelancers.count() < undeclined_applications.count()
JobRequest.has_freelancers_waiting_acceptance = property(_has_freelancers_waiting_acceptance)

def _has_enough_applications(self):
    """Returns whether or not the job request has received enough applications
    to be suitable for confirmation.
    """
    undeclined_applications = self.invitations.undeclined_applications()
    return undeclined_applications.count() >= self.number_of_freelancers
JobRequest.has_enough_applications = property(_has_enough_applications)


def get_job_requests_pending_confirmation():
    """Returns all the job requests that are pending confirmation from staff.
    """
    # TODO - this should be optimised!
    pending_job_request_ids = []
    for job_request in JobRequest.objects.filter(status=JobRequest.STATUS_OPEN):
        if job_request.has_enough_applications:
            pending_job_request_ids.append(job_request.id)
    return JobRequest.objects.filter(id__in=pending_job_request_ids)
