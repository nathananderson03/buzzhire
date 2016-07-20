from django.views.generic import ListView
from braces.views import LoginRequiredMixin
from apps.core.views import ContextMixin
from .models import Notification


class NotificationList(LoginRequiredMixin,
                       ContextMixin, ListView):
    "List of the user's notifications."
    paginate_by = 10
    extra_context = {'title': 'Notifications'}

    def get_queryset(self, *args, **kwargs):
        return Notification.objects.for_user(self.request.user)
