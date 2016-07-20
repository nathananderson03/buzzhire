from ...freelancer.views import (FreelancerForClientViewSet,
                                       OwnFreelancerViewSet)
from ...job.views import (JobRequestForFreelancerViewSet,
                          ServiceSpecificJobRequestForClientViewSet)
from apps.services.cleaner.models import (Cleaner, CleanerJobRequest,
                                          CleanerPayGrade)
from .serializers import (CleanerJobRequestForClientSerializer,
                          CleanerPayGradeSerializer)
from ...paygrade.views import BaseClientPayGradeViewSet


class CleanerForClientViewSet(FreelancerForClientViewSet):
    """All published cleaners - publicly available information.
    
    The generic fields are documented on the freelancer endpoint.
    """
    model_class = Cleaner


class OwnCleanerViewSet(OwnFreelancerViewSet):
    """Returns the cleaner's own profile.
    
    ## Fields
    
    The generic fields are documented on the freelancer endpoint.
    
    These are the fields specific to cleaners:
    
    - Currently no fields.
     
    """
    pass


class CleanerJobRequestForClientViewSet(ServiceSpecificJobRequestForClientViewSet):
    """Cleaner staff job requests for the currently logged in client.
    
    ## Fields
    
    The generic fields are documented on the job request
    endpoint for the client.
    
    These are the fields specific to cleaner staff job requests:
    
    - Currently no fields.
 
    """
    serializer_class = CleanerJobRequestForClientSerializer
    model_class = CleanerJobRequest


class CleanerJobRequestForFreelancerViewSet(JobRequestForFreelancerViewSet):
    """All cleaner job requests.  Publicly viewable information.
    
    The generic fields are documented on the job request endpoint.
    
    These are the fields specific to cleaner job requests:
    
    - Currently no fields.
 
    """
    model_class = CleanerJobRequest


class ClientCleanerPayGradeViewSet(BaseClientPayGradeViewSet):
    """Returns pay grade information for the cleaning job,
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
    model_class = CleanerPayGrade
    serializer_class = CleanerPayGradeSerializer