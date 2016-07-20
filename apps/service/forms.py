from django import forms
from . import services


class ServiceSelectForm(forms.Form):
    """Form for selecting a service.
    Optionally, can pass a 'use_plural' argument, specifying whether
    or not to use the plural version of the freelancer name.  
    """

    def __init__(self, *args, **kwargs):
        # Set whether or not to use the plural form of the service
        service_name_attr = 'freelancer_name'
        self.use_plural = kwargs.pop('use_plural', False)
        if self.use_plural:
            service_name_attr += '_plural'

        super(ServiceSelectForm, self).__init__(*args, **kwargs)
        # Populate the service field with each service
        service_choices = []
        for service in services.values():
            service_choices.append((service.key, getattr(service,
                                                         service_name_attr)))
        self.fields['service'] = forms.ChoiceField(choices=service_choices)
        self.fields['service'].widget.attrs['class'] = 'form-control'
