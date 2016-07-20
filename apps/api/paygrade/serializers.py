from rest_framework import serializers
from apps.api.serializers import MoneyField
from apps.paygrade.models import BasePayGrade


class BasePayGradeSerializer(serializers.ModelSerializer):
    """Serializer that provides pay grade information.
    """
    min_client_pay_per_hour = MoneyField()

    class Meta:
        model = BasePayGrade
        fields = ('min_client_pay_per_hour',)
