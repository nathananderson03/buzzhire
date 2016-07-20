from django.forms import widgets
from django.core import validators
from rest_framework import serializers
from sorl.thumbnail import get_thumbnail
from django.conf import settings
from ..serializers import MoneyField
from apps.freelancer.templatetags.freelancer import PHOTO_DIMENSIONS
from ..location.serializers import PostcodeField
from apps.freelancer.utils import service_for_freelancer
from apps.freelancer.models import Freelancer, FREELANCER_MIN_WAGE
from apps.core.validators import mobile_validator


class ThumbnailField(serializers.SerializerMethodField):
    "Serializer field for returning photo thumbnails."

    def __init__(self, *args, **kwargs):
        self.size = kwargs.pop('size')
        super(ThumbnailField, self).__init__(*args, **kwargs)

    def to_representation(self, value):
        if value.photo:
             return "%s%s" % (settings.BASE_URL,
                get_thumbnail(value.photo, PHOTO_DIMENSIONS[self.size]).url)
        return None


class SpecificFreelancerIdentityField(serializers.HyperlinkedIdentityField):
    """A read-only field that represents the identity URL for the specific,
    non-generic version of the freelancer.
    Optionally, specify pass_reverse_kwargs=False when instantiating.  This
    allows it to work with views that get a single object without needing
    any kwargs passed to the url, such as a RetrieveAndUpdateViewset in
    combination with a SingleObjectFriendlyRouter.
    """
    def __init__(self, pass_reverse_kwargs=True, *args, **kwargs):
        self.pass_reverse_kwargs = pass_reverse_kwargs
        super(SpecificFreelancerIdentityField, self).__init__(*args, **kwargs)

    def get_url(self, obj, view_name, request, format):
        service = service_for_freelancer(obj)
        view_name = service.key + '_' + view_name
        if self.pass_reverse_kwargs:
            return super(SpecificFreelancerIdentityField, self).get_url(obj,
                                                    view_name, request, format)
        else:
            # In this case, we don't want to pass any kwargs through to
            # the reverse function
            return self.reverse(view_name, request=request, format=format)


class FreelancerForClientSerializer(serializers.ModelSerializer):
    """Serializer that exposes information on the freelancer
    appropriate for client use.
    """
    reviews = serializers.SerializerMethodField()
    def get_reviews(self, obj):
      for r in obj.reviews():
        yield {'comment': r.comment, "score":r.score}

    service_key = serializers.SerializerMethodField()
    def get_service_key(self, obj):
        "Returns the service key."
        return service_for_freelancer(obj).key

    full_name = serializers.SerializerMethodField()
    specific_object = SpecificFreelancerIdentityField(
                                    view_name='freelancers_for_client-detail')

    minimum_pay_per_hour = MoneyField()

    def get_full_name(self, obj):
        return obj.get_full_name()

    photo_thumbnail_medium = ThumbnailField(size='medium')
    photo_thumbnail_large = ThumbnailField(size='large')


    class Meta:
        model = Freelancer
        fields = ('id', 'reference_number', 'specific_object',
                  'service_key', 'photo_thumbnail_medium',
                  'photo_thumbnail_large', 'english_fluency',
                  'full_name', 'first_name', 'last_name', 'mobile',
                  'years_experience', 'minimum_pay_per_hour',
                  'average_score', 'reviews')


class OwnFreelancerSerializer(FreelancerForClientSerializer):
    """Serializer that exposes information on the freelancer
    profile for their own use.
    """

    specific_object = SpecificFreelancerIdentityField(
                            view_name='freelancer_own-detail',
                            pass_reverse_kwargs=False)

    email = serializers.SerializerMethodField()
    def get_email(self, obj):
        return obj.user.email

    photo_thumbnail_medium = ThumbnailField(size='medium')
    photo_thumbnail_large = ThumbnailField(size='large')

    minimum_pay_per_hour = MoneyField(
            validators=[validators.MinValueValidator(FREELANCER_MIN_WAGE)])

    postcode = PostcodeField()

    latitude = serializers.SerializerMethodField()
    def get_latitude(self, obj):
        return obj.postcode.latitude

    longitude = serializers.SerializerMethodField()
    def get_longitude(self, obj):
        return obj.postcode.longitude

    class Meta(FreelancerForClientSerializer.Meta):
        fields = FreelancerForClientSerializer.Meta.fields + ('email', 'mobile',
                  'photo_thumbnail_medium', 'english_fluency',
                  'eligible_to_work', 'minimum_pay_per_hour',
                  'postcode', 'latitude', 'longitude',
                  'travel_distance', 'years_experience')
