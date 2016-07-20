from apps.services.waiting.models import WaitingJobRequest, WaitingPayGrade
from ...booking.serializers import BookingsJobRequestForClientSerializer
from ...paygrade.serializers import BasePayGradeSerializer


class WaitingJobRequestForClientSerializer(
                                        BookingsJobRequestForClientSerializer):
    class Meta(BookingsJobRequestForClientSerializer.Meta):
        model = WaitingJobRequest


class WaitingPayGradeSerializer(BasePayGradeSerializer):
    class Meta(BasePayGradeSerializer.Meta):
        model = WaitingPayGrade
