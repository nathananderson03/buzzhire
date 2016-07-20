from django.apps import apps
from django.conf import settings
from rest_framework import serializers
from apps.client.models import Client
from apps.api.account import serializers as account_serializers


class ClientForFreelancerSerializer(serializers.ModelSerializer):
    """Serializer that exposes information on the client
    appropriate for freelancer use.
    """
    class Meta:
        model = Client
        fields = ('id', 'reference_number', 'first_name', 'last_name',
                  'company_name')


class OwnClientSerializer(ClientForFreelancerSerializer):
    """Serializer that exposes information on the client
    profile for their own use.
    """

    email = serializers.SerializerMethodField()
    def get_email(self, obj):
        return obj.user.email


    class Meta(ClientForFreelancerSerializer.Meta):
        fields = ClientForFreelancerSerializer.Meta.fields + (
                'email', 'mobile', 'company_name')


class ClientSerializer(serializers.ModelSerializer):
    """
    -- currently used for: registration,
    Generic client serializer.
    """
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(max_length=140,
                                     style={'input_type': 'password'},
                                     write_only=True)

    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'email', 'password',
                  'mobile', 'company_name')

    def create(self, validated_data):
        """
        Take the user data nested in the request, and create a user object to go
        along with the client
        """
        # separate the account related data from the client data
        user_data = {
            'email': validated_data.pop('email'),
            'password': validated_data.pop('password'),
        }

        User = apps.get_model(settings.AUTH_USER_MODEL)

        # [MONKEY-PATCH] Manually picking the username out of the email.
        # This behavior is controlled by the allauth on the templated frontend.
        # The API here does it manually, so in case of a change of behavior,
        # we'd need to update here aswell
        #
        # -- left here to find this when changing the setting:
        # ACCOUNT_USERNAME_REQUIRED = False
        # (a search for the setting will show this line aswell)
        username = user_data['email'].split('@')[0]

        # create the user object
        user = User.objects.create_user(username=username, **user_data)

        # and use it with the client
        client = Client.objects.create(user=user, **validated_data)

        return client

