from rest_framework import viewsets, mixins, status
from .serializers import PaymentTokenSerializer, JobRequestPaymentSerializer
from apps.client.models import Client
from apps.api.views import RetrieveViewset
from apps.api.client.permissions import ClientOnlyPermission
from apps.api.job.views import JobRequestForClientViewSet
from apps.job.models import JobRequest
from rest_framework.decorators import detail_route
from rest_framework.response import Response

class PaymentTokenViewSet(RetrieveViewset):
    """A Braintree 'client token' for the currently logged in
    client.  This endpoint will generate a new token each time it is called.
    
    ## Fields
    
    - `client_token` The Braintree 'client token' for the client.

    """
    model_class = Client
    serializer_class = PaymentTokenSerializer
    permission_classes = (ClientOnlyPermission,)

    def get_object(self):
        return self.request.user.client


class JobRequestPaymentViewSet(mixins.CreateModelMixin,
                               viewsets.GenericViewSet):
    """Endpoint for creating a payment on a job request
    
    ## Fields
    
    - `job_request_id` The id of the job request that is being paid for.
    - `nonce` The payment nonce, provided by Braintree.
    """
    permission_classes = (ClientOnlyPermission,)
    serializer_class = JobRequestPaymentSerializer
