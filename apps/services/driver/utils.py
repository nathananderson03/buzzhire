from apps.booking.utils import JobMatcher
from apps.services.driver.models import DriverJobRequest, Driver


class DriverJobMatcher(JobMatcher):
    "JobMatcher tailored to matching drivers."

    flat_fields = JobMatcher.flat_fields + ('minimum_delivery_box',
                                            'own_vehicle', 'vehicle_type',
                                            'phone_requirement')

    def get_results(self, *args, **kwargs):
        results = super(DriverJobMatcher, self).get_results(*args, **kwargs)
        results = self.filter_by_vehicle_requirements(results)
        results = self.filter_by_phone_requirements(results)
        return results

    def filter_by_phone_requirements(self, results):
        "Filters by the phone requirement."
        PHONE_REQUIREMENT_MAP = {
            DriverJobRequest.PHONE_REQUIREMENT_NOT_REQUIRED: lambda r: r,
            DriverJobRequest.PHONE_REQUIREMENT_ANY:
                lambda r: r.exclude(
                    phone_type__in=(Driver.PHONE_TYPE_NON_SMARTPHONE, '')),
            DriverJobRequest.PHONE_REQUIREMENT_ANDROID:
                lambda r: r.filter(phone_type=Driver.PHONE_TYPE_ANDROID),
            DriverJobRequest.PHONE_REQUIREMENT_IPHONE:
                lambda r: r.filter(phone_type=Driver.PHONE_TYPE_IPHONE),
            DriverJobRequest.PHONE_REQUIREMENT_WINDOWS:
                lambda r: r.filter(phone_type=Driver.PHONE_TYPE_WINDOWS),
        }

        if self.search_terms['phone_requirement']:
            results = PHONE_REQUIREMENT_MAP[
                            self.search_terms['phone_requirement']](results)
        return results


    def filter_by_vehicle_requirements(self, results):
        "Filters by vehicle requirements."

        if self.search_terms['vehicle_type']:
            # The supplied vehicle type is a FlexibleVehicleType; unpack it
            # into individual VehicleTypes.
            vehicle_types = self.search_terms['vehicle_type'].as_queryset()
            if self.search_terms['own_vehicle']:
                # Filter by vehicle types that are owned
                filter_kwargs = {
                    'drivervehicletype__vehicle_type': \
                                    vehicle_types,
                    'drivervehicletype__own_vehicle': True
                }
                # Include delivery box filter, if specified
                if self.search_terms['minimum_delivery_box']:
                    filter_kwargs['drivervehicletype__delivery_box__gte'] = \
                                    self.search_terms['minimum_delivery_box']
                results = results.filter(**filter_kwargs)
            else:
                # Just filter by vehicle types
                filter_kwargs = {
                    'vehicle_types': vehicle_types
                }
            return results.filter(**filter_kwargs)

        return results