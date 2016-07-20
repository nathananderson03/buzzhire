from rest_framework import viewsets, mixins, status
from .serializers import BasePayGradeSerializer
from apps.paygrade.models import BasePayGrade
from apps.api.views import RetrieveViewset
from apps.api.client.permissions import ClientOrAdminOnlyPermission
from rest_framework.exceptions import ValidationError, NotFound
from django.core.exceptions import ObjectDoesNotExist


class BaseClientPayGradeViewSet(RetrieveViewset):
    """Returns the Pay Grade information for the client,
    given information about what kind of job it is.
    
    ## Required parameters
    
    - `years_experience` The minimum number of years of working experience
       required. Integer.  Choices are:
        - `0` - No preference
        - `1` - 1 year
        - `3` - 3 years
        - `5` - 5 years
    
    ## Returned fields
    
    - `min_client_pay_per_hour` The minimum pay per hour that will be accepted
      for the client to pay.

    """
    model_class = BasePayGrade
    serializer_class = BasePayGradeSerializer
    permission_classes = (ClientOrAdminOnlyPermission,)
    required_filters = ['years_experience']
    optional_filters = {}  # Can specify optional filters, keys as names,
                           # values as defaults

    def get_object(self):

        # Get the filters needed to get the pay grade
        # TODO - make this validation use built in validation
        # for the fields
        filter_kwargs = {}
        missing_filters = []
        for filter_name in self.required_filters:
            try:
                filter_kwargs[filter_name] = self.request.GET[filter_name]
            except KeyError:
                missing_filters.append(filter_name)

        if missing_filters:
            raise ValidationError({'missing_filters': missing_filters})

        for filter_name, default_value in self.optional_filters.items():
            get_value = self.request.GET.get(filter_name, None)
            filter_kwargs[filter_name] = get_value if get_value \
                                         else default_value

        try:
            return self.model_class.objects.get_pay_grade(**filter_kwargs)
        except ObjectDoesNotExist:
            raise NotFound

