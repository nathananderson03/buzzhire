from .project import ProjectConfiguration
from configurations_seddonym import installations
import os
import logging

class BraintreeSandboxMixin(object):
    """Settings for the Braintree sandbox.
    Note: BRAINTREE_PRIVATE_KEY should be included in secret.py.
    """
    BRAINTREE_MERCHANT_ID = '8jv5gg39h7kq69qw'
    BRAINTREE_PUBLIC_KEY = 'mwm76cyqycjc6hzq'
    BRAINTREE_SANDBOX = True

class HueyMixin(object):
    """Settings for the Huey task queue.
    Should specify a HUEY_NAME that is unique for the redis process.
    """
    HUEY_NAME = ''
    HUEY_PORT = 6379

    def HUEY(self):
        return {
            'backend': 'huey.backends.redis_backend',
            'name': self.HUEY_NAME,
            'connection': {'host': 'localhost', 'port': self.HUEY_PORT},
            'always_eager': False,
            'consumer_options': {'workers': 1},
        }

    @property
    def LOGGING(self):
        # Make sure we mail admins during uncaught exceptions during Huey tasks;
        # Otherwise issues with tasks can easily go unnoticed
        _LOGGING = super(HueyMixin, self).LOGGING
        _LOGGING['loggers']['huey'] = {
            'handlers': ['error', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        }
        return _LOGGING


class MandrillMixin(object):
    "Enables Mandrill email on the installation."
    EMAIL_HOST = 'smtp.mandrillapp.com'
    EMAIL_HOST_USER = 'nick@buzzhire.co'


class Local(BraintreeSandboxMixin, HueyMixin,
            MandrillMixin,
            installations.LocalMixin, ProjectConfiguration):
    PROJECT_ROOT = '/home/devmaster/buzzhire_django'
    BOOKINGS_EMAIL = 'bookingslocal@dev.buzzhire.co'
    SERVER_EMAIL = 'local@dev.buzzhire.co'
    ACCOUNT_PASSWORD_MIN_LENGTH = 1
    HUEY_NAME = 'buzzhire'
    API_ACTIVE = True

    BOOKINGS_EMAIL = 'support-local@dev.buzzhire.co'
    JOBS_EMAIL = 'jobs-local@dev.buzzhire.co'

    INSTALLED_APPS = ProjectConfiguration.INSTALLED_APPS + (
        'debug_toolbar',
    )

    @property
    def DATABASES(self):
        return {
            'default': {
                'NAME': 'buzzhire',
                'USER': 'postgres',
                'PASSWORD': '111',
                'ENGINE': 'django.contrib.gis.db.backends.postgis',
                'HOST': 'localhost',
            }
        }

class Dev(BraintreeSandboxMixin, HueyMixin,
          MandrillMixin,
          installations.WebfactionDevMixin, ProjectConfiguration):
    DOMAIN = 'dev.buzzhire.co'
    WEBFACTION_USER = 'buzzhire'
    DEBUG = False
    ACCOUNT_PASSWORD_MIN_LENGTH = 1

    BOOKINGS_EMAIL = 'support@dev.buzzhire.co'
    JOBS_EMAIL = 'jobs@dev.buzzhire.co'

    HUEY_NAME = 'dev'
    HUEY_PORT = 17610

    API_ACTIVE = True

    # Allow embedding, so responsinator.com can be used for testing
    X_FRAME_OPTIONS = "ALLOWALL"

class VagrantDev(BraintreeSandboxMixin, HueyMixin,
          MandrillMixin,
          installations.WebfactionDevMixin, ProjectConfiguration):
    DOMAIN = 'buzz.ubn'
    PROJECT_ROOT = '/vagrant'
    WEBFACTION_USER = 'buzzhire'
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    DEBUG = True
    ACCOUNT_PASSWORD_MIN_LENGTH = 1

    @property
    def DATABASES(self):
        return {
            'default': {
                'NAME': self.DEFAULT_DATABASE_NAME,
                'USER': self.DEFAULT_DATABASE_USER,
                'PASSWORD': self.DEFAULT_DATABASE_PASSWORD,
                'ENGINE': self.DEFAULT_DATABASE_ENGINE,
                'HOST': self.DEFAULT_DATABASE_HOST,
            }
        }

    @property
    def LOG_PATH(self):
        return '/vagrant/logs/'

    HUEY_NAME = 'dev'
    HUEY_PORT = 6379

    API_ACTIVE = True

    # Allow embedding, so responsinator.com can be used for testing
    X_FRAME_OPTIONS = "ALLOWALL"

class Live(HueyMixin,
           MandrillMixin,
           installations.WebfactionLiveMixin, ProjectConfiguration):
    DOMAIN = 'buzzhire.co'
    WEBFACTION_USER = 'buzzhire'

    ACCOUNT_PASSWORD_MIN_LENGTH = 6

    HUEY_NAME = 'live'
    HUEY_PORT = 17610

    CONTACT_EMAIL = 'contact@buzzhire.co'
    BOOKINGS_EMAIL = 'support@buzzhire.co'

    AWS_ACCESS_KEY_ID = 'AKIAI7ZMKSCZQGQRGUJQ'
    AWS_BUCKET_NAME = 'buzzhire-backups-media'

    DBBACKUP_STORAGE = 'dbbackup.storage.s3_storage'
    DBBACKUP_S3_BUCKET = 'buzzhire-backups-db'

    @property
    def DBBACKUP_S3_ACCESS_KEY(self):
        return self.AWS_ACCESS_KEY_ID

    @property
    def DBBACKUP_S3_SECRET_KEY(self):
        return self.AWS_SECRET_ACCESS_KEY

    BRAINTREE_MERCHANT_ID = 'q6xbcpbpcm4vtvcw'
    BRAINTREE_PUBLIC_KEY = 'skmbrjfnnc4kfxq5'
    BRAINTREE_SANDBOX = False

    TWILIO_ACCOUNT_SID = 'AC1480c67b0bebcaf9dd64492c96761570'
    TWILIO_PHONE_NUMBER = "+441347722127"

class Stage(Live):
    "The staging site - duplicates the live site, for deployment rehearsals."
    WEBFACTION_APPNAME = 'stage'
    DOMAIN = 'stage.buzzhire.co'
    HUEY_NAME = 'stage'
    HUEY_PORT = 17610
    COMING_SOON = False
