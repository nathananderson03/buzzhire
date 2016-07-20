from configurations_seddonym import StandardConfiguration
import os


class ProjectConfiguration(StandardConfiguration):
#     BASE_DIR = os.path.dirname(os.path.dirname(__file__))
#     STATICFILES_DIRS = (
#         os.path.join(BASE_DIR, "static"),
#     )

    MANAGERS = ADMINS = (
         ('David Seddon', 'david@seddonym.me'),
         ('Nikola Kolevski', 'Nikola.Kolevski@borneagency.com')
    )

    SITE_TITLE = 'BuzzHire'
    PROJECT_NAME = 'buzzhire'
    INSTALLED_APPS = StandardConfiguration.INSTALLED_APPS + (
        # Apps lower down the list should import from apps higher up the list,
        # and not the other way around
        'django.contrib.humanize',
        'django.contrib.gis',
        'crispy_forms',
        'allauth',
        'allauth.account',
        'sorl.thumbnail',
        'django_extensions',
        'django_inlinecss',
        'compressor',
        'djangobower',
        'dbbackup',
        'fsm_admin',
        'polymorphic',
        'django_bootstrap_breadcrumbs',
        'huey.djhuey',
        'import_export',
        'rest_framework',
        'rest_framework.authtoken',
        'apps.core',
        'apps.notification',
        'apps.location',
        'apps.account',
        'apps.service',
        'apps.client',
        'apps.freelancer',
        'apps.payment',
        'apps.paygrade',
        'apps.job',
        'apps.booking',
        'apps.feedback',
        'apps.reminder',
        'apps.services.driver',
        'apps.services.kitchen',
        'apps.services.bar',
        'apps.services.waiting',
        'apps.services.cleaner',
        'apps.api',
        'apps.main',
    )

    TEMPLATE_CONTEXT_PROCESSORS = StandardConfiguration.TEMPLATE_CONTEXT_PROCESSORS + (
         "allauth.account.context_processors.account",
         "allauth.socialaccount.context_processors.socialaccount",
         'apps.main.context_processors.main',
    )

    AUTHENTICATION_BACKENDS = (
        # Needed to login by username in Django admin, regardless of `allauth`
        "django.contrib.auth.backends.ModelBackend",

        # `allauth` specific authentication methods, such as login by e-mail
        "allauth.account.auth_backends.AuthenticationBackend",
    )

    MIDDLEWARE_CLASSES = StandardConfiguration.MIDDLEWARE_CLASSES + (
       'apps.feedback.middleware.FeedbackMiddleware',
       'apps.core.middleware.StrictAuthenticationMiddleware',
    )

    CRISPY_TEMPLATE_PACK = 'bootstrap3'

    ACCOUNT_EMAIL_REQUIRED = True
    ACCOUNT_USERNAME_REQUIRED = False
    ACCOUNT_EMAIL_VERIFICATION = 'none'
    ACCOUNT_AUTHENTICATION_METHOD = 'email'
    ACCOUNT_USER_DISPLAY = 'apps.account.utils.user_display'

    FACEBOOK_URL = 'www.facebook.com/buzzhire.uk'
    TWITTER_URL = 'twitter.com/buzzhire'

    STATICFILES_FINDERS = StandardConfiguration.STATICFILES_FINDERS + (
        'compressor.finders.CompressorFinder',
        'djangobower.finders.BowerFinder',
    )

    COMPRESS_PRECOMPILERS = (
        ('text/less', 'lessc {infile} {outfile}'),
    )

    LOGIN_URL = 'account_login'
    CURRENCIES = ('GBP',)

    TIME_INPUT_FORMATS = ['%I:%M %p']

    def BOWER_COMPONENTS_ROOT(self):
        return os.path.join(self.PROJECT_ROOT, 'components')

    # The way django-bower is used in this project is that we run
    # ./manage.py bower install locally, to add the packages to
    # components/bower_components.  However, this is under version control
    # so bower install doesn't need to be run by the other installations.
    BOWER_INSTALLED_APPS = (
        'eternicode/bootstrap-datepicker',
        'acpmasquerade/bootstrap3-timepicker2',
        'bootstrap-star-rating',
    )

    @property
    def DEFAULT_DATABASE_ENGINE(self):
        # Location-based database
        return 'django.contrib.gis.db.backends.postgis'

    # Min pay per hour, before commission
    CLIENT_MIN_WAGE = 8.0
    # The percent commission we charge on client rates
    COMMISSION_PERCENT = 13.5
    # Number of pence to round to
    COMMISSION_ROUND_PENCE = 25

    # API
    API_ACTIVE = True
    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.TokenAuthentication',
            'rest_framework.authentication.SessionAuthentication',
        )
    }

    def CONTACT_FROM_EMAIL(self):
        return 'BuzzHire <%s>' % self.CONTACT_EMAIL

    def BOOKINGS_FROM_EMAIL(self):
        return 'BuzzHire <%s>' % self.BOOKINGS_EMAIL


    # The minimum number of hours notice allowed to create a job request
    JOB_REQUEST_MINIMUM_HOURS_NOTICE = 4

    # Minimum number of hours a job can last
    MIN_JOB_DURATION = 2

    PARSE_CLIENT_APPLICATION_ID = '87WebYikYitgl6GOnavbGesoGvA6lka2oLVnH5i3'
    PARSE_FREELANCER_APPLICATION_ID = 'ARd59ixk04dHhZcY9aMYrBGHJGe9kLI7tdSYpdDV'

    CONTACT_PHONE = '020 3322 3738'
    BOOKINGS_EMAIL = 'support@buzzhire.co'
    JOBS_EMAIL = 'jobs@buzzhire.co'

    # This setting provides a way to specify the endpoint for getting
    # the minimum pay grade, while keeping apps.paygrade naive about apps.api.
    # See apps.paygrade.templatetags.min_pay_ajax_endpoint()
    PAY_GRADE_REVERSE_URL = '%(service)s_pay_grade_for_client-detail'

    # The number of minutes before the booking a freelancer should arrive
    ARRIVAL_PERIOD_MINUTES = 15

    # These are numbers for the test Twilio account
    TWILIO_ACCOUNT_SID = 'AC28ae162c411ca4ac235efcdb0206c672'
    TWILIO_PHONE_NUMBER = '+15005550006'
