from rest_framework import serializers
from apps.notification.models import Notification
from django.utils.timezone import template_localtime

class NotificationSerializer(serializers.ModelSerializer):
    "Serializer for Notifications."

    datetime_created_localtime = serializers.SerializerMethodField()
    def get_datetime_created_localtime(self, obj):
        return template_localtime(obj.datetime_created)

    content_type = serializers.SerializerMethodField()
    def get_content_type(self, obj):
        return obj.content_type.model

    class Meta:
        model = Notification
        fields = ('id', 'category', 'message',
                  'datetime_created', 'datetime_created_localtime',
                  'object_id', 'content_type')
