from django.views.generic import ListView, UpdateView, CreateView, FormView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.contrib import messages
from apps.account.views import AdminOnlyMixin
from apps.core.views import ContextMixin, TabsMixin, ContextTemplateView, \
    ConfirmationMixin, OwnerOnlyMixin
from apps.freelancer.views import FreelancerOnlyMixin
from apps.freelancer.models import Freelancer
from apps.job.models import JobRequest
from .models import (Booking, Availability, Invitation,
            JobAlreadyBookedByFreelancer, JobAlreadyAppliedToByFreelancer,
            JobFullyBooked, JobInPast, JobInvalidStatus)
from .forms import AvailabilityForm, JobMatchingForm, \
                    BookingOrInvitationConfirmForm, InvitationApplyForm, \
                    InvitationDeclineForm, BookingConfirmForm
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect
from .signals import (invitation_created,
                      booking_created, invitation_declined)
from django.core.exceptions import PermissionDenied
from apps.job.views import JobRequestDetail
from django.http.response import HttpResponseRedirect
from apps.service.forms import ServiceSelectForm
from apps.service.views import ServiceViewMixin
from apps.job import service_from_class
from apps.core.views import PolymorphicTemplateMixin
from .models import get_job_requests_pending_confirmation


class FreelancerHasBookingMixin(FreelancerOnlyMixin, OwnerOnlyMixin):
    """Mixin for single JobRequest views - freelancer must be booked
    onto the job request.
    """
    def is_owner(self):
        # We leverage the 'is_owner' method of OwnerOnlyMixin to determine
        # whether the freelancer is booked
        try:
            self.booking = self.get_object().bookings.get(
                                    freelancer=self.freelancer)
            return True
        except Booking.DoesNotExist:
            return False


class FreelancerBookingsList(FreelancerOnlyMixin,
                             ContextMixin, TabsMixin, ListView):
    """List of bookings assigned to a freelancer.
    This view has two modes - if self.past is True, it will return the
    job requests in the past, otherwise it will show upcoming job requests.   
    """
    paginate_by = 15
    extra_context = {'title': 'Bookings'}
    tabs = [
        ('Upcoming', reverse_lazy('freelancer_bookings_list')),
        ('Past', reverse_lazy('freelancer_bookings_list_past')),
    ]
    past = False

    def get_queryset(self, *args, **kwargs):
        queryset = Booking.objects.for_freelancer(self.freelancer)
        if self.past:
            return queryset.past()
        else:
            return queryset.future()


class FreelancerInvitationsList(FreelancerOnlyMixin,
                                ContextMixin, ListView):
    """List of current invitations for a freelancer.
    """
    paginate_by = 15
    extra_context = {'title': 'Pending job requests'}

    def get_queryset(self, *args, **kwargs):
        return Invitation.objects.can_be_applied_to_by_freelancer(
                                                            self.freelancer)


class FreelancerApplicationsList(FreelancerOnlyMixin,
                                 ContextMixin, TabsMixin, ListView):
    """List of jobs that a freelancer has applied to.
    This view has two modes - if self.past is True, it will return the
    jobs in the past, otherwise it will show upcoming jobs.   
    """
    template_name = 'booking/application_list.html'
    paginate_by = 15
    extra_context = {'title': 'Jobs applied to'}
    tabs = [
        ('Upcoming', reverse_lazy('freelancer_applications_list')),
        ('Past', reverse_lazy('freelancer_applications_list_past')),
    ]
    past = False

    def get_queryset(self, *args, **kwargs):
        queryset = Invitation.objects.applied_to_by_freelancer(self.freelancer)
        if self.past:
            return queryset.past()
        else:
            return queryset.future()


class AvailabilityUpdate(FreelancerOnlyMixin, SuccessMessageMixin,
                         ContextMixin, UpdateView):
    """View for freelancer to edit their availability.
    """
    model = Availability
    extra_context = {'title': 'Availability'}
    form_class = AvailabilityForm
    success_url = reverse_lazy('availability_update')
    success_message = 'Saved.'

    def get_object(self):
        # Return the Availability for the Freelancer, creating
        # (but not saving) one if it doesn't exist.
        try:
            return self.freelancer.availability
        except Availability.DoesNotExist:
            return Availability(freelancer=self.freelancer)


class JobMatchingView(AdminOnlyMixin,
                      PolymorphicTemplateMixin,
                      ContextMixin, ListView):
    """View for searching freelancers to match with a job request.
    """
    template_suffix = '_job_matching'
    paginate_by = 50
    extra_context = {'title': 'Job matching'}

    @property
    def model(self):
        return self.job_request.__class__

    def get(self, request, *args, **kwargs):
        # We use a form, but with the GET method as it's a search form.

        # First, handle the job request pk passed via the url.
        self.job_request = get_object_or_404(JobRequest,
                                        pk=kwargs.pop('job_request_pk'))
        form_kwargs = {'job_request': self.job_request}

        if self.request.GET.get('search', None):
            # A search has been made
            form_kwargs['data'] = self.request.GET

        self.form = self.get_form_class()(**form_kwargs)

        return super(JobMatchingView, self).get(request, *args, **kwargs)

    def get_form_class(self):
        """Returns the job matching form suitable for this service.
        """
        service = service_from_class(self.job_request.__class__)
        if service.job_matching_form:
            return service.job_matching_form
        return JobMatchingForm

    def get_queryset(self):
        "Called first by get()."
        # Return the object_list, but only if the search form validates
        if self.form.is_valid():
            return self.form.get_results()
        return []

    def get_context_data(self, **kwargs):
        context = super(JobMatchingView, self).get_context_data(**kwargs)
        context['form'] = self.form
        if self.form.is_valid():
            # Set a searched flag to let the template know a search has run
            context['searched'] = True
        return context


class BaseInvitationOrBookingConfirm(AdminOnlyMixin, ConfirmationMixin,
                                     FormView):
    """Base view for either inviting or booking a freelancer to a job.
    """
    question = 'Are you sure you want to invite this freelancer?'
    cancel_url = reverse_lazy('account_dashboard')
    template_name = 'account/dashboard_base.html'
    form_class = BookingOrInvitationConfirmForm
    model_class = None  # Override this when subclassing the view
    action_text = ''
    action_icon = ''

    def dispatch(self, *args, **kwargs):
        self.job_request = get_object_or_404(JobRequest,
                                             pk=kwargs.pop('job_request_pk'))
        self.freelancer = get_object_or_404(Freelancer,
                                             pk=kwargs.pop('freelancer_pk'))
        try:
            self.model_class.objects.get(jobrequest=self.job_request,
                                         freelancer=self.freelancer)
        except self.model_class.DoesNotExist:
            # This is what we want: the booking/invitation doesn't exist already
            pass
        else:
            # The booking/invitation already exists
            messages.error(self.request, 'That %s already exists.' \
                                    % self.model_class._meta.verbose_name)
            return redirect('job_request_admin_list')
        return super(BaseInvitationOrBookingConfirm, self).dispatch(
                                                            *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(BaseInvitationOrBookingConfirm, self).get_context_data(
                                                            *args, **kwargs)
        context['title'] = 'Create %s' % \
                                    self.model_class._meta.verbose_name

        return context

    def get_form_kwargs(self, *args, **kwargs):
        # Pass the job request and freelancer to the form
        form_kwargs = super(BaseInvitationOrBookingConfirm,
                            self).get_form_kwargs(*args, **kwargs)
        form_kwargs.update({
            'job_request': self.job_request,
            'freelancer': self.freelancer,
            'request': self.request,
            'action_text': self.action_text,
            'action_icon': self.action_icon,
        })
        return form_kwargs

    def form_valid(self, *args, **kwargs):
        self.instance = self.model_class.objects.create(
                                freelancer=self.freelancer,
                               jobrequest=self.job_request)
        messages.success(self.request, 'Created %s.'
                         % self.model_class._meta.verbose_name)
        return redirect(self.job_request.get_absolute_url())


class BookingConfirm(BaseInvitationOrBookingConfirm):
    """Confirmation form for the creation of a Booking
    - i.e. assigning a freelancer to a job.
    """
    question = 'Are you sure you want to create this booking?'
    model_class = Booking
    form_class = BookingConfirmForm
    action_text = 'Book'
    action_icon = 'confirm'

    def form_valid(self, *args, **kwargs):
        response = super(BookingConfirm, self).form_valid(*args, **kwargs)
        # Dispatch signal
        booking_created.send(sender=self, booking=self.instance)
        return response


class InvitationConfirm(BaseInvitationOrBookingConfirm):
    """Confirmation form for inviting a freelancer to a job.
    """
    question = 'Are you sure you want to invite this freelancer?'
    model_class = Invitation
    action_text = 'Invite'
    action_icon = 'invitation'

    def form_valid(self, *args, **kwargs):
        response = super(InvitationConfirm, self).form_valid(*args, **kwargs)
        # Dispatch signal
        invitation_created.send(sender=self, invitation=self.instance)
        return response


class InvitationApply(FreelancerOnlyMixin,
                       ConfirmationMixin,
                       FormView):
    """Confirmation form for a freelancer applying to a Job.
    """
    question = 'Are you sure you want to apply for this job?'
    action_text = 'Apply'
    action_icon = 'confirm'
    template_name = 'booking/apply_or_decline.html'
    form_class = InvitationApplyForm

    def dispatch(self, *args, **kwargs):
        try:
            return super(InvitationApply, self).dispatch(*args, **kwargs)
        except JobFullyBooked:
            return render(self.request, 'booking/fully_booked.html',
                          {'title': self.job_request})
        except JobAlreadyAppliedToByFreelancer:
            messages.add_message(self.request, messages.WARNING,
                                 'You have already applied to this job.')
        except JobAlreadyBookedByFreelancer:
            messages.add_message(self.request, messages.WARNING,
                                 'You are already booked for this job.')
        except JobInPast:
            messages.add_message(self.request, messages.WARNING,
                                 'Sorry, this job is now in the past.')
        except JobInvalidStatus:
            messages.add_message(self.request, messages.WARNING,
                    'Sorry, this job is no longer open for applications.')
        return redirect(self.job_request.get_absolute_url())

    def get_form_kwargs(self, *args, **kwargs):
        # Pass the job request and freelancer to the form
        try:
            self.invitation = Invitation.objects.get(
                                            pk=self.kwargs['invitation_pk'],
                                            freelancer=self.freelancer)
        except Invitation.DoesNotExist:
            # The invitation either does not exist, or does not belong
            # to the current freelancer
            raise PermissionDenied
        else:
            self.job_request = self.invitation.jobrequest

        self.invitation.validate_can_be_applied_to()

        form_kwargs = super(InvitationApply,
                            self).get_form_kwargs(*args, **kwargs)
        form_kwargs.update({
            'invitation': self.invitation,
            'action_text': 'Apply',
            'action_icon': 'confirm',
            'cancel_url': self.job_request.get_absolute_url()
        })
        return form_kwargs

    def get_context_data(self, *args, **kwargs):
        context = super(InvitationApply, self).get_context_data(
                                                            *args, **kwargs)
        context['title'] = 'Apply for job?'
        context['job_request'] = self.job_request

        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'You have now applied for the job.')
        return redirect(self.invitation.jobrequest.get_absolute_url())

class InvitationDecline(AdminOnlyMixin,
                       ConfirmationMixin,
                       FormView):
    """Confirmation form for the admin declining a freelancer's application.
    """
    question = "Decline this freelancer's application?"
    action_text = 'Decline'
    action_icon = 'no'
    template_name = 'booking/apply_or_decline.html'
    form_class = InvitationDeclineForm

    def dispatch(self, *args, **kwargs):
        try:
            return super(InvitationDecline, self).dispatch(*args, **kwargs)
        except JobAlreadyBookedByFreelancer:
            messages.add_message(self.request, messages.WARNING,
                        'The freelancer is already booked on the job.')
        return redirect(self.job_request.get_absolute_url())

    def get_form_kwargs(self, *args, **kwargs):
        # Pass the job request and freelancer to the form

        self.invitation = get_object_or_404(Invitation,
                                            pk=self.kwargs['invitation_pk'])
        self.job_request = self.invitation.jobrequest

        self.invitation.validate_can_be_declined()

        form_kwargs = super(InvitationDecline,
                            self).get_form_kwargs(*args, **kwargs)
        form_kwargs.update({
            'invitation': self.invitation,
            'action_text': 'Decline',
            'action_icon': 'no',
            'cancel_url': self.job_request.get_absolute_url()
        })
        return form_kwargs

    def get_context_data(self, *args, **kwargs):
        context = super(InvitationDecline, self).get_context_data(
                                                            *args, **kwargs)
        context['title'] = 'Decline application?'
        context['job_request'] = self.job_request

        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Declined.')
        # Dispatch signal
        invitation_declined.send(sender=self, invitation=self.invitation)
        return redirect(self.invitation.jobrequest.get_absolute_url())


# Add the ability for booked freelancers to see job requests on the job
# request detail view
def _is_booked_or_invited_freelancer(self):
    # If the user is a freelancer, are they booked on this job?
    try:
        self.freelancer = self.request.user.freelancer
    except Freelancer.DoesNotExist:
        self.freelancer = False
    else:
        return self.object.bookings.for_freelancer(self.freelancer).exists() \
            or self.object.invitations.for_freelancer(self.freelancer).exists()

JobRequestDetail.is_booked_or_invited_freelancer = \
                                            _is_booked_or_invited_freelancer
JobRequestDetail.grant_methods.append('is_booked_or_invited_freelancer')


class JobRequestsPendingConfirmation(AdminOnlyMixin, ContextMixin, ListView):
    """List of job requests pending confirmation, for admin users.
    """
    paginate_by = 15
    extra_context = {'title': 'Jobs pending confirmation'}

    def get_queryset(self, *args, **kwargs):
        return get_job_requests_pending_confirmation()
