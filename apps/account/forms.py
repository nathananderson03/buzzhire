from django.forms import Form, BooleanField
from allauth.account import forms
from apps.core.forms import CrispyFormMixin, ConfirmForm
from crispy_forms.helper import FormHelper

# Crispify all the allauth forms


class LoginForm(CrispyFormMixin, forms.LoginForm):
    submit_context = {'icon_name': 'login'}
    submit_text = 'Log in'
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['password'].label = False
        self.fields['login'].label = False


class LogoutForm(CrispyFormMixin, ConfirmForm):
    action_text = 'Logout'


class SignupForm(CrispyFormMixin, forms.SignupForm):
    submit_text = 'Sign up'


class SignupInnerForm(SignupForm):
    """This sign up form is the same as the standard SignupForm but with
    the <form> and submit buttons removed, used for including with other
    forms in a single html <form> tag. 
    """

    form_tag = False
    submit_name = None
    wrap_fieldset_title = ''

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.helper.form_show_labels = False
        self.fields['password2'].widget.attrs['placeholder'] = 'Password again'


class ResetPasswordForm(CrispyFormMixin, forms.ResetPasswordForm):
    submit_text = 'Reset'
    submit_context = {'icon_name': 'reset_password'}
    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        self.helper.form_show_labels = False
        self.fields['email'].widget.attrs['placeholder'] = 'Email'


class ResetPasswordKeyForm(CrispyFormMixin, forms.ResetPasswordKeyForm):
    submit_text = 'Save new password'
    submit_context = {'icon_name': 'password'}
    def __init__(self, *args, **kwargs):
        super(ResetPasswordKeyForm, self).__init__(*args, **kwargs)
        self.helper.form_show_labels = False
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Password again'


class ChangePasswordForm(CrispyFormMixin, forms.ChangePasswordForm):
    submit_context = {'icon_name': 'password'}
    submit_text = 'Save changes'

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

        self.fields['password2'].widget.attrs['placeholder'] = 'Password again'
        self.helper.form_class = 'edit-password-form col-md-6'


class AcceptTermsInnerForm(CrispyFormMixin, Form):
    """Form for accepting terms and conditions.
    
    Should be instantiated with the terms_url to link to.
    """
    form_tag = False
    submit_text = 'Sign up'
    submit_context = {'icon_name': 'register'}
    wrap_fieldset_title = 'Terms and conditions'

    terms = BooleanField(error_messages={
            'required': "You must agree to the terms and conditions."})

    def __init__(self, *args, **kwargs):
        self.terms_url = kwargs.pop('terms_url')
        super(AcceptTermsInnerForm, self).__init__(*args, **kwargs)
        self.fields['terms'].label = \
                'I accept the ' \
                '<a target="_blank" href="%s">terms and conditions</a>.' \
                                % self.terms_url
