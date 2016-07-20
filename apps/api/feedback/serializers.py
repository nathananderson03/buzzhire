from rest_framework import serializers
from apps.feedback.models import BookingFeedback
from rest_framework.validators import ValidationError
from ..booking.serializers import BookingForClientSerializer


class BookingAwaitingFeedbackFromClientSerializer(BookingForClientSerializer):
    "A booking that requires feedback from a client."
    job_request = serializers.HyperlinkedRelatedField(
                                    view_name='job_requests_for_client-detail',
                                    read_only=True,
                                    source='jobrequest')

    class Meta(BookingForClientSerializer.Meta):
        fields = BookingForClientSerializer.Meta.fields + ('job_request',)


class FreelancerHyperlinkedField(serializers.HyperlinkedRelatedField):
    """Field linking the freelancer from the feedback."""
    def get_attribute(self, instance):
        return instance.booking.freelancer

class JobRequestHyperlinkedField(serializers.HyperlinkedRelatedField):
    """Field linking the job request from the feedback."""
    def get_attribute(self, instance):
        return instance.booking.jobrequest


class FeedbackByClientSerializer(serializers.ModelSerializer):
    freelancer = FreelancerHyperlinkedField(
                        view_name='freelancers_for_client-detail',
                        read_only=True)
    job_request = JobRequestHyperlinkedField(
                        view_name='job_requests_for_client-detail',
                        read_only=True)

    def validate(self, attrs):
        # Check that they are the client for this booking
        if attrs['booking'].jobrequest.client != \
                                self.context['request'].user.client:
            raise ValidationError(
                {'booking': 'That booking is not owned by the client.'})

        # Check that the booking does not already have feedback
        if BookingFeedback.objects.filter(
                        author_type=BookingFeedback.AUTHOR_TYPE_CLIENT,
                        booking=attrs['booking']).exists():
            raise ValidationError(
                {'booking': 'Feedback for that booking already exists.'})

        # During creation, set the type of feedback to be the client.
        attrs['author_type'] = BookingFeedback.AUTHOR_TYPE_CLIENT
        attrs = super(FeedbackByClientSerializer, self).validate(attrs)
        return attrs

    class Meta:
        model = BookingFeedback
        fields = ('id', 'booking', 'freelancer', 'job_request',
                  'score', 'comment')
