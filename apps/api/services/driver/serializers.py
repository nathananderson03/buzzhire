from django.forms import widgets
from django.core.validators import ValidationError
from rest_framework import serializers
from apps.services.driver.models import (VehicleType, FlexibleVehicleType,
                Driver, DriverJobRequest, DriverVehicleType, DriverPayGrade)
from ...freelancer.serializers import (OwnFreelancerSerializer,
                                             FreelancerForClientSerializer)
from ...job.serializers import JobRequestForFreelancerSerializer
from ...booking.serializers import BookingsJobRequestForClientSerializer
from ...paygrade.serializers import BasePayGradeSerializer


class VehicleTypeSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('_name')
    def _name(self, obj):
        return str(obj)

    class Meta:
        model = VehicleType
        fields = ('id', 'name', 'delivery_box_applicable')


class FlexibleVehicleTypeSerializer(VehicleTypeSerializer):
    class Meta:
        model = FlexibleVehicleType
        fields = VehicleTypeSerializer.Meta.fields


class DriverForClientSerializer(FreelancerForClientSerializer):
    """Serializer for public views of driver."""
    vehicles = serializers.SerializerMethodField()
    def get_vehicles(self, obj):
        vehicles_list = []
        for vehicle in obj.drivervehicletype_set.all():
            vehicles_list.append({
                'vehicle_type_name': str(vehicle),
                'own_vehicle': vehicle.own_vehicle,
                'delivery_box': vehicle.delivery_box}
        )
        return vehicles_list

    class Meta(FreelancerForClientSerializer.Meta):
        model = Driver
        fields = FreelancerForClientSerializer.Meta.fields + ('vehicles',
                                                           'phone_type')


class OwnDriverSerializer(OwnFreelancerSerializer):
    """Serializer for the driver's own profile."""

#     vehicle_types = serializers.HyperlinkedRelatedField(read_only=True,
#                                     view_name='driver_vehicle_types-detail')

    class Meta:
        model = Driver
        fields = OwnFreelancerSerializer.Meta.fields + ('phone_type',)



class DriverJobRequestForFreelancerSerializer(
                                            JobRequestForFreelancerSerializer):
    vehicle_type_url = serializers.HyperlinkedRelatedField(read_only=True,
                                   view_name='flexible_vehicle_types-detail',
                                   source='vehicle_type')
    class Meta(JobRequestForFreelancerSerializer.Meta):
        model = DriverJobRequest
        fields = JobRequestForFreelancerSerializer.Meta.fields + \
                  ('vehicle_type', 'vehicle_type_url',
                   'minimum_delivery_box',
                   'delivery_box_applicable', 'own_vehicle',
                   'phone_requirement')



class DriverJobRequestForClientSerializer(BookingsJobRequestForClientSerializer):
    vehicle_type_url = serializers.HyperlinkedRelatedField(
                                   read_only=True,
                                   view_name='flexible_vehicle_types-detail',
                                   source='vehicle_type')

    class Meta(BookingsJobRequestForClientSerializer.Meta):
        model = DriverJobRequest
        fields = BookingsJobRequestForClientSerializer.Meta.fields + \
                  ('vehicle_type', 'vehicle_type_url',
                   'minimum_delivery_box',
                   'delivery_box_applicable', 'own_vehicle',
                   'phone_requirement')


class DriverVehicleTypeSerializer(serializers.ModelSerializer):
    """Serializer for driver vehicle types for the logged in driver.
    """
    vehicle_type_url = serializers.HyperlinkedRelatedField(read_only=True,
                                    view_name='vehicle_types-detail',
                                    source='vehicle_type')

    vehicle_type_name = serializers.SerializerMethodField()
    def get_vehicle_type_name(self, obj):
        return str(obj.vehicle_type)

    def validate(self, attrs):
        attrs['driver'] = self.context['request'].user.driver
        attrs = super(DriverVehicleTypeSerializer, self).validate(attrs)
        if attrs['driver'].drivervehicletype_set.filter(
                                vehicle_type=attrs['vehicle_type']).exists():
            raise ValidationError('The driver already has a %s.'
                                  % str(attrs['vehicle_type']).lower())
        return attrs

    class Meta:
        model = DriverVehicleType
        fields = ('id', 'vehicle_type', 'vehicle_type_name',
                  'vehicle_type_url',
                  'own_vehicle', 'delivery_box')


class DriverPayGradeSerializer(BasePayGradeSerializer):
    class Meta(BasePayGradeSerializer.Meta):
        model = DriverPayGrade