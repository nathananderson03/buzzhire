from apps.service import services, Service
from .models import WaitingJobRequest, WaitingFreelancer, WaitingPayGrade
from .forms import WaitingJobRequestForm, WaitingFreelancerForm
from apps.booking.forms import JobMatchingForm


class WaitingService(Service):
    "Class that defines the waiting staff service."
    key = 'waiting'
    weight = 1

    job_request_model = WaitingJobRequest
    job_request_form = WaitingJobRequestForm

    freelancer_model = WaitingFreelancer
    freelancer_form = WaitingFreelancerForm

    job_matching_form = JobMatchingForm

    pay_grade_model = WaitingPayGrade


services.register(WaitingService)
