from django.forms import widgets
from django.conf import settings
from django.core import validators
from rest_framework import serializers
from rest_framework.utils.field_mapping import get_field_kwargs
from apps.api.serializers import MoneyField
from apps.job import service_from_class
from apps.job.models import JobRequest
from ..location.serializers import PostcodeField
from ..client.serializers import ClientForFreelancerSerializer
from apps.job.validators import validate_start_date_and_time


class SpecificJobRequestIdentityField(serializers.HyperlinkedIdentityField):
    """A read-only field that represents the identity URL for the specific,
    non-generic version of the job request.
    """
    def get_url(self, obj, view_name, request, format):
        try:
            service = service_from_class(obj.__class__)
        except ValueError:
            # This can happen if a job request doesn't have a specific
            # service associated with it - don't cause the whole API to break
            # as a result
            pass
        else:
            view_name = service.key + '_' + view_name
        return super(SpecificJobRequestIdentityField, self).get_url(obj,
                                                    view_name, request, format)


class BaseJobRequestSerializer(serializers.ModelSerializer):
    """Base serializer for job requests ."""
    service_key = serializers.SerializerMethodField()
    def get_service_key(self, obj):
        "Returns the service key."
        try:
            return service_from_class(obj.__class__).key
        except ValueError:
            return 'unknown'


#     address = serializers.SerializerMethodField('_address')
#     def _address(self, obj):
#         return {
#             'address1': obj.address1,
#             'address2': obj.address2,
#             'city': obj.get_city_display(),
#             'postcode': str(obj.postcode),
#         }

    postcode = PostcodeField(required=True)

    latitude = serializers.SerializerMethodField()
    def get_latitude(self, obj):
        return obj.postcode.latitude

    longitude = serializers.SerializerMethodField()
    def get_longitude(self, obj):
        return obj.postcode.longitude

    city = serializers.SerializerMethodField()
    def get_city(self, obj):
        return obj.get_city_display()

    duration = serializers.IntegerField(
        validators=[validators.MinValueValidator(settings.MIN_JOB_DURATION)])

    class Meta:
        model = JobRequest
        fields = ('id', 'reference_number', 'service_key',
                  'specific_object', 'status',
                  'tips_included', 'date', 'start_time', 'duration',
                  'number_of_freelancers', 'address1', 'address2', 'city',
                  'postcode', 'longitude', 'latitude',
                  'years_experience', 'comments',
                  'summary_for_freelancer',
                  )
        read_only_fields = ('status',)


class JobRequestForFreelancerSerializer(BaseJobRequestSerializer):
    """Serializer for job requests for freelancer."""

    client = serializers.HyperlinkedRelatedField(read_only=True,
                                    view_name='clients_for_freelancer-detail')

    client_full = ClientForFreelancerSerializer(source='client')

    freelancer_pay_per_hour = MoneyField()

    specific_object = SpecificJobRequestIdentityField(
                            view_name='job_requests_for_freelancer-detail')

    class Meta(BaseJobRequestSerializer.Meta):
        fields = BaseJobRequestSerializer.Meta.fields + ('client',
                                    'client_full', 'freelancer_pay_per_hour')


class JobRequestForClientSerializer(BaseJobRequestSerializer):
    """Serializer for job requests for client."""

    # Make sure we use the same validators
    client_pay_per_hour = MoneyField(
                    validators=JobRequest._meta.get_field(
                                            'client_pay_per_hour').validators)

    client_total_cost = MoneyField(read_only=True)

    specific_object = SpecificJobRequestIdentityField(
                            view_name='job_requests_for_client-detail')

    def validate(self, attrs):

        # Populates the object with the client (useful for creation)
        attrs['client'] = self.context['request'].user.client
        attrs = super(JobRequestForClientSerializer, self).validate(attrs)
        validate_start_date_and_time(attrs['date'], attrs['start_time'])
        return attrs

    class Meta(BaseJobRequestSerializer.Meta):
        fields = BaseJobRequestSerializer.Meta.fields + (
                        'client_pay_per_hour', 'client_total_cost',
                        'needs_feedback_from_client')
