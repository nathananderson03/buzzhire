from django.db.models import Q
from rest_framework import viewsets, mixins
from ..freelancer.permissions import FreelancerOnlyPermission
from ..client.permissions import ClientOnlyPermission
from ..booking.serializers import BookingsJobRequestForClientSerializer
from .serializers import (JobRequestForFreelancerSerializer,
                          JobRequestForClientSerializer)
from apps.job.models import JobRequest
from apps.api.views import DateSliceMixin


class JobRequestForClientViewSet(DateSliceMixin, viewsets.ReadOnlyModelViewSet):
    """All job requests created by the logged in client.
    
    This endpoint can be used to list job requests.  To create job
    requests, you must use the service-specific endpoints.
    
    ## Query parameters
    
    - `dateslice` Optional. Limit results by date.  Choices are:
        - `past` All past job requests for the client.
        - `future` All future job requests for the client.
      
      For example, to get all future job requests, the endpoint would be
      `/client/job-requests/?dateslice=future`. 
     
    ## Fields
    
    - `id` Unique id for the job request.  Can be used as a unique id for 
           more specific kinds of job request objects,
           such as driver job requests. Integer. Read only.
    - `reference_number` Public reference number for the job request.  Read only.
    - `service_key` Name of the service provided.
    - `specific_object` API URL for the service-specific version
       of the job request, which may contain additional service-specific fields.  
    - `status` The status of the job request:  Choices are:
        - `"IC"` - The client has created the job request but has not yet paid.
        - `"OP"` -  Open.  The client has paid and the job request is now ready for booking.
        - `"CF"` - Confirmed.  The freelancers have now been assigned.
        - `"CP"` - Complete.  The work has been completed.
        - `"CA"` - Cancelled.  The job request has been cancelled.
    - `tips_included` Whether tips are included in the fee.  Boolean.
    - `date` The start date of the job.  Format `"YYYY-MM-DD"`.  When creating
       a new job request, the date and start_time (below) must be in the future.
    - `start_time` The start time of the job.  Format `"00:00:00"`.
    - `duration` The duration of the job, in hours.  Integer.  Minimum 2.
    - `number_of_freelancers` The number of freelancers required to
      undertake the job.  Integer, 1 - 9.
    - `address1` - First line of the address the job is taking place at.
    - `address2` - Second line of address.
    - `city` - City.  Must be `"London"`.
    - `postcode` - A valid London postcode.
    - `longitude` The longitude value of the postcode.  Read only.
    - `latitude` The latitude value of the postcode.  Read only.
    - `years_experience` The minimum number of years of working experience
       required. Integer.  Choices are:
        - `0` - No preference
        - `1` - 1 year
        - `3` - 3 years
        - `5` - 5 years
    - `comments` Any extra information the client wants to tell the freelancer.
      Free text.    
    - `client_pay_per_hour` The amount, in GBP, that the client will
      pay per hour.  Decimal, must be 8.0 or greater.
    - `client_total_cost` The total cost of the job to the client, in GBP.
    - `needs_feedback_from_client` Whether or not feedback is required for this
       job request.  Boolean.  Read only.
    - `bookings` A list of any bookings of freelancers onto this job request.
       Read only. Fields for each bookings are:
        - `id` The unique booking id.
        - `reference_number` Public reference number for the booking.
        - `freelancer` URL of freelancer endpoint.
        - `date_created` The date and time the booking was created.
    """
    serializer_class = BookingsJobRequestForClientSerializer
    permission_classes = (ClientOnlyPermission,)
    model_class = JobRequest

    def get_queryset(self):
        queryset = self.model_class.objects.for_client(
                                                self.request.user.client)
        queryset = self.datesliced_queryset(queryset)
        return queryset


class ServiceSpecificJobRequestForClientViewSet(mixins.CreateModelMixin,
                                                JobRequestForClientViewSet):
    """Viewset for service specific job request viewsets to inherit.
    Allows creation of job requests (not allowed on the generic job request
    endpoint).
    """
    pass

class JobRequestForFreelancerViewSet(DateSliceMixin,
                                     viewsets.ReadOnlyModelViewSet):
    """All job requests for the logged in freelancer
    (ones either invited or booked on).
    
    ## Query parameters
    
    - `dateslice` Optional. Limit results by date.  Choices are:
        - `past` Past job requests.
        - `future` Future job requests.
    
    ## Fields
    
    - `id` Unique id for the job request.  Can be used as a unique id for 
           more specific kinds of job request objects,
           such as driver job requests. Integer. Read only.
    - `reference_number` Public reference number for the job request.  Read only.
    - `service_key` Name of the service provided.
    - `specific_object` API URL for the service-specific version
       of the job request, which may contain additional service-specific fields.  
    - `status` The status of the job request:  Choices are:
        - `"IC"` - The client has created the job request but has not yet paid.
        - `"OP"` -  Open.  The client has paid and the job request is now ready for booking.
        - `"CF"` - Confirmed.  The freelancers have now been assigned.
        - `"CP"` - Complete.  The work has been completed.
        - `"CA"` - Cancelled.  The job request has been cancelled.
    - `tips_included` Whether tips are included in the fee.  Boolean.
    - `date` The start date of the job.  Format `"YYYY-MM-DD"`.
    - `start_time` The start time of the job.  Format `"00:00:00"`.
    - `duration` The duration of the job, in hours.  Integer.
    - `number_of_freelancers` The number of freelancers required to
      undertake the job.  Integer.
    - `address1` - First line of the address the job is taking place at.
    - `address2` - Second line of address.
    - `city` - City.  Must be `"London"`.
    - `postcode` - A valid London postcode.
    - `longitude` The longitude value of the postcode.  Read only.
    - `latitude` The latitude value of the postcode.  Read only.
    - `years_experience` The minimum number of years of working experience
       required. Integer.  Choices are:
        - `0` - No preference
        - `1` - 1 year
        - `3` - 3 years
        - `5` - 5 years
    - `comments` Any extra information the client wants to tell the freelancer.
      Free text.
    - `summary_for_freelancer` A brief description of the job, for the
      freelancer to read.
    - `client` The client who created the job request.  API endpoint.  Read only.
    - `client_full` Full json object of the client.  Read only.
    - `freelancer_pay_per_hour`: The amount, in GBP, that the freelancer will
      be paid per hour.  This is based on the `client_pay_per_hour` field.
      Decimal.  Read only.
    """
    serializer_class = JobRequestForFreelancerSerializer
    permission_classes = (FreelancerOnlyPermission,)
    model_class = JobRequest

    def get_queryset(self):
        # Limit to job requests that the freelancer has been
        # invited to or booked on
        freelancer = self.request.user.freelancer
        # TODO: This returned the same JobRequest object multiple times.
        #       Not that bad for the overview, but breaks the individual views:
        #       fine:   /api/v1/freelancer/job-requests/
        #       broken: /api/v1/freelancer/job-requests/155/
        from_bookings = map(lambda x:x.jobrequest.id, freelancer.bookings.all())
        from_invitations = map(lambda x:x.jobrequest.id, freelancer.invitations.all())
        queryset = self.model_class.objects.filter(id__in=set(from_bookings + from_invitations))

        queryset = self.datesliced_queryset(queryset)

        return queryset

