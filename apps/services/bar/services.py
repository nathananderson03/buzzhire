from apps.service import services, Service
from .models import BarJobRequest, BarFreelancer, BarPayGrade
from .forms import BarJobRequestForm, BarFreelancerForm, BarJobMatchingForm


class BarService(Service):
    "Class that defines the bar staff service."
    key = 'bar'
    weight = -5

    job_request_model = BarJobRequest
    job_request_form = BarJobRequestForm

    freelancer_model = BarFreelancer
    freelancer_form = BarFreelancerForm

    job_matching_form = BarJobMatchingForm

    pay_grade_model = BarPayGrade

services.register(BarService)
