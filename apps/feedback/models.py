from django.db import models
from django.core import validators
from apps.job.models import JobRequest
from apps.booking.models import Booking
from apps.freelancer.models import Freelancer
from django.db.models import Avg


def _average_score(self):
    """Returns the average score for the Freelancer.
     The algorithm should be all ratings for that driver,
     but with the 5 most recent given double weighting, to one decimal point.
    """
    # Specify the querysets - giving double weighting to the most
    # recent five feedbacks
    feedback = BookingFeedback.objects.feedback_for_freelancer(self).order_by(
                                                                    '-date')
    weighted_feedback = (
        (feedback[:5], 2),
        (feedback[5:], 1),
    )

    # Assemble a list of averages which we will then average.  This allows
    # us to 'weight' certain querysets by including them multiple times in
    # the averages list.
    averages = [5]
    for feedbacks, weighting in weighted_feedback:
        average = feedbacks.aggregate(Avg('score')).values()[0]
        # Add the average as many times as the weighting specifies
        # (not adding it if it's None)
        [averages.append(average) for i in range(weighting) if average != None]

    if not averages:
        return None

    return round(sum(averages) / len(averages), 1)

def _reviews(self, limit=20):
  feedback = BookingFeedback.objects.feedback_for_freelancer(self).order_by('-date')
  # TODO: Look at BookingFeedback Serializer
  return feedback[:limit] 

Freelancer.average_score = _average_score
Freelancer.reviews = _reviews

class FakeQuerySet(list):
    """An object that can be used to 'fake' a queryset, but which is actually a
    list of, for example, unsaved model instances.
    """
    ordered = True


class BookingFeedbackManager(models.Manager):
    "Model manager for BookingFeedbacks."

    def client_feedback_list(self, job_request):
        """Returns a list of non-saved BookingFeedback objects for the
        job request, for the client.
        """
        feedback_list = FakeQuerySet()
        # TODO - using get_bookings_awaiting_feedback_for_client is not
        # the most efficient way of doing this - it's a quick fix for now
        for booking in get_bookings_awaiting_feedback_for_client(
                                            job_request.client, job_request):
            feedback = BookingFeedback(
                booking=booking,
                author_type=BookingFeedback.AUTHOR_TYPE_CLIENT
            )
            feedback_list.append(feedback)
        return feedback_list

    def freelancer_feedback_list(self, job_request, freelancer):
        """Returns a list containing a single non-saved BookingFeedback object
        for the job request, for the freelancer.
        """
        feedback_list = FakeQuerySet()

        feedback = BookingFeedback(
            booking=job_request.bookings.get(freelancer=freelancer),
            author_type=BookingFeedback.AUTHOR_TYPE_FREELANCER
        )
        feedback_list.append(feedback)
        return feedback_list

    def client_feedback_exists(self, job_request):
        """Returns whether or not client feedback exists for the supplied
        job request.
        """
        return self.filter(author_type=BookingFeedback.AUTHOR_TYPE_CLIENT,
                           booking__jobrequest=job_request).exists()

    def freelancer_feedback_exists(self, job_request, freelancer):
        """Returns whether or not the supplied freelancer has left feedback
        for the supplied job request.
        """
        return self.feedback_by_freelancer(freelancer).filter(
                                    booking__jobrequest=job_request).exists()

    def client_feedback_from_booking(self, booking):
        """Returns the BookingFeedback given by the client for the supplied
        booking.  Raises DoesNotExist on failure.
        """
        return self.get(author_type=BookingFeedback.AUTHOR_TYPE_CLIENT,
                        booking=booking)

    def freelancer_feedback_from_booking(self, booking):
        """Returns the BookingFeedback given by the freelancer for the supplied
        booking.  Raises DoesNotExist on failure.
        """
        return self.get(author_type=BookingFeedback.AUTHOR_TYPE_FREELANCER,
                        booking=booking)

    def feedback_for_freelancer(self, freelancer):
        """Returns all the feedback for a particular freelancer.
        """
        return self.filter(author_type=BookingFeedback.AUTHOR_TYPE_CLIENT,
                           booking__freelancer=freelancer)

    def feedback_by_freelancer(self, freelancer):
        """Returns all the feedback by a particular freelancer.
        """
        return self.filter(author_type=BookingFeedback.AUTHOR_TYPE_FREELANCER,
                           booking__freelancer=freelancer)


    def feedback_by_client(self, client):
        """Returns all the feedback by a particular client.
        """
        return self.filter(author_type=BookingFeedback.AUTHOR_TYPE_CLIENT,
                           booking__jobrequest__client=client)


class BookingFeedback(models.Model):
    """A feedback associated with a booking, for a client or freelancer."""
    AUTHOR_TYPE_CLIENT = 'CL'
    AUTHOR_TYPE_FREELANCER = 'FR'
    AUTHOR_TYPE_CHOICES = (
        (AUTHOR_TYPE_CLIENT, 'Client'),
        (AUTHOR_TYPE_FREELANCER, 'Freelancer'),
    )

    author_type = models.CharField(max_length=2,
              choices=AUTHOR_TYPE_CHOICES,
              help_text='Whether the author of the feedback is '
                            'the client or the freelancer.')
    booking = models.ForeignKey(Booking)

    MAX_SCORE = 5

    score = models.PositiveSmallIntegerField(
                        validators=[validators.MinValueValidator(1),
                                    validators.MaxValueValidator(MAX_SCORE)])

    comment = models.TextField(blank=True)

    date = models.DateTimeField(auto_now_add=True)

    objects = BookingFeedbackManager()

    TARGET_MAP = {
        AUTHOR_TYPE_CLIENT:
                lambda booking: booking.freelancer,
        AUTHOR_TYPE_FREELANCER:
                lambda booking: booking.jobrequest.client,
    }

    def get_target(self):
        "Returns the client / freelancer that the feedback is for."
        return self.TARGET_MAP[self.author_type](self.booking)

    def get_author(self):
        "Returns the client / freelancer who authored the feedback."
        # Just get the opposite author type so we can use the TARGET_MAP
        opposite_author_type = [i for i in self.TARGET_MAP.keys()
                               if i != self.author_type][0]
        return self.TARGET_MAP[opposite_author_type](self.booking)

    class Meta:
        ordering = '-date',

    def __unicode__(self):
        return "%s for %s by %s" % (self.score,
                                    self.get_target(),
                                    self.get_author())


def _needs_feedback_from_client(self):
    """Returns whether or not the JobRequest needs any feedback from client.
    """
    return self.status == JobRequest.STATUS_COMPLETE and \
            get_bookings_awaiting_feedback_for_client(self.client,
                                                      self).exists()
JobRequest.needs_feedback_from_client = _needs_feedback_from_client


def get_bookings_awaiting_feedback_for_freelancer(freelancer):
    """Returns all the Bookings that are awaiting feedback from the freelancer.
    
    Should return bookings:
    - for job requests that are complete;
    - for the supplied freelancer;
    - where the supplied freelancer hasn't provided any feedback.
    """
    booking_pks = BookingFeedback.objects.feedback_by_freelancer(
                            freelancer).values_list('booking__pk', flat=True)
    bookings = Booking.objects.for_freelancer(
                freelancer=freelancer).complete().exclude(
                                                        pk__in=booking_pks)

    return bookings

def get_bookings_awaiting_feedback_for_client(client,
                                              job_request=None):
    """Returns all the Bookings that are awaiting feedback from the client.
    
    Optionally, filter by job request (TODO: this is an inefficient way to
    do it - we should improve it.)
    
    
    Should return bookings:
    - for job requests that are complete;
    - for the supplied client;
    - where the supplied client hasn't provided any feedback.
    """
    # TODO - surely this should be the same approach as in
    # get_bookings_awaiting_feedback_for_freelancer.  Work out which performs
    # better and make consistent.
    bookings = Booking.objects.for_client(
                client).exclude(bookingfeedback__author_type=\
                                    BookingFeedback.AUTHOR_TYPE_CLIENT
                ).complete()
    if job_request:
        bookings = bookings.filter(jobrequest=job_request)
    return bookings

def get_job_requests_awaiting_feedback_for_client(client):
    """Returns all the JobRequests that are awaiting feedback from the client.
    
    Should return job requests:
    - that are complete;
    - for the supplied client;
    - where the supplied client still needs to provide feedback.
    """
    # Get job request pks for the client's job requests that still need feedback
    jobs_needing_feedback = set(get_bookings_awaiting_feedback_for_client(
                            client).values_list('jobrequest_id', flat=True))
    return JobRequest.objects.filter(pk__in=jobs_needing_feedback)
