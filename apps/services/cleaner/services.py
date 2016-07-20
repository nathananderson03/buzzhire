from apps.service import services, Service
from .models import CleanerJobRequest, Cleaner, CleanerPayGrade
from .forms import CleanerJobRequestForm, CleanerForm
from apps.booking.forms import JobMatchingForm


class CleanerService(Service):
    "Class that defines the cleaner service."
    key = 'cleaner'
    weight = 10
    job_request_model = CleanerJobRequest
    job_request_form = CleanerJobRequestForm

    freelancer_model = Cleaner
    freelancer_form = CleanerForm

    job_matching_form = JobMatchingForm

    pay_grade_model = CleanerPayGrade

services.register(CleanerService)
