from apps.job.forms import JobRequestForm
from apps.freelancer.forms import FreelancerForm
from .models import CleanerJobRequest, Cleaner



class CleanerJobRequestForm(JobRequestForm):
    "General form for cleaner job requests."

    comment_placeholder = 'Anything else to tell the cleaner? Should ' \
                        'the cleaner bring their own equipment?'

    class Meta(JobRequestForm.Meta):
         model = CleanerJobRequest


class CleanerForm(FreelancerForm):
    """Edit form for a cleaner's profile."""

    class Meta(FreelancerForm.Meta):
        model = Cleaner
