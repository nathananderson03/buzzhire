"""The service app defines an API for other apps to hook into to register
different types of services.

It is essentially a registry that follows a similar pattern to the
Django admin site, except instead of registering a Model in myapp/admin.py:

    admin.site.register(MyModel, MyModelAdmin)

you extend the Service class, and then register it in myapp/services.py:

    services.register(MyService)
    
The app itself does not handle very much behaviour beyond simply registering
Service classes, and providing some ways to detect which service is relevant.
Other apps use this app to define certain behaviour that can then be extended
by apps that define services.

These apps (the ones that define and register Service classes) should be placed
within the services (not 'service') package.       
   
For example, apps.job.views.JobRequestCreate view allows service apps to define
which model and job request form is used for their service:

    class JobRequestCreate(...,
                        ServiceViewMixin,
                        ...):
        ...
        
        @property
        def model(self):
            return self.service.job_request_model
    
        def get_form_class(self):
            return self.service.job_request_form

Then, apps.driver.services.py defines the model and form, and registers itself:

    class DriverService(Service):
        key = 'driver'
        job_request_model = DriverJobRequest
        job_request_form = DriverJobRequestForm
        
        ...
    
    services.register(DriverService)
"""
from apps.core.utils import WeightedRegistry, classproperty
from django.utils.module_loading import autodiscover_modules
from django.utils.encoding import force_text


default_app_config = 'apps.service.config.ServiceConfig'


"""Allows different job request types to be registered with the job app.

Usage:

   # services.py

   from apps.service import services, Service

   class MyService(Service):
       weight = 0
       job_request_model = MyModel
       
   services.register(MyService)
"""

services = WeightedRegistry()


class Service(object):
    """Class for registering different job services.  Apps should subclass
    Service, setting the attributes below and registering them
    as per the documentation above.
    """
    weight = 0
    job_request_model = None
    freelancer_model = None
    freelancer_additional_menu_items = []
    job_matching_form = None
    pay_grade_model = None

    @classproperty
    def service_name(cls):
        """Human readable version of the service, e.g. 'delivery'.
        """
        return cls.job_request_model.service

    @classproperty
    def freelancer_name(cls):
        """Human readable version of the type of freelancer for this service.
        Should be in the singular version.
        """
        return cls.freelancer_model._meta.verbose_name

    @classproperty
    def freelancer_name_plural(cls):
        """Human readable version used to refer to multiple freelancers
        for this service.
        """
        return force_text(cls.freelancer_model._meta.verbose_name_plural)


def autodiscover():
    """Automatically imports any services.py file in an app.
    """
    autodiscover_modules('services')


def service_from_class(job_request_model_class):
    "Returns the service for the supplied job request class."
    for service in services.values():
        if service.job_request_model == job_request_model_class:
            return service
    raise ValueError('Could not get find a service registered for '
                     '%s job_request.' % job_request_model_class)

