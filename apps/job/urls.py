from django.conf.urls import url
from . import views
from apps.job.models import JobRequest



urlpatterns = [
     url(r'^admin/$', views.AdminJobList.as_view(),
         name='job_request_admin_list'),
     url(r'^admin/(?P<status>[\w]+)/$', views.AdminJobList.as_view(),
        name='job_request_admin_list_tab'),

     url(r'^requested/$', views.RequestedJobList.as_view(),
         name='requested_jobs'),

     url(r'^requested/past/$', views.RequestedJobList.as_view(past=True),
         name='requested_jobs_past'),

    url(r'^create/$', views.ServiceSelect.as_view(), name='service_select'),

    url(r'^create/(?P<service_key>[\w]+)/$',
                       views.JobRequestCreate.as_view(),
                       name='job_request_create'),

#     url(r'^create/(?P<service_key>[\w]+)/new-client/$',
#          views.JobRequestCreateAnonymous.as_view(),
#          name='job_request_create_anon'),

    url(r'^create/(?P<service_key>[\w]+)/sign-up/$',
         views.ClientSignUpView.as_view(),
         name='job_request_create_anon'),


    url(r'^requests/(?P<pk>[\d]+)/checkout/$',
        views.JobRequestCheckout.as_view(),
        name='job_request_checkout'),

     url(r'^requests/(?P<pk>[\d]+)/done/$',
         views.JobRequestDone.as_view(),
         name='job_request_done'),

    url(r'^requests/(?P<pk>[\d]+)/$', views.JobRequestDetail.as_view(),
        name='jobrequest_detail'),


    url(r'^requests/(?P<pk>[\d]+)/edit/$',
        views.JobRequestUpdate.as_view(),
        name='jobrequest_edit'),
]

