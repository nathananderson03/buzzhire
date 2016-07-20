from django.conf.urls import url
from . import views
from .models import Notification


urlpatterns = [
    url(r'^$',
        views.NotificationList.as_view(),
        name='notification_list'),
]
