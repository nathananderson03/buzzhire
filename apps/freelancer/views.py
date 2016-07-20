from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.views import redirect_to_login
from apps.core.views import ContextMixin, PolymorphicTemplateMixin, \
    OwnerOnlyMixin, ExtraFormsView
from allauth.account.utils import complete_signup
from allauth.account import app_settings
from .models import Freelancer
from .forms import PhotoUploadForm, SignupFormFreelancerDetailsMixin
from django.views.generic import DetailView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from apps.service.forms import ServiceSelectForm
from apps.service.views import ServiceViewMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import FormView
from apps.account.views import SignupView as BaseSignupView
from apps.account.forms import SignupInnerForm, AcceptTermsInnerForm
from .utils import service_for_freelancer
from apps.core.views import PolymorphicTemplateMixin


class FreelancerOnlyMixin(object):
    """Views mixin - only allow freelancers to access.
    Adds freelancer as an attribute on the view.
    """
    def dispatch(self, request, *args, **kwargs):
        # If the user is not logged in, give them the chance to
        if self.request.user.is_anonymous():
            return redirect_to_login(self.request.path)
        try:
            self.freelancer = self.request.user.freelancer
            self.service = service_for_freelancer(self.freelancer)
        except Freelancer.DoesNotExist:
            raise PermissionDenied
        return super(FreelancerOnlyMixin, self).dispatch(request,
                                                         *args, **kwargs)


class OwnedByFreelancerMixin(FreelancerOnlyMixin, OwnerOnlyMixin):
    """Views mixin - only allow drivers who own the object in question to
    access the view.
    """
    def is_owner(self):
        "Whether or not the current user should be treated as the 'owner'."
        return self.get_object().freelancer == self.freelancer


class FreelancerDetailView(PolymorphicTemplateMixin, DetailView):
    """Detail view for clients to look at a Freelancer.
    """
    model = Freelancer
    template_suffix = '_detail'

    def get_object(self):
        object = super(FreelancerDetailView, self).get_object()

        # Forbid anonymous users
        if not self.request.user.is_authenticated():
            raise PermissionDenied

        # Forbid other freelancers
        if self.request.user.is_freelancer and \
                    self.request.user.freelancer != object:
            raise PermissionDenied

        # Forbid clients who don't have the freelancers as booked on their job
        if self.request.user.is_client:
            if not object.bookings.for_client(
                                    self.request.user.client).exists():
                 raise PermissionDenied

        # Prevent non-admins from seeing unpublished freelancers.
        if not object.published and not self.request.user.is_admin:
                raise PermissionDenied

        return object

    def get_context_data(self, *args, **kwargs):
        context = super(FreelancerDetailView, self).get_context_data(*args,
                                                                 **kwargs)
        context['title'] = self.object.get_full_name()
        return context


class FreelancerUpdateView(FreelancerOnlyMixin, ContextMixin,
                       SuccessMessageMixin, UpdateView):
    "Profile edit page for freelancers."

    @property
    def model(self):
        return self.service.freelancer_model

    def get_object(self):
        return self.freelancer

    def get_form_class(self):
        return self.service.freelancer_form

    template_name = 'account/dashboard_base.html'
    success_url = reverse_lazy('account_dashboard')
    extra_context = {'title': 'Edit profile'}
    success_message = 'Saved.'


class FreelancerPhotoView(FreelancerOnlyMixin, ContextMixin, DetailView):
    "View of a freelancer's own photo."
    template_name = 'freelancer/photo_page.html'
    extra_context = {'title': 'Photo'}

    def get_object(self):
        return self.freelancer


class FreelancerPhotoUpdateView(FreelancerOnlyMixin, ContextMixin,
                                SuccessMessageMixin, UpdateView):
    "Page for freelancer to upload their own photo."
    template_name = 'freelancer/photo_upload.html'
    extra_context = {'title': 'Upload photo'}
    form_class = PhotoUploadForm
    success_url = reverse_lazy('freelancer_photo')
    success_message = 'Uploaded.'

    def get_object(self):
        return self.freelancer


class SignupServiceSelect(ContextMixin, FormView):
    """View that allows them to select which service they provide,
    and redirects them to the sign up page for that service.
    """
    form_class = ServiceSelectForm
    template_name = 'freelancer/service_select.html'
    extra_context = {'title': 'Become a freelancer'}

    def form_valid(self, form):
        return redirect('freelancer_signup', form.cleaned_data['service'])


class SignupView(ServiceViewMixin, PolymorphicTemplateMixin,
                 ExtraFormsView, BaseSignupView):
    """Freelancer sign up view.
    
    Uses the service key specified in the url to pull in the correct
    freelancer forms.
    """
    form_class = SignupInnerForm
    template_suffix = '_signup'

    # The form prefix for the account form
    prefix = 'account'
    success_url = reverse_lazy('account_dashboard')

    @property
    def model(self):
        return self.service.freelancer_model

    def get_context_data(self, *args, **kwargs):
        context = super(SignupView, self).get_context_data(*args, **kwargs)

        # Tailor the page title to the service
        context['title'] = '%s sign up' % \
                                self.service.freelancer_name.capitalize()

        return context

    def get_extra_forms(self):
        # Dynamically create a form class by mixing in the
        # SignupFormFreelancerDetailsMixin
        # with the freelancer form for this service
        form_class = type(
                'SignUp%sDetailsForm' % self.service.freelancer_model.__name__,
                (SignupFormFreelancerDetailsMixin,
                self.service.freelancer_form),
                {})
        return {
            'freelancer': form_class,
            'terms': AcceptTermsInnerForm,
        }


    def get_form_kwargs(self, prefix=None):
        form_kwargs = super(SignupView, self).get_form_kwargs(prefix)

        # Set the url for the freelancer terms
        if prefix == 'terms':
            form_kwargs['terms_url'] = reverse('freelancer_terms')

        return form_kwargs


    def form_valid(self, form):
        """Adapted from BaseSignupView to save the freelancer too.
        """

        user = form.save(self.request)
        # Save freelancer form too
        self.bound_forms['freelancer'].save(user)
        return complete_signup(self.request, user,
                               app_settings.EMAIL_VERIFICATION,
                               self.get_success_url())
