from django.conf.urls import patterns, url
from apps.core.views import ContextTemplateView
from . import views


urlpatterns = [
    url(r'^bookings/$', views.FreelancerBookingsList.as_view(),
         name='freelancer_bookings_list'),

    url(r'^bookings/past/$', views.FreelancerBookingsList.as_view(past=True),
         name='freelancer_bookings_list_past'),

    url(r'^create/(?P<job_request_pk>[\d]+)/(?P<freelancer_pk>[\d]+)/$',
         views.BookingConfirm.as_view(),
         name='booking_create'),

    url(r'^invite/(?P<job_request_pk>[\d]+)/(?P<freelancer_pk>[\d]+)/$',
         views.InvitationConfirm.as_view(),
         name='invitation_create'),

    url(r'^invitations/$',
         views.FreelancerInvitationsList.as_view(),
         name='freelancer_invitations_list'),

    url(r'^apply/(?P<invitation_pk>[\d]+)/$',
         views.InvitationApply.as_view(),
         name='invitation_apply'),

    url(r'^decline/(?P<invitation_pk>[\d]+)/$',
         views.InvitationDecline.as_view(),
         name='invitation_decline'),

    url(r'^applied/$', views.FreelancerApplicationsList.as_view(),
         name='freelancer_applications_list'),

    url(r'^applied/past/$', views.FreelancerApplicationsList.as_view(past=True),
         name='freelancer_applications_list_past'),

    url(r'^availability/$', views.AvailabilityUpdate.as_view(),
         name='availability_update'),

    url(r'^job-matching/(?P<job_request_pk>[\d]+)/$',
        views.JobMatchingView.as_view(),
         name='job_matching_for_job_request'),

    url(r"^jobs-pending-confirmation/$",
        views.JobRequestsPendingConfirmation.as_view(),
        name="job_requests_pending_confirmation"),
]
