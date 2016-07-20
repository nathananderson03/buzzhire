from rest_framework import serializers
from apps.client.models import Client
from apps.payment.utils import PaymentAPI, PaymentException
from apps.job.models import JobRequest
import logging

logger = logging.getLogger('project')


class PaymentTokenSerializer(serializers.ModelSerializer):
    """Serializer that provides client payment token.
    """
    client_token = serializers.SerializerMethodField()
    def get_client_token(self, obj):
        # Generates a Braintree 'client token' for the Client model
        return PaymentAPI().generate_client_token(obj)

    class Meta:
        model = Client
        fields = ('client_token',)


class JobRequestPaymentSerializer(serializers.Serializer):
    """Serializer for a job request payment.
    
    NB this is not a model serializer; creating a job request payment does not
    create a model, instead it attempts to take payment on a job request.
    
    """
    job_request_id = serializers.IntegerField()
    nonce = serializers.CharField(max_length=200)

    def validate_job_request_id(self, value):
        client = self.context['request'].user.client
        try:
            self.job_request = JobRequest.objects.for_client(client).get(
                                                                    id=value)
        except:
            raise serializers.ValidationError(
                                'Could not get job request for that client.')

        if self.job_request.status != JobRequest.STATUS_CHECKOUT:
            raise serializers.ValidationError(
                                        'Job request must be in checkout.')
        return value

    def create(self, validated_data):
        # Take payment
        try:
            api = PaymentAPI()
            api.take_payment(validated_data['nonce'],
                             amount=self.job_request.client_total_cost.amount,
                             order_id=self.job_request.reference_number)
        except PaymentException as e:
            logger.exception(e)
            raise serializers.ValidationError(
                               'Sorry, there was an issue taking payment.')
        else:
            # Payment successful; open the job request
            self.job_request.open()
            self.job_request.save()

        return validated_data
