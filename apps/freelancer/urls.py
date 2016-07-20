from django.conf.urls import url
from apps.core.views import ContextTemplateView
from . import views

urlpatterns = [

    url(r"^signup/$", views.SignupServiceSelect.as_view(),
        name="freelancer_signup_select"),

    url(r"^signup/thankyou/$", ContextTemplateView.as_view(
                template_name='freelancer/thankyou.html',
                extra_context={'title': 'Thanks for signing up'}),
                name="freelancer_thankyou"),

    url(r"^signup/(?P<service_key>[\w]+)/$", views.SignupView.as_view(),
        name="freelancer_signup"),

    url(r"^edit/$", views.FreelancerUpdateView.as_view(),
        name="freelancer_change"),

    url(r"^(?P<pk>[\d]+)/$", views.FreelancerDetailView.as_view(),
        name="freelancer_detail"),

    url(r"^photo/$", views.FreelancerPhotoView.as_view(),
        name="freelancer_photo"),
    url(r"^photo/add/$", views.FreelancerPhotoUpdateView.as_view(),
        name="freelancer_photo_update"),

    url(r'^terms-and-conditions/$', ContextTemplateView.as_view(
                    template_name='freelancer/terms.html',
                    extra_context={'title': 'Freelancer terms and conditions'}),
                    name='freelancer_terms'),
]

