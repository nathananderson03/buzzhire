from ...freelancer.views import (FreelancerForClientViewSet,
                                       OwnFreelancerViewSet)
from ...job.views import (JobRequestForFreelancerViewSet,
                          ServiceSpecificJobRequestForClientViewSet)
from apps.services.bar.models import (BarFreelancer, BarJobRequest,
                                      BarPayGrade)
from .serializers import (BarFreelancerForClientSerializer,
                          PrivateBarFreelancerSerializer,
                          BarJobRequestForFreelancerSerializer,
                          BarJobRequestForClientSerializer,
                          BarPayGradeSerializer)
from ...paygrade.views import BaseClientPayGradeViewSet

class BarFreelancerForClientViewSet(FreelancerForClientViewSet):
    """All published bar staff - publicly available information.
    
    ## Fields
    
    The generic fields are documented on the freelancer endpoint.
    
    These are the fields specific to bar staff:
        
    - `role`: The role of the freelancer.  Choices are:
        - `"MX"` - Mixologist
        - `"BM"` - Barman
        - `"BT"` - Barista
    """
    serializer_class = BarFreelancerForClientSerializer

    model_class = BarFreelancer


class OwnBarFreelancerViewSet(OwnFreelancerViewSet):
    """Returns the bar staff's own profile.
    
    ## Fields
    
    The generic fields are documented on the freelancer endpoint.
    
    These are the fields specific to bar staff:
    
    - `role`: The role of the freelancer.  Choices are:
        - `"MX"` - Mixologist
        - `"BM"` - Barman
        - `"BT"` - Barista
    """
    serializer_class = PrivateBarFreelancerSerializer


class BarJobRequestForClientViewSet(ServiceSpecificJobRequestForClientViewSet):
    """Bar staff job requests for the currently logged in client.
    
    ## Fields
    
    The generic fields are documented on the job request
    endpoint for the client.
    
    These are the fields specific to bar staff job requests:
    
    - `role`: The role of the freelancer.  Choices are:
        - `"MX"` - Mixologist
        - `"BM"` - Barman
        - `"BT"` - Barista
 
    """
    model_class = BarJobRequest
    serializer_class = BarJobRequestForClientSerializer


class BarJobRequestForFreelancerViewSet(JobRequestForFreelancerViewSet):
    """All bar staff job requests.  Publicly viewable information.
    
    ## Fields
    
    The generic fields are documented on the job request endpoint.
    
    These are the fields specific to bar staff job requests:
    
    - `role`: The role needed.  Choices are:
        - `"MX"` - Mixologist
        - `"BM"` - Barman
        - `"BT"` - Barista
    """
    serializer_class = BarJobRequestForFreelancerSerializer
    model_class = BarJobRequest


class ClientBarPayGradeViewSet(BaseClientPayGradeViewSet):
    """Returns pay grade information for the bar job,
    given information about what kind of job it is.
    
    ## Required parameters
    
    - `years_experience` The minimum number of years of working experience
       required. Integer.  Choices are:
        - `0` - No preference
        - `1` - 1 year
        - `3` - 3 years
        - `5` - 5 years
    - `role`: The role of the freelancer.  Choices are:
        - `"MX"` - Mixologist
        - `"BM"` - Barman
        - `"BT"` - Barista
    
    ## Returned fields
    
    - `min_client_pay_per_hour` The minimum pay per hour that will be accepted
      for the client to pay.

    """
    model_class = BarPayGrade
    serializer_class = BarPayGradeSerializer
    required_filters = ['years_experience', 'role']
