from django.core.exceptions import PermissionDenied
from django.views.generic.base import TemplateView
from apps.core.views import ContextTemplateView, ContextMixin
from apps.service.forms import ServiceSelectForm
from django.shortcuts import redirect


class TestError(TemplateView):
    "View used to trigger site error, for testing purposes."
    def dispatch(self, *args, **kwargs):
        raise Exception('Test exception raised.')


class TestDenied(TemplateView):
    "View used to trigger permission denied, for testing purposes."
    def dispatch(self, *args, **kwargs):
        raise PermissionDenied


class HomeView(TemplateView):
    "The home page."
    template_name = 'main/home.html'

    def dispatch(self, *args, **kwargs):
        # Redirect to the dashboard, if the user is logged in
        if self.request.user.is_authenticated():
            return redirect('account_dashboard')

        return super(HomeView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context['form'] = ServiceSelectForm(use_plural=True)
        return context
