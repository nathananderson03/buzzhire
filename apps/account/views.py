from allauth.account import views
from apps.core.views import ContextMixin, ConfirmationMixin, \
                            ContextTemplateView
from braces.views import LoginRequiredMixin
from . import forms
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied


class DashboardView(LoginRequiredMixin, ContextTemplateView):
    extra_context = {'title': 'Dashboard'}
    template_name = 'account/dashboard.html'


class SignupView(ContextMixin, views.SignupView):
    extra_context = {'title': 'Register'}
    form_class = forms.SignupForm


class LoginView(ContextMixin, views.LoginView):
    extra_context = {'title': 'Log in'}
    form_class = forms.LoginForm
    success_url = reverse_lazy('account_dashboard')


class LogoutView(ContextMixin, ConfirmationMixin, views.LogoutView):
    extra_context = {'title': 'Log out'}
    question = 'Are you sure you want to log out?'
    cancel_url = reverse_lazy('index')


class AccountInactiveView(ContextTemplateView):
    extra_context = {'title': 'Account disabled'}
    form_class = forms.SignupForm
    template_name = 'account/account_inactive.html'


class PasswordResetView(ContextMixin, views.PasswordResetView):
    extra_context = {'title': 'Reset password'}
    form_class = forms.ResetPasswordForm


class PasswordResetDoneView(ContextMixin, views.PasswordResetDoneView):
    extra_context = {'title': 'Now check your email'}


class PasswordResetFromKeyView(ContextMixin, views.PasswordResetFromKeyView):
    extra_context = {'title': 'New password'}
    form_class = forms.ResetPasswordKeyForm


class PasswordResetFromKeyDoneView(ContextMixin,
                                   views.PasswordResetFromKeyDoneView):
    extra_context = {'title': 'Password reset complete'}


class PasswordChangeView(LoginRequiredMixin, ContextMixin,
                         views.PasswordChangeView):
    extra_context = {'title': 'Edit password'}
    form_class = forms.ChangePasswordForm
    template_name = 'account/dashboard_base.html'

class PasswordSetView(ContextMixin, views.PasswordSetView):
    extra_context = {'title': 'Password changed'}


class AdminOnlyMixin(object):
    """Views mixin - only allow admins to access."""
    def dispatch(self, request, *args, **kwargs):
        # If the user is not logged in, give them the chance to
        if self.request.user.is_anonymous():
            return redirect_to_login(self.request.path)
        elif not self.request.user.is_admin:
            raise PermissionDenied
        return super(AdminOnlyMixin, self).dispatch(request, *args, **kwargs)
