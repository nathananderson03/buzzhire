from django.db.models import Q
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from ..freelancer.permissions import FreelancerOnlyPermission
from .serializers import (BookingSerializer, InvitationSerializer,
                          ApplicationSerializer)
from apps.api.views import DateSliceMixin
from apps.booking.models import (Booking, Invitation,
                            JobAlreadyBookedByFreelancer, JobFullyBooked)


class BookingForFreelancerViewSet(DateSliceMixin, viewsets.ReadOnlyModelViewSet):
    """All bookings for the currently logged in freelancer.
    
    Note: you must be logged in as a freelancer.

    ## Query parameters
    
    - `dateslice` Optional. Limit results by date.  Choices are:
        - `past` All past bookings for the Freelancer.
        - `future` All future bookings for the Freelancer.
    
    ## Fields
    
    - `id` Unique id for the booking. Integer. Read only.
    - `reference_number` Public reference number for the booking.  Read only.
    - `job_request` API URL for the job request the booking is for.  
    - `date_created` Date and time of when the booking was created.
    """
    serializer_class = BookingSerializer

    permission_classes = (FreelancerOnlyPermission,)

    def get_queryset(self):
        queryset = Booking.objects.for_freelancer(self.request.user.freelancer)
        queryset = self.datesliced_queryset(queryset)
        return queryset


class InvitationForFreelancerViewSet(viewsets.ReadOnlyModelViewSet):
    """All invitations that can be applied to by the currently
    logged in freelancer.
    
    Note: you must be logged in as a freelancer.
    
    ## Fields
    
    - `id` Unique id for the invitation. Integer. Read only.
    - `reference_number` Public reference number for the invitation.  Read only.
    - `job_request` API URL for the job request the invitation is for.  
    - `date_created` Date and time of when the invitation was created.
    - `apply_endpoint` The API endpoint to POST to in order to
      apply to the job.
      
    ## Applying to jobs
    
    To apply to a job from an invitation, POST to the `apply_endpoint`
    provided.  No data is required.
    
    If the application was received successfully, it will return a 200.
    
    Invitations are not guaranteed to stay valid - for example, if a job is
    becomes fully booked.  If the invitation is no longer valid, the response
    will be a 404.
    """
    serializer_class = InvitationSerializer

    permission_classes = (FreelancerOnlyPermission,)

    def get_queryset(self):
        return Invitation.objects.can_be_applied_to_by_freelancer(
                                                self.request.user.freelancer)

    @detail_route(methods=['post'])
    def apply(self, request, pk=None):

        invitation = self.get_object()

        # Validation - at present the validation already happens in
        # get_queryset(), but we may want to give more specific feedback (as
        # it will just say 'Not found' if it can't find the invitation.
#         try:
#             invitation.validate_can_be_accepted()
#         except JobFullyBooked:
#             return Response('This job request is now fully booked.',
#                             status=status.HTTP_400_BAD_REQUEST)
#         except JobAlreadyBookedByFreelancer:
#             # This shouldn't happen, but just in case
#             return Response('This job request has already been accepted' \
#                             'by the freelancer.',
#                             status=status.HTTP_400_BAD_REQUEST)

        # TODO - consider potential race condition here?

        invitation.mark_as_applied()
        # This must return a json object for the app to treat it as a success
        return Response({'message': 'Applied.'})


class ApplicationForFreelancerViewSet(DateSliceMixin,
                                      viewsets.ReadOnlyModelViewSet):
    """All Applications that have been made by the freelancer, and that have
    not been converted into Bookings.
    
    Applications are just Invitations that have been applied to.  The list of
    Applications will include ones which are still awaiting acceptance, and ones
    which have been declined.  Accepted applications will not appear here.
    
    Note: you must be logged in as a freelancer.
    
    ## Query parameters
    
    - `dateslice` Optional. Limit results by date.  Choices are:
        - `past` All past bookings for the Freelancer.
        - `future` All future bookings for the Freelancer.
    
    ## Fields
    
    - `id` Unique id for the invitation. Integer. Read only.
    - `reference_number` Public reference number for the invitation.  Read only.
    - `job_request` API URL for the job request the invitation is for.  
    - `date_created` Date and time of when the invitation was created.
    - `date_applied` Date and time of when the job was applied to.
    - `date_declined` Date and time of when the application was declined,
      or `null` if it hasn't been declined.
    
    """
    serializer_class = ApplicationSerializer

    permission_classes = (FreelancerOnlyPermission,)

    def get_queryset(self):
        queryset = Invitation.objects.applied_to_by_freelancer(
                                                self.request.user.freelancer)
        queryset = self.datesliced_queryset(queryset)
        return queryset
