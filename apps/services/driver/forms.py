from django import forms
from django.forms import widgets
from crispy_forms import layout
from django.core.exceptions import ValidationError
from apps.core.forms import CrispyFormMixin
from crispy_forms.helper import FormHelper
from .models import Driver, DriverJobRequest, DriverVehicleType, \
                        VehicleType, FlexibleVehicleType
from apps.job.forms import JobRequestForm
from apps.core.widgets import ChoiceAttrsRadioSelect
from apps.freelancer.forms import FreelancerForm
from apps.booking.forms import JobMatchingForm
from .utils import DriverJobMatcher


class DriverJobRequestForm(JobRequestForm):
    """Form for creating/editing driver job requests.
    """
    comment_placeholder = 'Please specify the number of miles the driver will travel during the shift. Is there a ' \
                        'specific type of equipment the driver should bring?'

    def __init__(self, *args, **kwargs):
        super(DriverJobRequestForm, self).__init__(*args, **kwargs)
        self.adjust_vehicle_type_widget()
        self.helper.layout[2].insert(1, 'phone_requirement')
        self.helper.layout.insert(3,
            layout.Fieldset('',
                layout.Div('vehicle_type', css_class="radios-wrapper"),
                'own_vehicle',
                'minimum_delivery_box',
            )
        )


    def adjust_vehicle_type_widget(self):
        """Adjusts the vehicle type widget so it has
        'data-delivery-box_applicable' set on any radios that need a delivery
        box.  The javascript will use this to hide/show the delivery box field. 
        """
        # Adjust display of radios
        self.fields['vehicle_type'].empty_label = 'Any'
        self.fields['vehicle_type'].initial = ''  # Set 'Any' radio as default

        # Build list of the vehicle types that need a delivery box
        vehicle_type_choices = list(VehicleType.objects.filter(
                    delivery_box_applicable=True).values_list('pk', flat=True))
        vehicle_type_choices.append('')  # Also add the 'any' choice
        vehicle_type_attrs = dict(
            [(i, {'data-delivery-box-applicable': 'true'}) \
             for i in vehicle_type_choices])
        self.fields['vehicle_type'].widget = ChoiceAttrsRadioSelect(
                                choice_attrs=vehicle_type_attrs)

    class Meta(JobRequestForm.Meta):
         model = DriverJobRequest
         fields = JobRequestForm.Meta.fields + ('vehicle_type', 'own_vehicle',
                  'minimum_delivery_box', 'phone_requirement')
         widgets = {
                'vehicle_type': ChoiceAttrsRadioSelect(),
         }


class DriverForm(FreelancerForm):
    """Edit form for a driver's profile."""

    def __init__(self, *args, **kwargs):
        super(DriverForm, self).__init__(*args, **kwargs)
        self.helper.layout.insert(2,
            layout.Fieldset(
                'Your equipment',
                'phone_type',
            ),
        )


    class Meta(FreelancerForm.Meta):
        model = Driver
        exclude = FreelancerForm.Meta.exclude \
                        + ('vehicle_types', 'motorcycle_licence')



class DriverVehicleTypeForm(CrispyFormMixin, forms.ModelForm):
    "Form for creating/editing a driver vehicle."

    @property
    def submit_text(self):
        return 'Save' if self.instance.pk else 'Create'

    @property
    def submit_context(self):
        icon_name = 'save' if self.instance.pk else 'create'
        return {'icon_name': icon_name}


    def __init__(self, *args, **kwargs):
        self.driver = kwargs.pop('driver')
        super(DriverVehicleTypeForm, self).__init__(*args, **kwargs)

        # Limit choices to vehicle types they haven't already created
        existing_vehicle_types = self.driver.vehicle_types.values('pk')
        if self.instance.pk:
            # If we're editing it, we should include the object's own vehicle
            existing_vehicle_types = existing_vehicle_types.exclude(
                                            pk=self.instance.vehicle_type.pk)
        self.fields['vehicle_type'].queryset = VehicleType.objects.exclude(
                                            pk__in=existing_vehicle_types)

    def save(self):
        self.instance.driver = self.driver
        return super(DriverVehicleTypeForm, self).save()

    class Meta:
        model = DriverVehicleType
        fields = ('vehicle_type', 'own_vehicle', 'delivery_box')


class DriverJobMatchingForm(JobMatchingForm):
    """Job matching form specifically for drivers.
    """

    job_matcher = DriverJobMatcher
    vehicle_type = forms.ModelChoiceField(
                                queryset=FlexibleVehicleType.objects.all(),
                                required=False)


    phone_requirement = forms.ChoiceField(required=False,
                        choices=DriverJobRequest.PHONE_REQUIREMENT_CHOICES)
#     DRIVING_EXPERIENCE_CHOICES = (
#         (0, 'No preference'),
#         (1, '1 year'),
#         (3, '3 years'),
#         (5, '5 years'),
#     )

#     driving_experience = forms.ChoiceField(label='Minimum driving experience',
#                                     required=False,
#                                     choices=DRIVING_EXPERIENCE_CHOICES)

    own_vehicle = forms.BooleanField(
                                label='The driver needs their own vehicle.',
                                required=False)
    minimum_delivery_box = forms.ChoiceField(required=False,
                        choices=DriverVehicleType.DELIVERY_BOX_CHOICES,
                        help_text='N.B. This will filter out any vehicle '
                            'that does not have a delivery box of at least '
                            'this size, including cars.')
