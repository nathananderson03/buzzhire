from django import forms
from apps.core.forms import CrispyFormMixin
from .models import Lead, Client
from crispy_forms.helper import FormHelper


class LeadForm(CrispyFormMixin, forms.ModelForm):
    """A form for filling out an expression of interest.
    """
    submit_text = 'Keep me posted'
    submit_context = {'icon_name': 'confirm'}
    class Meta:
        model = Lead
        exclude = ('created',)


class ClientForm(CrispyFormMixin, forms.ModelForm):
    """A form for editing client details.
    """
    submit_text = 'Save changes'
    submit_context = {'icon_name': 'edit'}
    wrap_fieldset_title = 'Account Details'

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)

        self.helper.form_show_labels = False
        self.helper.form_class = 'edit-account-form col-md-6'


    class Meta:
        model = Client
        exclude = ('user',)
        widgets = {
            "first_name":forms.TextInput(attrs={'placeholder':'First name'}),
            "last_name":forms.TextInput(attrs={'placeholder':'Last name'}),
            "mobile":forms.TextInput(attrs={'placeholder':'Mobile'}),
            "company_name":forms.TextInput(attrs={'placeholder':'Company name'})
        }

class ClientInnerForm(ClientForm):
    """A form for filling out client details, included with SignupForm in
    a single html <form>.
    """
    form_tag = False
    submit_name = None
    submit_context = {'icon_name': 'register'}
    wrap_fieldset_title = 'About you'

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)

        self.helper.form_show_labels = False

    def save(self, user):
        "Saves the client model, given the user."
        self.instance.user = user
        return super(ClientForm, self).save()
