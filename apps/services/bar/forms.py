from django import forms
from apps.job.forms import JobRequestForm
from apps.freelancer.forms import FreelancerForm
from apps.booking.forms import JobMatchingForm
from .models import BarJobRequest, BarFreelancer, ROLE_CHOICES
from .utils import BarJobMatcher


class BarJobRequestForm(JobRequestForm):
    "General form for bar staff job requests."

    comment_placeholder = 'Does the freelancer need to bring a specific ' \
            'uniform? Does the freelancer need to have obtained a ' \
            'particular certification?'

    def __init__(self, *args, **kwargs):
        super(BarJobRequestForm, self).__init__(*args, **kwargs)
        self.helper.layout[2].insert(1, 'role')

    class Meta(JobRequestForm.Meta):
         model = BarJobRequest
         fields = JobRequestForm.Meta.fields + ('role',)


class BarFreelancerForm(FreelancerForm):
    """Edit form for a bar staff's profile."""

    def __init__(self, *args, **kwargs):
        super(BarFreelancerForm, self).__init__(*args, **kwargs)
        self.helper.layout[1].append('role')

    class Meta(FreelancerForm.Meta):
        model = BarFreelancer


class BarJobMatchingForm(JobMatchingForm):
    """Job matching form specifically for bar staff.
    """

    job_matcher = BarJobMatcher
    role = forms.ChoiceField(required=False,
                        choices=((None, '-------'),) + ROLE_CHOICES)
