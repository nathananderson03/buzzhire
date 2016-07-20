from django.conf.urls import patterns, url, include
from rest_framework.authtoken import views
from .routers import SingleObjectFriendlyRouter
from .booking import views as booking_views
from .freelancer import views as freelancer_views
from .client import views as client_views
from .job import views as job_views
from .services.driver import views as driver_views
from .services.cleaner import views as cleaner_views
from .services.kitchen import views as kitchen_views
from .services.bar import views as bar_views
from .services.waiting import views as waiting_views
from .feedback import views as feedback_views
from .payment import views as payment_views
from .notification import views as notification_views
from .paygrade import views as paygrade_views
from .account import views as account_views


# This app is where we define the endpoints for the API,
# used by native mobile apps.

class AppRouter(SingleObjectFriendlyRouter):
    # Define extra endpoints, in a list of two-tuples.  The first item should
    # be the local path, the second the url name.
    extra_endpoints = [
        ('account/password_reset', 'password_reset'),
    ]

router = AppRouter()

# General data

router.register(r'driver/vehicle-types',
                driver_views.VehicleTypeViewSet,
                base_name='vehicle_types')
router.register(r'driver/flexible-vehicle-types',
                driver_views.FlexibleVehicleTypeViewSet,
                base_name='flexible_vehicle_types')

# All users
router.register(r'notifications',
                notification_views.NotificationsForUserViewSet,
                base_name='notifications')

# For clients

# Own profile
router.register(r'client',
                client_views.OwnClientViewSet,
                base_name='client_own')

# Freelancer profile for client (all types)
router.register(r'client/freelancers',
                freelancer_views.FreelancerForClientViewSet,
                base_name='freelancers_for_client')
router.register(r'client/driver/freelancers',
                driver_views.DriverForClientViewSet,
                base_name='driver_freelancers_for_client')
router.register(r'client/cleaner/freelancers',
                cleaner_views.CleanerForClientViewSet,
                base_name='cleaner_freelancers_for_client')
router.register(r'client/kitchen/freelancers',
                kitchen_views.KitchenFreelancerForClientViewSet,
                base_name='kitchen_freelancers_for_client')
router.register(r'client/bar/freelancers',
                bar_views.BarFreelancerForClientViewSet,
                base_name='bar_freelancers_for_client')
router.register(r'client/waiting/freelancers',
                waiting_views.WaitingFreelancerForClientViewSet,
                base_name='waiting_freelancers_for_client')

# Client's job requests (all types)
router.register(r'client/job-requests',
                job_views.JobRequestForClientViewSet,
                base_name='job_requests_for_client')
router.register(r'client/driver/job-requests',
                driver_views.DriverJobRequestForClientViewSet,
                base_name='driver_job_requests_for_client')
router.register(r'client/cleaner/job-requests',
                cleaner_views.CleanerJobRequestForClientViewSet,
                base_name='cleaner_job_requests_for_client')
router.register(r'client/kitchen/job-requests',
                kitchen_views.KitchenJobRequestForClientViewSet,
                base_name='kitchen_job_requests_for_client')
router.register(r'client/bar/job-requests',
                bar_views.BarJobRequestForClientViewSet,
                base_name='bar_job_requests_for_client')
router.register(r'client/waiting/job-requests',
                waiting_views.WaitingJobRequestForClientViewSet,
                base_name='waiting_job_requests_for_client')

# Client pay grade info
router.register(r'client/driver/pay-grade',
                driver_views.ClientDriverPayGradeViewSet,
                base_name='driver_pay_grade_for_client')
router.register(r'client/cleaner/pay-grade',
                cleaner_views.ClientCleanerPayGradeViewSet,
                base_name='cleaner_pay_grade_for_client')
router.register(r'client/kitchen/pay-grade',
                kitchen_views.ClientKitchenPayGradeViewSet,
                base_name='kitchen_pay_grade_for_client')
router.register(r'client/bar/pay-grade',
                bar_views.ClientBarPayGradeViewSet,
                base_name='bar_pay_grade_for_client')
router.register(r'client/waiting/pay-grade',
                waiting_views.ClientWaitingPayGradeViewSet,
                base_name='waiting_pay_grade_for_client')


# Client payment
router.register(r'client/payment/token',
                payment_views.PaymentTokenViewSet,
                base_name='client_payment_token')
router.register(r'client/payment/create',
                payment_views.JobRequestPaymentViewSet,
                base_name='client_job_request_pay')

# Client's feedback
router.register(r'client/booking/awaiting-feedback',
                feedback_views.ClientFeedbackBacklogViewSet,
                base_name='client_feedback_backlog')
router.register(r'client/feedback',
                 feedback_views.FeedbackByClientViewSet,
                 base_name='client_feedback')
# router.register(r'client/feedback/received',
#                 feedback_views.ClientFeedbackReceivedViewSet,
#                 base_name='client_feedback_received')


# For freelancers

# Own profile (all types)
router.register(r'freelancer',
                freelancer_views.OwnFreelancerViewSet,
                base_name='freelancer_own')
router.register(r'freelancer/availability',
                freelancer_views.OwnFreelancerAvailabilityViewSet,
                base_name='freelancer_availability_own')
router.register(r'freelancer/driver',
                driver_views.OwnDriverViewSet,
                base_name='driver_freelancer_own')
router.register(r'freelancer/bar',
                bar_views.OwnBarFreelancerViewSet,
                base_name='bar_freelancer_own')
router.register(r'freelancer/waiting',
                waiting_views.OwnWaitingFreelancerViewSet,
                base_name='waiting_freelancer_own')
router.register(r'freelancer/kitchen',
                kitchen_views.OwnKitchenFreelancerViewSet,
                base_name='kitchen_freelancer_own')
router.register(r'freelancer/cleaner',
                cleaner_views.OwnCleanerViewSet,
                base_name='cleaner_freelancer_own')


# Freelancer's clients
router.register(r'freelancer/clients',
                client_views.ClientForFreelancerViewSet,
                base_name='clients_for_freelancer')

# Freelancer's bookings & invitations
router.register(r'freelancer/bookings',
                booking_views.BookingForFreelancerViewSet,
                base_name='bookings_for_freelancer')
router.register(r'freelancer/invitations',
                booking_views.InvitationForFreelancerViewSet,
                base_name='invitations_for_freelancer')
router.register(r'freelancer/applications',
                booking_views.ApplicationForFreelancerViewSet,
                base_name='applications_for_freelancer')

# Freelancer's job requests (all types)
router.register(r'freelancer/job-requests',
                job_views.JobRequestForFreelancerViewSet,
                base_name='job_requests_for_freelancer')
router.register(r'freelancer/driver/job-requests',
                driver_views.DriverJobRequestForFreelancerViewSet,
                base_name='driver_job_requests_for_freelancer')
router.register(r'freelancer/cleaner/job-requests',
                cleaner_views.CleanerJobRequestForFreelancerViewSet,
                base_name='cleaner_job_requests_for_freelancer')
router.register(r'freelancer/kitchen/job-requests',
                kitchen_views.KitchenJobRequestForFreelancerViewSet,
                base_name='kitchen_job_requests_for_freelancer')
router.register(r'freelancer/bar/job-requests',
                bar_views.BarJobRequestForFreelancerViewSet,
                base_name='bar_job_requests_for_freelancer')
router.register(r'freelancer/waiting/job-requests',
                waiting_views.WaitingJobRequestForFreelancerViewSet,
                base_name='waiting_job_requests_for_freelancer')

# Driver's own vehicle types
router.register(r'freelancer/driver/vehicles',
                driver_views.DriverVehicleForDriverViewSet,
                base_name='driver_vehicle_types')





urlpatterns = [
    url(r'^v1/auth/', include('rest_framework.urls',
                              namespace='rest_framework')),
    url(r'^v1/token-auth/', views.obtain_auth_token),
    url(r'^v1/client/register/', client_views.ClientRegisterView.as_view()),
    url(r'^v1/', include(router.urls)),
    url(r'^v1/freelancer/earnings/$',
        freelancer_views.FreelancerEarningView.as_view(),
        name='combined-list'),
    # User accounts
    url(r'^v1/account/password_reset/$',
        account_views.PasswordResetViewSet.as_view(),
        name='password_reset'),
]
