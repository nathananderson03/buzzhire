from django.conf.urls import patterns, url
from apps.core.views import ContextTemplateView
from . import views


urlpatterns = [
    url(r'^get-min-pay/$', views.GetMinPayJson.as_view(),
         name='paygrade_get_min_pay'),
]
