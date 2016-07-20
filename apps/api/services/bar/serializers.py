from django.forms import widgets
from rest_framework import serializers
from apps.services.bar.models import BarFreelancer, BarJobRequest, BarPayGrade
from ...freelancer.serializers import (OwnFreelancerSerializer,
                                             FreelancerForClientSerializer)
from ...job.serializers import JobRequestForFreelancerSerializer
from ...booking.serializers import BookingsJobRequestForClientSerializer
from ...paygrade.serializers import BasePayGradeSerializer


class BarFreelancerForClientSerializer(FreelancerForClientSerializer):
    """Serializer for public views of bar."""

    class Meta(FreelancerForClientSerializer.Meta):
        model = BarFreelancer
        fields = FreelancerForClientSerializer.Meta.fields + ('role',)


class PrivateBarFreelancerSerializer(OwnFreelancerSerializer):
    """Serializer for the bar freelancer's own profile."""

    class Meta(OwnFreelancerSerializer.Meta):
        model = BarFreelancer
        fields = OwnFreelancerSerializer.Meta.fields + ('role',)



class BarJobRequestForFreelancerSerializer(JobRequestForFreelancerSerializer):
    class Meta(JobRequestForFreelancerSerializer.Meta):
        model = BarJobRequest
        fields = JobRequestForFreelancerSerializer.Meta.fields + \
                  ('role',)


class BarJobRequestForClientSerializer(BookingsJobRequestForClientSerializer):
    class Meta(BookingsJobRequestForClientSerializer.Meta):
        model = BarJobRequest
        fields = BookingsJobRequestForClientSerializer.Meta.fields + \
                  ('role',)


class BarPayGradeSerializer(BasePayGradeSerializer):
    class Meta(BasePayGradeSerializer.Meta):
        model = BarPayGrade