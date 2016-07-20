from ...freelancer.views import (FreelancerForClientViewSet,
                                       OwnFreelancerViewSet)
from ...job.views import (JobRequestForFreelancerViewSet,
                          ServiceSpecificJobRequestForClientViewSet)
from apps.services.waiting.models import (WaitingFreelancer, WaitingJobRequest,
                                          WaitingPayGrade)
from .serializers import (WaitingJobRequestForClientSerializer,
                          WaitingPayGradeSerializer)
from ...paygrade.views import BaseClientPayGradeViewSet


class OwnWaitingFreelancerViewSet(OwnFreelancerViewSet):
    """Returns the waiting staff's own profile.
    
    ## Fields
    
    The generic fields are documented on the freelancer endpoint.
    
    These are the fields specific to waiting staff:
    
    - Currently no fields.
     
    """
    pass


class WaitingFreelancerForClientViewSet(FreelancerForClientViewSet):
    """All published waiting staff - publicly available information.
    
    The generic fields are documented on the freelancer endpoint.
    """
    model_class = WaitingFreelancer



class WaitingJobRequestForClientViewSet(ServiceSpecificJobRequestForClientViewSet):
    """Waiting staff job requests for the currently logged in client.
    
    ## Fields
    
    The generic fields are documented on the job request
    endpoint for the client.
    
    These are the fields specific to waiting staff job requests:
    
    - Currently no fields.
 
    """
    serializer_class = WaitingJobRequestForClientSerializer
    model_class = WaitingJobRequest


class WaitingJobRequestForFreelancerViewSet(JobRequestForFreelancerViewSet):
    """All waiting staff job requests.  Publicly viewable information.
    
    The generic fields are documented on the job request endpoint.
    
    These are the fields specific to waiting staff job requests:
    
    - Currently no fields.
 
    """
    model_class = WaitingJobRequest


class ClientWaitingPayGradeViewSet(BaseClientPayGradeViewSet):
    """Returns pay grade information for the waiting job,
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
    model_class = WaitingPayGrade
    serializer_class = WaitingPayGradeSerializer