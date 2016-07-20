from django.conf.urls import url
from apps.core.views import ContextTemplateView
from . import views

urlpatterns = [
    url(r"^vehicles/$", views.DriverVehicleTypeListView.as_view(),
        name="drivervehicletype_list"),
    url(r"^vehicles/add/$", views.DriverVehicleTypeCreateView.as_view(),
        name="drivervehicletype_add"),
    url(r"^vehicles/(?P<pk>[\d]+)/$", views.DriverVehicleTypeUpdateView.as_view(),
        name="drivervehicletype_change"),
    url(r"^vehicles/(?P<pk>[\d]+)/delete/$", views.DriverVehicleTypeDeleteView.as_view(),
        name="drivervehicletype_delete"),

]

