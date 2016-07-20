from django import forms
from apps.job.forms import JobRequestForm
from apps.freelancer.forms import FreelancerForm
from apps.booking.forms import JobMatchingForm
from .models import KitchenJobRequest, KitchenFreelancer, ROLE_CHOICES
from .utils import KitchenJobMatcher


class KitchenJobRequestForm(JobRequestForm):
    "General form for kitchen staff job requests."

    comment_placeholder = 'Does the freelancer need to bring a specific ' \
            'uniform? Does the freelancer need to have obtained a ' \
            'particular certification?'

    def __init__(self, *args, **kwargs):
        super(KitchenJobRequestForm, self).__init__(*args, **kwargs)
        self.helper.layout[2].insert(1, 'role')

    class Meta(JobRequestForm.Meta):
         model = KitchenJobRequest
         fields = JobRequestForm.Meta.fields + ('role',)


class KitchenFreelancerForm(FreelancerForm):
    """Edit form for a kitchen staff's profile."""

    def __init__(self, *args, **kwargs):
        super(KitchenFreelancerForm, self).__init__(*args, **kwargs)
        self.helper.layout[1].append('role')

    class Meta(FreelancerForm.Meta):
        model = KitchenFreelancer


class KitchenJobMatchingForm(JobMatchingForm):
    """Job matching form specifically for kitchen staffs.
    """

    job_matcher = KitchenJobMatcher
    role = forms.ChoiceField(required=False,
                        choices=((None, '-------'),) + ROLE_CHOICES)
