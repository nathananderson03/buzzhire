from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from ..freelancer.permissions import FreelancerOnlyPermission
from .serializers import (ClientForFreelancerSerializer, OwnClientSerializer,
                          ClientSerializer)
from .authentication import CSRFExemptAuthentication
from apps.client.models import Client
from apps.api.views import RetrieveAndUpdateViewset
from .permissions import ClientOnlyPermission
from apps.booking.models import Booking, Invitation
from apps.job.models import JobRequest
from django.db.models import Q


class ClientForFreelancerViewSet(viewsets.ReadOnlyModelViewSet):
    """Clients viewable by the currently logged in freelancer.

    ## Fields

    - `id` Unique id for the client. Integer.
    - `reference_number` Public reference number for the client.
    - `first_name` Their first name.
    - `last_name` Their last name.
    - `company_name` The name of their company, if applicable.
    """
    serializer_class = ClientForFreelancerSerializer
    permission_classes = (FreelancerOnlyPermission,)

    def get_queryset(self):
        # Limit by only clients whose job requests the freelancer is booked on
        # Job requests for the freelancer
        freelancer = self.request.user.freelancer
        job_requests = JobRequest.objects.filter(
                    Q(bookings__freelancer=freelancer) | \
                    Q(invitations__freelancer=freelancer))
        return Client.objects.filter(job_requests__in=job_requests).distinct()


class OwnClientViewSet(RetrieveAndUpdateViewset):
    """The currently logged in client's profile.

    ## Fields

    - `id` Unique id for the client. Integer. Read only.
    - `reference_number` Public reference number for the client.  Read only.
    - `email` Their email address.  Read only.
    - `mobile` Their UK mobile phone number.
    - `company_name` The name of their company, if applicable.

    """
    model = Client
    serializer_class = OwnClientSerializer

    permission_classes = (ClientOnlyPermission,)

    def get_object(self):
        return self.request.user.client


class ClientRegisterView(CreateAPIView):
    model = Client
    serializer_class = ClientSerializer

    authentication_classes = (CSRFExemptAuthentication,)

