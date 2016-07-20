from django.views.generic import (CreateView, UpdateView, TemplateView,
                            ListView, DetailView, FormView)
from django.views.generic.detail import SingleObjectMixin, \
                                        SingleObjectTemplateResponseMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy, reverse
from allauth.account import app_settings
from allauth.account.utils import complete_signup
from django.shortcuts import redirect
from braces.views._access import AnonymousRequiredMixin
from apps.core.views import ContextMixin, TabsMixin, ConfirmationMixin, \
                                GrantCheckingMixin, PolymorphicTemplateMixin, \
                                ExtraFormsView
from apps.account.views import AdminOnlyMixin
from apps.account.forms import LoginForm, AcceptTermsInnerForm
from apps.client.views import ClientOnlyMixin, OwnedByClientMixin
from apps.client.forms import ClientInnerForm
from apps.client.models import Client
from apps.account.views import SignupView as BaseSignupView
from .models import JobRequest
from .forms import JobRequestInnerFormMixin, JobRequestUpdateMixin, \
                    JobRequestSignupInnerForm, JobRequestCheckoutForm
from apps.service.forms import ServiceSelectForm
from django.http.response import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from . import service_from_class
from apps.service import services
from apps.service.views import ServiceViewMixin


class ServiceSelect(ContextMixin, FormView):
    """View that allows them to select which service they  want,
    and redirects them to the job request creation page for that service.
    """
    form_class = ServiceSelectForm
    template_name = 'job/service_select.html'
    extra_context = {'title': 'Book a freelancer'}

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(ServiceSelect, self).get_form_kwargs(*args,
                                                                    **kwargs)
        # Use the plural version of the freelancer title
        form_kwargs['use_plural'] = True
        return form_kwargs

    def form_valid(self, form):
        return redirect('job_request_create',
                       form.cleaned_data['service'])


class JobRequestCreate(ClientOnlyMixin, ServiceViewMixin, ContextMixin,
                       PolymorphicTemplateMixin, CreateView):
    """View class for logged in clients to create a job request,
    intended to be subclassed.
    """
    template_suffix = '_form'

    def get_context_data(self, *args, **kwargs):
        # Tailor the page title to the service
        context = super(JobRequestCreate, self).get_context_data(
                                                            *args, **kwargs)
        context['title'] = 'Book %s' % self.service.freelancer_name_plural
        return context

    @property
    def model(self):
        return self.service.job_request_model

    def get_form_class(self):
        return self.service.job_request_form

    def dispatch(self, request, *args, **kwargs):
        # if not logged in, redirect to a job request pre-sign up page
        if request.user.is_anonymous():
            return redirect('job_request_create_anon',
                            services[kwargs['service_key']].key)
        return super(JobRequestCreate, self).dispatch(request, *args,
                                                            **kwargs)
    def get_success_url(self):
        return reverse('job_request_checkout', args=(self.object.pk,))

    def form_valid(self, form):
        """Adapted version of ModelFormMixin.form_valid
        that supplies the client.
        """
        self.object = form.save(client=self.client)
        return HttpResponseRedirect(self.get_success_url())


class ClientSignUpView(ServiceViewMixin, ExtraFormsView, BaseSignupView):
    template_name = 'job/client_signup.html'
    form_class = JobRequestSignupInnerForm
    # The form prefix for the account form
    prefix = 'account'

    def get_extra_forms(self):
        # Dynamically generate a JobRequestInnerForm that is specific to
        # the service.  All this is doing is creating a class on the fly
        # that mixes in the JobRequestInnerFormMixin to the service specific
        # JobRequestForm that is defined on the service.
        return {
            'client': ClientInnerForm,
            'terms': AcceptTermsInnerForm,
        }

    def get_form_kwargs(self, prefix=None):
        form_kwargs = super(ClientSignUpView, self).get_form_kwargs(prefix)

        # Set the url for the client terms
        if prefix == 'terms':
            form_kwargs['terms_url'] = reverse('client_terms')

        return form_kwargs

    def form_valid(self, form):
        """Adapted from BaseSignupView to save the client and log them in.
        """
        user = form.save(self.request)

        # Save extra forms too
        client = self.bound_forms['client'].save(user=user)

        # Complete sign up and log them in
        return complete_signup(self.request, user,
                               app_settings.EMAIL_VERIFICATION,
                               self.get_success_url())

    def get_authenticated_redirect_url(self):
        # If they are already authenticated, redirect here
        return self.get_success_url()

    def get_success_url(self):
        return reverse('job_request_create', args=(self.service.key,))


# class JobRequestCreateAnonymous(ServiceViewMixin,
#                                 PolymorphicTemplateMixin,
#                                 BaseSignupView):
#     """Page for anonymous users who want to create a job request.
#
#     N.B. in the process of decommissioning this view.
#     """
#     form_class = JobRequestSignupInnerForm
#     # The form prefix for the account form
#     prefix = 'account'
#     template_suffix = '_create_anon'
#
#     @property
#     def model(self):
#         # Specify the model for the PolymorphicTemplateMixin
#         return self.service.job_request_model
#
#     def get_extra_forms(self):
#         # Dynamically generate a JobRequestInnerForm that is specific to
#         # the service.  All this is doing is creating a class on the fly
#         # that mixes in the JobRequestInnerFormMixin to the service specific
#         # JobRequestForm that is defined on the service.
#         job_request_form_class = type(
#                 '%sInnerForm' % self.service.job_request_model.__name__,
#                 (JobRequestInnerFormMixin,
#                  self.service.job_request_form),
#                 {})
#         return {
#             'client': ClientInnerForm,
#             'job_request': job_request_form_class,
#         }
#
#     def get_context_data(self, *args, **kwargs):
#         context = super(JobRequestCreateAnonymous,
#                         self).get_context_data(*args, **kwargs)
#         # Tailor the page title to the service
#         context['title'] = 'Book %s' % self.service.freelancer_name_plural.title()
#
#         context['extra_forms'] = []
#         for prefix, form_class in self.extra_forms.items():
#             context['extra_forms'].append(self.get_form(form_class, prefix))
#         return context
#
#     def get_form(self, form_class, prefix=None):
#         # Now is a good time to set the extra_forms too
#         self.extra_forms = self.get_extra_forms()
#         # Pass the prefix through to get_form_kwargs
#         return form_class(**self.get_form_kwargs(prefix))
#
#     def get_form_kwargs(self, prefix=None):
#         """Standard get_form_kwargs() method adapted to return
#         the extra forms too."""
#
#         if prefix is None:
#             # This is for the main form (signup form)
#             prefix = self.get_prefix()
#
#         kwargs = {
#             'initial': self.get_initial(),
#             'prefix': prefix,
#         }
#
#         if self.request.method in ('POST', 'PUT'):
#             kwargs.update({
#                 'data': self.request.POST,
#                 'files': self.request.FILES,
#             })
#         return kwargs
#
#     def post(self, request, *args, **kwargs):
#         "Standard post method adapted to validate both forms."
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         self.bound_forms = {self.get_prefix(): form}
#         for prefix, form_class in self.extra_forms.items():
#             self.bound_forms[prefix] = self.get_form(form_class, prefix)
#
#         if all([f.is_valid() for f in self.bound_forms.values()]):
#             # If all the forms validate
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)
#
#     def form_valid(self, form):
#         """Adapted from BaseSignupView to save the freelancer too.
#         We do not currently run the complete_signup process, as we
#         don't want the freelancer to be logged in after sign up.
#         """
#         user = form.save(self.request)
#
#         # Save extra forms too
#         client = self.bound_forms['client'].save(user=user)
#         self.job_request = self.bound_forms['job_request'].save(client=client)
#
#         # Complete sign up and log them in
#         return complete_signup(self.request, user,
#                                app_settings.EMAIL_VERIFICATION,
#                                self.get_success_url())
#
#     def get_authenticated_redirect_url(self):
#         return reverse('job_request_create', args=(self.service.key,))
#
#     def get_success_url(self):
#         return reverse('job_request_checkout', args=(self.job_request.pk,))


class RequestedJobList(ClientOnlyMixin, ContextMixin, TabsMixin, ListView):
    """List of job requests ordered by a client.
    This view has two modes - if self.past is True, it will return the
    job requests in the past, otherwise it will show upcoming job requests.   
    """
    paginate_by = 15
    extra_context = {'title': 'Requested jobs'}
    tabs = [
        ('Upcoming', reverse_lazy('requested_jobs')),
        ('Past', reverse_lazy('requested_jobs_past')),
    ]
    past = False

    def get_queryset(self, *args, **kwargs):
        queryset = JobRequest.objects.for_client(self.client)
        if self.past:
            return queryset.past()
        else:
            return queryset.future()


class JobRequestDetail(GrantCheckingMixin, PolymorphicTemplateMixin,
                       DetailView):
    """Detail page for job requests.
    We use the GrantCheckingMixin as we want other apps that this app
    doesn't know about (e.g. bookings) to grant certain freelancers access.
    """
    model = JobRequest
    require_login = True
    allow_admin = True
    grant_methods = ['is_owned_by_client']
    template_suffix = '_detail'

    def is_owned_by_client(self):
        """Grant method - returns True if the user is a client, and they
        own the job request.
        """
        try:
            self.client = self.request.user.client
        except Client.DoesNotExist:
            self.client = False
        else:
            return self.object.client == self.client

    def get_context_data(self, *args, **kwargs):
        context = super(JobRequestDetail, self).get_context_data(*args,
                                                                       **kwargs)
        context['title'] = self.object
        context['client'] = self.client
        return context



class JobRequestUpdate(AdminOnlyMixin, SuccessMessageMixin,
                       PolymorphicTemplateMixin, UpdateView):
    "Edit page for job requests."
    model = JobRequest
    success_message = 'Saved.'
    template_suffix = '_form'

    def get_form_class(self):
        # Return the form registered on the service as job_request_edit_form
        self.service = service_from_class(self.object.__class__)
        # Dynamically create a form class by mixing in the
        # JobRequestUpdateMixin with the job request form for this service
        return type(
            '%sJobRequestUpdateForm' % self.service.job_request_model.__name__,
            (JobRequestUpdateMixin,
            self.service.job_request_form),
            {})

    def get_context_data(self, *args, **kwargs):
        context = super(JobRequestUpdate, self).get_context_data(*args,
                                                                 **kwargs)
        context['title'] = 'Edit %s' % self.object
        context['service'] = self.service
        return context


class JobRequestCheckout(OwnedByClientMixin, SingleObjectMixin,
                               FormView):
    "Checkout page where client pays for and opens the job request."
    model = JobRequest
    template_name = 'job/checkout.html'
    form_class = JobRequestCheckoutForm

    def dispatch(self, *args, **kwargs):
        self.object = self.get_object()
        if self.object.status != JobRequest.STATUS_CHECKOUT:
            return redirect(self.object.get_absolute_url())
        return super(JobRequestCheckout, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(JobRequestCheckout, self).get_context_data(*args,
                                                                    **kwargs)
        context['title'] = 'Confirm job'
        context['service'] = service_from_class(self.object.__class__)
        return context

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(JobRequestCheckout,
                            self).get_form_kwargs(*args, **kwargs)
        # Pass the job request to the form
        # import pdb; pdb.set_trace()
        form_kwargs['instance'] = self.object
        return form_kwargs

    def form_valid(self, form):
        form.save()
        return super(JobRequestCheckout, self).form_valid(form)

    def get_success_url(self):
        # Redirect to confirmation page
        return reverse('job_request_done', args=(self.object.pk,))


class JobRequestDone(OwnedByClientMixin, ContextMixin, DetailView):
    "Confirmation page on successful job request submission."
    template_name = 'job/done.html'
    extra_context = {'title': 'Thanks for your booking'}
    model = JobRequest


class AdminJobList(AdminOnlyMixin, ContextMixin, TabsMixin, ListView):
    """List of job requests for admin users.
    """
    paginate_by = 15
    extra_context = {'title': 'Job requests'}

    def get_tabs(self):
        "Returns a list of two-tuples for the tabs."
        tabs = []
        for status_value, status_title in JobRequest.STATUS_CHOICES:
            tabs.append((status_title,
                         reverse('job_request_admin_list_tab',
                                 kwargs={'status': status_value})))
        return tabs

    def get_queryset(self, *args, **kwargs):

        status_tab = self.kwargs.get('status')

        if (status_tab == JobRequest.STATUS_OPEN):
            queryset = JobRequest.objects.filter(status=JobRequest.STATUS_OPEN).order_by('date', 'start_time')
        else:
            queryset = JobRequest.objects.filter(status=self.kwargs.get('status', JobRequest.STATUS_OPEN))

        return queryset

