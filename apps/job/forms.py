from decimal import Decimal
from copy import deepcopy
from moneyed import Money
from datetime import date, datetime, timedelta
from django import forms
from django.forms import widgets
from django.conf import settings
from apps.core.forms import CrispyFormMixin, ConfirmForm
from apps.account.forms import SignupInnerForm
from django.template.loader import render_to_string
from apps.core.email import send_mail
from crispy_forms import layout
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from apps.core.widgets import ChoiceAttrsRadioSelect
from django.forms.widgets import HiddenInput
from apps.core.widgets import Bootstrap3SterlingMoneyWidget, Bootstrap3TextInput
from django.forms import widgets
from apps.location.forms import PostcodeFormMixin
from apps.payment.utils import PaymentAPI, PaymentException
from .signals import job_request_changed
from .models import JobRequest
from . import service_from_class
from .validators import validate_start_date_and_time
from crispy_forms.helper import FormHelper
import logging
from django.utils.safestring import mark_safe


logger = logging.getLogger('project')


class JobRequestForm(CrispyFormMixin, PostcodeFormMixin,
                           forms.ModelForm):
    """Form for submitting a job request.
    Should be instantiated with a Client object.
    """
    submit_text = 'Continue'
    postcode_required = True

    @property
    def submit_context(self):
        return {'icon_name': self.service.key}

    def __init__(self, *args, **kwargs):
        self.service = service_from_class(self.Meta.model)


        if 'data' in kwargs:
            # If the form has been submitted, add the disabled city widget
            # value to the data before continuing.  This is because otherwise,
            # if the form fails validation then it doesn't show anything in the
            # city widget the second time.
            data = kwargs['data'].copy()
            # The posted key is different if the form has a prefix
            self.prefix = kwargs.get('prefix')
            data[self.add_prefix('city')] = JobRequest.CITY_LONDON
            kwargs['data'] = data
        super(JobRequestForm, self).__init__(*args, **kwargs)

        self.fields['address1'].label = False
        self.fields['address1'].widget.attrs['placeholder'] = "Address line 1"
        self.fields['address2'].label = False
        self.fields['address2'].widget.attrs['placeholder'] = "Address line 2"
        self.fields['raw_postcode'].label = False
        self.fields['raw_postcode'].widget.attrs['placeholder'] = "Postcode"
        self.fields['city'].label = False

        amount, currency = self.fields['client_pay_per_hour'].fields
        default_min_pay = self.get_min_client_pay_per_hour()
        self.fields['client_pay_per_hour'].initial = default_min_pay
        self.fields['client_pay_per_hour'].widget = Bootstrap3SterlingMoneyWidget(
          amount_widget=widgets.NumberInput(
                    attrs={'min': default_min_pay.amount}),
          currency_widget=widgets.HiddenInput,
          attrs={'step': '0.25'})
        self.fields['start_time'].widget = forms.TimeInput()
        self.fields['duration'].widget = Bootstrap3TextInput(addon_after='hours')
        self.fields['city'].widget.attrs = {'disabled': 'disabled'}

        self.fields['comments'].widget.attrs = {'rows': 3}
        self.fields['comments'].label = False

        self.fields['client_pay_per_hour'].label = False


        # Allow subclassing forms to insert service-specific text
        # in the comments field
        if getattr(self, 'comment_placeholder'):
            self.fields['comments'].widget.attrs['placeholder'] = \
                                                    self.comment_placeholder

        self.helper.layout = layout.Layout(
            layout.Fieldset(
                '<span class="booking-form-num">1</span>Date and time',
                'date', 'start_time', 'duration',
            ),
            layout.Fieldset(
                '<span class="booking-form-num">2</span>Job location',
                'address1', 'address2',
                'city',
                'raw_postcode',
            ),
            layout.Fieldset(
                '<span class="booking-form-num">3</span>Freelancer details',
                'number_of_freelancers',
                'years_experience',
            ),
            layout.Fieldset(
                '<span class="booking-form-num">4</span>Budget',
                'client_pay_per_hour',
                'tips_included',
            ),
            layout.Fieldset(
                '<span class="booking-form-num">5</span>Further info',
                'comments'
            ),
        )

        # Add the submit button, but allow subclassing forms to suppress it
        if self.submit_name:
            self.helper.layout.append(self.get_submit_button())

    def get_min_client_pay_per_hour(self, **kwargs):
        """Returns the minimum client pay per hour for the job request
        being created, as a moneyed.Money object.
        
        Keyword arguments should be valid keyword arguments to be passed to the
        pay grade model's get_pay_grade method, which will vary depending on
        the pay grade model.
        
        If kwargs are not supplied, it will use the defaults.
        """
        pay_grade_model = self.service.pay_grade_model

        # Set default fields, if not provided
        for filter_field in pay_grade_model.filter_fields:
            if filter_field not in kwargs:
                if not self.is_bound:
                    # The form hasn't been submitted, so use the defaults
                    kwargs[filter_field] = self.fields[filter_field].initial
                else:
                    # The form has been submitted; use the data
                    submitted_value = self.data[filter_field]
                    # Convert empty strings to None, to be valid
                    # for get_pay_grade()
                    if not submitted_value:
                        submitted_value = None
                    kwargs[filter_field] = submitted_value

        try:
            pay_grade = pay_grade_model.objects.get_pay_grade(**kwargs)
        except ObjectDoesNotExist:
            # Fall back to settings.CLIENT_MIN_WAGE on error
            return Money(settings.CLIENT_MIN_WAGE, 'GBP')
        else:
            return pay_grade.min_client_pay_per_hour

    def clean(self):
        self.cleaned_data = super(JobRequestForm, self).clean()

        # Validate the pay
        self.validate_client_pay_per_hour()

        # Validate the date and time
        validate_start_date_and_time(self.cleaned_data.get('date'),
                                     self.cleaned_data.get('start_time'))

    def validate_client_pay_per_hour(self):
        """Validates the client pay per hour based on the other fields,
        making sure it matches the pay grade.
        """
        # Get what the minimum pay should be based on those fields
        min_pay = self.get_min_client_pay_per_hour()
        # Validate
        if self.cleaned_data['client_pay_per_hour'].amount < min_pay.amount:
            self.add_error('client_pay_per_hour',
                mark_safe('This is below the minimum pay for a freelancer ' \
                'with that experience, which is &pound;%s.' % min_pay.amount))

    def save(self, client, commit=True):
        """We require the client to be passed at save time.  This is
        to make it easier to include the form before the client is created,
        such as in the anonymous creation of bookings."""
        # Make sure the client is saved in the job request
        self.instance.client = client
        self.instance.postcode = self.cleaned_data['postcode']
        return super(JobRequestForm, self).save(commit)

    class Meta:
        model = JobRequest
        fields = ('date', 'start_time', 'duration',
                  'address1', 'address2', 'city',
                  'client_pay_per_hour', 'tips_included',
                  'number_of_freelancers', 'years_experience',
                  'comments')


class JobRequestInnerFormMixin(object):
    """Form mixin, designed to be used with forms subclassing JobRequestForm,
    which are to be included with other forms in a single html <form>.
    """
    form_tag = False
    submit_name = None
    wrap_fieldset_title = 'Job details'


class JobRequestSignupInnerForm(SignupInnerForm):
    submit_name = None


class JobRequestUpdateMixin(object):
    "Form mixin for job request edit forms."
    submit_text = 'Save'
    submit_context = {}

    def __init__(self, *args, **kwargs):
        super(JobRequestUpdateMixin, self).__init__(*args, **kwargs)
        # Add this field dynamically - the usual form field definition
        # doesn't work for mixins not inheriting from forms.Form.
        self.fields['notify'] = forms.BooleanField(
            label='Notify the client when saving this job.',
            required=False, initial=True)

        self.helper.layout.insert(-1,
            layout.Fieldset('Notifications',
                'notify',
                layout.HTML('<div class="alert alert-warning" '
                    'style="clear: both;">Note: upon saving, '
                    'new invitations will be sent out to any matching '
                    'freelancers who have not already been invited.</div>')
            )
        )

    def save(self, *args, **kwargs):
        kwargs['client'] = self.instance.client
        instance = super(JobRequestUpdateMixin, self).save(*args, **kwargs)

        # Send signal
        job_request_changed.send(sender=self,
              instance=self.instance,
              changed_data=self.changed_data,
              silent=(not self.cleaned_data['notify']))

        return instance


class JobRequestCheckoutForm(CrispyFormMixin, forms.Form):
    submit_text = 'Confirm job'
    submit_context = {'icon_name': 'pay'}
    submit_template_name = 'payment/forms/buttons.html'

    # This is the hidden field that the Braintree drop in UI fills out,
    # which allows us to take the payment.
    payment_method_nonce = forms.CharField(required=True,
                                           widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance')
        super(JobRequestCheckoutForm, self).__init__(*args, **kwargs)
        self.helper.layout.insert(0, layout.Div(
                                        css_id='payment-method-container'))

    def clean(self):
        cleaned_data = super(JobRequestCheckoutForm, self).clean()
        # Check everything else is valid before attempting payment
        if self.is_valid():
            # Attempt payment
            try:
                api = PaymentAPI()
                api.take_payment(self.cleaned_data['payment_method_nonce'],
                                 amount=self.instance.client_total_cost.amount,
                                 order_id=self.instance.reference_number)

            except PaymentException as e:
                logger.exception(e)
                raise forms.ValidationError(
                                   'Sorry, there was an issue taking payment.')

    def save(self):
        # Payment will have been successfully processed
        self.instance.open()
        self.instance.save()

