from apps.job.forms import JobRequestForm
from apps.freelancer.forms import FreelancerForm
from .models import WaitingJobRequest, WaitingFreelancer



class WaitingJobRequestForm(JobRequestForm):
    "General form for waiting staff job requests."

    comment_placeholder = 'Does the freelancer need to bring a specific ' \
            'uniform? Does the freelancer need to have obtained a ' \
            'particular certification?'

    class Meta(JobRequestForm.Meta):
         model = WaitingJobRequest


class WaitingFreelancerForm(FreelancerForm):
    """Edit form for a waiting staff's profile."""

    class Meta(FreelancerForm.Meta):
        model = WaitingFreelancer
