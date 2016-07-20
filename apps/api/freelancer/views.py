from django.db.models import Q
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from ..client.permissions import ClientOnlyPermission
from apps.api.views import RetrieveAndUpdateViewset
from .serializers import FreelancerForClientSerializer, OwnFreelancerSerializer
from ..booking.serializers import AvailabilitySerializer
from .permissions import FreelancerOnlyPermission
from apps.freelancer.models import Freelancer
from apps.booking.models import Booking, Availability
from apps.job.models import JobRequest
from rest_framework.response import Response
from rest_framework import status
from collections import defaultdict
from moneyed.classes import Money
from decimal import Decimal

class FreelancerForClientViewSet(viewsets.ReadOnlyModelViewSet):
    """The freelancers that the currently logged in client has permission to see.
    
    ## Fields
    
    - `id` Unique id for the freelancer.  Can be used as a unique id for 
           more specific kinds of freelancer objects, such as drivers.
           Integer.
    - `reference_number` Public reference number for the freelancer.
    - `specific_object` API URL for the service-specific version
       of the freelancer, which may contain additional service-specific fields.  
    - `service_key` The name of the service the freelancer offers.
    - `photo_thumbnail_medium` A thumbnail image, 75px x 97px,
       or `null` if they have not provided a photo.
    - `photo_thumbnail_large` A thumbnail image, 233px x 300px,
       or `null` if they have not provided a photo.
    - `english_fluency` Their English fluency level.  Choices are:
        - `"BA"` - Basic
        - `"CO"` - Conversational
        - `"FL"` - Fluent
        - `"NA"` - Native
    - `full_name` Their full name.
    - `first_name` Their first name.
    - `last_name` Their last name.
    - `mobile` Their mobile phone number.
    - `years_experience` The number of years of working experience.
        Integer.  Choices are:
        - `0` - Less than 1 year
        - `1` - 1 - 3 years
        - `3` - 3 - 5 years
        - `5` - More than 5 years
    - `minimum_pay_per_hour` The minimum hourly rate, in GBP, the freelancer is
      willing to work for.  Decimal.
    - `average_score` The average rating score, out of 5,
                    that the freelancer has received, or null if there is no feedback.
                    Decimal.  Read only.
    """
    serializer_class = FreelancerForClientSerializer

    permission_classes = (ClientOnlyPermission,)
    model_class = Freelancer

    def get_queryset(self):
        # Show only published freelancers who are booked in to the client's jobs
        client_bookings = Booking.objects.for_client(self.request.user.client)
        return self.model_class.published_objects.filter(
                                    bookings__in=client_bookings).distinct()


class OwnFreelancerViewSet(RetrieveAndUpdateViewset):
    """The currently logged in freelancer's profile.
    
    ## Fields
    
    - `id` Unique id for the freelancer.  Can be used as a unique id for 
           more specific kinds of freelancer objects, such as drivers.
           Integer. Read only.
    - `reference_number` Public reference number for the freelancer.  Read only.
    - `service` The name of the service the freelancer offers.
    - `email` Their email address.  Read only.
    - `full_name` Their full name.  Read only.
    - `first_name` Their first name.
    - `last_name` Their last name.
    - `mobile` Their mobile telephone number (must be UK based).
    - `photo_thumbnail_medium` A thumbnail image, 75px x 97px, or `null` if they
      have not provided a photo.  Read only.
    - `photo_thumbnail_large` A thumbnail image, 233px x 300px,
       or `null` if they have not provided a photo.
    - `english_fluency` Their English fluency level.  Choices are:
        - `"BA"` - Basic
        - `"CO"` - Conversational
        - `"FL"` - Fluent
        - `"NA"` - Native
    - `eligible_to_work` Whether they are eligible to work in the UK. Boolean.
    - `minimum_pay_per_hour` The minimum pay they will accept per hour, in GBP.
       Decimal.
   - `average_score` The average rating score, out of 5,
            that the freelancer has received, or null if there is no feedback.
            Decimal.  Read only.
    - `postcode` The freelancer's home postcode.
    - `longitude` The longitude value of the postcode.  Read only.
    - `latitude` The latitude value of the postcode.  Read only.
    - `travel_distance` How far the freelancer is willing to travel for work.
       Integer. Choices are:
        - `1` - One mile
        - `2` - Two miles
        - `5` - Five miles
        - `10` - 10 miles
        - `20` - 20 miles
        - `50` - 50 miles
    - `years_experience` The number of years of working experience.
        Integer.  Choices are:
        - `0` - Less than 1 year
        - `1` - 1 - 3 years
        - `3` - 3 - 5 years
        - `5` - More than 5 years
    """
    model = Freelancer
    serializer_class = OwnFreelancerSerializer

    permission_classes = (FreelancerOnlyPermission,)

    def get_object(self):
        return self.request.user.freelancer

class OwnFreelancerAvailabilityViewSet(RetrieveAndUpdateViewset):
    """The currently logged in freelancer's availability.
    """
    model = Availability
    serializer_class = AvailabilitySerializer

    permission_classes = (FreelancerOnlyPermission,)

    def get_object(self):
        # Return the Availability for the Freelancer, creating
        # (but not saving) one if it doesn't exist.
        freelancer = self.request.user.freelancer
        try:
           return freelancer.availability
        except Availability.DoesNotExist:
           return Availability(freelancer=freelancer)


class FreelancerEarningView(APIView):
    """The currently logged in freelancer's earnings.

    A bit crude, this should probably change for future versions of the app.

    ## Fields

    - `"CF"` - Confirmed.  The freelancers confirmed jobs.
    - `"CP"` - Complete.  The freelancers completed jobs.
    """
    permission_classes = (FreelancerOnlyPermission,)

    def get(self, request, format=None):
      fl = self.request.user.freelancer
      jrs = JobRequest.objects.filter(bookings__freelancer=fl)
      # TODO: Foreign currencies are ignored for now
      result = defaultdict(lambda:Money(0, "GBP"))
      for j in filter(lambda x:x.status in set(['CP', 'CF']), jrs):
        result[j.status] += j.client_pay_per_hour * j.duration
      # Converting for serialization
      for st in result.keys():
        result[st] = {"amount": result[st].amount, "currency": result[st].currency.code}
      return Response(result, status=status.HTTP_200_OK)

