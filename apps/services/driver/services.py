from apps.service import services, Service
from .models import DriverJobRequest, Driver, DriverPayGrade
from .forms import DriverJobRequestForm, DriverForm, DriverJobMatchingForm
from django.core.urlresolvers import reverse_lazy


class DriverService(Service):
    "Class that defines the driver service."
    key = 'driver'
    weight = -10
    job_request_model = DriverJobRequest
    job_request_form = DriverJobRequestForm

    freelancer_model = Driver
    freelancer_form = DriverForm

    freelancer_additional_menu_items = [
        (reverse_lazy('drivervehicletype_list'),
         'Vehicles', 'vehicletypes')
    ]

    job_matching_form = DriverJobMatchingForm

    pay_grade_model = DriverPayGrade

services.register(DriverService)
