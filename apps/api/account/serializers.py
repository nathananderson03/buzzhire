from django.apps import apps
from django.conf import settings
from rest_framework import serializers, exceptions
from apps.account.forms import ResetPasswordForm


class PasswordResetSerializer(serializers.Serializer):

    """
    Serializer for requesting a password reset e-mail.
    """

    email = serializers.EmailField()

    password_reset_form_class = ResetPasswordForm

    def validate_email(self, value):
        # Create PasswordResetForm with the serializer
        self.form = self.password_reset_form_class(data=self.initial_data)
        if not self.form.is_valid():
            try:
                error_message = self.form.errors['email'][0]
            except (KeyError, ValueError):
                error_message = 'There was an unexpected issue.'
            raise serializers.ValidationError(error_message)
        return value

    def save(self):
        request = self.context.get('request')
        self.form.save(request=request)


class UserSerializer(serializers.Serializer):
    """
    Generic user auth model serializer.
    """

    class Meta:
        model = apps.get_model(settings.AUTH_USER_MODEL)
        fields = ('email', 'password')

