from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from ...job.views import (JobRequestForFreelancerViewSet,
                          ServiceSpecificJobRequestForClientViewSet)
from ...freelancer.permissions import FreelancerOnlyPermission
from ...freelancer.views import (FreelancerForClientViewSet,
                                       OwnFreelancerViewSet)
from .serializers import (DriverForClientSerializer,
                    OwnDriverSerializer, VehicleTypeSerializer,
                    FlexibleVehicleTypeSerializer,
                    DriverJobRequestForFreelancerSerializer,
                    DriverJobRequestForClientSerializer,
                    DriverVehicleTypeSerializer,
                    DriverPayGradeSerializer)
from apps.services.driver.models import (VehicleType, FlexibleVehicleType, Driver,
                      DriverJobRequest, DriverVehicleType, DriverPayGrade)
from .permissions import DriverOnlyPermission
from ...views import RetrieveAndUpdateViewset
from ...paygrade.views import BaseClientPayGradeViewSet


class DriverForClientViewSet(FreelancerForClientViewSet):
    """All drivers that the currently logged in client can see.
    
    The generic fields are documented on the freelancer endpoint.
    
    ## Specific fields
    
    - `vehicles` List of vehicles that the driver has.
      See documentation on the 'Driver vehicles' endpoint for details.
    - `phone_type` What kind of phone they have.  Choices are:
        - `"AN"` - Android
        - `"IP"` - iPhone
        - `"WI"` - Windows
        - `"OT"` - Other smartphone
        - `"NS"` - Non smartphone       
    """
    serializer_class = DriverForClientSerializer
    model_class = Driver


class OwnDriverViewSet(OwnFreelancerViewSet):
    """Returns the driver's own profile.
    
    ## Fields
    
    The generic fields are documented on the freelancer endpoint.
    
    ## Specific fields
    - `phone_type` What kind of phone they have.  Choices are:
        - `"AN"` - Android
        - `"IP"` - iPhone
        - `"WI"` - Windows
        - `"OT"` - Other smartphone
        - `"NS"` - Non smartphone      
    """
    serializer_class = OwnDriverSerializer


class DriverJobRequestForFreelancerViewSet(JobRequestForFreelancerViewSet):
    """All driver job requests.  Publicly viewable information.
    
    The generic fields are documented on the job request endpoint.
    
    - `vehicle_type`: The id of the flexible vehicle type that would
      be appropriate for the job, or null if any vehicle would be appropriate.
    - `vehicle_type_url`: API endpoint for the vehicle type url.
    - `own_vehicle`: Whether the driver needs to supply their own vehicle.
    - `delivery_box_applicable`: Whether the minimum delivery box requirement
      is relevant.
    - `minimum_delivery_box`: The minimum size of delivery box required (only
      relevant if `delivery_box_applicable` is `true`).  Integer.  Choices are:
        - `0` - None
        - `2` - Standard
        - `4` - Pizza
    - `phone_requirement` The kind of phone the freelancer needs to do the job.
      Choices are:
        - `"NR"` - No smart phone needed.
        - `"AY"` - Any smart phone.
        - `"AN"` - Android.
        - `"IP"` - iPhone.
        - `"WI"` - Windows.
    """
    serializer_class = DriverJobRequestForFreelancerSerializer
    model_class = DriverJobRequest


class DriverJobRequestForClientViewSet(
                                ServiceSpecificJobRequestForClientViewSet):
    """Driver job requests for the currently logged in client.
    
    ## Fields
    
    The generic fields are documented on the job request
    endpoint for the client.
    
    These are the fields specific to driver job requests:
    
    - `vehicle_type`: The id of the flexible vehicle type that would
      be appropriate for the job, or null if any vehicle would be appropriate.
    - `vehicle_type_url`: API endpoint for the vehicle type url.
    - `own_vehicle`: Whether the driver needs to supply their own vehicle.
    - `delivery_box_applicable`: Whether the minimum delivery box requirement
      is relevant (determined from the vehicle type). Read only.
    - `minimum_delivery_box`: The minimum size of delivery box required (only
      relevant if `delivery_box_applicable` is `true`).  Integer.  Choices are:
        - `0` - None
        - `2` - Standard
        - `4` - Pizza
    - `phone_requirement` The kind of phone the freelancer needs to do the job.
      Choices are:
        - `"NR"` - No smart phone needed.
        - `"AY"` - Any smart phone.
        - `"AN"` - Android.
        - `"IP"` - iPhone.
        - `"WI"` - Windows.
 
    """
    model_class = DriverJobRequest
    serializer_class = DriverJobRequestForClientSerializer


class VehicleTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """All the vehicle types for the site.  Read only.
        
    ## Fields
    
    - `id` Unique id for the vehicle type.  Integer.
    - `name` Human-readable name of the vehicle type.
    - `delivery_box_applicable`: Whether it is applicable to this vehicle
      type to ask about a delivery box.
    """
    serializer_class = VehicleTypeSerializer

    def get_queryset(self):
        return VehicleType.objects.all()


class FlexibleVehicleTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """All flexible vehicle types for the site.  Read only.
    
    These are vehicle types that can include more than one vehicle type,
    e.g. Motorcycle / Scooter.  They are used on job requests, where the
    vehicle requirements are less strict.

    ## Fields
    
    See the vehicle types endpoint for documentation.
    """
    serializer_class = FlexibleVehicleTypeSerializer

    def get_queryset(self):
        return FlexibleVehicleType.objects.all()


class DriverVehicleForDriverViewSet(viewsets.ModelViewSet):
    """All the vehicles belonging to the currently logged in driver
    (aka 'driver vehicles').
    
    ## Fields
    
    - `id` Unique id for the driver vehicle.  Read only.
    - `vehicle_type` The id for type of vehicle.
    - `vehicle_type_name` The human readable name of the vehicle type.  Read only.
    - `vehicle_type_url` Url of API endpoint for the vehicle type. Read only.
    - `own_vehicle` Whether the driver can provide the vehicle on a job.
    - `delivery_box` If applicable, the size of delivery box.  Integer. Choices:
        - `0` - None.
        - `2` - Standard.
        - `4` - Pizza.
    """
    serializer_class = DriverVehicleTypeSerializer

    permission_classes = (DriverOnlyPermission,)

    def get_queryset(self):
        return self.request.user.driver.drivervehicletype_set.all()


class ClientDriverPayGradeViewSet(BaseClientPayGradeViewSet):
    """Returns pay grade information for the driving job,
    given information about what kind of job it is.
    
    ## Required parameters
    
    - `years_experience` The minimum number of years of working experience
       required. Integer.  Choices are:
        - `0` - No preference
        - `1` - 1 year
        - `3` - 3 years
        - `5` - 5 years
    
    ## Optional parameters
    
    - `vehicle_type`: The id of the flexible vehicle type that would
      be appropriate for the job.  Do not supply if any vehicle
      would be appropriate.
      
    ## Returned fields
    
    - `min_client_pay_per_hour` The minimum pay per hour that will be accepted
      for the client to pay.
    
    """
    model_class = DriverPayGrade
    serializer_class = DriverPayGradeSerializer
    required_filters = ['years_experience']
    optional_filters = {'vehicle_type': None}
