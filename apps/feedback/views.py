from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from extra_views import FormSetView
from apps.client.views import OwnedByClientMixin, ClientOnlyMixin
from apps.core.views import ContextMixin
from apps.freelancer.views import FreelancerOnlyMixin
from apps.job.models import JobRequest
from apps.booking.views import FreelancerHasBookingMixin
from apps.booking.models import Booking
from .models import BookingFeedback, \
                            get_bookings_awaiting_feedback_for_freelancer, \
                            get_job_requests_awaiting_feedback_for_client
from .forms import BookingFeedbackForm
from django.contrib import messages
from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy


class FeedbackAllowedMixin(object):
    """Views mixin - redirects to job request page, with an appropriate
    error message, if the client/freelancer is not allowed to provide feedback
    on this job request.
    
    To decide whether it's a client or a freelancer,
    self.author_type must be set in the subclass. 
    """

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        message = None
        if self.object.status != JobRequest.STATUS_COMPLETE:
            message = "You cannot leave feedback for a job that " \
                        "hasn't finished yet."
        elif self.has_given_all_feedback():
            message = 'You have already left feedback for this job.'
        if message:
            messages.error(self.request, message)
            return redirect(self.object.get_absolute_url())

        return super(FeedbackAllowedMixin, self).dispatch(request,
                                                           *args, **kwargs)

    def has_given_all_feedback(self):
        """Returns whether or not the user (client or freelancer) has given
        all the feedback needed for this job request.
        """
        if self.author_type == BookingFeedback.AUTHOR_TYPE_CLIENT:
            return not self.object.needs_feedback_from_client()
        else:
            return BookingFeedback.objects.freelancer_feedback_exists(
                                                self.object, self.freelancer)


class FreelancerBacklog(ContextMixin, FreelancerOnlyMixin, ListView):
    """List for the freelancer of completed job requests that are still
    waiting for their feedback.
    """
    template_name = 'feedback/freelancer_backlog.html'
    extra_context = {'title': 'Jobs awaiting feedback'}

    def get_queryset(self):
        return get_bookings_awaiting_feedback_for_freelancer(self.freelancer)


class ClientBacklog(ContextMixin, ClientOnlyMixin, ListView):
    """List for the client of completed job requests that are still
    waiting for their feedback.
    """
    template_name = 'feedback/client_backlog.html'
    extra_context = {'title': 'Jobs awaiting feedback'}

    def get_queryset(self):
        return get_job_requests_awaiting_feedback_for_client(self.client)


class BaseFeedbackCreateView(FeedbackAllowedMixin,
                             ContextMixin, SingleObjectMixin,
                             FormSetView):
    """Base view for a client/freelancer to leave feedback
    for a particular job request.
    """
    template_name = 'feedback/feedback_create.html'
    extra_context = {'title': 'Leave feedback'}
    model = JobRequest
    extra = 0
    form_class = BookingFeedbackForm
    author_type = None  # This should be overridden in the subclass

    def get_initial(self):
        # Convert to initial values
        initial = [BookingFeedbackForm.get_initial(feedback)
                   for feedback in self.get_feedback_list()]
        return initial

    def formset_valid(self, formset):
        [form.save() for form in formset]
        messages.add_message(self.request, messages.INFO,
                             'Thanks for your feedback.')
        return super(BaseFeedbackCreateView, self).formset_valid(formset)


class ClientFeedbackCreate(OwnedByClientMixin,
                            BaseFeedbackCreateView):
    """Page for a client to leave feedback on the freelancers
    for a particular job request.
    """
    author_type = BookingFeedback.AUTHOR_TYPE_CLIENT

    def get_feedback_list(self):
        return BookingFeedback.objects.client_feedback_list(self.object)

    def get_success_url(self):
        return self.object.get_absolute_url()


class FreelancerFeedbackCreate(FreelancerHasBookingMixin,
                               BaseFeedbackCreateView):
    """Page for a freelancer to leave feedback on the client
    for a particular job request.
    """
    author_type = BookingFeedback.AUTHOR_TYPE_FREELANCER
    success_url = reverse_lazy('freelancer_backlog')

    def get_feedback_list(self):
        return BookingFeedback.objects.freelancer_feedback_list(self.object,
                                                            self.freelancer)

    def get_context_data(self, *args, **kwargs):
        context = super(FreelancerFeedbackCreate, self).get_context_data(*args,
                                                                    **kwargs)
        context['for_freelancer'] = True
        return context
