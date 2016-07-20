from apps.services.cleaner.models import CleanerJobRequest, CleanerPayGrade
from ...booking.serializers import BookingsJobRequestForClientSerializer
from ...paygrade.serializers import BasePayGradeSerializer


class CleanerJobRequestForClientSerializer(
                                        BookingsJobRequestForClientSerializer):
    class Meta(BookingsJobRequestForClientSerializer.Meta):
        model = CleanerJobRequest


class CleanerPayGradeSerializer(BasePayGradeSerializer):
    class Meta(BasePayGradeSerializer.Meta):
        model = CleanerPayGrade
