from django.contrib import admin
from apps.job.admin import JobRequestAdmin
from apps.freelancer.admin import FreelancerAdmin
from apps.paygrade.admin import PayGradeAdmin
from . import models


class DriverAdmin(FreelancerAdmin):
    exclude = ('driving_experience_old', 'driving_experience_old_2',
               'vehicle_types_old')


class DriverVehicleTypeAdmin(admin.ModelAdmin):
    list_display = ('vehicle_type', 'driver', 'own_vehicle', 'delivery_box')


class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'equivalent_to', 'delivery_box_applicable')


admin.site.register(models.Driver, DriverAdmin)
admin.site.register(models.VehicleType, VehicleTypeAdmin)
admin.site.register(models.DriverVehicleType, DriverVehicleTypeAdmin)


class DriverJobRequestAdmin(JobRequestAdmin):
    list_display = ('reference_number', 'client', 'date', 'start_time',
                    'duration', 'end_datetime',
                    'client_pay_per_hour', 'number_of_freelancers',
                    'status')
    exclude = JobRequestAdmin.exclude + ('driving_experience_old',)

admin.site.register(models.DriverJobRequest, DriverJobRequestAdmin)


class DriverPayGradeAdmin(PayGradeAdmin):
    list_display = ('vehicle_type',) + PayGradeAdmin.list_display

admin.site.register(models.DriverPayGrade, DriverPayGradeAdmin)