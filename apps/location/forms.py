from django import forms
from apps.location.models import Postcode
from apps.location.utils import GeoLocationMatchException


class PostcodeFormMixin(forms.Form):
    """Mixin for a form that has a Postcode ForeignKey field on it.
    Defines a 'raw_postcode' field that should be displayed on the form
    (instead of the postcode field) and then the postcode will be populated.
    
    Can set the attribute postcode_required to True to require the field.
    
    TODO - consider whether this should be done using a widget/alternative
    form field instead.
    """
    postcode_required = False
    raw_postcode = forms.CharField(label='Postcode', max_length=10)


    def __init__(self, *args, **kwargs):
        super(PostcodeFormMixin, self).__init__(*args, **kwargs)
        self.fields['raw_postcode'].required = self.postcode_required

        # For update forms, populate the raw_postcode with the postcode
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['raw_postcode'].initial = str(self.instance.postcode)

    def clean_raw_postcode(self):
        # We use the raw postcode form field to generate a postcode instance
        # to link with the postcode ForeignKey field.
        compressed_postcode = self.cleaned_data['raw_postcode'].replace(
                                                                    ' ', '')
        # If they supply a postcode
        if compressed_postcode:
            is_model_form = hasattr(self, 'instance')
            if is_model_form and self.instance.postcode_id and \
                                    compressed_postcode == \
                                    self.instance.postcode.compressed_postcode:
                # Postcode is the same, don't attempt to recreate it
                self.cleaned_data['postcode'] = self.instance.postcode
            else:
                # If the postcode is new or different, create/link it
                # with a new postcode instance
                try:
                    self.cleaned_data['postcode'], created = \
                                Postcode.objects.get_or_create(
                                    compressed_postcode=compressed_postcode)
                except GeoLocationMatchException:
                    raise ValidationError('That was not a valid postcode.')

        return compressed_postcode
